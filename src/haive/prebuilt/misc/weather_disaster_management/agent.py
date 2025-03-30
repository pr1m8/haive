from langchain_core.messages import SystemMessage
from pydantic import BaseModel
from typing import Dict, Union, Literal
from src.haive.prebuilt.misc.weather_disaster_management.state import WeatherState, WeatherLocation
from src.haive.prebuilt.misc.weather_disaster_management.config import WeatherDisasterManagerConfig
from src.haive.toolkits.weather import weather_tool
from src.haive.core.engine.agent.agent import Agent, AgentConfig,register_agent
from datetime import datetime
from langgraph.types import Command
from langgraph.graph import END
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os


@register_agent(WeatherDisasterManagerConfig)
class WeatherDisasterManagementAgent(Agent[WeatherDisasterManagerConfig]):
    def __init__(self, config: WeatherDisasterManagerConfig=WeatherDisasterManagerConfig()):
        super().__init__(config)
      

    def get_human_verification(self, state: WeatherState) -> WeatherState:
        """Get human verification for low/medium severity alerts"""
        severity = state.severity.strip().lower()

        if severity in ["low", "medium"]:
            print("\n" + "="*50)
            print(f"Low/Medium severity alert for {state['city']} requires human approval:")
            print(f"Disaster Type: {state['disaster_type']}")
            print(f"Current Weather: {state['weather_data']['weather']}")
            print(f"Temperature: {state['weather_data']['temperature']}°C")
            print(f"Wind Speed: {state['weather_data']['wind_speed']} m/s")
            print(f"Severity: {state['severity']}")
            print(f"Response Plan: {state['response']}")
            print("\nType 'y' to approve sending alert or 'n' to reject (waiting for input):")
            print("="*50)

            # Block and wait for input
            while True:
                try:
                    user_input = input().lower().strip()
                    if user_input in ['y', 'n']:
                        approved = user_input == 'y'
                        print(f"Human verification result: {'Approved' if approved else 'Rejected'}")
                        break
                    else:
                        print("Please enter 'y' for yes or 'n' for no:")
                except Exception as e:
                    print(f"Error reading input: {str(e)}")
                    print("Please try again with 'y' or 'n':")

            return {
                "human_approved": approved,
                "messages": [
                    SystemMessage(content=f"Human verification: {'Approved' if approved else 'Rejected'}")
                ]
            }
        else:
            # Auto-approve for high/critical severity
            return Command(update={
                "human_approved": True,
                "messages":[
                    SystemMessage(content=f"Auto-approved {severity} severity alert")
                ]
            })
        
    def data_logging(self, state: WeatherState) -> WeatherState:
        """Log weather data, disaster analysis, and response to a file."""
        log_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": state.city,
            "weather_data": state.weather_data,
            "disaster_type": state.disaster_type,
            "severity": state.severity,
            "response": state.response,
            "social_media_reports": state.social_media_reports
        }

        try:
            with open("disaster_log.txt", "a") as log_file:
                log_file.write(json.dumps(log_data) + "\n")

            return Command(update={
                "messages": [SystemMessage(content="Data logged successfully")]
            })
        except Exception as e:
            return Command(update={
                "messages": [SystemMessage(content=f"Failed to log data: {str(e)}")]
            })

    def send_email_alert(self, state: WeatherState) -> WeatherState:
        """Send weather alert email"""
        sender_email = os.getenv("SENDER_EMAIL")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        password = os.getenv("EMAIL_PASSWORD")

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Weather Alert: {state.severity} severity weather event in {state.city}"

        body = self.format_weather_email(state)
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()

            # Add confirmation message
            severity = state.severity.strip().lower()
            if severity in ["low", "medium"]:
                print(f"\nVerification was approved by human, Email sent to {receiver_email} successfully")
            else:
                print(f"\nEmail sent successfully for high severity alert to {receiver_email}")

            return Command(update={
                "messages":[SystemMessage(content=f"Successfully sent weather alert email for {state['city']}")],
                "alerts": state.alerts + [f"Email alert sent: {datetime.now()}"]
            })

        except Exception as e:
            return Command(update={
                "messages": [SystemMessage(content=f"Failed to send email alert: {str(e)}")]
            })
        
    def format_weather_email(state: WeatherState) -> str:
        """Format weather data and severity assessment into an email message"""
        weather_data = state.weather_data
        social_media_reports = "\n".join(state.social_media_reports)

        email_content = f"""
        Weather Alert for {state.city}

        Disaster Type: {state.disaster_type}
        Severity Level: {state.severity}

        Current Weather Conditions:
        - Weather Description: {weather_data.weather}
        - Temperature: {weather_data.temperature}C
        - Wind Speed: {weather_data.wind_speed} m/s
        - Humidity: {weather_data.humidity}%
        - Pressure: {weather_data.pressure} hPa
        - Cloud Cover: {weather_data.cloud_cover}%


        Response Plan:
        {state.response}

        This is an automated weather alert generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        if state.severity.lower() in ['low', 'medium']:
            email_content += "\nNote: This low/medium severity alert has been verified by a human operator."

        return email_content
    def social_media_monitoring(self, state: WeatherState) -> WeatherState:
        """Simulate monitoring social media for additional reports of the weather event."""
        print(self.engines)
        print(self.engines["social_media_monitoring"])
        social_media_report = self.engines["social_media_monitoring"].invoke({
            "disaster_type": state.disaster_type,
            "severity": state.severity,
            "city": state.city
        })
        
        print(social_media_report)
        #social_media_report = random.choice(simulated_reports)
        return Command(update={
            "social_media_reports": [social_media_report],
            "messages":[SystemMessage(content=f"Social media report added: {social_media_report}")]
        })
    def handle_no_approval(self, state: WeatherState) -> WeatherState:
        """Handle cases where human verification was rejected"""
        print("\nVerification was not approved by human, Email not sent")

        message = (
            f"Alert not sent for {state.city} - "
            f"Weather severity level '{state.severity}' was deemed non-critical "
            f"by human operator and verification was rejected."
        )
        return Command(update={
            "messages":  [SystemMessage(content=message)]
        })
     
    def verify_approval_router(state: WeatherState) -> Literal["send_email_alert", "handle_no_approval"]:
        """Route based on human approval decision"""
        return "send_email_alert" if state.human_approved else "handle_no_approval"
    
    def get_weather_data(
            self,
            state:Union[BaseModel, Dict],
            unit: Literal["celsius", "fahrenheit"] = "celsius"):
        """Fetch weather data using LangChain-compatible tool, update state."""
        city = state.city
        messages = state.messages

        try:
            result = weather_tool.invoke({
            "city": state.city,
            "country": state.country,
            "parse": True,
            "temperature_unit": unit
            })


            return Command(update={
                "weather_data": result,
                "messages":  [SystemMessage(content=f"✅ Weather data fetched for {city}")]
            })

        except Exception as e:
            fallback_data = {
                "weather": "N/A",
                "wind_speed_mps": "N/A",
                "cloud_cover_percent": "N/A",
                "temp_current": "N/A",
                "humidity_percent": "N/A",
                "pressure": "N/A"
            }

            return Command(update={
                "weather_data": fallback_data,
                "messages":  [SystemMessage(content=f"❌ Failed to fetch weather for {city}: {str(e)}")]
            })
        
    def public_works_response(self, state: WeatherState) -> WeatherState:
        """Generate public works response plan"""
       
        try:
            response = self.engines["public_works_response"].invoke({
                "disaster_type": state["disaster_type"],
                "severity": state["severity"],
                "city": state["city"]
            }).content

            return Command(update={
                "response": response,
                "messages": [SystemMessage(content="Public works response plan generated")]
            })
        except Exception as e:
            return Command(update={
                "response": "Failed to generate response plan",
                "messages": [SystemMessage(content=f"Failed to generate public works response: {str(e)}")]
            })
    def civil_defense_response(self, state: WeatherState) -> WeatherState:
        """Generate civil defense response plan"""
       
        try:
            chain = self.engines["civil_defense_response"]
            response = chain.invoke({
                "disaster_type": state.disaster_type,
                "severity": state.severity,
                "city": state.city
            }).content

            return Command(update={
                "response": response,
                "messages": [SystemMessage(content="Civil defense response plan generated")]
            })
        except Exception as e:
            return Command(update={
                "response": "Failed to generate response plan",
                "messages": [SystemMessage(content=f"Failed to generate civil defense response: {str(e)}")]
            })
    def emergency_response(self, state: WeatherState) -> WeatherState:
        """Generate emergency response plan"""
     
        try:
            response = self.engines["emergency_response"].invoke({
                "disaster_type": state["disaster_type"],
                "severity": state["severity"],
                "city": state["city"]
            }).content

            return Command(update={
                "response": response,
                "messages": [SystemMessage(content="Emergency response plan generated")]
            })
        except Exception as e:
            return Command(update={
                "response": "Failed to generate response plan",
                "messages": [SystemMessage(content=f"Failed to generate emergency response: {str(e)}")]
            })
    def analyze_disaster_type(self, state: WeatherState) -> WeatherState:
        """Analyze weather data to identify potential disasters"""
        weather_data = state.weather_data
      
        try:
            chain = self.engines["analyze_disaster_type"]
            disaster_type = chain.invoke(weather_data).content
            return Command(update={
                "disaster_type": disaster_type,
                "messages": [SystemMessage(content=f"Disaster type identified: {disaster_type}")]
            })
        except Exception as e:
            return Command(update={
                "disaster_type": "Analysis Failed",
                "messages": [SystemMessage(content=f"Failed to analyze disaster type: {str(e)}")]
            })
    def assess_severity(self, state: WeatherState) -> WeatherState:
        """Assess the severity of the identified weather situation"""
        weather_data = state.weather_data
        

        try:
            response = self.engines["assess_severity"].invoke({
                **weather_data,
                "disaster_type": state.disaster_type
            }).content

            return Command(update={
                "severity": response,
                "messages": [SystemMessage(content=f"Severity assessed as: {response}")]
            })
        except Exception as e:
            return Command(update={
                "severity": "Assessment Failed",
                "messages": state["messages"] + [SystemMessage(content=f"Failed to assess severity: {str(e)}")]
            })
        

    def setup_workflow(self) -> None:
        """Set up the self.graph for the agent."""
        # Add nodes
        self.graph.add_node("get_weather", self.get_weather_data)
        self.graph.add_node("social_media_monitoring", self.social_media_monitoring)
        self.graph.add_node("analyze_disaster", self.analyze_disaster_type)
        self.graph.add_node("assess_severity", self.assess_severity)
        self.graph.add_node("data_logging", self.data_logging)
        self.graph.add_node("emergency_response", self.emergency_response)
        self.graph.add_node("civil_defense_response", self.civil_defense_response)
        self.graph.add_node("public_works_response", self.public_works_response)
        self.graph.add_node("get_human_verification", self.get_human_verification)
        self.graph.add_node("send_email_alert", self.send_email_alert)
        self.graph.add_node("handle_no_approval", self.handle_no_approval)

        # Add edges
        self.graph.add_edge("get_weather", "social_media_monitoring")
        self.graph.add_edge("social_media_monitoring", "analyze_disaster")
        self.graph.add_edge("analyze_disaster", "assess_severity")
        self.graph.add_edge("assess_severity", "data_logging")
        # clean up
        self.graph.add_conditional_edges("data_logging", self.route_response)

        self.graph.add_edge("civil_defense_response", "get_human_verification")
        self.graph.add_edge("public_works_response", "get_human_verification")
        self.graph.add_conditional_edges("get_human_verification", self.verify_approval_router)
        self.graph.add_edge("emergency_response", "send_email_alert")
        self.graph.add_edge("send_email_alert", END)
        self.graph.add_edge("handle_no_approval", END)

        self.graph.set_entry_point("get_weather")
    def route_response(state: WeatherState) -> Literal["emergency_response", "send_email_alert", "civil_defense_response", "public_works_response"]:
        """Route to appropriate department based on disaster type and severity"""
        disaster = state.disaster_type.strip().lower()
        severity = state.severity.strip().lower()

        if severity in ["critical", "high"]:
            return "emergency_response"
            "send_email_alert"
        elif "flood" in disaster or "storm" in disaster:
            return "public_works_response"
        else:
            return "civil_defense_response"
        

    def run_weather_emergency_system(self, location: WeatherLocation):
        """Initialize and run the weather emergency system for a given city"""

        print(f"Running weather emergency system for {location}")
        print(f"Initializing state for {location.__str__()}")
        initial_state = WeatherState(
            city=location.city,
            country=location.country,
            weather_data={},
            disaster_type="",
            severity="",
            response="",
            messages=[],
            alerts=[],
            social_media_reports=[],
            human_approved=False
        )

        try:
            result = self.app.invoke(initial_state,config=self.runnable_config,debug=True )
            print(f"Completed weather check for {location}")
            return result
        except Exception as e:
            print(f"Error running weather emergency system: {str(e)}")

a = WeatherDisasterManagementAgent()
a.run_weather_emergency_system(location=WeatherLocation(city="New York", country="US"))