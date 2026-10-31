"""
Enterprise Knowledge Assistant - Main Application Entry Point
Streamlit frontend for enterprise documentation Q&A hackathon project.
"""

import streamlit as st
from frontend.components import (
    render_sidebar,
    render_header,
    render_chat_history,
    render_answer_section,
    render_evaluation_panel,
    get_mock_response_by_scenario,
)

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 2. Enterprise Custom Styling (CSS)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Base typography and background adjustments */
        .main {
            background-color: #f8fafc;
        }
        
        /* Make chat bubbles sleek and distinct */
        .stChatMessage {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            padding: 0.75rem 1rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }
        
        /* Input container styling */
        div[data-testid="stTextInput"] input {
            border-radius: 6px;
            border: 1px solid #cbd5e1;
            padding: 0.6rem 0.85rem;
            font-size: 0.95rem;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 1px #2563eb;
        }

        /* Buttons styling */
        button[kind="primary"] {
            background-color: #2563eb;
            color: white;
            border-radius: 6px;
            font-weight: 600;
            border: none;
            padding: 0.5rem 1.25rem;
            transition: all 0.2s ease;
        }
        button[kind="primary"]:hover {
            background-color: #1d4ed8;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        }

        /* Sidebar container styling */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }
        
        /* Mock notification banner */
        .mock-banner {
            background-color: #fff7ed;
            border: 1px solid #ffedd5;
            border-left: 4px solid #f97316;
            padding: 0.5rem 0.85rem;
            border-radius: 4px;
            font-size: 0.8rem;
            color: #9a3412;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. Session State Initialization
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

# -----------------------------------------------------------------------------
# 4. Render Sidebar Component
# -----------------------------------------------------------------------------
sidebar_state = render_sidebar()
selected_scenario = sidebar_state["scenario"]

# -----------------------------------------------------------------------------
# 5. Render Header Component
# -----------------------------------------------------------------------------
render_header()

# Mock Notice Banner for hackathon transparency
st.markdown(
    f"""
    <div class="mock-banner">
        <strong>⚡ Hackathon Frontend Active:</strong> Operating in <em>Frontend Prototype Mode</em>. 
        Active response simulation: <strong>{selected_scenario}</strong>. 
        <em>(AI backend / RAG vector database will be linked in next phase).</em>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 6. Main Q&A Interface Section
# -----------------------------------------------------------------------------
st.markdown("### 💬 Ask a Question")
st.caption("Ask questions across all indexed corporate handbooks, policies, and technical guidelines.")

# Quick-ask sample question buttons if chat is empty
if not st.session_state.messages:
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b; margin-bottom: 0.35rem; font-weight: 500;">
            💡 Quick Demo Queries (Click to test):
        </div>
        """,
        unsafe_allow_html=True,
    )
    sample_col1, sample_col2, sample_col3 = st.columns(3)
    
    with sample_col1:
        if st.button("📋 Standard Approval Process", use_container_width=True):
            st.session_state["prefill_question"] = "What is the standard procedure and timeline for expense approvals?"
            st.rerun()
    with sample_col2:
        if st.button("📱 Mobile Device & Security Policy", use_container_width=True):
            st.session_state["prefill_question"] = "Are employees allowed to connect personal mobile devices to production network zones?"
            st.rerun()
    with sample_col3:
        if st.button("🚨 Incident Escalation SLA", use_container_width=True):
            st.session_state["prefill_question"] = "What are the escalation procedures and response times for Sev-1 outages?"
            st.rerun()

# Text input for questions
default_input_value = st.session_state.pop("prefill_question", "")

with st.container():
    col_input, col_btn = st.columns([5, 1])
    
    with col_input:
        user_question = st.text_input(
            label="Employee Question Input",
            placeholder="e.g., What is our remote work hardware reimbursement policy?",
            value=default_input_value,
            label_visibility="collapsed",
            key="user_question_input",
        )
    
    with col_btn:
        submit_clicked = st.button("Submit", type="primary", use_container_width=True)

# Process question submission
if submit_clicked and user_question.strip():
    with st.spinner("Searching document repository and generating response..."):
        # Retrieve structured mock response matching current scenario
        mock_response = get_mock_response_by_scenario(
            scenario=selected_scenario,
            question=user_question.strip(),
        )

        # Store interaction in session state
        st.session_state.messages.append({
            "question": user_question.strip(),
            "response": mock_response,
        })
        st.rerun()

elif submit_clicked and not user_question.strip():
    st.warning("Please type a question before clicking Submit.", icon="⚠️")

# -----------------------------------------------------------------------------
# 7. Render Q&A Conversation & Answer Section
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 📋 Responses & Citations")

# Render chat history with answers, citations, and evidence excerpts
render_chat_history(st.session_state.messages)

# Conversation controls (Clear chat)
if st.session_state.messages:
    clear_col1, clear_col2 = st.columns([6, 1])
    with clear_col2:
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# -----------------------------------------------------------------------------
# 8. Evaluation Panel Placeholder (RAG Metrics)
# -----------------------------------------------------------------------------
st.markdown("---")
render_evaluation_panel()

# -----------------------------------------------------------------------------
# 9. Developer / Hackathon Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align: center; color: #94a3b8; font-size: 0.75rem; padding: 1.5rem 0 0.5rem 0;">
        Enterprise Knowledge Assistant &nbsp;|&nbsp; Streamlit Frontend Prototype &nbsp;|&nbsp; Built for AI Engineer Hackathon
    </div>
    """,
    unsafe_allow_html=True,
)
