import streamlit as st

DEFAULT_OPENAI_KEY = "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"

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
