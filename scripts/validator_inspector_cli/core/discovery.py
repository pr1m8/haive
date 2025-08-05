from __future__ import annotations

from pathlib import Path

import libcst as cst
import libcst.matchers as m
from rich.console import Console
from validator_inspector_cli.core.reporting import report_and_log

console = Console()


class ValidatorInspector(cst.CSTVisitor):
    def __init__(self):
        self.issues = []

    def visit_FunctionDef(self, node: cst.FunctionDef):
        decorators = [d.decorator for d in node.decorators]
        for dec in decorators:
            if m.matches(dec, m.Call(func=m.Name("model_validator"))):
                mode_arg = next(
                    (
                        arg
                        for arg in dec.args
                        if arg.keyword and arg.keyword.value == "mode"
                    ),
                    None,
                )
                uses_cls = any(
                    param.name.value == "cls" for param in node.params.params
                )
                return_annot = node.returns.annotation if node.returns else None

                # Check for missing cls if mode='before'
                if (
                    not uses_cls
                    and mode_arg
                    and getattr(mode_arg.value, "value", "") == "before"
                ):
                    self.issues.append(
                        (node.name.value, "Missing `cls` in mode='before' validator."),
                    )

                # Check if return annotation includes 'Self'
                if (
                    not return_annot
                    or not hasattr(return_annot, "code")
                    or "Self" not in return_annot.code
                ):
                    self.issues.append(
                        (
                            node.name.value,
                            "Missing or incorrect return annotation (should use `Self`).",
                        ),
                    )


def analyze_validators(filepath: str) -> None:
    """Analyze a Python file for validator-related issues."""
    file_path = Path(filepath)
    try:
        source = file_path.read_text(encoding="utf-8")
    except Exception as e:
        report_and_log(filepath, [("<read_error>", f"Failed to read file: {e}")])
        return

    try:
        tree = cst.parse_module(source)
    except Exception as e:
        report_and_log(filepath, [("<parse_error>", f"Failed to parse CST: {e}")])
        return

    inspector = ValidatorInspector()
    tree.visit(inspector)
    report_and_log(filepath, inspector.issues)
