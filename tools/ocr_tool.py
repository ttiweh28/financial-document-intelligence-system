from agents.tool import FunctionTool

import easyocr
import os

_reader = None

def _get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'])
    return _reader

def ocr_extract_text(file_path: str) -> str:
    """Extract text from a financial document using OCR."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    supported_formats = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf')
    if not file_path.lower().endswith(supported_formats):
        raise ValueError(f"Unsupported file format. Supported: {supported_formats}")
    
    try:
        results = _get_reader().readtext(file_path, detail=0)
        if not results:
            return "No text could be extracted from the document."
        return "\n".join(results)
    except Exception as e:
        raise RuntimeError(f"OCR extraction failed: {str(e)}")


ocr_tool = FunctionTool(
    name="ocr_extract_text",
    description="Extract text from financial documents using OCR",
    params_json_schema={
        "type": "object",
        "properties": {
            "file_path": {"type": "string"}
        },
        "required": ["file_path"]
    },
    on_invoke_tool=ocr_extract_text
)