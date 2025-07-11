def check_interfaces(
    obj: Any,
    interfaces: Dict[str, Optional[List[str]]],
    require_callable: bool = True,
    check_signatures: bool = False,
    return_mode: str = "detailed",
) -> Union[
    bool, Dict[str, Dict[str, bool]], Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]
]:
    """Check if an object implements specified interfaces with optional parameter checking.

    Args:
        obj: The object to inspect
        interfaces: Dictionary mapping method names to lists of required parameters
                   (None for methods where parameters don't need checking)
        require_callable: If True, only consider attributes that are callable
        check_signatures: If True, verify method signatures contain required parameters
        return_mode: How to return results ("all", "any", "dict", "detailed")

    Returns:
        Results based on return_mode, including signature compatibility details
        when check_signatures=True

    Examples:
        # Define required interfaces
        required_interfaces = {
            "invoke": ["input_data", "config"],  # Method must accept these parameters
            "create_runnable": ["runnable_config"],
            "to_dict": None  # Don't care about parameters
        }

        # Check if engine implements all interfaces
        if check_interfaces(engine, required_interfaces, return_mode="all"):
            # All interfaces implemented correctly
            pass
    """
    results = {}

    for method_name, required_params in interfaces.items():
        # Check if method exists
        has_method = hasattr(obj, method_name)

        if has_method:
            attr = getattr(obj, method_name)

            # Check if callable (if required)
            if require_callable and not callable(attr):
                has_method = False
                results[method_name] = {"exists": False, "signature_ok": False}
                continue

            # Check signature if requested and parameters specified
            signature_ok = True
            if check_signatures and required_params is not None:
                try:
                    sig = inspect.signature(attr)
                    param_names = set(sig.parameters.keys())
                    missing_params = [
                        p for p in required_params if p not in param_names
                    ]
                    signature_ok = len(missing_params) == 0
                except (ValueError, TypeError):
                    # Can't inspect signature
                    signature_ok = False

            results[method_name] = {"exists": has_method, "signature_ok": signature_ok}
        else:
            results[method_name] = {"exists": False, "signature_ok": False}

    # Return based on specified mode
    if return_mode == "all":
        return all(r["exists"] and r["signature_ok"] for r in results.values())

    if return_mode == "any":
        return any(r["exists"] and r["signature_ok"] for r in results.values())

    if return_mode == "dict":
        return results

    if return_mode == "detailed":
        present = {}
        missing = {}

        for method, result in results.items():
            if result["exists"] and result["signature_ok"]:
                present.setdefault("methods", set()).add(method)
            elif result["exists"] and not result["signature_ok"]:
                present.setdefault("methods", set()).add(method)
                missing.setdefault("signatures", set()).add(method)
            else:
                missing.setdefault("methods", set()).add(method)

        return present, missing

    raise ValueError(f"Invalid return_mode: {return_mode}")
