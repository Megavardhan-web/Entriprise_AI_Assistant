from pathlib import Path
import re

import fitz  # PyMuPDF
from bs4 import BeautifulSoup


SUPPORTED_EXTENSIONS = {".pdf", ".html", ".htm", ".md", ".txt"}


def extract_policy_metadata(text):
    """
    Extract policy metadata from document text.

    Expected labels:
    Document ID: HR-LEAVE-001
    Version: 2.0
    Effective Date: 1 July 2026
    Status: Current
    """
    metadata = {}

    patterns = {
        "version": r"(?im)^\s*Version:\s*(.+?)\s*$",
        "effective_date": r"(?im)^\s*Effective Date:\s*(.+?)\s*$",
        "status": r"(?im)^\s*Status:\s*(.+?)\s*$",
        "document_id": r"(?im)^\s*Document ID:\s*(.+?)\s*$",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)

        if match:
            metadata[key] = match.group(1).strip()

    return metadata


def create_metadata(path, page, file_type, text):
    """
    Create basic metadata and add policy-specific metadata.
    """
    metadata = {
        "source": path.name,
        "page": page,
        "file_type": file_type,
    }

    metadata.update(extract_policy_metadata(text))

    return metadata


def load_document(file_path):
    """
    Load PDF, HTML, Markdown, or TXT documents.

    Returns a list of dictionaries:
    [
        {
            "text": "...",
            "metadata": {...}
        }
    ]
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    documents = []

    # -----------------------------------
    # PDF
    # -----------------------------------
    if extension == ".pdf":

        with fitz.open(path) as pdf:

            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text")

                if text.strip():
                    metadata = create_metadata(
                        path=path,
                        page=page_number,
                        file_type="pdf",
                        text=text,
                    )

                    documents.append({
                        "text": text,
                        "metadata": metadata,
                    })

    # -----------------------------------
    # HTML
    # -----------------------------------
    elif extension in {".html", ".htm"}:

        html = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        soup = BeautifulSoup(html, "html.parser")

        # Remove irrelevant page elements
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        if text.strip():
            metadata = create_metadata(
                path=path,
                page=1,
                file_type="html",
                text=text,
            )

            documents.append({
                "text": text,
                "metadata": metadata,
            })

    # -----------------------------------
    # Markdown and TXT
    # -----------------------------------
    else:

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        if text.strip():
            metadata = create_metadata(
                path=path,
                page=1,
                file_type=extension[1:],
                text=text,
            )

            documents.append({
                "text": text,
                "metadata": metadata,
            })

    return documents