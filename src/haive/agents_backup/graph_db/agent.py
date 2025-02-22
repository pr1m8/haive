from src.haive.agents.graph_db.state import OverallState,InputState,OutputState
from src.haive.agents.graph_db.aug_llms import correct_cypher_aug_llm_config,validate_cypher_aug_llm_config,\
      guardrails_aug_llm_config, text2cypher_aug_llm_config, \
        correct_cypher_aug_llm_config, generate_final_aug_llm_config
from src.haive.agents.base import AgentArchitecture,AgentArchitectureConfig
from pydantic import Field,BaseModel
from typing import List,Dict,Literal,Annotated,Union,Any,Optional
from src.haive.core.aug_llm.base import AugLLMConfig
from langgraph.types import Command
from neo4j.exceptions import CypherSyntaxError
from neo4j import GraphDatabase
from langchain_neo4j import Neo4jGraph,Neo4jVector
from langchain_neo4j.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
#from langchain_neo4j import Neo4jVector
#from langchain_openai import OpenAIEmbeddings
def guardrails_condition(
    state: OverallState,
) -> Literal["generate_cypher", "generate_final_answer"]:
    if state.get("next_action") == "end":
        return "generate_final_answer"
    elif state.get("next_action") == "movie":
        return "generate_cypher"
    
def validate_cypher_condition(
    state: OverallState,
) -> Literal["generate_final_answer", "correct_cypher", "execute_cypher"]:
    if state.get("next_action") == "end":
        return "generate_final_answer"
    elif state.get("next_action") == "correct_cypher":
        return "correct_cypher"
    elif state.get("next_action") == "execute_cypher":
        return "execute_cypher"
# ROuting,Branches, Stategraph, Required fields 
# Stategraph output parser. 
# Stategraph inoput ouput ConfigSchema

# Setup workflow, compile, add in demo, add in template . 

class GraphDBConfig(BaseModel):
    graph_db_uri: str = Field(default="bolt://localhost:7687",description="The URI of the graph database")
    graph_db_user: str = Field(default="neo4j",description="The username of the graph database")
    graph_db_password: str = Field(default="password",description="The password of the graph database")
    graph_db_database: str = Field(default="neo4j",description="The name of the database to connect to")
    enhanced_schema: bool = Field(default=True,description="Whether to use the enhanced schema")
    #@validator("graph_db_uri")
    #def validate_graph_db_uri(cls,v):
    #    if not v.startswith("bolt://"):
    #         raise ValueError("The graph database URI must start with 'bolt://'")
    #    return v
    @classmethod    
    def get_graph_db(cls):
        """Neo4j database wrapper for various graph operations.
        Parameters:
        url (Optional[str]): The URL of the Neo4j database server.
        username (Optional[str]): The username for database authentication.
        password (Optional[str]): The password for database authentication.
        database (str): The name of the database to connect to. Default is 'neo4j'.
        timeout (Optional[float]): The timeout for transactions in seconds.
                Useful for terminating long-running queries.
                By default, there is no timeout set.
        sanitize (bool): A flag to indicate whether to remove lists with
                more than 128 elements from results. Useful for removing
                embedding-like properties from database responses. Default is False.
        refresh_schema (bool): A flag whether to refresh schema information
                at initialization. Default is True.
        enhanced_schema (bool): A flag whether to scan the database for
                example values and use them in the graph schema. Default is False.
        driver_config (Dict): Configuration passed to Neo4j Driver.

        *Security note*: Make sure that the database connection uses credentials
            that are narrowly-scoped to only include necessary permissions.
            Failure to do so may result in data corruption or loss, since the calling
            code may attempt commands that would result in deletion, mutation
            of data if appropriately prompted or reading sensitive data if such
            data is present in the database.
            The best way to guard against such negative outcomes is to (as appropriate)
            limit the permissions granted to the credentials used with this tool.
        """
        return Neo4jGraph(
            url=cls.graph_db_uri,
            username=cls.graph_db_user,
            password=cls.graph_db_password,
            database=cls.graph_db_database,
            timeout=10,
            sanitize=True,
            refresh_schema=True,
            enhanced_schema=cls.enhanced_schema,
            #driver_config={"max_connection_lifetime": 3600}
        )  
    @classmethod
    def get_graph_db_schema(cls,enhanced_schema:bool=True):
        return GraphDBConfig.get_graph_db(enhanced_schema=enhanced_schema)
    

class GraphDBAgentConfig(AgentArchitectureConfig):
    aug_llm_configs: Dict[str,AugLLMConfig] = Field(description="The LLM runnable configs for the graph database agent",\
                                                              default={
                                                                  "correct_cypher": correct_cypher_aug_llm_config,
                                                                  "validate_cypher": validate_cypher_aug_llm_config,
                                                                  "generate_cypher": text2cypher_aug_llm_config,
                                                                  "guardrails": guardrails_aug_llm_config,
                                                                  "generate_final_answer": generate_final_aug_llm_config
                                                              })
    
    state_schema: OverallState = Field(default_factory=OverallState,description="The state schema for the graph database agent")
    graph_db_config: GraphDBConfig = Field(default_factory=GraphDBConfig,description="The graph database config for the graph database agent")




