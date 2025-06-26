# PDF Document Loaders in Haive Framework

This document outlines the implementation of PDF document loaders in the Haive framework.

## PDF Loader Options

LangChain provides several PDF loader implementations, each with different characteristics:

| Loader                  | Speed  | Quality   | Features                  | Dependencies                          |
| ----------------------- | ------ | --------- | ------------------------- | ------------------------------------- |
| PyPDFLoader             | Fast   | Medium    | Basic text extraction     | pypdf                                 |
| PDFMinerLoader          | Medium | High      | Detailed text with layout | pdfminer.six                          |
| PDFPlumberLoader        | Slow   | High      | Table extraction          | pdfplumber                            |
| UnstructuredPDFLoader   | Medium | High      | OCR support               | unstructured, pdf2image, pdfminer.six |
| PyMuPDFLoader           | Fast   | Medium    | Fast extraction           | pymupdf                               |
| MathpixPDFLoader        | Medium | Very High | OCR with math recognition | mathpix-pdf-to-html                   |
| PDFMinerPDFasHTMLLoader | Medium | Medium    | Converts PDF to HTML      | pdfminer.six                          |
| OnlinePDFLoader         | Medium | Medium    | Downloads and loads PDF   | pypdf, requests                       |
| PyPDFium2Loader         | Fast   | Medium    | Uses Google's PDFium      | pypdfium2                             |
| AmazonTextractPDFLoader | Slow   | High      | Uses AWS Textract         | boto3                                 |

## Implementation Strategy

Our approach is to create a unified `PDFSource` class that provides access to all these loaders through different loading strategies:

```python
@auto_source
class PDFSource(LocalSource):
    """PDF document source."""
    file_path: FilePath

    class Config:
        file_extensions = ['.pdf']
        loader_strategies = {
            'fast': {
                'class': 'PyPDFLoader',
                'speed': 'fast',
                'quality': 'medium',
                'best_for': ['text_heavy']
            },
            'ocr': {
                'class': 'UnstructuredPDFLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['scanned', 'images']
            },
            'tables': {
                'class': 'PDFPlumberLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['tables', 'forms']
            },
            'math': {
                'class': 'MathpixPDFLoader',
                'speed': 'medium',
                'quality': 'very_high',
                'best_for': ['math', 'equations'],
                'requires_auth': True,
                'required_credentials': ['mathpix_api_key']
            },
            'aws': {
                'class': 'AmazonTextractPDFLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['complex_layouts', 'forms'],
                'requires_auth': True,
                'required_credentials': ['aws_credentials']
            }
        }
```

## Loader Selection Logic

We'll implement logic to select the most appropriate loader based on:

1. **File Characteristics**:
   - File size
   - Text vs. image-based PDFs
   - Presence of tables
   - Presence of math equations

2. **User Preferences**:
   - Speed vs. quality preference
   - Specific needs (e.g., table extraction, OCR)

3. **Available Dependencies**:
   - Check for installed libraries
   - Check for required credentials

## Specific Loader Implementations

### PyPDFLoader

```python
def create_pypdf_loader(self):
    """Create a PyPDFLoader instance."""
    # Import here to avoid dependency issues
    from langchain_community.document_loaders import PyPDFLoader

    # Create and return the loader
    return PyPDFLoader(str(self.file_path))
```

### UnstructuredPDFLoader

```python
def create_unstructured_loader(self, **kwargs):
    """Create an UnstructuredPDFLoader instance with OCR if needed."""
    # Import here to avoid dependency issues
    from langchain_community.document_loaders import UnstructuredPDFLoader

    # Configure OCR mode
    ocr_config = {
        "ocr_enabled": True,
        "ocr_languages": "eng",  # Default to English
        "mode": "elements"  # Extract elements rather than just text
    }

    # Update with any user-provided settings
    ocr_config.update(kwargs)

    # Create and return the loader
    return UnstructuredPDFLoader(str(self.file_path), **ocr_config)
```

### PDFPlumberLoader

```python
def create_pdfplumber_loader(self):
    """Create a PDFPlumberLoader for table extraction."""
    # Import here to avoid dependency issues
    from langchain_community.document_loaders import PDFPlumberLoader

    # Create and return the loader
    return PDFPlumberLoader(str(self.file_path))
```

## Advanced Features

### PDF Preprocessing

We'll implement preprocessing functions to improve extraction quality:

```python
def preprocess_pdf(self, rotation=None, password=None):
    """Preprocess the PDF for better extraction."""
    # Import required libraries
    import tempfile
    from pypdf import PdfReader, PdfWriter

    # Create a temporary file for the processed PDF
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_path = temp_file.name

    # Read the original PDF
    reader = PdfReader(str(self.file_path), password=password)
    writer = PdfWriter()

    # Process each page
    for page in reader.pages:
        # Apply rotation if specified
        if rotation is not None:
            page.rotate(rotation)

        # Add to the new PDF
        writer.add_page(page)

    # Write the processed PDF
    with open(temp_path, "wb") as output_file:
        writer.write(output_file)

    # Update the file path to the processed file
    self.processed_path = temp_path

    return temp_path
```

