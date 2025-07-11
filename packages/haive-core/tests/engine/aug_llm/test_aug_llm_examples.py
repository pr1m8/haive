# tests/core/engine/test_aug_llm_task_examples.py

import logging
import os

import pytest
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel, Field

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Skip tests if API keys aren't available
def check_api_keys():
    """Check if necessary API keys are available in environment."""
    api_keys = {
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    }

    return any(api_keys.values())


# Test skipping decorator
skip_if_no_api_keys = pytest.mark.skipif(
    not check_api_keys(), reason="No API keys available for LLM testing"
)


# Test fixtures
@pytest.fixture
def azure_llm_config():
    """Create Azure LLM config for testing."""
    return AzureLLMConfig(
        model="gpt-4o", temperature=0.0, max_tokens=1000  # Deterministic for testing
    )


# --------------------------------
# Generic Task Templates
# --------------------------------


@pytest.fixture
def summarization_prompt():
    """Create a summarization prompt template with content placeholder."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a summarization expert. Provide a concise summary of the content below.
        Focus on the main points and key takeaways.
        
        Your summary should:
        - Be about 3-5 sentences long
        - Highlight the most important information
        - Omit unnecessary details
        - Be objective and factual
        """
            ),
            HumanMessagePromptTemplate.from_template(
                "Please summarize the following content:\n\n{content}"
            ),
        ]
    )


@pytest.fixture
def analysis_prompt():
    """Create an analysis prompt template with content placeholder."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are an analytical assistant. Provide a detailed analysis of the content below.
        
        Your analysis should:
        - Identify key themes and patterns
        - Evaluate the strengths and weaknesses
        - Consider implications and potential applications
        - Be organized with clear subheadings
        """
            ),
            HumanMessagePromptTemplate.from_template(
                "Please analyze the following content:\n\n{content}"
            ),
        ]
    )


@pytest.fixture
def extraction_prompt():
    """Create an extraction prompt template with content placeholder."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a data extraction specialist. Extract the following types of information 
        from the content below:
        
        1. Names of people
        2. Organizations mentioned
        3. Locations
        4. Dates and times
        5. Key metrics or statistics
        
        Format your response as a structured list with categories.
        """
            ),
            HumanMessagePromptTemplate.from_template(
                "Extract information from the following content:\n\n{content}"
            ),
        ]
    )


@pytest.fixture
def qa_prompt():
    """Create a Q&A prompt template with content and question placeholders."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a question answering assistant. Answer the question based only on the 
        provided content. If the content doesn't contain the answer, say 'I don't have 
        enough information to answer this question.'
        
        Keep your answers concise and to the point.
        """
            ),
            HumanMessagePromptTemplate.from_template(
                """
        Content:
        {content}
        
        Question: {question}
        """
            ),
        ]
    )


@pytest.fixture
def comparison_prompt():
    """Create a comparison prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a comparison specialist. Compare and contrast the items provided.
        
        Your response should:
        - Identify similarities and differences
        - Evaluate relative strengths and weaknesses
        - Provide a balanced assessment
        - End with a brief recommendation if appropriate
        """
            ),
            HumanMessagePromptTemplate.from_template(
                """
        Compare the following:
        
        Item 1: {item1}
        
        Item 2: {item2}
        
        Comparison criteria: {criteria}
        """
            ),
        ]
    )


@pytest.fixture
def translation_prompt():
    """Create a translation prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a translation assistant. Translate the provided text from the source 
        language to the target language.
        
        Maintain the meaning, tone, and style of the original as much as possible.
        """
            ),
            HumanMessagePromptTemplate.from_template(
                """
        Text to translate: {text}
        
        Source language: {source_language}
        Target language: {target_language}
        """
            ),
        ]
    )


