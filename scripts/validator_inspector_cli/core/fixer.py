from __future__ import annotations

from pathlib import Path

import libcst as cst
import libcst.matchers as m
from rich.console import Console
from validator_inspector_cli.core.reporting import log_debug

console = Console()


class ValidatorFixer(cst.CSTTransformer):
    def leave_FunctionDef(
        self,
        original_node: cst.FunctionDef,
        updated_node: cst.FunctionDef,
    ) -> cst.FunctionDef:
        decorators = [d.decorator for d in updated_node.decorators]
        is_validator = any(
            m.matches(dec, m.Call(func=m.Name("model_validator"))) for dec in decorators
        )
        if not is_validator:
            return updated_node

        log_debug(f"Fixing function: {original_node.name.value}")

        # Remove @classmethod
        new_decorators = [
            d
            for d in updated_node.decorators
            if not m.matches(d.decorator, m.Name("classmethod"))
        ]

        # Replace 'cls' with 'self' in parameters
        new_params = []
        for param in updated_node.params.params:
            if param.name.value == "cls":
                param = param.with_changes(name=cst.Name("self"))
            new_params.append(param)
        new_param_list = updated_node.params.with_changes(params=new_params)

        # Replace "cls" with "self" in function body
        class ReplaceClsWithSelf(cst.CSTTransformer):
            def leave_Name(self, orig, updated):
                if updated.value == "cls":
                    return updated.with_changes(value="self")
                return updated

        new_body = updated_node.body.visit(ReplaceClsWithSelf())

        # Ensure return annotation is Self
        ret_annot = updated_node.returns
        if not ret_annot or not (
            isinstance(ret_annot.annotation, cst.Name)
            and ret_annot.annotation.value == "Self"
        ):
            ret_annot = cst.Annotation(annotation=cst.Name("Self"))

        return updated_node.with_changes(
            decorators=new_decorators,
            params=new_param_list,
            body=new_body,
            returns=ret_annot,
        )


class SelfImportAdder(cst.CSTTransformer):
    def leave_Module(
        self,
        original_node: cst.Module,
        updated_node: cst.Module,
    ) -> cst.Module:
        for stmt in updated_node.body:
            if m.matches(stmt, m.SimpleStatementLine()):
                for expr in stmt.body:
                    if (
                        isinstance(expr, cst.ImportFrom)
                        and expr.module
                        and expr.module.value == "typing"
                        and any(name.name.value == "Self" for name in expr.names)
                    ):
                        return updated_node

        # Try to merge with existing typing import if possible
        for idx, stmt in enumerate(updated_node.body):
            if isinstance(stmt, cst.SimpleStatementLine):
                for expr in stmt.body:
                    if (
                        isinstance(expr, cst.ImportFrom)
                        and expr.module
                        and expr.module.value == "typing"
                    ):
                        names = list(expr.names)
                        names.append(cst.ImportAlias(name=cst.Name("Self")))
                        updated_import = expr.with_changes(names=names)
                        updated_stmt = stmt.with_changes(body=[updated_import])
                        return updated_node.with_changes(
                            body=[
                                *updated_node.body[:idx],
                                updated_stmt,
                                *updated_node.body[idx + 1 :],
                            ],
                        )

        # If no typing import, prepend one
        new_import = cst.parse_statement("from typing import Self\n")
        return updated_node.with_changes(body=[new_import, *list(updated_node.body)])


def fix_validators(filepath: str) -> cst.Module:
    try:
        source = Path(filepath).read_text(encoding="utf-8")
        tree = cst.parse_module(source)
        fixed_tree = tree.visit(ValidatorFixer())
        final_tree = fixed_tree.visit(SelfImportAdder())
        return final_tree
    except Exception as e:
        console.print(f"[red]Fixing failed in {filepath}: {e}[/red]")
        log_debug(f"Fix failed in {filepath}: {e}")
        raise


def apply_fixes(filepath: str):
    try:
        fixed_tree = fix_validators(filepath)
        Path(filepath).write_text(fixed_tree.code, encoding="utf-8")
        console.print(f"[green]Applied fixes to {filepath}[/green]")
        log_debug(f"Applied fixes to {filepath}")
    except Exception as e:
        console.print(f"[red]Apply failed for {filepath}: {e}[/red]")
        log_debug(f"Apply failed for {filepath}: {e}")
