# Additional tests for AugLLMConfig formats and schemas

import json
import pprint
from typing import Any, Literal

import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import (
    JsonOutputParser,
    PydanticOutputParser,
    StrOutputParser,
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.tools import StructuredTool, tool
from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.schema_composer import SchemaComposer

from .conftest import WeatherQuery, check_api_keys, skip_if_no_api_keys

# Define the decorator
skip_if_no_api_keys = pytest.mark.skipif(
    check_api_keys() == False,  # Make sure check_api_keys() is defined
    reason="No API keys available for LLM testing",
)
# Import your existing fixtures here
# from tests.core.engine.test_aug_llm_config import azure_llm_config, check_api_keys, skip_if_no_api_keys, simple_chat_prompt, structured_chat_prompt, weather_tool, calculator_tool

# --------------------------------
# New structured output models
# --------------------------------


class ProductReview(BaseModel):
    """Model for a product review."""

    product_name: str = Field(description="Name of the product")
    rating: int = Field(description="Rating from 1-5 stars", ge=1, le=5)
    pros: list[str] = Field(description="List of positive aspects")
    cons: list[str] = Field(description="List of negative aspects")
    summary: str = Field(description="Brief summary of the review")
    recommendation: Literal["Recommended", "Not Recommended", "Neutral"] = Field(
        description="Overall recommendation"
    )


class UserProfile(BaseModel):
    """Model for a user profile."""

    username: str = Field(description="User's handle")
    name: str | None = Field(None, description="User's full name")
    age: int | None = Field(None, description="User's age")
    interests: list[str] = Field(default_factory=list, description="User's interests")
    bio: str | None = Field(None, description="User's biography")
    contact_info: dict[str, str] | None = Field(
        None, description="User's contact information"
    )
    preferences: dict[str, Any] = Field(
        default_factory=dict, description="User's preferences"
    )


class RecipeIngredient(BaseModel):
    """Model for a recipe ingredient."""

    name: str = Field(description="Ingredient name")
    quantity: float | None = Field(None, description="Amount needed")
    unit: str | None = Field(None, description="Unit of measurement")
    notes: str | None = Field(None, description="Special notes about this ingredient")


class RecipeStep(BaseModel):
    """Model for a recipe step."""

    number: int = Field(description="Step number")
    instruction: str = Field(description="Step instruction")
    time_minutes: int | None = Field(
        None, description="Time needed for this step in minutes"
    )


class Recipe(BaseModel):
    """Model for a complete recipe."""

    title: str = Field(description="Recipe title")
    description: str | None = Field(None, description="Recipe description")
    prep_time_minutes: int | None = Field(
        None, description="Preparation time in minutes"
    )
    cook_time_minutes: int | None = Field(None, description="Cooking time in minutes")
    servings: int | None = Field(None, description="Number of servings")
    ingredients: list[RecipeIngredient] = Field(description="List of ingredients")
    steps: list[RecipeStep] = Field(description="List of steps")
    tags: list[str] | None = Field(None, description="Recipe tags")


class MovieReview(BaseModel):
    """Model for a movie review."""

    movie_title: str = Field(description="Title of the movie")
    year: int | None = Field(None, description="Release year")
    director: str | None = Field(None, description="Movie director")
    rating: float = Field(description="Rating from 0.0 to 10.0", ge=0.0, le=10.0)
    review_text: str = Field(description="The main review text")
    pros: list[str] | None = Field(None, description="Positive aspects")
    cons: list[str] | None = Field(None, description="Negative aspects")
    recommendation: Literal["Must See", "Worth Watching", "Skip It"] = Field(
        description="Overall recommendation"
    )


# --------------------------------
# Additional fixtures for testing
# --------------------------------


@pytest.fixture
def complex_chat_prompt():
    """Create a more complex chat prompt with multiple components."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a specialized assistant with varied capabilities.
        
        When analyzing content, provide detailed breakdowns.
        When summarizing, be concise and focus on key points.
        When explaining, use simple language and examples.
        
        Always format your responses clearly using markdown when appropriate.
        """
            ),
            MessagesPlaceholder(variable_name="context", optional=True),
            MessagesPlaceholder(variable_name="examples", optional=True),
            MessagesPlaceholder(variable_name="messages"),
            HumanMessagePromptTemplate.from_template(
                "Additional instructions: {instructions}"
            ),
        ]
    )