@pytest.fixture
def code_generation_prompt():
    """Create a code generation prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a coding assistant. Generate code based on the requirements provided.
        
        Your code should be:
        - Well-structured and organized
        - Properly commented
        - Following best practices for the language
        - Ready to use
        """
            ),
            HumanMessagePromptTemplate.from_template(
                """
        Requirements: {requirements}
        
        Programming language: {language}
        
        Additional specifications: {specifications}
        """
            ),
        ]
    )


@pytest.fixture
def format_conversion_prompt():
    """Create a format conversion prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a format conversion assistant. Convert the provided content from the 
        source format to the target format.
        
        Maintain all the information from the original content while adapting to the 
        new format's conventions and requirements.
        """
            ),
            HumanMessagePromptTemplate.from_template(
                """
        Content to convert:
        {content}
        
        Source format: {source_format}
        Target format: {target_format}
        """
            ),
        ]
    )


# --------------------------------
# Test Sample Content
# --------------------------------


@pytest.fixture
def sample_article():
    """Sample article text for testing."""
    return """
    # Advances in Machine Learning: A 2023 Perspective

    The field of machine learning has seen remarkable progress in 2023, with breakthroughs in several key areas. Large language models (LLMs) have continued to evolve, with models like GPT-4 demonstrating unprecedented capabilities in natural language understanding and generation. These models are now being applied across industries, from healthcare to financial services.

    ## Multimodal Learning

    One of the most significant developments has been in multimodal learning, where models can process and generate content across different modalities such as text, images, audio, and video. Models like DALL-E 3 and Midjourney have pushed the boundaries of image generation, while systems like GPT-4V have demonstrated the ability to reason about visual content alongside text.

    ## Efficiency Improvements

    Researchers have made substantial progress in making AI models more efficient. Techniques like quantization, pruning, and knowledge distillation have enabled the deployment of powerful models on edge devices with limited computational resources. This trend towards "AI at the edge" is enabling new applications in IoT, autonomous vehicles, and mobile devices.

    ## Responsible AI

    The focus on responsible AI has intensified, with increased attention to issues of bias, fairness, transparency, and privacy. New methods for evaluating and mitigating bias in training data and model outputs have been developed, while regulatory frameworks around the world are evolving to address the ethical challenges posed by AI systems.

    ## Conclusion

    As we look ahead to 2024, the pace of innovation in machine learning shows no signs of slowing down. The integration of AI into everyday applications continues to accelerate, bringing both exciting opportunities and important challenges for researchers, developers, policymakers, and society as a whole.
    """


@pytest.fixture
def sample_product_comparison():
    """Sample product comparison text for testing."""
    return {
        "item1": """
        iPhone 15 Pro:
        - 6.1-inch OLED display with ProMotion technology
        - A17 Pro chip with 6-core CPU and 6-core GPU
        - Triple camera system (48MP main, 12MP ultra-wide, 12MP telephoto)
        - Titanium design, USB-C port
        - iOS 17
        - Starting price: $999
        """,
        "item2": """
        Samsung Galaxy S23 Ultra:
        - 6.8-inch Dynamic AMOLED display
        - Snapdragon 8 Gen 2 processor
        - Quad camera system (200MP main, 12MP ultra-wide, 10MP telephoto, 10MP telephoto)
        - S Pen included, aluminum design
        - Android 13 with One UI 5.1
        - Starting price: $1,199
        """,
        "criteria": "Camera quality, performance, display, battery life, and value for money.",
    }


