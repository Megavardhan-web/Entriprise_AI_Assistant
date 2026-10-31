"""
Enterprise Documentation Q&A Assistant - Frontend UI Components
Reusable Streamlit components for enterprise-style document Q&A application.
"""

from typing import Any, Dict, List
import streamlit as st


def get_file_icon(filename: str) -> str:
    """Return an appropriate emoji icon based on file extension."""
    lower_name = filename.lower()
    if lower_name.endswith(".pdf"):
        return "📕"
    if lower_name.endswith(".html") or lower_name.endswith(".htm"):
        return "🌐"
    if lower_name.endswith(".md"):
        return "📝"
    if lower_name.endswith(".txt"):
        return "📄"
    return "📁"


def format_file_size(size_bytes: int) -> str:
    """Format bytes into a human-readable string (KB/MB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def render_sidebar() -> Dict[str, Any]:
    """
    Render the sidebar for document upload, document management,
    and UI state controls for demo/testing.

    Returns:
        dict: Information about sidebar interactions (uploaded files, demo scenario, etc.)
    """
    with st.sidebar:
        # 1. Application Name & Header
        st.markdown(
            """
            <div style="padding-bottom: 0.5rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem;">
                <h2 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #1e293b;">
                    🏢 Enterprise Knowledge Assistant
                </h2>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.8rem; color: #64748b;">
                    AI-Powered Enterprise Documentation Q&A
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Document Upload Section
        st.markdown("### 📂 Document Repository")
        st.caption(
            "Upload company manuals, compliance policies, and technical docs to index."
        )

        # Initialize uploader key in session_state if not present
        if "uploader_key" not in st.session_state:
            st.session_state.uploader_key = 0

        uploaded_files = st.file_uploader(
            label="Upload documents",
            type=["pdf", "html", "md", "txt"],
            accept_multiple_files=True,
            key=f"doc_uploader_{st.session_state.uploader_key}",
            help="Supported file types: PDF, HTML, Markdown (.md), Plain Text (.txt)",
            label_visibility="collapsed",
        )

        # Update uploaded documents list in session state
        if uploaded_files:
            st.session_state.uploaded_docs = [
                {
                    "name": file.name,
                    "size": file.size,
                    "type": file.name.split(".")[-1].upper(),
                }
                for file in uploaded_files
            ]

        # 3. Uploaded Documents List Section
        st.markdown("---")
        doc_count = len(st.session_state.get("uploaded_docs", []))
        st.markdown(f"#### 📑 Uploaded Documents ({doc_count})")

        if doc_count > 0:
            for doc in st.session_state.uploaded_docs:
                icon = get_file_icon(doc["name"])
                size_str = format_file_size(doc["size"])
                st.markdown(
                    f"""
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 10px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                        <div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 70%;">
                            <span style="margin-right: 6px;">{icon}</span>
                            <span style="font-size: 0.85rem; font-weight: 500; color: #0f172a;" title="{doc['name']}">{doc['name']}</span>
                        </div>
                        <span style="font-size: 0.75rem; color: #64748b; background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{size_str}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Clear documents button
            if st.button("🗑️ Clear Uploaded Documents", use_container_width=True):
                st.session_state.uploaded_docs = []
                st.session_state.uploader_key += 1
                st.rerun()
        else:
            st.info(
                "No documents uploaded yet.\nUpload PDF, HTML, MD, or TXT files above.",
                icon="ℹ️",
            )

        # 4. Hackathon UI State Testing Section (Mock switcher)
        st.markdown("---")
        st.markdown("#### 🧪 UI State Simulator")
        st.caption(
            "Test how the frontend renders different AI backend responses:"
        )

        scenario = st.selectbox(
            "Select Response Scenario:",
            options=[
                "Standard Answer (Verified with Citations)",
                "Conflicting Information Warning",
                "Insufficient Evidence Warning",
                "Answer Not Found Warning",
            ],
            index=0,
            help="Allows hackathon judges and developers to inspect all UI warning components and citation cards.",
        )

        # 5. Architecture & Connection Status Badge
        st.markdown("---")
        st.markdown(
            """
            <div style="background: #f1f5f9; border-left: 3px solid #3b82f6; padding: 8px 12px; border-radius: 4px; font-size: 0.75rem; color: #334155;">
                <strong>Backend Status:</strong><br/>
                🟡 Frontend Prototype (Mock Data)<br/>
                <em>RAG / Vector DB / LLM hookup ready</em>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return {
            "uploaded_files": st.session_state.get("uploaded_docs", []),
            "scenario": scenario,
        }


def render_header():
    """Render the main header with enterprise branding and system description."""
    st.markdown(
        """
        <div style="background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%); padding: 1.5rem 2rem; border-radius: 10px; color: white; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div>
                    <h1 style="color: white; font-size: 1.75rem; font-weight: 700; margin: 0;">
                        Enterprise Knowledge Assistant
                    </h1>
                    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0.5rem 0 0 0;">
                        Reliable, citation-grounded Q&A across your organization's technical documents, policies, and standard operating procedures.
                    </p>
                </div>
                <div style="margin-top: 0.5rem;">
                    <span style="background-color: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6; color: #93c5fd; font-size: 0.75rem; padding: 4px 10px; border-radius: 20px; font-weight: 500;">
                        ⚡ AI Engineer Hackathon
                    </span>
                    <span style="background-color: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #6ee7b7; font-size: 0.75rem; padding: 4px 10px; border-radius: 20px; font-weight: 500; margin-left: 6px;">
                        UI Prototype
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_history(messages: List[Dict[str, Any]]):
    """
    Render past question-answer pairs in a chat-style interface.

    Args:
        messages: List of chat interaction dictionaries.
    """
    if not messages:
        st.markdown(
            """
            <div style="text-align: center; padding: 2rem 1rem; border: 2px dashed #cbd5e1; border-radius: 8px; margin: 1rem 0; color: #64748b;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💬</div>
                <h4 style="margin: 0; color: #334155;">No questions asked yet</h4>
                <p style="font-size: 0.85rem; margin: 0.25rem 0 0 0;">
                    Type an employee question below or pick a sample question to inspect the assistant's grounded answer format.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for msg in messages:
        # Render User Question
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**{msg['question']}**")

        # Render Assistant Answer
        with st.chat_message("assistant", avatar="🤖"):
            render_answer_section(msg["response"])


def render_answer_section(response_data: Dict[str, Any]):
    """
    Dedicated answer display component with answer text, source citations,
    supporting evidence excerpts, and warning banners.

    Args:
        response_data: Dictionary containing answer, citations, evidence, and warnings.
    """
    # 1. Display any warning components first if present in the response
    warning_type = response_data.get("warning_type")
    warning_message = response_data.get("warning_message")

    if warning_type == "conflicting_information":
        render_conflicting_info_warning(
            warning_message
            or "Conflicting guidelines detected between multiple policy documents."
        )
    elif warning_type == "insufficient_evidence":
        render_insufficient_evidence_warning(
            warning_message
            or "Low retrieval confidence. The available documents provide only partial information."
        )
    elif warning_type == "answer_not_found":
        render_not_found_warning(
            warning_message
            or "The requested information could not be verified in any uploaded documentation."
        )

    # 2. Main Generated Answer Body
    st.markdown(
        """
        <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #2563eb; margin-bottom: 0.25rem;">
            Generated Enterprise Response:
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem 1.25rem; font-size: 0.95rem; color: #1e293b; line-height: 1.6; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);">
            {response_data.get('answer', 'No answer text generated.')}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3. Source Citations Section
    citations = response_data.get("citations", [])
    if citations:
        st.markdown("##### 📌 Source Citations")
        col_count = min(len(citations), 3)
        cols = st.columns(col_count)

        for idx, citation in enumerate(citations):
            col_idx = idx % col_count
            with cols[col_idx]:
                doc_name = citation.get("document", "Unknown Document")
                page_num = citation.get("page", "N/A")
                section = citation.get("section", "General")
                relevance = citation.get("relevance", "High")

                st.markdown(
                    f"""
                    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 3px solid #2563eb; border-radius: 6px; padding: 0.6rem 0.8rem; margin-bottom: 0.5rem; font-size: 0.8rem;">
                        <div style="font-weight: 600; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{doc_name}">
                            📄 {doc_name}
                        </div>
                        <div style="color: #475569; margin-top: 4px;">
                            <strong>Section:</strong> {section}
                        </div>
                        <div style="color: #475569;">
                            <strong>Page:</strong> {page_num} &nbsp;|&nbsp; <strong>Relevance:</strong> <span style="color: #16a34a; font-weight: 600;">{relevance}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # 4. Supporting Evidence Excerpts
    evidence_list = response_data.get("evidence", [])
    if evidence_list:
        with st.expander("🔍 View Supporting Evidence Excerpts", expanded=False):
            st.caption(
                "Verbatim text passages retrieved from the source documentation that support this answer:"
            )
            for idx, item in enumerate(evidence_list, start=1):
                quote = item.get("text", "")
                source_ref = item.get("source_ref", "Reference")
                st.markdown(
                    f"""
                    <div style="background-color: #f1f5f9; border-left: 4px solid #64748b; padding: 0.75rem 1rem; border-radius: 4px; margin-bottom: 0.75rem; font-size: 0.85rem; color: #334155;">
                        <div style="font-style: italic; margin-bottom: 0.4rem;">
                            "{quote}"
                        </div>
                        <div style="font-size: 0.75rem; color: #64748b; text-align: right; font-weight: 500;">
                            — [{idx}] {source_ref}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_conflicting_info_warning(message: str):
    """
    Render a warning alert indicating conflicting information across documents.
    """
    st.markdown(
        f"""
        <div style="background-color: #fffbeb; border: 1px solid #fde68a; border-left: 5px solid #d97706; padding: 0.85rem 1.15rem; border-radius: 6px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.1rem;">⚠️</span>
                <strong style="color: #92400e; font-size: 0.9rem;">Conflicting Information Detected</strong>
            </div>
            <p style="margin: 0.35rem 0 0 0; font-size: 0.85rem; color: #b45309; line-height: 1.4;">
                {message}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insufficient_evidence_warning(message: str):
    """
    Render a warning alert indicating insufficient evidence was retrieved.
    """
    st.markdown(
        f"""
        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-left: 5px solid #2563eb; padding: 0.85rem 1.15rem; border-radius: 6px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.1rem;">ℹ️</span>
                <strong style="color: #1e40af; font-size: 0.9rem;">Insufficient Evidence Warning</strong>
            </div>
            <p style="margin: 0.35rem 0 0 0; font-size: 0.85rem; color: #1d4ed8; line-height: 1.4;">
                {message}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_not_found_warning(message: str):
    """
    Render a warning alert indicating no answer was found in the documentation.
    """
    st.markdown(
        f"""
        <div style="background-color: #fef2f2; border: 1px solid #fecaca; border-left: 5px solid #dc2626; padding: 0.85rem 1.15rem; border-radius: 6px; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.1rem;">🚫</span>
                <strong style="color: #991b1b; font-size: 0.9rem;">Answer Not Found in Documentation</strong>
            </div>
            <p style="margin: 0.35rem 0 0 0; font-size: 0.85rem; color: #b91c1c; line-height: 1.4;">
                {message}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_evaluation_panel():
    """
    Render the placeholder evaluation panel for future retrieval and
    answer-quality metrics (RAG Triad, RAGAS, TruLens).
    """
    with st.expander("📊 Evaluation Panel (Placeholder for RAG Metrics)", expanded=False):
        st.markdown(
            """
            <div style="background-color: #f8fafc; border: 1px dashed #94a3b8; border-radius: 6px; padding: 0.75rem 1rem; margin-bottom: 1rem;">
                <p style="margin: 0; font-size: 0.85rem; color: #475569;">
                    <strong>ℹ️ Future Integration Placeholder:</strong> When your AI backend (RAG pipeline, ChromaDB vector store, and Groq/LLM generation) is hooked up, this panel will display live retrieval and generation quality metrics.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Retrieval Precision@K",
                value="--",
                delta="Awaiting Backend",
                help="Proportion of top-K retrieved document chunks that are relevant to the query.",
            )
            st.metric(
                label="Context Relevance",
                value="--",
                help="Semantic score measuring whether the retrieved context contains only pertinent information.",
            )

        with col2:
            st.metric(
                label="Answer Faithfulness",
                value="--",
                delta="Awaiting Backend",
                help="Groundedness score measuring whether all claims in the answer can be inferred from context.",
            )
            st.metric(
                label="Answer Relevance",
                value="--",
                help="Measures how well the generated answer directly addresses the employee question.",
            )

        with col3:
            st.metric(
                label="Retrieval Latency",
                value="-- ms",
                help="Time taken to search vector database and retrieve relevant chunks.",
            )
            st.metric(
                label="Total Tokens",
                value="--",
                help="Estimated input and output token consumption for this Q&A turn.",
            )


def get_mock_response_by_scenario(scenario: str, question: str) -> Dict[str, Any]:
    """
    Generate realistic mock response data corresponding to the selected
    UI state scenario. This ensures the frontend can be thoroughly demonstrated
    without pretending backend AI functionality is currently connected.

    Args:
        scenario: The selected UI scenario string.
        question: The user query text.

    Returns:
        dict: Structured answer data including citations, evidence, and warnings.
    """
    if "Conflicting Information" in scenario:
        return {
            "answer": (
                f"**[MOCK DATA]** Regarding your inquiry on: *\"{question}\"*, "
                "the enterprise records contain conflicting policy guidelines across different departments. "
                "The Global IT Security Handbook permits personal mobile device usage with MDM registration, "
                "whereas the Financial Compliance Policy strictly prohibits unmanaged endpoints on enterprise networks."
            ),
            "warning_type": "conflicting_information",
            "warning_message": (
                "Discrepancy detected between 'IT_Security_Handbook_2025.pdf' (Section 4.1) "
                "and 'Financial_Compliance_Standards.pdf' (Section 9.3). Please consult compliance officers."
            ),
            "citations": [
                {
                    "document": "IT_Security_Handbook_2025.pdf",
                    "page": "14",
                    "section": "Sec 4.1 Mobile Device Management",
                    "relevance": "High",
                },
                {
                    "document": "Financial_Compliance_Standards.pdf",
                    "page": "42",
                    "section": "Sec 9.3 Endpoint Authorization",
                    "relevance": "High",
                },
            ],
            "evidence": [
                {
                    "text": "Employees may connect personal smartphones provided corporate MDM profiles are installed and updated monthly.",
                    "source_ref": "IT_Security_Handbook_2025.pdf (Page 14, Sec 4.1)",
                },
                {
                    "text": "Under no circumstances shall non-company owned hardware connect to production network zones or process customer telemetry.",
                    "source_ref": "Financial_Compliance_Standards.pdf (Page 42, Sec 9.3)",
                },
            ],
        }

    elif "Insufficient Evidence" in scenario:
        return {
            "answer": (
                f"**[MOCK DATA]** The documentation mentions preliminary guidelines for: *\"{question}\"*, "
                "but the retrieved documentation does not provide definitive steps or complete policy specifics. "
                "A tentative protocol is mentioned, but formal approval processes are missing."
            ),
            "warning_type": "insufficient_evidence",
            "warning_message": (
                "Retrieved passages contain partial keywords, but context relevance is below threshold (Confidence: 42%). "
                "The answer may be incomplete."
            ),
            "citations": [
                {
                    "document": "Operations_Overview.md",
                    "page": "N/A",
                    "section": "Appendix B: Provisional Protocols",
                    "relevance": "Moderate",
                }
            ],
            "evidence": [
                {
                    "text": "Provisional workflows are subject to quarterly review. Detailed execution matrices are maintained separately.",
                    "source_ref": "Operations_Overview.md (Appendix B)",
                }
            ],
        }

    elif "Answer Not Found" in scenario:
        return {
            "answer": (
                f"**[MOCK DATA]** I could not find information addressing: *\"{question}\"* "
                "in any of the uploaded enterprise documents."
            ),
            "warning_type": "answer_not_found",
            "warning_message": (
                "No relevant document sections matched your query with sufficient semantic similarity. "
                "Try rephrasing your question or uploading supplementary documentation."
            ),
            "citations": [],
            "evidence": [],
        }

    else:
        # Standard Verified Answer
        return {
            "answer": (
                f"**[MOCK DATA]** Based on the uploaded enterprise documentation regarding: *\"{question}\"*:\n\n"
                "1. **Eligibility & Scope:** All regular full-time team members are covered under this standard procedure.\n"
                "2. **Standard Processing Timeline:** Requests submitted before 3:00 PM EST are processed within two business days.\n"
                "3. **Approval Hierarchy:** Requires initial manager endorsement followed by automated audit verification in the enterprise portal.\n"
                "4. **Exceptions & Escalations:** Urgent escalations must follow the Sev-2 expedited escalation protocol defined in Appendix C."
            ),
            "warning_type": None,
            "warning_message": None,
            "citations": [
                {
                    "document": "Employee_Handbook_2025.pdf",
                    "page": "18",
                    "section": "Sec 3.2 Standard Procedures",
                    "relevance": "96%",
                },
                {
                    "document": "Enterprise_SOP_Technical_Specs.html",
                    "page": "N/A",
                    "section": "Processing Workflows & SLAs",
                    "relevance": "88%",
                },
            ],
            "evidence": [
                {
                    "text": "Standard request turnaround is 48 business hours when submitted prior to 15:00 EST cutoff. Manager sign-off required.",
                    "source_ref": "Employee_Handbook_2025.pdf (Page 18, Sec 3.2)",
                },
                {
                    "text": "Automated workflow verification handles routing to compliance auditing without manual intervention unless flagged.",
                    "source_ref": "Enterprise_SOP_Technical_Specs.html (Workflow SLAs)",
                },
            ],
        }
