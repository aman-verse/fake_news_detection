import streamlit as st

def show():

    st.markdown(
        """
        <style>
        .hero-title {
            text-align: center;
            font-size: 72px;
            font-weight: 800;
            margin-top: 0;
            margin-bottom: 5px;
            transform: translateY(-45px);
            background: linear-gradient(
                90deg,
                #168cff,
                #00d9e8,
                #5cff70
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-line {
            width: 300px;
            height: 3px;
            margin: 0 auto 25px auto;
            background: linear-gradient(
                90deg,
                #168cff,
                #00d9e8,
                #5cff70
            );
            border-radius: 5px;
        }

        .hero-subtitle {
            text-align: center;
            font-size: 30px;
            font-weight: 700;
            margin-top: -45px;
            margin-bottom: 15px;
        }

        .hero-description {
            text-align: center;
            font-size: 17px;
            color: #b8c0cc;
            line-height: 1.6;
            max-width: 750px;
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    logo_left, logo_center, logo_right = st.columns(
        [2, 1, 2]
    )

    with logo_center:

        st.image(
            "assets/images/verifi_logo.png",
            width=180
        )

    st.markdown(
        """
        <h1 class="hero-title">
            Verifi
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-line"></div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h2 class="hero-subtitle">
            AI-Powered News Verification Platform
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="hero-description">
            Investigate news articles, screenshots and online claims
            using evidence from relevant trusted sources.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    cta1, cta2, cta3 = st.columns(
        [1, 1, 1]
    )

    with cta1:
        pass

    with cta2:

        if st.button(
            "🔎  Verify News",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.navigation = "Verify News"
            st.rerun()

    with cta3:
        pass

    st.write("")
    st.divider()

    st.subheader("Verification, not just prediction")

    st.write(
        "Verifi is designed to combine multiple signals before "
        "producing a final assessment."
    )

    st.write("")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Analysis",
            "NLP",
            "Context-aware"
        )

    with m2:
        st.metric(
            "Input",
            "Text + Image",
            "OCR supported"
        )

    with m3:
        st.metric(
            "Evidence",
            "Multi-source",
            "Cross-checking"
        )

    with m4:
        st.metric(
            "Output",
            "Explainable",
            "Evidence-backed"
        )

    st.write("")
    st.divider()

    st.header("What Verifi can analyze")

    st.write(
        "A verification system needs more than a classifier. "
        "These modules work together during an investigation."
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.subheader("🧠 AI Analysis")

            st.write(
                "Analyze the language and context of a claim "
                "using NLP models."
            )

            st.caption(
                "Claims • Entities • Context • Semantics"
            )

    with col2:

        with st.container(border=True):

            st.subheader("📷 Image Intelligence")

            st.write(
                "Extract news text from screenshots and "
                "image-based posts using OCR."
            )

            st.caption(
                "Screenshots • Posters • Social Posts"
            )

    with col3:

        with st.container(border=True):

            st.subheader("🌐 Evidence Search")

            st.write(
                "Find relevant information from trusted news "
                "organizations and official sources."
            )

            st.caption(
                "News • Official Sources • Relevant Evidence"
            )

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.subheader("🔎 Claim Analysis")

            st.write(
                "Break an article into meaningful factual "
                "claims that can be investigated."
            )

            st.caption(
                "Claims • Entities • Relationships"
            )

    with col2:

        with st.container(border=True):

            st.subheader("📊 Explainable Verdict")

            st.write(
                "Show the reasoning and evidence behind "
                "the final assessment."
            )

            st.caption(
                "Verdict • Confidence • Evidence"
            )

    with col3:

        with st.container(border=True):

            st.subheader("🛡️ Evidence First")

            st.write(
                "Prioritize supporting evidence instead of "
                "depending entirely on a model score."
            )

            st.caption(
                "Sources • Similarity • Verification"
            )

    st.write("")
    st.divider()

    st.header("How Verifi works")

    st.write(
        "The verification pipeline moves from the submitted "
        "content to evidence and finally to an explainable result."
    )

    st.write("")

    step1, step2, step3, step4, step5 = st.columns(5)

    with step1:

        st.markdown("### 01")

        st.subheader("Submit")

        st.write(
            "Paste an article or upload a screenshot."
        )

    with step2:

        st.markdown("### 02")

        st.subheader("Understand")

        st.write(
            "Extract text, entities and important claims."
        )

    with step3:

        st.markdown("### 03")

        st.subheader("Investigate")

        st.write(
            "Search for relevant supporting or contradicting evidence."
        )

    with step4:

        st.markdown("### 04")

        st.subheader("Compare")

        st.write(
            "Compare the claim with discovered evidence."
        )

    with step5:

        st.markdown("### 05")

        st.subheader("Verdict")

        st.write(
            "Present an evidence-backed assessment."
        )

    st.write("")
    st.divider()

    st.header("Why evidence matters")

    left, right = st.columns([1, 1])

    with left:

        with st.container(border=True):

            st.subheader("❌ A simple classifier")

            st.write(
                "News article"
            )

            st.write("↓")

            st.write(
                "Model prediction"
            )

            st.write("↓")

            st.error(
                "Fake / Real"
            )

            st.caption(
                "A prediction alone does not explain whether "
                "the underlying claim is actually supported."
            )

    with right:

        with st.container(border=True):

            st.subheader("✅ Verifi approach")

            st.write(
                "News article"
            )

            st.write("↓")

            st.write(
                "Claim + context"
            )

            st.write("↓")

            st.write(
                "Relevant evidence"
            )

            st.write("↓")

            st.success(
                "Evidence-backed verdict"
            )

            st.caption(
                "The result is accompanied by the evidence and "
                "reasoning used during verification."
            )

    st.write("")
    st.divider()

    st.header("Technology stack")

    tabs = st.tabs([
        "🤖 AI / NLP",
        "📷 OCR",
        "🌐 Verification",
        "🖥️ Application"
    ])

    with tabs[0]:

        st.subheader("AI & NLP")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info("Transformers")

        with c2:
            st.info("Sentence Transformers")

        with c3:
            st.info("Scikit-learn")

    with tabs[1]:

        st.subheader("Image Processing")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info("OCR")

        with c2:
            st.info("Image preprocessing")

        with c3:
            st.info("Text extraction")

    with tabs[2]:

        st.subheader("Evidence & Verification")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info("Trusted news sources")

        with c2:
            st.info("Official sources")

        with c3:
            st.info("Semantic similarity")

    with tabs[3]:

        st.subheader("Application")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.info("Python")

        with c2:
            st.info("Streamlit")

        with c3:
            st.info("Modular architecture")

    st.write("")
    st.divider()

    st.header("Ready to verify a claim?")

    st.write(
        "Don't trust a headline blindly. Submit the news and "
        "let Verifi investigate the evidence."
    )

    st.write("")

    if st.button(
        "🔍 Start Verification",
        type="primary",
        use_container_width=True
    ):

        st.session_state.navigation  = "Verify News"
        st.rerun()