@pytest.fixture
def sample_business_data():
    """Sample business data for extraction."""
    return """
    QUARTERLY BUSINESS REVIEW
    
    Company: TechNova Solutions Inc.
    Date: October 15, 2023
    Prepared by: Jennifer Martinez, Chief Financial Officer
    
    FINANCIAL HIGHLIGHTS:
    
    - Q3 2023 revenue reached $24.5 million, a 18.3% increase compared to Q3 2022
    - Gross margin improved to 68.2% (up from 65.7% in previous quarter)
    - Operating expenses totaled $10.2 million, representing 41.6% of revenue
    - EBITDA of $6.5 million, with EBITDA margin of 26.5%
    - Cash reserves of $18.7 million as of September 30, 2023
    
    KEY BUSINESS DEVELOPMENTS:
    
    1. Product Development:
       - Successfully launched TechNova Analytics Platform 4.0 on August 12, 2023
       - Completed beta testing of mobile application with 200 users
       - R&D team expanded to 45 engineers with the addition of 8 new hires
    
    2. Sales & Marketing:
       - Secured 3 new enterprise clients: Axis Global, MediaCorp, and Peterson Healthcare
       - Expanded partnership with Microsoft for cloud integration services
       - Attended 5 industry conferences, generating 180+ qualified leads
    
    3. Operations:
       - Opened new office in Austin, TX on September 5, 2023
       - Implemented new CRM system across all departments
       - Reduced customer support response time by 35% through AI-assisted ticketing
    
    CHALLENGES & RISKS:
    
    - Increasing competition from Apex Technologies in the enterprise segment
    - Supply chain delays affecting hardware component availability
    - Talent acquisition challenges in the Seattle market
    
    OUTLOOK & NEXT STEPS:
    
    - Q4 revenue projected at $26.8-28.2 million
    - Planning Series C funding round for Q1 2024, targeting $50 million
    - International expansion priorities: Germany, Japan, and Australia
    - Board meeting scheduled for November 10, 2023 at headquarters
    """


@pytest.fixture
def sample_code_requirements():
    """Sample code generation requirements."""
    return {
        "requirements": """
        Create a Python function that processes a CSV file with the following specifications:
        
        1. The function should accept a file path as input
        2. It should read the CSV file, which contains columns for Name, Email, Age, and Subscription Status
        3. The function should filter for active subscribers (Subscription Status = "Active") who are over 30 years old
        4. It should calculate the average age of this filtered group
        5. The function should return a dictionary with:
           - count: number of people in the filtered group
           - average_age: the average age of the filtered group
           - emails: a list of email addresses from the filtered group
        6. The function should handle common errors (file not found, invalid CSV format, etc.)
        """,
        "language": "Python",
        "specifications": """
        - Use the pandas library for CSV processing
        - Include type hints
        - Add docstring and comments
        - Include a simple example of how to call the function
        """,
    }


# --------------------------------
# Task-specific tests
# --------------------------------


@skip_if_no_api_keys
def test_summarization_example(azure_llm_config, summarization_prompt, sample_article):
    """Test AugLLMConfig for content summarization."""
    # Create AugLLM for summarization
    summarizer = AugLLMConfig(
        name="content_summarizer",
        llm_config=azure_llm_config,
        prompt_template=summarization_prompt,
        output_parser=StrOutputParser(),
    )

    # Test with sample article
    summary = summarizer.invoke({"content": sample_article})

    print("\n" + "=" * 20 + " Article Summary " + "=" * 20)
    print(summary)

    # Test with custom content
    custom_content = """
    The Internet of Things (IoT) refers to the network of physical objects embedded with sensors,
    software, and other technologies for the purpose of connecting and exchanging data with other
    devices and systems over the internet. IoT devices include everyday objects like smart home
    devices, wearable health monitors, connected appliances, and industrial equipment with sensors.
    As of 2023, there are an estimated 15 billion IoT devices worldwide, with projections suggesting
    this number could reach 30 billion by 2030. The growth of 5G networks is expected to accelerate
    IoT adoption by providing faster, more reliable connectivity for devices.
    """

    custom_summary = summarizer.invoke({"content": custom_content})

    print("\n" + "=" * 20 + " IoT Summary " + "=" * 20)
    print(custom_summary)

    assert len(summary) > 0
    assert len(custom_summary) > 0


