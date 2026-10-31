from pathlib import Path
import fitz  # PyMuPDF
from bs4 import BeautifulSoup


SUPPORTED_EXTENSIONS = {".pdf", ".html", ".htm", ".md", ".txt"}


def load_document(file_path):
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    documents = []

    if extension == ".pdf":
        with fitz.open(path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text")

                if text.strip():
                    documents.append({
                        "text": text,
                        "metadata": {
                            "source": path.name,
                            "page": page_number,
                            "file_type": "pdf"
                        }
                    })

    elif extension in {".html", ".htm"}:
        html = path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        if text.strip():
            documents.append({
                "text": text,
                "metadata": {
                    "source": path.name,
                    "page": 1,
                    "file_type": "html"
                }
            })

    # Markdown and TXT
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")

        if text.strip():
            documents.append({
                "text": text,
                "metadata": {
                    "source": path.name,
                    "page": 1,
                    "file_type": extension[1:]
                }
            })

    return documents