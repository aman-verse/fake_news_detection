import os
import streamlit as st

DEFAULT_OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")

def render_sidebar():

    with st.sidebar:

        st.image(
            "assets/images/verifi_logo.png",
            width=145
        )

        st.caption(
            "AI-Powered News Verification"
        )

        st.divider()

        if "navigation" not in st.session_state:
            st.session_state.navigation = st.session_state.get("page", "Home")

        st.caption("NAVIGATION")

        pages = [
            ("⌂", "Home"),
            ("✓", "Verify News"),
            ("◷", "History"),
            ("ⓘ", "About")
        ]

        for icon, page in pages:

            if st.button(
                f"{icon}   {page}",
                key=f"sidebar_{page}",
                use_container_width=True,
                type=(
                    "primary"
                    if st.session_state.navigation == page
                    else "secondary"
                )
            ):

                st.session_state.navigation = page
                st.session_state.page = page

                st.rerun()

        st.divider()

        st.caption("API SETTINGS")

        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = DEFAULT_OPENAI_KEY

        user_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.openai_api_key,
            type="password",
            help="Your OpenAI secret key for GPT verification."
        )
        if user_key != st.session_state.openai_api_key:
            st.session_state.openai_api_key = user_key

        st.divider()

        st.caption("VERIFICATION ENGINE")

        st.success(
            "●  GPT Engine Active"
        )

        st.caption(
            "OpenAI GPT  •  OCR  •  Evidence"
        )

        st.divider()

        st.caption("Verifi v1.0")
        st.caption("AI-Powered Truth Verification")

    return st.session_state.navigation
