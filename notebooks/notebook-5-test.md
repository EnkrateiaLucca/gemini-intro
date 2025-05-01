# Building a PDF Chat System with Gemini 2.0

In this notebook, we'll create a simple but powerful PDF chat system using Google's Gemini 2.0 models. This system will allow us to upload PDF documents and have interactive conversations about their contents.

## Why Gemini for PDF Processing?

Gemini models have several advantages for PDF processing:

- Native vision capabilities to understand both text and visuals in documents
- Support for long documents (up to 3,600 pages)
- Ability to analyze diagrams, charts, and tables
- Capability to extract structured information
- Support for document summarization and transcription

## Setting Up the Environment

Let's start by installing the necessary packages:

```python
!pip install -q google-generativeai httpx
```

Now let's import the required libraries:

```python
from google import genai
from google.genai import types
import httpx
import io
import pathlib
import os
```

## Initialize the Gemini API Client

To use the Gemini API, you'll need an API key. If you don't have one yet, you can get it from [Google AI Studio](https://aistudio.google.com/).

```python
# Set your API key
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
# Or load from environment variable
# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Initialize the client
client = genai.Client(api_key=GOOGLE_API_KEY)
```

## PDF Upload Methods

There are two main ways to handle PDFs with Gemini:

1. **Direct Upload** (for files < 20MB)
2. **File API** (for larger files or when you need to reuse the PDF)

Let's implement both methods:

### Method 1: Direct Upload (Small PDFs)

```python
def process_small_pdf(pdf_path, prompt):
    """
    Process a small PDF file (< 20MB) using direct upload.
    
    Args:
        pdf_path: Path to the PDF file or URL
        prompt: Question or instruction for the model
        
    Returns:
        Model response
    """
    # Check if the path is a URL
    if pdf_path.startswith(('http://', 'https://')):
        # Download the PDF from URL
        pdf_data = httpx.get(pdf_path).content
    else:
        # Read from local file
        pdf_data = pathlib.Path(pdf_path).read_bytes()
    
    # Generate content with the PDF and prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Part.from_bytes(
                data=pdf_data,
                mime_type='application/pdf',
            ),
            prompt
        ]
    )
    
    return response
```

### Method 2: File API (Large PDFs)

```python
def process_large_pdf(pdf_path, prompt):
    """
    Process a large PDF file using the File API.
    
    Args:
        pdf_path: Path to the PDF file or URL
        prompt: Question or instruction for the model
        
    Returns:
        Model response
    """
    # Check if the path is a URL
    if pdf_path.startswith(('http://', 'https://')):
        # Download the PDF from URL
        pdf_data = io.BytesIO(httpx.get(pdf_path).content)
        
        # Upload the PDF using the File API
        uploaded_file = client.files.upload(
            file=pdf_data,
            config=dict(mime_type='application/pdf')
        )
    else:
        # Upload the local PDF using the File API
        uploaded_file = client.files.upload(
            file=pdf_path
        )
    
    # Generate content with the uploaded file and prompt
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[uploaded_file, prompt]
    )
    
    return response
```

## Building a Simple PDF Chat Interface

Now let's create a simple chat interface for interacting with PDFs:

```python
class PDFChat:
    def __init__(self, pdf_path):
        """
        Initialize the PDF Chat system.
        
        Args:
            pdf_path: Path to the PDF file or URL
        """
        self.pdf_path = pdf_path
        
        # Determine if it's a large file or URL
        if pdf_path.startswith(('http://', 'https://')):
            # For URLs, we'll check the file size
            try:
                head_response = httpx.head(pdf_path)
                content_length = int(head_response.headers.get('content-length', 0))
                self.is_large = content_length > 20 * 1024 * 1024  # 20MB
            except:
                # If we can't determine size, assume it's large
                self.is_large = True
        else:
            # For local files, check actual size
            file_size = pathlib.Path(pdf_path).stat().st_size
            self.is_large = file_size > 20 * 1024 * 1024  # 20MB
            
        # Upload the file if it's large
        if self.is_large:
            if pdf_path.startswith(('http://', 'https://')):
                pdf_data = io.BytesIO(httpx.get(pdf_path).content)
                self.uploaded_file = client.files.upload(
                    file=pdf_data,
                    config=dict(mime_type='application/pdf')
                )
            else:
                self.uploaded_file = client.files.upload(
                    file=pdf_path
                )
            print(f"Large PDF uploaded successfully with ID: {self.uploaded_file.name}")
    
    def chat(self, prompt):
        """
        Chat with the PDF.
        
        Args:
            prompt: Question or instruction for the model
            
        Returns:
            Model response text
        """
        if self.is_large:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[self.uploaded_file, prompt]
            )
        else:
            if self.pdf_path.startswith(('http://', 'https://')):
                pdf_data = httpx.get(self.pdf_path).content
            else:
                pdf_data = pathlib.Path(self.pdf_path).read_bytes()
                
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Part.from_bytes(
                        data=pdf_data,
                        mime_type='application/pdf',
                    ),
                    prompt
                ]
            )
        
        return response.text
```

## Example Usage

Let's see our PDF Chat system in action with some example use cases:

```python
# Example 1: Chat with a small PDF from a URL
pdf_url = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"
pdf_chat = PDFChat(pdf_url)

# Get a summary of the document
summary = pdf_chat.chat("Summarize this document in 5 bullet points")
print("Document Summary:")
print(summary)
print("\n" + "-"*50 + "\n")

# Ask specific questions about the content
answer = pdf_chat.chat("What are the main findings or conclusions of this paper?")
print("Main Findings:")
print(answer)
```

```python
# Example 2: Chat with a large NASA document
nasa_pdf = "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"
nasa_chat = PDFChat(nasa_pdf)

# Ask about the mission objectives
mission = nasa_chat.chat("What were the main mission objectives described in this document?")
print("Mission Objectives:")
print(mission)
```

## Advanced Use Cases

### 1. Extracting Structured Information

```python
# Extract information in a structured format
structured_info = pdf_chat.chat("Extract the key figures and statistics from this document and format them as a JSON object")
print("Structured Information:")
print(structured_info)
```

### 2. Analyzing Charts and Diagrams

```python
# Analyze charts or diagrams in the document
chart_analysis = pdf_chat.chat("Describe any charts, graphs, or diagrams in the document and explain what they show")
print("Chart Analysis:")
print(chart_analysis)
```

### 3. Comparing Multiple PDFs

```python
# Function to compare two PDFs
def compare_pdfs(pdf_url_1, pdf_url_2, comparison_prompt):
    # Upload both PDFs using File API
    pdf_data_1 = io.BytesIO(httpx.get(pdf_url_1).content)
    pdf_data_2 = io.BytesIO(httpx.get(pdf_url_2).content)
    
    uploaded_pdf_1 = client.files.upload(
        file=pdf_data_1,
        config=dict(mime_type='application/pdf')
    )
    
    uploaded_pdf_2 = client.files.upload(
        file=pdf_data_2,
        config=dict(mime_type='application/pdf')
    )
    
    # Generate comparison
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[uploaded_pdf_1, uploaded_pdf_2, comparison_prompt]
    )
    
    return response.text

# Example usage
pdf_url_1 = "https://arxiv.org/pdf/2312.11805"  # Gemini paper
pdf_url_2 = "https://arxiv.org/pdf/2403.05530"  # Another AI paper

comparison = compare_pdfs(
    pdf_url_1, 
    pdf_url_2, 
    "What are the key differences between these two papers? Organize your answer in a table."
)
print("PDF Comparison:")
print(comparison)
```

## Best Practices for Working with PDFs

1. **Document Preparation**:
   - Ensure PDFs are correctly rotated
   - Use clear, non-blurry documents for best results
   - For scanned documents, ensure good image quality

2. **Prompt Engineering**:
   - Be specific about the section or page you're interested in
   - For long documents, use "Find in the document..." style prompts
   - Request structured outputs (tables, JSON) for easier parsing

3. **Performance Optimization**:
   - Use File API for PDFs larger than 20MB
   - Reuse uploaded files for multiple queries about the same document
   - Consider extracting only relevant pages for faster processing

## Limitations

- While Gemini supports up to 3,600 pages, very large documents may be processed less accurately
- Complex layouts, low-quality scans, or handwritten text may reduce accuracy
- Performance may vary with highly technical or specialized content

## Conclusion

In this notebook, we've built a simple yet powerful PDF chat system using Gemini 2.0. This system allows us to upload PDFs of various sizes and have interactive conversations about their contents. We've also explored several advanced use cases and best practices for working with PDF documents.

With Gemini's multimodal capabilities, you can understand not just the text but also the visual elements in your documents, making it an excellent tool for document understanding and analysis.