@skip_if_no_api_keys
def test_qa_example(azure_llm_config, qa_prompt, sample_article):
    """Test AugLLMConfig for question answering on specific content."""
    # Create AugLLM for question answering
    qa_system = AugLLMConfig(
        name="content_qa", llm_config=azure_llm_config, prompt_template=qa_prompt
    )

    # Test with different questions
    questions = [
        "What are the key areas of machine learning progress mentioned in the article?",
        "What is multimodal learning according to the article?",
        "What efficiency techniques are mentioned in the article?",
        "Who wrote this article?",  # This information isn't in the content
        "What year is the article focusing on?",
    ]

    print("\n" + "=" * 20 + " Q&A Examples " + "=" * 20)

    for question in questions:
        answer = qa_system.invoke({"content": sample_article, "question": question})

        content = answer.content if hasattr(answer, "content") else answer
        print(f"\nQ: {question}\nA: {content}\n")

        # Basic validation
        assert content is not None
        assert len(content) > 0


@skip_if_no_api_keys
def test_data_extraction_example(
    azure_llm_config, extraction_prompt, sample_business_data
):
    """Test AugLLMConfig for data extraction from specific content."""
    # Create AugLLM for data extraction
    extractor = AugLLMConfig(
        name="data_extractor",
        llm_config=azure_llm_config,
        prompt_template=extraction_prompt,
    )

    # Extract data from the business report
    extracted_data = extractor.invoke({"content": sample_business_data})

    content = (
        extracted_data.content if hasattr(extracted_data, "content") else extracted_data
    )

    print("\n" + "=" * 20 + " Extracted Business Data " + "=" * 20)
    print(content)

    # Define structured output model for extraction
    class BusinessDataExtraction(BaseModel):
        people: list[str] = Field(description="Names of people mentioned")
        organizations: list[str] = Field(description="Organizations mentioned")
        locations: list[str] = Field(description="Locations mentioned")
        dates: list[str] = Field(description="Dates mentioned")
        metrics: list[str] = Field(description="Key metrics or statistics")

    # Create structured extractor
    structured_extractor = AugLLMConfig(
        name="structured_data_extractor",
        llm_config=azure_llm_config,
        prompt_template=extraction_prompt,
        structured_output_model=BusinessDataExtraction,
    )

    # Extract structured data
    structured_data = structured_extractor.invoke({"content": sample_business_data})

    print("\n" + "=" * 20 + " Structured Business Data Extraction " + "=" * 20)
    print(f"People: {structured_data.people}")
    print(f"Organizations: {structured_data.organizations}")
    print(f"Locations: {structured_data.locations}")
    print(f"Dates: {structured_data.dates}")
    print(f"Metrics: {structured_data.metrics}")

    # Basic validation
    assert len(structured_data.people) > 0
    assert len(structured_data.organizations) > 0
    assert len(structured_data.metrics) > 0


@skip_if_no_api_keys
def test_comparison_example(
    azure_llm_config, comparison_prompt, sample_product_comparison
):
    """Test AugLLMConfig for product comparison."""
    # Create AugLLM for comparison
    comparator = AugLLMConfig(
        name="product_comparator",
        llm_config=azure_llm_config,
        prompt_template=comparison_prompt,
    )

    # Compare the products
    comparison = comparator.invoke(sample_product_comparison)

    content = comparison.content if hasattr(comparison, "content") else comparison

    print("\n" + "=" * 20 + " Product Comparison " + "=" * 20)
    print(content)

    # Try another comparison
    custom_comparison = {
        "item1": "Python programming language",
        "item2": "JavaScript programming language",
        "criteria": "Learning curve, performance, versatility, and job market demand.",
    }

    lang_comparison = comparator.invoke(custom_comparison)

    lang_content = (
        lang_comparison.content
        if hasattr(lang_comparison, "content")
        else lang_comparison
    )

    print("\n" + "=" * 20 + " Programming Language Comparison " + "=" * 20)
    print(lang_content)

    # Basic validation
    assert content is not None
    assert lang_content is not None
    assert len(content) > 0
    assert len(lang_content) > 0


