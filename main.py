import base64
import streamlit as st

from pineapple import PineappleDocument, DisplayedDocument


def initialize_state():
    default_values = {
        "title": None,
        "base64_pdf": None,
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_value(key, value):
    st.session_state[key] = value


initialize_state()

if st.session_state.title:
    st.write(f"Current document: {st.session_state.title}")
else:
    st.write("No document selected")

uploaded_file = st.file_uploader('Upload new PDF', type='pdf')

if uploaded_file is not None:
    set_value("title", "LoRA!")
    base64_pdf = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
    set_value("base64_pdf", base64_pdf)

if st.session_state.base64_pdf is not None:
    pdf_display = f'<embed src="data:application/pdf;base64,{st.session_state.base64_pdf}"' \
                  f'width="700" height="1000" type="application/pdf">'
    """pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="900" height="800" ' \
                  f'type="application/pdf"></iframe> '"""
    st.markdown(pdf_display, unsafe_allow_html=True)

with st.sidebar:
    st.write("You'll find AI stuffz in here!")
