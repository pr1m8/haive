from src.haive.core.graph.branches import Branch

route_branch = Branch(
    function=lambda state: (
        "emergency_response" if state["severity"].strip().lower() in ["critical", "high"]
        else "public_works_response" if "flood" in state["disaster_type"].strip().lower() or "storm" in state["disaster_type"].strip().lower()
        else "civil_defense_response"
    ),
    destinations={
        "emergency_response": "emergency_response",
        "public_works_response": "public_works_response",
        "civil_defense_response": "civil_defense_response",
    },
    default="send_email_alert"
)