@skip_if_no_api_keys
def test_code_generation_example(
    azure_llm_config, code_generation_prompt, sample_code_requirements
):
    """Test AugLLMConfig for code generation."""
    # Create AugLLM for code generation
    code_generator = AugLLMConfig(
        name="code_generator",
        llm_config=azure_llm_config,
        prompt_template=code_generation_prompt,
    )

    # Generate code based on requirements
    generated_code = code_generator.invoke(sample_code_requirements)

    content = (
        generated_code.content if hasattr(generated_code, "content") else generated_code
    )

    print("\n" + "=" * 20 + " Generated Python Code " + "=" * 20)
    print(content)

    # Try a simpler code generation task
    simple_task = {
        "requirements": "Create a function that checks if a string is a palindrome.",
        "language": "Python",
        "specifications": "Keep it simple and efficient.",
    }

    simple_code = code_generator.invoke(simple_task)

    simple_content = (
        simple_code.content if hasattr(simple_code, "content") else simple_code
    )

    print("\n" + "=" * 20 + " Simple Function Generation " + "=" * 20)
    print(simple_content)

    # Basic validation
    assert "def" in content
    assert "def" in simple_content
    assert "pandas" in content
    assert "palindrome" in simple_content.lower()


@skip_if_no_api_keys
def test_format_conversion_example(azure_llm_config, format_conversion_prompt):
    """Test AugLLMConfig for format conversion."""
    # Create AugLLM for format conversion
    converter = AugLLMConfig(
        name="format_converter",
        llm_config=azure_llm_config,
        prompt_template=format_conversion_prompt,
    )

    # Convert markdown to HTML
    markdown_content = """
    # Project Status Report
    
    ## Completed Tasks
    
    - Implemented user authentication system
    - Designed database schema
    - Created initial API endpoints
    
    ## Pending Tasks
    
    1. Frontend UI development
    2. Integration testing
    3. Deployment pipeline setup
    
    **Deadline**: November 30, 2023
    
    Contact: [project-team@example.com](mailto:project-team@example.com)
    """

    html_conversion = converter.invoke(
        {
            "content": markdown_content,
            "source_format": "Markdown",
            "target_format": "HTML",
        }
    )

    html_content = (
        html_conversion.content
        if hasattr(html_conversion, "content")
        else html_conversion
    )

    print("\n" + "=" * 20 + " Markdown to HTML Conversion " + "=" * 20)
    print(html_content)

    # Convert JSON to YAML
    json_content = """
    {
      "server": {
        "host": "example.com",
        "port": 8080,
        "ssl": true
      },
      "database": {
        "type": "postgres",
        "credentials": {
          "username": "admin",
          "password": "secure_password"
        },
        "options": {
          "max_connections": 100,
          "timeout": 30
        }
      },
      "features": ["authentication", "logging", "api", "websockets"]
    }
    """

    yaml_conversion = converter.invoke(
        {"content": json_content, "source_format": "JSON", "target_format": "YAML"}
    )

    yaml_content = (
        yaml_conversion.content
        if hasattr(yaml_conversion, "content")
        else yaml_conversion
    )

    print("\n" + "=" * 20 + " JSON to YAML Conversion " + "=" * 20)
    print(yaml_content)

    # Basic validation
    assert "<h1>" in html_content
    assert "<ul>" in html_content
    assert "server:" in yaml_content
    assert "host: example.com" in yaml_content


