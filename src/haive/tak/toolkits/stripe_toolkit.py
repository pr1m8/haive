from stripe_agent_toolkit.crewai.toolkit import StripeAgentToolkit
import os
stripe_agent_toolkit = StripeAgentToolkit(
    secret_key=os.getenv("STRIPE_SECRET_KEY"),
    configuration={
        "actions": {
            "payment_links": {
                "create": True,
            },
        }
    },
)