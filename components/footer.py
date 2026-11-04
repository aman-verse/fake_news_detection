import streamlit as st

def render_footer():

    st.divider()

    left, middle, right = st.columns(3)

    with left:
        st.caption("🛡️ Verifi")

    with middle:
        st.caption("AI-powered news verification")

    with right:
        st.caption("Version 1.0 • 2026")
