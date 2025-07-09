"""Utility functions for taxonomy generation and document processing.

This module provides utility functions for parsing, formatting, and managing
taxonomy-related data structures. It includes functions for handling XML-formatted
outputs, document summaries, and taxonomy clusters.

Note:
    All XML parsing functions assume well-formed XML input with specific expected tags.
    Malformed XML may raise parsing errors.

Example:
    Basic usage for taxonomy parsing::

        xml_output = '''
            <id>1</id>
            <name>Category A</name>
            <description>Description text</description>
        '''
        taxonomy = parse_taxonomy(xml_output)
"""

import logging
import re

from langchain_core.documents import Document

from haive.agents.document_modifiers.tnt.state import TaxonomyGenerationState

# from haive.core.utils.doc_utils import format_docs,format_taxonomy
logger = logging.getLogger(__name__)


# Check if we should just use markdown, how to handle logging./
# logger  - fix
def parse_summary(xml_string: str) -> dict:
    """Parse summary and explanation from XML-formatted string.

    Extracts the content within <summary> and <explanation> tags from the input XML string.
    If tags are not found, returns empty strings for the missing elements.

    Args:
        xml_string: XML-formatted string containing <summary> and <explanation> tags.
            Example::
                <summary>Main points...</summary>
                <explanation>Detailed analysis...</explanation>

    Returns:
        dict: Dictionary containing:
            - summary (str): Content within <summary> tags
            - explanation (str): Content within <explanation> tags

    Example:
        >>> xml = "<summary>Key points</summary><explanation>Details</explanation>"
        >>> result = parse_summary(xml)
        >>> print(result)
        {'summary': 'Key points', 'explanation': 'Details'}
    """
    summary_pattern = r"<summary>(.*?)</summary>"
    explanation_pattern = r"<explanation>(.*?)</explanation>"

    summary_match = re.search(summary_pattern, xml_string, re.DOTALL)
    explanation_match = re.search(explanation_pattern, xml_string, re.DOTALL)

    summary = summary_match.group(1).strip() if summary_match else ""
    explanation = explanation_match.group(1).strip() if explanation_match else ""

    return {"summary": summary, "explanation": explanation}


def parse_taxonomy(output_text: str) -> dict:
    """Parse taxonomy information from LLM-generated output.

    Extracts cluster information including IDs, names, and descriptions from
    XML-formatted output text.

    Args:
        output_text: XML-formatted string containing taxonomy clusters.
            Expected format::
                <id>1</id>
                <name>Category Name</name>
                <description>Category Description</description>

    Returns:
        dict: Dictionary containing:
            - clusters (list): List of dictionaries, each with:
                - id (str): Cluster identifier
                - name (str): Cluster name
                - description (str): Cluster description

    Example:
        >>> text = "<id>1</id><name>Tech</name><description>Technology</description>"
        >>> taxonomy = parse_taxonomy(text)
        >>> print(taxonomy)
        {'clusters': [{'id': '1', 'name': 'Tech', 'description': 'Technology'}]}
    """
    cluster_matches = re.findall(
        r"\s*<id>(.*?)</id>\s*<name>(.*?)</name>\s*<description>(.*?)</description>\s*",
        output_text,
        re.DOTALL,
    )
    clusters = [
        {"id": id.strip(), "name": name.strip(), "description": description.strip()}
        for id, name, description in cluster_matches
    ]
    # We don't parse the explanation since it isn't used downstream
    return {"clusters": clusters}


def parse_labels(output_text: str) -> dict:
    """Parse category labels from prediction output.

    Extracts category information from XML-formatted prediction text.
    Handles multiple categories but returns only the first one.

    Args:
        output_text: XML-formatted string containing category predictions.
            Expected format::
                <category>Label Name</category>

    Returns:
        dict: Dictionary containing:
            - category (str): The first category label found

    Note:
        If multiple categories are found, a warning is logged and only
        the first category is returned.

    Example:
        >>> text = "<category>Technology</category>"
        >>> result = parse_labels(text)
        >>> print(result)
        {'category': 'Technology'}
    """
    category_matches = re.findall(
        r"\s*<category>(.*?)</category>.*",
        output_text,
        re.DOTALL,
    )
    categories = [{"category": category.strip()} for category in category_matches]
    if len(categories) > 1:
        logger.warning(f"Multiple selected categories: {categories}")
    label = categories[0]
    stripped = re.sub(r"^\d+\.\s*", "", label["category"]).strip()
    return {"category": stripped}


