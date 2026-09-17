
import streamlit as st
from huggingface_hub import InferenceClient

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MCQ Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #f5f7fb;
    }

    /* Header */
    .main-header {
        text-align: center;
        padding: 25px 10px 10px 10px;
    }

    .main-header h1 {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .main-header p {
        font-size: 17px;
        color: #6b7280;
    }

    /* Cards */
    .card {
        background: white;
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
    }

    /* Section title */
    .section-title {
        font-size: 22px;
        font-weight: 650;
        margin-bottom: 15px;
    }

    /* Generate button */
    div.stButton > button {
        width: 100%;
        height: 48px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
    }

    /* Result box */
    .result-box {
        background: white;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        padding: 30px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<div class="main-header">
    <h1>📝 MCQ Generator</h1>
    <p>Generate intelligent multiple-choice questions using Large Language Models</p>
</div>
""", unsafe_allow_html=True)

st.write("")


# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns([2.2, 1])

with col1:
    st.markdown("""
    <div class="card">
        <div class="section-title">📚 Enter Your Topic</div>
    """, unsafe_allow_html=True)

    topic = st.text_area(
        "Topic",
        placeholder="Example: Artificial Intelligence, Python, DBMS, Machine Learning...",
        height=150,
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)


with col2:
    st.markdown("""
    <div class="card">
        <div class="section-title">⚙️ Quiz Settings</div>
    """, unsafe_allow_html=True)

    num_questions = st.selectbox(
        "Number of Questions",
        [5, 6, 7, 8, 9, 10],
        index=0
    )

    st.info(
        "💡 Choose the number of questions you want the AI to generate."
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- GENERATE BUTTON ----------------
st.markdown("""
<div class="card">
""", unsafe_allow_html=True)

generate = st.button("✨ Generate MCQs")

st.markdown("</div>", unsafe_allow_html=True)


# ---------------- GENERATION ----------------
if generate:

    if not topic.strip():
        st.warning("⚠️ Please enter a topic before generating questions.")

    else:

        try:
            with st.spinner("🤖 AI is generating your MCQs..."):

                client = InferenceClient(
                    provider="auto",
                    api_key=st.secrets["Access_Token"]
                )

                prompt = f"""
You are an expert educational question generator.

Generate exactly {num_questions} multiple-choice questions
on the following topic:

{topic}

For every question:

- Number the question.
- Provide exactly four options.
- Label them A, B, C, and D.
- Provide the correct answer.
- Keep the questions clear, educational, and suitable for students.
- Avoid duplicate questions.

Use this format:

Question 1: [Question]

A) [Option]
B) [Option]
C) [Option]
D) [Option]

Correct Answer: [Letter and answer]

Repeat the same format for all {num_questions} questions.
"""

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=2500
                )

                result = response.choices[0].message.content

            # ---------------- RESULTS ----------------
            st.markdown("""
            <div class="result-box">
            """, unsafe_allow_html=True)

            st.markdown("## 🎯 Generated MCQs")
            st.caption(
                f"Topic: {topic}  •  Questions: {num_questions}"
            )

            st.markdown("---")

            st.markdown(result)

            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:

            st.error(
                "❌ Something went wrong while generating the questions."
            )

            st.code(str(e))


# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <p>📝 MCQ Generator • Powered by AI & Large Language Models</p>
</div>
""", unsafe_allow_html=True)