@skip_if_no_api_keys
def test_translation_example(azure_llm_config, translation_prompt):
    """Test AugLLMConfig for language translation."""
    # Create AugLLM for translation
    translator = AugLLMConfig(
        name="translator",
        llm_config=azure_llm_config,
        prompt_template=translation_prompt,
    )

    # Translate English to Spanish
    spanish_translation = translator.invoke(
        {
            "text": "Machine learning is transforming how we interact with technology every day.",
            "source_language": "English",
            "target_language": "Spanish",
        }
    )

    spanish_content = (
        spanish_translation.content
        if hasattr(spanish_translation, "content")
        else spanish_translation
    )

    print("\n" + "=" * 20 + " English to Spanish Translation " + "=" * 20)
    print(spanish_content)

    # Translate English to French
    french_translation = translator.invoke(
        {
            "text": "The artificial intelligence revolution has only just begun.",
            "source_language": "English",
            "target_language": "French",
        }
    )

    french_content = (
        french_translation.content
        if hasattr(french_translation, "content")
        else french_translation
    )

    print("\n" + "=" * 20 + " English to French Translation " + "=" * 20)
    print(french_content)

    # Translate with tone guidance
    formal_translation = translator.invoke(
        {
            "text": "Hey there! Can you help me figure out how to use this app?",
            "source_language": "English",
            "target_language": "Japanese",
            "messages": [
                HumanMessage(
                    content="Please maintain a formal, respectful tone in the translation."
                )
            ],
        }
    )

    formal_content = (
        formal_translation.content
        if hasattr(formal_translation, "content")
        else formal_translation
    )

    print("\n" + "=" * 20 + " English to Formal Japanese Translation " + "=" * 20)
    print(formal_content)

    # Basic validation
    assert spanish_content is not None
    assert french_content is not None
    assert formal_content is not None
    assert len(spanish_content) > 0
    assert len(french_content) > 0
    assert len(formal_content) > 0


@skip_if_no_api_keys
def test_analysis_example(azure_llm_config, analysis_prompt, sample_article):
    """Test AugLLMConfig for content analysis."""
    # Create AugLLM for analysis
    analyzer = AugLLMConfig(
        name="content_analyzer",
        llm_config=azure_llm_config,
        prompt_template=analysis_prompt,
    )

    # Analyze the article
    analysis = analyzer.invoke({"content": sample_article})

    content = analysis.content if hasattr(analysis, "content") else analysis

    print("\n" + "=" * 20 + " Article Analysis " + "=" * 20)
    print(content)

    # Create custom analysis prompt for SWOT analysis
    swot_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""
        You are a business analyst specialized in SWOT analysis. Analyze the provided 
        business information and create a complete SWOT analysis with the following sections:
        
        1. Strengths: Internal positive factors
        2. Weaknesses: Internal negative factors
        3. Opportunities: External positive factors
        4. Threats: External negative factors
        
        For each section, provide 3-5 bullet points with brief explanations.
        """
            ),
            HumanMessagePromptTemplate.from_template(
                "Perform a SWOT analysis for the following business:\n\n{business_info}"
            ),
        ]
    )

    # Create SWOT analyzer
    swot_analyzer = AugLLMConfig(
        name="swot_analyzer", llm_config=azure_llm_config, prompt_template=swot_prompt
    )

    # Sample business info
    business_info = """
    GreenTech Solutions is a 5-year-old renewable energy startup focusing on residential solar 
    panel installation and maintenance. The company currently operates in three states with 
    45 employees and annual revenue of $3.2 million. GreenTech has developed proprietary 
    software for solar efficiency analysis that is 15% more accurate than industry standards.
    
    The company has strong customer satisfaction scores (4.8/5) but has struggled with 
    installation delays due to supply chain issues. Competitors include both large national 
    solar providers and local installation companies. The government recently announced 
    new tax incentives for renewable energy adoption.
    
    The company's founder has ambitions to expand to 10 states within the next three years 
    but is concerned about rising equipment costs and potential changes in regulations.
    """

    # Perform SWOT analysis
    swot_analysis = swot_analyzer.invoke({"business_info": business_info})

    swot_content = (
        swot_analysis.content if hasattr(swot_analysis, "content") else swot_analysis
    )

    print("\n" + "=" * 20 + " SWOT Analysis " + "=" * 20)
    print(swot_content)

    # Basic validation
    assert "Strengths" in swot_content
    assert "Weaknesses" in swot_content
    assert "Opportunities" in swot_content
    assert "Threats" in swot_content
