import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from backend.services.document_formatter import (
    format_docx,
    format_pdf,
    format_txt,
    format_html_preview,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .notice {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #cccccc;
        margin-bottom: 20px;
    }

    .document-preview {
        padding: 30px;
        border: 1px solid #dddddd;
        border-radius: 10px;
        background-color: white;
        color: black;
        min-height: 400px;
        line-height: 1.7;
    }

    .document-brand {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .document-content {
        font-family: "Times New Roman", serif;
        font-size: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.markdown(
    """
    <div class="notice">
    <b>Disclaimer:</b>
    LegalEase generates AI-assisted legal document drafts.
    The generated document should be reviewed by a qualified
    legal professional before use.
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# BACKEND URL
# --------------------------------------------------

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = "Employment Contract"


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.subheader("📄 Create Your Legal Document")


document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement (NDA)",
        "Service Agreement",
        "Partnership Agreement",
        "Other",
    ],
)


parties = st.text_area(
    "Parties",
    placeholder=(
        "Example:\n"
        "Employer: ABC Technologies Pvt Ltd\n"
        "Employee: John Doe"
    ),
    height=120,
)


effective_date = st.text_input(
    "Effective Date",
    placeholder="Example: 1 October 2026",
)


terms = st.text_area(
    "Terms and Conditions",
    placeholder=(
        "Enter terms separated by semicolons (;)\n\n"
        "Example:\n"
        "Monthly salary is Rs. 40,000; "
        "Working hours are 9 AM to 6 PM; "
        "Notice period is 30 days; "
        "Confidential information must not be disclosed"
    ),
    height=180,
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button(
    "✨ Generate Document",
    use_container_width=True,
):

    if not parties.strip():
        st.error("Please enter the parties.")

    elif not effective_date.strip():
        st.error("Please enter the effective date.")

    elif not terms.strip():
        st.error("Please enter the terms and conditions.")

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
        }

        try:

            with st.spinner(
                "Generating your legal document..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.generated_content = (
                    data["content"]
                )

                st.session_state.document_type = (
                    data["document_type"]
                )

                st.success(
                    "Document generated successfully!"
                )

            else:

                try:
                    error_message = response.json().get(
                        "detail",
                        "Unknown backend error."
                    )
                except Exception:
                    error_message = response.text

                st.error(
                    f"Generation failed: {error_message}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Backend server is not running. "
                "Please start FastAPI first."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request took too long. "
                "Please try again."
            )

        except Exception as error:

            st.error(
                f"Unexpected error: {error}"
            )


# --------------------------------------------------
# GENERATED DOCUMENT
# --------------------------------------------------

if st.session_state.generated_content:

    st.divider()

    st.subheader("📝 Generated Document")

    edited_content = st.text_area(
        "Edit your document if required:",
        value=st.session_state.generated_content,
        height=500,
    )

    st.session_state.generated_content = edited_content

    st.subheader("👀 Document Preview")

    preview_html = format_html_preview(
        st.session_state.generated_content
    )

    st.markdown(
        preview_html,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------
    # DOWNLOAD SECTION
    # --------------------------------------------------

    st.subheader("⬇️ Download Document")

    txt_file = format_txt(
        st.session_state.generated_content
    )

    docx_file = format_docx(
        st.session_state.generated_content,
        st.session_state.document_type,
    )

    pdf_file = format_pdf(
        st.session_state.generated_content,
        st.session_state.document_type,
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.download_button(
            label="📄 Download TXT",
            data=txt_file,
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True,
        )


    with col2:

        st.download_button(
            label="📝 Download DOCX",
            data=docx_file,
            file_name="LegalEase_Document.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )


    with col3:

        st.download_button(
            label="📕 Download PDF",
            data=pdf_file,
            file_name="LegalEase_Document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )