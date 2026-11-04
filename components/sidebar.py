import streamlit as st

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

        st.caption("VERIFICATION ENGINE")

        st.success(
            "●  System Online"
        )

        st.caption(
            "NLP  •  OCR  •  Evidence  •  NLI"
        )

        st.divider()

        st.caption("Verifi v1.0")
        st.caption("Evidence-first verification")

    return st.session_state.navigation
