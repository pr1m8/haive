from pathlib import Path

import libcst as cst
import libcst.matchers as m
from rich.console import Console

console = Console()


class ValidatorFixer(cst.CSTTransformer):
    def __init__(self):
        self.needs_self_import = False

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        decorators = [d.decorator for d in updated_node.decorators]

        # Check if this is a model_validator (NOT field_validator)
        model_validator_dec = None
        for dec in decorators:
            if m.matches(dec, m.Call(func=m.Name("model_validator"))):
                model_validator_dec = dec
                break
            # SKIP field_validator - never modify these
            if m.matches(dec, m.Call(func=m.Name("field_validator"))):
                return updated_node

        if not model_validator_dec:
            return updated_node

        # Extract mode parameter
        mode_arg = None
        for arg in model_validator_dec.args:
            if arg.keyword and arg.keyword.value == "mode":
                mode_arg = arg.value
                break

        # Determine if this is mode="after" (the only case we should modify)
        is_after_mode = False
        if mode_arg:
            if hasattr(mode_arg, "quote") and "after" in str(mode_arg.value):
                is_after_mode = True
        else:
            # Default mode for model_validator is "before" - don't modify
            return updated_node

        # Only modify mode="after" validators
        if not is_after_mode:
            return updated_node

        console.print(
            f"[yellow]Fixing mode='after' validator: {original_node.name.value}[/yellow]"
        )

        # Remove @classmethod decorator
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

        # Fix return annotation to Self (only for mode="after")
        ret_annot = updated_node.returns
        if not ret_annot or not (
            isinstance(ret_annot.annotation, cst.Name)
            and ret_annot.annotation.value == "Self"
        ):
            ret_annot = cst.Annotation(annotation=cst.Name("Self"))
            self.needs_self_import = True

        return updated_node.with_changes(
            decorators=new_decorators,
            params=new_param_list,
            body=new_body,
            returns=ret_annot,
        )


class SelfImportAdder(cst.CSTTransformer):
    def __init__(self, needs_self_import: bool):
        self.needs_self_import = needs_self_import

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        # Only add Self import if we actually made changes that need it
        if not self.needs_self_import:
            return updated_node

        # Check if Self is already imported
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
                            ]
                        )

        # If no typing import, prepend one
        new_import = cst.parse_statement("from typing import Self\n")
        return updated_node.with_changes(body=[new_import, *list(updated_node.body)])


def fix_validators(filepath: str) -> tuple[cst.Module, bool]:
    """Fix validators and return (tree, was_modified)."""
    try:
        source = Path(filepath).read_text(encoding="utf-8")
        tree = cst.parse_module(source)

        fixer = ValidatorFixer()
        fixed_tree = tree.visit(fixer)

        # Only add imports if we made changes
        final_tree = fixed_tree.visit(SelfImportAdder(fixer.needs_self_import))

        # Check if anything actually changed
        was_modified = fixed_tree.code != tree.code

        return final_tree, was_modified

    except Exception as e:
        console.print(f"[red]Fixing failed in {filepath}: {e}[/red]")
        raise


def apply_fixes(filepath: str):
    try:
        fixed_tree, was_modified = fix_validators(filepath)

        if was_modified:
            Path(filepath).write_text(fixed_tree.code, encoding="utf-8")
            console.print(f"[green]Applied fixes to {filepath}[/green]")
        else:
            console.print(f"[dim]No changes needed in {filepath}[/dim]")

    except Exception as e:
        console.print(f"[red]Apply failed for {filepath}: {e}[/red]")
