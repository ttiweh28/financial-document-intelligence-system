from agents.tool import FunctionTool
import easyocr
import os
import numpy as np
from pdf2image import convert_from_path

_reader = None

def _get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'])
    return _reader


def ocr_extract_text(ctx, file_path: str) -> str:
    """Extract text from images or PDFs using OCR."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    supported_formats = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf')
    if not file_path.lower().endswith(supported_formats):
        raise ValueError(f"Unsupported file format. Supported: {supported_formats}")

    try:
        reader = _get_reader()
        all_text = []

        if file_path.lower().endswith(".pdf"):
            images = convert_from_path(file_path)

            for img in images:
                img_np = np.array(img)
                results = reader.readtext(img_np, detail=0)
                all_text.extend(results)
        else:
            results = reader.readtext(file_path, detail=0)
            all_text = results

        if not all_text:
            return "No text could be extracted from the document."

        return "\n".join(all_text)

    except Exception as e:
        print("OCR DEBUG ERROR:", e)
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