from pathlib import Path
import streamlit as st

from rag import answer_question
from ingestion.pipeline import ingest_uploaded_files


# -----------------------------------
# Configuration
# -----------------------------------
st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="📚",
    layout="wide"
)


# -----------------------------------
# Constants
# -----------------------------------
UPLOAD_DIR = Path("data/user_uploads")

SUPPORTED_EXTENSIONS = ["pdf", "txt", "md", "html", "htm"]


# -----------------------------------
# Session state
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed_uploads" not in st.session_state:
    st.session_state.indexed_uploads = []


# -----------------------------------
# Sidebar
# -----------------------------------
with st.sidebar:
    st.title("📚 Enterprise AI")
    st.caption("Documentation Q&A Assistant")

    st.divider()

    # Document upload section
    st.markdown("### 📂 Upload documents")

    uploaded_files = st.file_uploader(
        "Choose documents to add",
        type=SUPPORTED_EXTENSIONS,
        accept_multiple_files=True,
        help="Upload PDF, TXT, Markdown, or HTML documents."
    )

    if uploaded_files:
        st.write("Selected files:")

        for uploaded_file in uploaded_files:
            st.caption(f"📄 {uploaded_file.name}")

        if st.button(
            "📥 Index uploaded documents",
            use_container_width=True
        ):
            try:
                UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

                saved_file_paths = []

                # Save uploaded files locally
                for uploaded_file in uploaded_files:
                    file_path = UPLOAD_DIR / uploaded_file.name

                    file_path.write_bytes(uploaded_file.getvalue())

                    saved_file_paths.append(file_path)

                # Ingest and store their chunks in ChromaDB
                with st.spinner(
                    "Reading documents, creating embeddings, and indexing..."
                ):
                    chunk_count = ingest_uploaded_files(saved_file_paths)

                st.session_state.indexed_uploads.extend(
                    [file.name for file in uploaded_files]
                )

                st.success(
                    f"Successfully indexed {len(uploaded_files)} document(s). "
                    f"Created/stored {chunk_count} chunks."
                )

            except Exception as error:
                st.error("Document indexing failed.")

                with st.expander("Technical error details"):
                    st.code(str(error))

    if st.session_state.indexed_uploads:
        st.markdown("#### Indexed in this session")

        for filename in st.session_state.indexed_uploads:
            st.caption(f"✅ {filename}")

    st.divider()

    # About section
    st.markdown("### About")

    st.write(
        "Ask questions about your organization's "
        "policies, procedures, and uploaded documents."
    )

    st.markdown("### Capabilities")

    st.write(
        "• Document-grounded answers\n"
        "• Upload your own documents\n"
        "• Source citations\n"
        "• Evidence checking\n"
        "• Conflict warnings"
    )

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# -----------------------------------
# Main page
# -----------------------------------
st.title("Enterprise Documentation Assistant")

st.caption(
    "Upload documents in the sidebar, index them, "
    "and ask questions grounded in your documents."
)


# -----------------------------------
# Display previous messages
# -----------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display sources for assistant messages
        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("📄 View sources"):
                for source in message["sources"]:

                    st.markdown(
                        f"**{source.get('citation', '')} "
                        f"{source.get('document', 'Unknown document')}**"
                    )

                    st.caption(
                        f"Page: {source.get('page', 'N/A')} | "
                        f"Section: {source.get('section', 'N/A')} | "
                        f"Version: {source.get('version', 'N/A')} | "
                        f"Status: {source.get('status', 'N/A')}"
                    )

        # Display conflict warning
        if (
            message["role"] == "assistant"
            and message.get("conflict_detected")
        ):
            st.warning(
                "Possible conflicting information was detected "
                "in the retrieved documents. Check the sources carefully."
            )


# -----------------------------------
# Chat input
# -----------------------------------
question = st.chat_input(
    "Ask a question about your indexed documents..."
)


if question:

    # Save and display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents and generating an answer..."
        ):

            try:
                result = answer_question(question)

                answer = result.get(
                    "answer",
                    "I couldn't generate an answer."
                )

                st.markdown(answer)

                # Evidence warning
                if result.get("status") == "insufficient_evidence":

                    st.warning(
                        "I couldn't find enough supporting information "
                        "in the indexed documents to answer confidently."
                    )

                # Conflict warning
                if result.get("conflict_detected"):

                    st.warning(
                        "Possible conflicting information was detected. "
                        "Please review the sources below."
                    )

                # Sources
                sources = result.get("sources", [])

                if sources:

                    with st.expander(
                        "📄 View sources",
                        expanded=True
                    ):

                        for source in sources:

                            st.markdown(
                                f"**{source.get('citation', '')} "
                                f"{source.get('document', 'Unknown document')}**"
                            )

                            st.caption(
                                f"Page: {source.get('page', 'N/A')} | "
                                f"Section: {source.get('section', 'N/A')} | "
                                f"Version: {source.get('version', 'N/A')} | "
                                f"Status: {source.get('status', 'N/A')}"
                            )

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "conflict_detected": result.get(
                        "conflict_detected",
                        False
                    )
                })

            except Exception as error:

                st.error(
                    "Something went wrong while answering. "
                    "Check that your documents are indexed and "
                    "your GROQ_API_KEY is configured."
                )

                with st.expander("Technical error details"):
                    st.code(str(error))