class GraphDBAgent(AgentArchitecture):
    def __init__(self, config: GraphDBAgentConfig):
        super().__init__(config)
        self.graph_db_enhanced_schema = self.config.graph_db_config.get_graph_db(enhanced_schema=True)
        #self.graph_db    
        #self.graph_db.query("MATCH (n) RETURN n")
        self.corrector_schema = [
            Schema(el["start"], el["type"], el["end"])
            for el in self.graph_db_enhanced_schema.structured_schema.get("relationships")
        ]

        self.cypher_query_corrector = CypherQueryCorrector(self.corrector_schema)
        self.no_results = "No results found"



    def setup_workflow(self):
        self.workflow = self.compose_workflow(self.config.llm_runnable_configs)

    def correct_cypher(self,state: OverallState) -> OverallState:
        """
        Correct the Cypher statement based on the provided errors.
        """
        corrected_cypher = self.workflow["correct_cypher"].invoke(
            {
                "question": state.get("question"),
                "errors": state.get("cypher_errors"),
                "cypher": state.get("cypher_statement"),
                "schema": self.graph_db_enhanced_schema.schema,
            }
        )

        return Command(update={
            "next_action": "validate_cypher",
            "cypher_statement": corrected_cypher,
            "steps": ["correct_cypher"],
        }
        )



    def validate_cypher(self,state: OverallState) -> OverallState:
        """
        Validates the Cypher statements and maps any property values to the database.
        """
        errors = []
        mapping_errors = []
        # Check for syntax errors
        try:
            self.graph_db_config.graph_db_uri.query(f"EXPLAIN {state.get('cypher_statement')}")
        except CypherSyntaxError as e:
            errors.append(e.message)
        # Experimental feature for correcting relationship directions
        corrected_cypher = self.cypher_query_corrector(state.get("cypher_statement"))
        if not corrected_cypher:
            errors.append("The generated Cypher statement doesn't fit the graph schema")
        if not corrected_cypher == state.get("cypher_statement"):
            print("Relationship direction was corrected")
        # Use LLM to find additional potential errors and get the mapping for values
        llm_output = self.workflow["validate_cypher"].invoke(
            {
                "question": state.get("question"),
                "schema": self.graph_db_enhanced_schema.schema,
                "cypher": state.get("cypher_statement"),
            }
        )
        if llm_output.errors:
            errors.extend(llm_output.errors)
        if llm_output.filters:
            for filter in llm_output.filters:
                # Do mapping only for string values
                if (
                    not [
                        prop
                        for prop in self.graph_db_enhanced_schema.structured_schema["node_props"][
                            filter.node_label
                        ]
                        if prop["property"] == filter.property_key
                    ][0]["type"]
                    == "STRING"
                ):
                    continue
                mapping = self.graph_db_enhanced_schema.query(
                    f"MATCH (n:{filter.node_label}) WHERE toLower(n.`{filter.property_key}`) = toLower($value) RETURN 'yes' LIMIT 1",
                    {"value": filter.property_value},
                )
                if not mapping:
                    print(
                        f"Missing value mapping for {filter.node_label} on property {filter.property_key} with value {filter.property_value}"
                    )
                    mapping_errors.append(
                        f"Missing value mapping for {filter.node_label} on property {filter.property_key} with value {filter.property_value}"
                    )
        if mapping_errors:
            next_action = "end"
        elif errors:
            next_action = "correct_cypher"
        else:
            next_action = "execute_cypher"

        return Command(update={
            "next_action": next_action,
            "cypher_statement": corrected_cypher,
            "cypher_errors": errors,
            "steps": ["validate_cypher"],
        })

    def generate_cypher(self,state: OverallState) -> OverallState:
        """
        Generates a cypher statement based on the provided schema and user input
        """
        NL = "\n"
        fewshot_examples = (NL * 2).join(
            [
                f"Question: {el['question']}{NL}Cypher:{el['query']}"
                for el in self.example_selector.select_examples(
                    {"question": state.get("question")}
                )
            ]
        )
        generated_cypher = self.workflow["text2cypher"].invoke(
            {
                "question": state.get("question"),
                "fewshot_examples": fewshot_examples,
                "schema": self.graph_db_enhanced_schema.schema,
            }
        )
        return Command(update={
            "cypher_statement": generated_cypher,
            "steps": ["generate_cypher"]
        })

    def execute_cypher(self,state: OverallState) -> OverallState:
        """
        Executes the given Cypher statement.
        """

        records = self.graph_db_enhanced_schema.query(state.get("cypher_statement"))
        return Command(update={
            "database_records": records if records else self.no_results,
            "next_action": "end",
            "steps": ["execute_cypher"],
        })
    
    def generate_final_answer(self,state: OverallState) -> OutputState:
        """
        Decides if the question is related to movies.
        """
        final_answer = self.workflow["generate_final_answer"].invoke(
            {"question": state.get("question"), "results": state.get("database_records")}
        )
        return Command(update={
            "answer": final_answer,
            "steps": ["generate_final_answer"]
        })
