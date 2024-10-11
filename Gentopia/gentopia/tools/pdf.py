import io
import urllib.request
from typing import Any, Type
from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool
from pydantic import BaseModel, Field

class PDFAnalyzerArgs(BaseModel):
    pdf_source: str = Field(..., description="URL of the PDF")

class PDFAnalyzer(BaseTool):
    """Analyzes PDFs from URLs."""
    name: str = "pdf_analyzer"
    description: str = "Extracts text and metadata from online PDFs."
    args_schema: Type[BaseModel] = PDFAnalyzerArgs

    def _run(self, pdf_source: str) -> str:
        try:
            with urllib.request.urlopen(pdf_source) as response:
                pdf_file = io.BytesIO(response.read())
                reader = PdfReader(pdf_file)
                
                analysis = f"PDF Analysis for {pdf_source}:\n"
                analysis += f"Total pages: {len(reader.pages)}\n\n"

                if reader.metadata:
                    analysis += "Metadata:\n"
                    for key, value in reader.metadata.items():
                        analysis += f"{key}: {value}\n"
                    analysis += "\n"

                for i, page in enumerate(reader.pages[:3], 1):
                    text = page.extract_text()
                    analysis += f"Page {i} preview:\n{text[:200]}...\n\n"

                return analysis

        except Exception as e:
            return f"Error analyzing PDF: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Async not supported.")


if __name__ == "__main__":
    analyzer = PDFAnalyzer()
    result = analyzer._run()
    print(result)