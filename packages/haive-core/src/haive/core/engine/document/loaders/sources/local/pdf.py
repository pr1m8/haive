"""PDF document source implementation.

Shows how to implement a concrete source with multiple loader strategies.
"""

from typing import Any, Dict, Optional

from haive.core.engine.document.loaders.sources.base import LocalSource
from haive.core.engine.document.loaders.sources.registry import register_source


@register_source(
    name="pdf",
    file_extensions=[".pdf"],
    mime_types=["application/pdf"],
    loaders={
        "fast": {
            "class": "PyPDFLoader",
            "speed": "fast",
            "quality": "medium",
            "best_for": ["text_heavy", "simple_layouts"],
        },
        "quality": {
            "class": "UnstructuredPDFLoader",
            "speed": "medium",
            "quality": "high",
            "requires_packages": ["unstructured", "pdf2image", "pdfplumber"],
            "best_for": ["complex_layouts", "mixed_content"],
        },
        "ocr": {
            "class": "PDFPlumberLoader",
            "speed": "slow",
            "quality": "high",
            "best_for": ["scanned_documents", "tables", "forms"],
        },
        "math": {
            "class": "MathpixPDFLoader",
            "speed": "slow",
            "quality": "high",
            "requires_packages": ["mathpix"],
            "requires_auth": True,
            "best_for": ["equations", "scientific_papers"],
        },
        "pymupdf": {
            "class": "PyMuPDFLoader",
            "speed": "fast",
            "quality": "medium",
            "requires_packages": ["pymupdf"],
            "best_for": ["fast_extraction", "embedded_images"],
        },
    },
    default_loader="fast",
    priority=10,  # High priority for PDF files
)
class PDFSource(LocalSource):
    """Source for PDF documents with multiple extraction strategies.

    This source supports various PDF loaders optimized for different use cases:
    - fast: Quick text extraction with PyPDF
    - quality: High-quality extraction with Unstructured
    - ocr: OCR support with PDFPlumber
    - math: Mathematical equation extraction with Mathpix
    - pymupdf: Fast extraction with PyMuPDF
    """

    # PDF-specific options
    extract_images: bool = False
    ocr_enabled: bool = False
    split_pages: bool = True
    password: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        """Get kwargs for PDF loaders."""
        # Start with base kwargs
        kwargs = super().get_loader_kwargs()

        # Add PDF-specific options based on loader
        if self.preferred_loader == "quality" or self.preferred_loader == "ocr":
            # Unstructured/PDFPlumber options
            kwargs.update(
                {
                    "mode": "elements" if self.extract_images else "single",
                    "strategy": "ocr_only" if self.ocr_enabled else "fast",
                }
            )

        if self.password:
            kwargs["password"] = self.password

        if self.preferred_loader == "fast":
            # PyPDF options
            kwargs["extract_images"] = self.extract_images

        return kwargs

    def validate_source(self) -> bool:
        """Validate PDF file."""
        if not super().validate_source():
            return False

        # Could add PDF-specific validation here
        # e.g., check PDF header, file size limits, etc.
        return True


# Additional specialized PDF sources could be registered


@register_source(
    name="academic_pdf",
    file_extensions=[".pdf"],
    url_patterns=["arxiv.org", "doi.org", "ncbi.nlm.nih.gov"],
    loaders={
        "grobid": {
            "class": "GrobidLoader",
            "module": "langchain_community.document_loaders",
            "speed": "medium",
            "quality": "high",
            "requires_packages": ["grobid-client"],
            "best_for": ["academic_papers", "citations", "structured_extraction"],
        },
        "arxiv": {
            "class": "ArxivLoader",
            "speed": "medium",
            "quality": "high",
            "best_for": ["arxiv_papers"],
        },
    },
    default_loader="grobid",
    priority=15,  # Higher priority for academic PDFs
)
class AcademicPDFSource(LocalSource):
    """Specialized source for academic PDF papers.

    Optimized for extracting structured information from academic papers
    including citations, abstract, methodology, etc.
    """

    extract_citations: bool = True
    extract_figures: bool = True
    extract_tables: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        """Get kwargs for academic PDF loaders."""
        kwargs = super().get_loader_kwargs()

        if self.preferred_loader == "grobid":
            kwargs.update(
                {
                    "include_figures": self.extract_figures,
                    "include_tables": self.extract_tables,
                    "consolidate_citations": self.extract_citations,
                }
            )

        return kwargs