def get_content(state: TaxonomyGenerationState) -> list[dict]:
    """Extract document content from taxonomy generation state.

    Args:
        state: Current state of the taxonomy generation process.
            Must contain a 'documents' key with list of document dictionaries.

    Returns:
        list: List of dictionaries, each containing:
            - content (str): The content of a document

    Example:
        >>> state = {"documents": [{"content": "doc1"}, {"content": "doc2"}]}
        >>> contents = get_content(state)
        >>> print(contents)
        [{'content': 'doc1'}, {'content': 'doc2'}]
    """
    docs = state["documents"]
    return [{"content": doc["content"]} for doc in docs]


def reduce_summaries(combined: dict) -> TaxonomyGenerationState:
    """Merge summarized content with original documents.

    Takes a dictionary containing both original documents and their summaries,
    and combines them into a single state object.

    Args:
        combined: Dictionary containing:
            - documents (list): Original document list
            - summaries (list): Corresponding summaries

    Returns:
        TaxonomyGenerationState: Updated state containing:
            - documents (list): List of documents with added summaries

    Example:
        >>> combined = {
        ...     "documents": [{"id": 1, "content": "text"}],
        ...     "summaries": [{"summary": "sum", "explanation": "exp"}]
        ... }
        >>> state = reduce_summaries(combined)
    """
    summaries = combined["summaries"]
    documents = combined["documents"]
    return {
        "documents": [
            {
                "id": doc["id"],
                "content": doc["content"],
                "summary": summ_info["summary"],
                "explanation": summ_info["explanation"],
            }
            for doc, summ_info in zip(documents, summaries, strict=False)
        ]
    }


# IMPLEMTN WITH MARKDOWN
def format_taxonomy_md(clusters: list[dict]) -> str:
    """Format taxonomy clusters as a Markdown table.

    Args:
        clusters: List of cluster dictionaries, each containing:
            - id (str): Cluster identifier
            - name (str): Cluster name
            - description (str): Cluster description

    Returns:
        str: Markdown-formatted table string

    Example:
        >>> clusters = [{"id": "1", "name": "Tech", "description": "Technology"}]
        >>> md_table = format_taxonomy_md(clusters)
    """
    md = "## Final Taxonomy\n\n"
    md += "| ID | Name | Description |\n"
    md += "|----|------|-------------|\n"

    for label in clusters:
        id = label["id"]
        name = label["name"].replace("|", "\\|")
        description = label["description"].replace("|", "\\|")
        md += f"| {id} | {name} | {description} |\n"

    return md


def format_docs(docs: list[Document]) -> str:
    """Format documents as XML table for taxonomy generation.

    Args:
        docs: List of Document objects, each must have:
            - id: Document identifier
            - summary: Document summary text

    Returns:
        str: XML-formatted string containing conversation summaries

    Example:
        >>> docs = [Document(id="1", summary="text")]
        >>> xml = format_docs(docs)
        >>> print(xml)
        <conversations>
        <conv_summ id=1>text</conv_summ>
        </conversations>
    """
    xml_table = "<conversations>\n"
    for doc in docs:
        xml_table += f"<conv_summ id={doc.id}>{doc.summary}</conv_summ>\n"
    xml_table += "</conversations>"
    return xml_table


def format_taxonomy(clusters: list[dict]) -> str:
    """Convert taxonomy clusters to XML format.

    Args:
        clusters: List of cluster dictionaries, each containing:
            - id (str): Cluster identifier
            - name (str): Cluster name
            - description (str): Cluster description

    Returns:
        str: XML-formatted taxonomy string

    Example:
        >>> clusters = [{"id": "1", "name": "Tech", "description": "Technology"}]
        >>> xml = format_taxonomy(clusters)
        >>> print(xml)
        <cluster_table>
          <cluster>
            <id>1</id>
            <name>Tech</name>
            <description>Technology</description>
          </cluster>
        </cluster_table>
    """
    xml = "<cluster_table>\n"
    for label in clusters:
        xml += "  <cluster>\n"
        xml += f'    <id>{label["id"]}</id>\n'
        xml += f'    <name>{label["name"]}</name>\n'
        xml += f'    <description>{label["description"]}</description>\n'
        xml += "  </cluster>\n"
    xml += "</cluster_table>"
    return xml
