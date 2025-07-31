from pathlib import Path

import libcst as cst
import libcst.matchers as m
from rich.console import Console

console = Console()


class ValidatorInspector(cst.CSTVisitor):
    def __init__(self):
        self.issues = []

    def visit_FunctionDef(self, node: cst.FunctionDef):
        decorators = [d.decorator for d in node.decorators]

        for dec in decorators:
            # Handle model_validator
            if m.matches(dec, m.Call(func=m.Name("model_validator"))):
                self._check_model_validator(node, dec)

            # Handle field_validator (should never be modified)
            elif m.matches(dec, m.Call(func=m.Name("field_validator"))):
                self._check_field_validator(node, dec)

    def _check_model_validator(self, node: cst.FunctionDef, decorator: cst.Call):
        """Check model_validator for issues."""
        # Extract mode parameter
        mode_arg = next(
            (
                arg
                for arg in decorator.args
                if arg.keyword and arg.keyword.value == "mode"
            ),
            None,
        )

        uses_cls = any(param.name.value == "cls" for param in node.params.params)
        uses_self = any(param.name.value == "self" for param in node.params.params)
        has_classmethod = any(
            m.matches(d.decorator, m.Name("classmethod")) for d in node.decorators
        )
        return_annot = node.returns.annotation if node.returns else None

        # Determine mode (default is "before" if not specified)
        mode = "before"  # default
        if mode_arg and hasattr(mode_arg, "value") and "after" in str(mode_arg.value):
            mode = "after"

        if mode == "before":
            # mode="before" should use @classmethod + cls + return Any/dict
            if not has_classmethod:
                self.issues.append(
                    (
                        node.name.value,
                        "mode='before' validator should have @classmethod decorator",
                    )
                )
            if not uses_cls:
                self.issues.append(
                    (
                        node.name.value,
                        "mode='before' validator should use 'cls' parameter",
                    )
                )
            # Don't require specific return annotation for mode="before"

        elif mode == "after":
            # mode="after" should use self + return Self
            if has_classmethod:
                self.issues.append(
                    (
                        node.name.value,
                        "mode='after' validator should NOT have @classmethod decorator",
                    )
                )
            if uses_cls and not uses_self:
                self.issues.append(
                    (
                        node.name.value,
                        "mode='after' validator should use 'self' parameter, not 'cls'",
                    )
                )

            # Check if return annotation should be Self
            should_report_annotation_issue = False
            if not return_annot:
                should_report_annotation_issue = True
            # Check if the annotation is specifically "Self"
            elif isinstance(return_annot, cst.Name):
                if return_annot.value != "Self":
                    should_report_annotation_issue = True
            else:
                # For complex annotations, convert to string and check
                try:
                    annot_str = return_annot.code
                    if "Self" not in annot_str:
                        should_report_annotation_issue = True
                except:
                    should_report_annotation_issue = True

            if should_report_annotation_issue:
                self.issues.append(
                    (
                        node.name.value,
                        "Missing or incorrect return annotation (should use `Self`).",
                    )
                )

    def _check_field_validator(self, node: cst.FunctionDef, decorator: cst.Call):
        """Check field_validator - these should NOT be modified."""
        # field_validator should always be @classmethod + cls
        uses_cls = any(param.name.value == "cls" for param in node.params.params)
        has_classmethod = any(
            m.matches(d.decorator, m.Name("classmethod")) for d in node.decorators
        )

        if not has_classmethod:
            self.issues.append(
                (
                    node.name.value,
                    "field_validator should have @classmethod decorator (do NOT modify)",
                )
            )
        if not uses_cls:
            self.issues.append(
                (
                    node.name.value,
                    "field_validator should use 'cls' parameter (do NOT modify)",
                )
            )

        # field_validator should NOT return Self
        return_annot = node.returns.annotation if node.returns else None
        if (
            return_annot
            and hasattr(return_annot, "code")
            and "Self" in return_annot.code
        ):
            self.issues.append(
                (
                    node.name.value,
                    "field_validator should NOT return Self (do NOT modify)",
                )
            )


def analyze_validators(filepath: str) -> None:
    """Analyze a Python file for validator-related issues."""
    file_path = Path(filepath)
    try:
        source = file_path.read_text(encoding="utf-8")
    except Exception as e:
        from validator_inspector_cli_fixed.core.reporting import report_and_log

        report_and_log(filepath, [("<read_error>", f"Failed to read file: {e}")])
        return

    try:
        tree = cst.parse_module(source)
    except Exception as e:
        from validator_inspector_cli_fixed.core.reporting import report_and_log

        report_and_log(filepath, [("<parse_error>", f"Failed to parse CST: {e}")])
        return

    inspector = ValidatorInspector()
    tree.visit(inspector)

    from validator_inspector_cli_fixed.core.reporting import report_and_log

    report_and_log(filepath, inspector.issues)
