import io
import urllib.request
from typing import Any, Type
from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool
from pydantic import BaseModel, Field

# Define the argument model for the PDF analyzer
class PDFAnalyzerArgs(BaseModel):
    pdf_source: str = Field(..., description="URL of the PDF")

# Define the PDFAnalyzer tool
class PDFAnalyzer(BaseTool):
    """Analyzes PDFs from URLs."""
    name: str = "pdf_analyzer"
    description: str = "Extracts text and metadata from online PDFs."
    args_schema: Type[BaseModel] = PDFAnalyzerArgs

    # Main function that runs the PDF analysis
    def _run(self, pdf_source: str) -> str:
        try:
            # Open the PDF from the URL
            with urllib.request.urlopen(pdf_source) as response:
                pdf_file = io.BytesIO(response.read())
                reader = PdfReader(pdf_file)
                
                # Initialize analysis output
                analysis = "PDF Analysis for " + pdf_source + ":\n"
                analysis += "Total pages: " + str(len(reader.pages)) + "\n\n"

                # Extract and display metadata if available
                if reader.metadata:
                    analysis += "Metadata:\n"
                    for key, value in reader.metadata.items():
                        analysis += str(key) + ": " + str(value) + "\n"
                    analysis += "\n"

                # Preview the first three pages of the PDF
                for i, page in enumerate(reader.pages[:3], 1):
                    text = page.extract_text()
                    analysis += "Page " + str(i) + " preview:\n" + text[:200] + "...\n\n"

                return analysis

        # Handle any exceptions that occur during analysis
        except Exception as e:
            raise ValueError("Error analyzing PDF: " + str(e))

    # Async version is not implemented
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Async not supported.")

# Example usage of the PDFAnalyzer
if __name__ == "__main__":
    analyzer = PDFAnalyzer()
    result = analyzer._run()
    print(result)