### PDF Analysis

We'll implement analysis functions to determine the best loader:

```python
def analyze_pdf(self):
    """Analyze the PDF to determine its characteristics."""
    # Import required libraries
    from pypdf import PdfReader

    # Initialize analysis results
    analysis = {
        "page_count": 0,
        "has_text": False,
        "text_ratio": 0.0,
        "has_images": False,
        "image_count": 0,
        "has_tables": False,
        "has_forms": False,
        "is_scanned": False,
        "estimated_text_quality": 0.0
    }

    # Read the PDF
    reader = PdfReader(str(self.file_path))
    analysis["page_count"] = len(reader.pages)

    # Analyze each page
    text_chars = 0
    for i, page in enumerate(reader.pages):
        # Extract text
        text = page.extract_text() or ""
        text_chars += len(text)

        # Check for images
        if "/XObject" in page.resources and page.resources["/XObject"]:
            analysis["has_images"] = True
            analysis["image_count"] += len(page.resources["/XObject"])

        # Check for forms
        if "/AcroForm" in reader.trailer["/Root"]:
            analysis["has_forms"] = True

        # Simple detection of tables (based on patterns)
        if self._detect_tables_in_text(text):
            analysis["has_tables"] = True

    # Calculate text ratio and determine if likely scanned
    if analysis["page_count"] > 0:
        avg_chars_per_page = text_chars / analysis["page_count"]
        analysis["text_ratio"] = min(1.0, avg_chars_per_page / 2000)  # Normalize against 2000 chars/page
        analysis["has_text"] = text_chars > 0
        analysis["is_scanned"] = analysis["has_images"] and analysis["text_ratio"] < 0.1

    # Estimate text quality based on characteristics
    if analysis["is_scanned"]:
        analysis["estimated_text_quality"] = 0.2  # Low quality for scanned docs
    elif analysis["has_text"]:
        analysis["estimated_text_quality"] = min(1.0, analysis["text_ratio"])

    return analysis
```

## Auto-Selection Logic

We'll implement logic to select the most appropriate loader based on the PDF analysis:

```python
def select_best_loader(self, criteria=None):
    """Select the best loader based on PDF analysis and criteria."""
    criteria = criteria or {}
    prefer_speed = criteria.get("prefer_speed", False)
    prefer_quality = criteria.get("prefer_quality", False)

    # Analyze the PDF
    analysis = self.analyze_pdf()

    # Select loader based on analysis
    if analysis["is_scanned"]:
        # For scanned documents, use OCR
        if self.has_credential('mathpix_api_key'):
            return 'math'  # MathpixPDFLoader for best OCR
        else:
            return 'ocr'   # UnstructuredPDFLoader with OCR

    elif analysis["has_tables"]:
        # For documents with tables
        return 'tables'    # PDFPlumberLoader for tables

    elif prefer_speed:
        # For speed-critical applications
        return 'fast'      # PyPDFLoader for speed

    elif prefer_quality:
        # For quality-critical applications
        if analysis["estimated_text_quality"] < 0.5:
            return 'ocr'   # Use OCR for better quality
        else:
            return 'tables' # PDFPlumberLoader for quality

    # Default to fast loader
    return 'fast'
```

## Full Implementation

The complete `PDFSource` implementation will include:

1. File analysis capabilities
2. Preprocessing functions
3. Multiple loader strategies
4. Auto-selection logic
5. Credential management for API-based loaders

This provides a robust and flexible approach to PDF loading that can adapt to different document characteristics and user needs.

## Usage Examples

### Basic Usage

```python
from haive.document_loaders import PDFSource

# Create a PDF source
pdf_source = PDFSource(file_path="/path/to/document.pdf")

# Load the document with auto-selected strategy
documents = pdf_source.load_documents()
```

### Specifying a Strategy

```python
# Use OCR-based loading
documents = pdf_source.load_documents(strategy="ocr")

# Extract tables
documents = pdf_source.load_documents(strategy="tables")
```

### With Preprocessing

```python
# Preprocess to fix rotation and then load
pdf_source.preprocess_pdf(rotation=90)
documents = pdf_source.load_documents()
```

### With Credentials

```python
from haive.document_loaders import CredentialManager

# Create a credential manager
credential_manager = CredentialManager()

# Add credentials
credential_manager.store_credential(
    "mathpix_api_key",
    {"type": "api_key", "value": "your-api-key"}
)

# Authenticate the source
pdf_source.authenticate(credential_manager)

# Load with Mathpix
documents = pdf_source.load_documents(strategy="math")
```

## Conclusion

This implementation provides a comprehensive approach to PDF loading that leverages all available LangChain loaders while adding intelligent selection, preprocessing, and analysis capabilities.

## Status

- ⬜ Core `PDFSource` implementation
- ⬜ Loader strategy definitions
- ⬜ PDF analysis functions
- ⬜ Preprocessing capabilities
- ⬜ Auto-selection logic
- ⬜ Integration with credential management
- ⬜ Testing and validation