@pytest.fixture
def custom_template_with_variables():
    """Create a chat template with multiple variables."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a helpful assistant that provides information about {topic}.
        Your tone should be {tone} and you should focus on {focus_area}.
        """
            ),
            HumanMessagePromptTemplate.from_template(
                "I want to know about {query}. Remember to include {important_aspect}."
            ),
            MessagesPlaceholder(variable_name="additional_context", optional=True),
            MessagesPlaceholder(variable_name="messages", optional=True),
        ]
    )


@pytest.fixture
def json_parser():
    """Create a JSON output parser."""
    return JsonOutputParser()


@pytest.fixture
def advanced_weather_tool():
    """Create a more advanced weather tool with multiple parameters."""

    def get_weather_forecast(
        location: str,
        days: int = 1,
        include_hourly: bool = False,
        units: Literal["celsius", "fahrenheit"] = "celsius",
    ) -> dict[str, Any]:
        """Get detailed weather forecast for a location.

        Args:
            location: City or location name
            days: Number of days to forecast (1-7)
            include_hourly: Whether to include hourly breakdown
            units: Temperature units (celsius or fahrenheit)

        Returns:
            Weather forecast data
        """
        # Simulate forecast data
        base_temp = {
            "New York": 75,
            "London": 60,
            "Tokyo": 70,
            "Sydney": 80,
            "Paris": 65,
        }.get(location, 70)

        # Convert if needed
        if units == "celsius":
            base_temp = round((base_temp - 32) * 5 / 9)

        # Generate forecasts for requested days
        forecasts = []
        for i in range(days):
            # Simple variation per day
            temp_adjustment = i * 2 - 4  # -4, -2, 0, 2, 4, ...

            daily_forecast = {
                "date": f"2023-10-{15 + i}",
                "high_temp": base_temp + temp_adjustment + 5,
                "low_temp": base_temp + temp_adjustment - 5,
                "conditions": ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"][i % 4],
                "precipitation_chance": [10, 30, 60, 20][i % 4],
            }

            # Add hourly if requested
            if include_hourly:
                hourly = []
                for hour in range(0, 24, 3):  # Every 3 hours
                    hourly.append(
                        {
                            "time": f"{hour:02d}:00",
                            "temp": base_temp
                            + temp_adjustment
                            + (5 if 10 <= hour <= 16 else 0),
                            "conditions": ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"][
                                (i + hour // 6) % 4
                            ],
                        }
                    )
                daily_forecast["hourly"] = hourly

            forecasts.append(daily_forecast)

        return {
            "location": location,
            "units": units,
            "days": days,
            "forecasts": forecasts,
        }

    return StructuredTool.from_function(get_weather_forecast)


