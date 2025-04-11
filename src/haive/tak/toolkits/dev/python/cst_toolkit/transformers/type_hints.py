import libcst as cst

class TypeHintTransformer(cst.CSTTransformer):
    """Adds type hints to function parameters and return types."""
    def __init__(self, type_map):
        super().__init__()
        self.type_map = type_map  # {"param_name": "int", "return": "str"}

    def leave_FunctionDef(self, original_node, updated_node):
        updated_params = []
        for param in updated_node.params.params:
            param_name = param.name.value
            annotation = self.type_map.get(param_name, None)
            if annotation:
                param = param.with_changes(annotation=cst.Annotation(cst.Name(annotation)))
            updated_params.append(param)

        return_annotation = self.type_map.get("return")
        return updated_node.with_changes(
            params=updated_node.params.with_changes(params=updated_params),
            returns=cst.Annotation(cst.Name(return_annotation)) if return_annotation else updated_node.returns
        )