@pytest.fixture
def recipe_search_tool():
    """Create a recipe search tool."""

    def search_recipes(
        query: str,
        cuisine: str | None = None,
        max_results: int = 3,
        diet_restrictions: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Search for recipes based on criteria.

        Args:
            query: Search terms
            cuisine: Type of cuisine (Italian, Mexican, etc.)
            max_results: Maximum number of results to return
            diet_restrictions: List of dietary restrictions

        Returns:
            List of matching recipes
        """
        # Simulated recipe database
        recipes = [
            {
                "id": "r1",
                "title": "Spaghetti Carbonara",
                "cuisine": "Italian",
                "ingredients": ["pasta", "eggs", "bacon", "cheese", "pepper"],
                "diet_tags": ["contains_gluten", "contains_dairy"],
            },
            {
                "id": "r2",
                "title": "Chicken Tacos",
                "cuisine": "Mexican",
                "ingredients": ["tortillas", "chicken", "salsa", "cheese", "lettuce"],
                "diet_tags": ["contains_gluten", "contains_dairy"],
            },
            {
                "id": "r3",
                "title": "Vegetable Curry",
                "cuisine": "Indian",
                "ingredients": ["rice", "vegetables", "curry paste", "coconut milk"],
                "diet_tags": ["vegan", "gluten_free"],
            },
            {
                "id": "r4",
                "title": "Greek Salad",
                "cuisine": "Greek",
                "ingredients": [
                    "tomatoes",
                    "cucumber",
                    "feta cheese",
                    "olives",
                    "olive oil",
                ],
                "diet_tags": ["vegetarian", "gluten_free"],
            },
            {
                "id": "r5",
                "title": "Beef Stir Fry",
                "cuisine": "Chinese",
                "ingredients": ["beef", "vegetables", "soy sauce", "rice"],
                "diet_tags": ["gluten_free"],
            },
        ]

        # Filter by search terms
        matches = []
        query_terms = query.lower().split()
        for recipe in recipes:
            # Search in title and ingredients
            title_matches = any(term in recipe["title"].lower() for term in query_terms)
            ingredient_matches = any(
                any(term in ingredient.lower() for term in query_terms)
                for ingredient in recipe["ingredients"]
            )

            # Apply cuisine filter if provided
            cuisine_match = True
            if cuisine:
                cuisine_match = cuisine.lower() == recipe["cuisine"].lower()

            # Apply diet restrictions if provided
            diet_match = True
            if diet_restrictions:
                for restriction in diet_restrictions:
                    if restriction.startswith("no_"):
                        # Check that recipe doesn't have this tag
                        restricted_item = restriction[3:]  # Remove "no_" prefix
                        if any(
                            tag.endswith(restricted_item) for tag in recipe["diet_tags"]
                        ):
                            diet_match = False
                            break
                    # Check that recipe has this tag
                    elif restriction not in recipe["diet_tags"]:
                        diet_match = False
                        break

            # Add to matches if it passes all filters
            if (title_matches or ingredient_matches) and cuisine_match and diet_match:
                matches.append(recipe)

        # Return limited number of results
        return matches[:max_results]

    return StructuredTool.from_function(search_recipes)


# --------------------------------
# Schema pretty printing tests
# --------------------------------


@skip_if_no_api_keys
def test_schema_pretty_printing(azure_llm_config, structured_chat_prompt):
    """Test creating and pretty printing schemas from AugLLMConfig."""
    # Create several different AugLLM configs
    person_extractor = AugLLMConfig(
        name="person_extractor",
        llm_config=azure_llm_config,
        prompt_template=structured_chat_prompt,
        structured_output_model=UserProfile,
    )

    recipe_analyzer = AugLLMConfig(
        name="recipe_analyzer",
        llm_config=azure_llm_config,
        prompt_template=structured_chat_prompt,
        structured_output_model=Recipe,
    )

    movie_reviewer = AugLLMConfig(
        name="movie_reviewer",
        llm_config=azure_llm_config,
        prompt_template=structured_chat_prompt,
        structured_output_model=MovieReview,
    )

    # Create schemas for these engines
    user_schema = SchemaComposer.create_model(
        [person_extractor], name="UserProfileSchema"
    )
    recipe_schema = SchemaComposer.create_model([recipe_analyzer], name="RecipeSchema")
    movie_schema = SchemaComposer.create_model(
        [movie_reviewer], name="MovieReviewSchema"
    )

    # Pretty print the schemas and their fields
    for schema_name, schema in [
        ("UserProfile", user_schema),
        ("Recipe", recipe_schema),
        ("MovieReview", movie_schema),
    ]:
        print(f"\n{'='*20} {schema_name} Schema {'='*20}")

        # Print model fields
        print(f"\nFields in {schema.__name__}:")
        for field_name, field_info in schema.model_fields.items():
            field_type = field_info.annotation
            field_default = field_info.default
            print(f"  - {field_name}: {field_type}")
            if field_default is not ...:
                print(f"      Default: {field_default}")
            if field_info.description:
                print(f"      Description: {field_info.description}")

        # Create an example instance
        if schema_name == "UserProfile":
            instance = schema(
                username="jdoe",
                name="John Doe",
                age=30,
                interests=["coding", "hiking", "reading"],
                bio="Software developer with a passion for AI",
                preferences={"theme": "dark", "notifications": True},
            )
        elif schema_name == "Recipe":
            instance = schema(
                title="Chocolate Chip Cookies",
                description="Classic homemade cookies",
                prep_time_minutes=15,
                cook_time_minutes=10,
                servings=12,
                ingredients=[
                    {"name": "flour", "quantity": 2.0, "unit": "cups"},
                    {"name": "chocolate chips", "quantity": 1.0, "unit": "cup"},
                    {"name": "butter", "quantity": 0.5, "unit": "cup"},
                ],
                steps=[
                    {
                        "number": 1,
                        "instruction": "Mix dry ingredients",
                        "time_minutes": 2,
                    },
                    {
                        "number": 2,
                        "instruction": "Add chocolate chips",
                        "time_minutes": 1,
                    },
                    {"number": 3, "instruction": "Bake at 350°F", "time_minutes": 10},
                ],
                tags=["dessert", "baking", "cookies"],
            )
        elif schema_name == "MovieReview":
            instance = schema(
                movie_title="Inception",
                year=2010,
                director="Christopher Nolan",
                rating=9.2,
                review_text="A mind-bending masterpiece with stunning visuals.",
                pros=["Innovative concept", "Great acting", "Amazing visuals"],
                cons=["Complex plot may confuse some viewers"],
                recommendation="Must See",
            )

        # Pretty print the instance
        print(f"\nExample {schema_name} instance:")
        pprint.pprint(instance.model_dump(), width=80, sort_dicts=False)

        # Convert to JSON and pretty print
        print(f"\n{schema_name} as JSON:")
        print(json.dumps(instance.model_dump(), indent=2))

    # Create a combined schema
    combined_schema = SchemaComposer.compose_schema(
        [person_extractor, recipe_analyzer, movie_reviewer], name="CombinedSchema"
    )

    print("\n" + "=" * 20 + " Combined Schema " + "=" * 20)
    print(f"\nFields in {combined_schema.__name__}:")
    for field_name, field_info in combined_schema.model_fields.items():
        field_type = field_info.annotation
        print(f"  - {field_name}: {field_type}")

    # Test StateSchema creation
    state_schema = SchemaComposer.create_model(
        [person_extractor, recipe_analyzer, movie_reviewer], name="ContentAnalysisState"
    )
    print("-" * 100)
    print("State Schema")
    state_schema.pretty_print()
    print(state_schema)
    print("-" * 100)

    print("\n" + "=" * 20 + " State Schema " + "=" * 20)
    print(f"\nFields in {state_schema.__name__}:")
    for field_name, field_info in state_schema.model_fields.items():
        field_type = field_info.annotation
        print(f"  - {field_name}: {field_type}")

    # Verify this is a StateSchema with shared fields and reducers
    print(f"\nShared fields: {state_schema.__shared_fields__}")
    print(f"Reducer fields: {list(state_schema.__reducer_fields__.keys())}")

    # No assertions needed - this test is for demonstration purposes
    assert True


# --------------------------------
# Various input format tests
# --------------------------------


@skip_if_no_api_keys
def test_various_input_formats(
    azure_llm_config, complex_chat_prompt, custom_template_with_variables
):
    """Test AugLLMConfig with various input formats."""
    # Create AugLLM with complex input structure
    aug_llm = AugLLMConfig(
        name="flexible_assistant",
        llm_config=azure_llm_config,
        prompt_template=complex_chat_prompt,
    )

    # Test 1: Simple string input
    result1 = aug_llm.create_runnable().invoke("Tell me about quantum computing")
    print("\n" + "=" * 20 + " Result from string input " + "=" * 20)
    print(result1.content if hasattr(result1, "content") else result1)

    # Test 2: Message list input
    messages_input = [
        HumanMessage(content="What are the main cloud providers?"),
        AIMessage(
            content="The main cloud providers include AWS, Microsoft Azure, and Google Cloud Platform."
        ),
        HumanMessage(content="Tell me more about Azure specifically"),
    ]

    result2 = aug_llm.invoke({"messages": messages_input})
    print("\n" + "=" * 20 + " Result from message list input " + "=" * 20)
    print(result2.content if hasattr(result2, "content") else result2)

    # Test 3: Complex input with all template variables
    complex_input = {
        "context": [
            SystemMessage(content="Azure is Microsoft's cloud computing platform.")
        ],
        "examples": [
            HumanMessage(content="What services does Azure offer?"),
            AIMessage(
                content="Azure offers compute, storage, database, AI, analytics, and many other services."
            ),
        ],
        "messages": [
            HumanMessage(content="How do Azure Functions compare to AWS Lambda?")
        ],
        "instructions": "Compare pricing, features, and integration capabilities",
    }

    result3 = aug_llm.invoke(complex_input)
    print("\n" + "=" * 20 + " Result from complex input " + "=" * 20)
    print(result3.content if hasattr(result3, "content") else result3)

    # Test 4: Custom template with variables
    custom_template = custom_template_with_variables  # Now using the fixture directly
    custom_llm = AugLLMConfig(
        name="custom_template_llm",
        llm_config=azure_llm_config,
        prompt_template=custom_template,
    )

    custom_input = {
        "topic": "artificial intelligence",
        "tone": "educational",
        "focus_area": "ethical considerations",
        "query": "the impact of large language models",
        "important_aspect": "bias and fairness",
        "additional_context": [
            SystemMessage(content="Large language models have revolutionized NLP.")
        ],
    }

    result4 = custom_llm.invoke(custom_input)
    print("\n" + "=" * 20 + " Result from custom template " + "=" * 20)
    print(result4.content if hasattr(result4, "content") else result4)

    # All tests should produce reasonable results
    assert result1 is not None
    assert result2 is not None
    assert result3 is not None
    assert result4 is not None


# --------------------------------
# Output parser tests
# --------------------------------


@skip_if_no_api_keys
def test_different_output_parsers(
    azure_llm_config, structured_chat_prompt, json_parser
):
    """Test AugLLMConfig with different output parsers."""
    # Test 1: String output parser
    str_parser = StrOutputParser()
    str_llm = AugLLMConfig(
        name="string_output_llm",
        llm_config=azure_llm_config,
        prompt_template=structured_chat_prompt,
        output_parser=str_parser,
    )

    str_result = str_llm.invoke("List 3 programming languages")
    print("\n" + "=" * 20 + " String Parser Result " + "=" * 20)
    print(str_result)
    assert isinstance(str_result, str)

    # Test 2: JSON output parser
    system_prompt = """
    You are a data generation assistant. Generate data in JSON format based on the request.
    Return ONLY valid JSON with no explanations or narrative text.
    """

    json_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    json_llm = AugLLMConfig(
        name="json_output_llm",
        llm_config=azure_llm_config,
        prompt_template=json_prompt,
        output_parser=json_parser,
    )

    json_result = json_llm.invoke(
        "Generate a list of 3 users with name, age, and email fields"
    )
    print("\n" + "=" * 20 + " JSON Parser Result " + "=" * 20)
    print(json.dumps(json_result, indent=2))
    assert isinstance(json_result, (dict, list))

    # Test 3: Pydantic output parser
    pydantic_parser = PydanticOutputParser(pydantic_object=ProductReview)

    system_prompt = f"""
    You are a product review analysis assistant. Extract the product review information.
    {pydantic_parser.get_format_instructions()}
    """

    pydantic_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    pydantic_llm = AugLLMConfig(
        name="pydantic_output_llm",
        llm_config=azure_llm_config,
        prompt_template=pydantic_prompt,
        output_parser=pydantic_parser,
    )

    review_text = """
    The Sony WH-1000XM4 headphones are amazing. The noise cancellation is top-notch,
    and the sound quality is excellent. Battery life is impressive at around 30 hours.
    On the downside, they're a bit pricey, and the touch controls can be finicky.
    Overall, I'd give them 4.5/5 stars and definitely recommend them to anyone looking
    for premium wireless headphones.
    """

    pydantic_result = pydantic_llm.invoke(review_text)
    print("\n" + "=" * 20 + " Pydantic Parser Result " + "=" * 20)
    print(pydantic_result.model_dump_json(indent=2))
    assert isinstance(pydantic_result, ProductReview)

    # Test 4: Custom output processor using lambda
    def extract_key_points(text: str) -> list[str]:
        """Custom function to extract key points from text."""
        # In a real scenario, this might use regex or more complex parsing
        lines = text.split("\n")
        points = [line.strip() for line in lines if line.strip().startswith("-")]
        return points if points else [line.strip() for line in lines if line.strip()]

    system_prompt = """
    You are a summarization assistant. Provide key points from the given text.
    Format each key point on a new line starting with a dash (-).
    """

    custom_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # Create with custom postprocessing
    custom_llm = AugLLMConfig(
        name="custom_processor_llm",
        llm_config=azure_llm_config,
        prompt_template=custom_prompt,
        postprocess=extract_key_points,
    )

    custom_result = custom_llm.invoke(
        """
    Summarize the key features of modern smartphones, including 
    cameras, processors, displays, and battery technology.
    """
    )

    print("\n" + "=" * 20 + " Custom Processor Result " + "=" * 20)
    for i, point in enumerate(custom_result, 1):
        print(f"{i}. {point}")

    assert isinstance(custom_result, list)
    assert len(custom_result) > 0


# --------------------------------
# Advanced tools and structured output tests
# --------------------------------


@skip_if_no_api_keys
def test_advanced_tools_with_structured_output(
    azure_llm_config, advanced_weather_tool, recipe_search_tool
):
    """Test using advanced tools with structured output models."""
    # Create system prompt that encourages tool use
    system_prompt = """
    You are a helpful assistant with access to specialized tools.
    Use the appropriate tool based on the user's request.
    Provide results in a structured format.
    """

    tool_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # Create different AugLLM configs for different scenarios

    # 1. Weather forecast tool with structured output
    weather_llm = AugLLMConfig(
        name="weather_forecast_llm",
        llm_config=azure_llm_config,
        prompt_template=tool_prompt,
        tools=[advanced_weather_tool],
        structured_output_model=WeatherQuery,
    )

    # Test weather forecast query
    weather_query = (
        "What's the weather forecast for Tokyo for the next 3 days in celsius?"
    )
    weather_result = weather_llm.invoke(weather_query)

    print("\n" + "=" * 20 + " Weather Forecast Tool With Structured Output " + "=" * 20)
    print(f"Query: {weather_query}")
    print(f"Structured Output: {weather_result.model_dump()}")

    # 2. Recipe search tool with full Recipe output model
    recipe_system_prompt = """
    You are a culinary assistant that can search for recipes and provide detailed information.
    Use the recipe search tool to find recipes, then transform them into complete recipe instructions.
    Provide your response as a fully structured recipe.
    """

    recipe_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=recipe_system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    recipe_llm = AugLLMConfig(
        name="recipe_llm",
        llm_config=azure_llm_config,
        prompt_template=recipe_prompt,
        tools=[recipe_search_tool],
        structured_output_model=Recipe,
    )

    # Test recipe search query
    recipe_query = "Find me a vegetarian recipe"
    recipe_result = recipe_llm.invoke(recipe_query)

    print("\n" + "=" * 20 + " Recipe Tool With Structured Output " + "=" * 20)
    print(f"Query: {recipe_query}")
    print(f"Structured Output: {json.dumps(recipe_result.model_dump(), indent=2)}")

    # 3. Tool combination with product review output
    combined_system_prompt = """
    You are a comprehensive research assistant with multiple tools.
    First research product information using available tools, then generate a product review.
    Format your response as a structured product review.
    """

    combined_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=combined_system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # Create a simple product info lookup tool
    @tool
    def get_product_info(product_name: str) -> dict[str, Any]:
        """Look up information about a product."""
        # Simulated product database
        products = {
            "iphone": {
                "name": "iPhone 15 Pro",
                "category": "Smartphone",
                "price": 999,
                "features": [
                    "A17 chip",
                    "48MP camera",
                    "Titanium design",
                    "USB-C port",
                ],
                "release_date": "2023-09-22",
            },
            "macbook": {
                "name": "MacBook Air M2",
                "category": "Laptop",
                "price": 1199,
                "features": [
                    "M2 chip",
                    "13.6-inch display",
                    "18 hour battery",
                    "1080p camera",
                ],
                "release_date": "2022-07-15",
            },
            "airpods": {
                "name": "AirPods Pro 2",
                "category": "Earbuds",
                "price": 249,
                "features": [
                    "Active noise cancellation",
                    "Adaptive transparency",
                    "Spatial audio",
                    "H2 chip",
                ],
                "release_date": "2022-09-23",
            },
        }

        # Case-insensitive lookup
        for key, info in products.items():
            if (
                product_name.lower() in key.lower()
                or key.lower() in product_name.lower()
            ):
                return info

        return {"error": f"Product '{product_name}' not found"}

    # Create the combined LLM
    combined_llm = AugLLMConfig(
        name="product_review_llm",
        llm_config=azure_llm_config,
        prompt_template=combined_prompt,
        tools=[get_product_info],
        structured_output_model=ProductReview,
    )

    # Test product review generation
    product_query = "Write a review of the latest iPhone"
    product_result = combined_llm.invoke(product_query)

    print("\n" + "=" * 20 + " Product Review Tool With Structured Output " + "=" * 20)
    print(f"Query: {product_query}")
    print(f"Structured Output: {json.dumps(product_result.model_dump(), indent=2)}")

    # Verify basic functionality
    assert isinstance(weather_result, WeatherQuery)
    assert isinstance(recipe_result, Recipe)
    assert isinstance(product_result, ProductReview)

    # Enhanced schema creation - show how the schema builder works with tools and structured outputs
    print("\n" + "=" * 20 + " Schema From Tool Configs " + "=" * 20)
    combined_schema = SchemaComposer.create_model(
        [weather_llm, recipe_llm, combined_llm], name="ToolsSchema"
    )

    # Print model fields
    print(f"\nFields in {combined_schema.__name__}:")
    for field_name, field_info in combined_schema.model_fields.items():
        field_type = field_info.annotation
        print(f"  - {field_name}: {field_type}")
