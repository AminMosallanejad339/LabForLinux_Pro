import streamlit as st
import pandas as pd
import os
import re
import time
from streamlit import session_state as state

# Configure page
st.set_page_config(page_title="Lab", layout="wide", page_icon="🧠")

# Directory containing CSV files
CSV_DIR = os.path.join(os.getcwd(), 'directfolder')
csv_files = [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]

# Initialize session state
state_keys = {
    'current_index': 0,
    'selected_file': None,
    'user_answer': '',
    'wrong_attempts': 0,
    'df': pd.DataFrame(),
    'show_answer': False,
    'dark_mode': False
}

for key, default in state_keys.items():
    if key not in state:
        state[key] = default

# App title and description
st.title("🧠 Linux Practice Lab")
st.markdown("Sharpen your SQL skills with interactive exercises. Use `Ctrl+Enter` to submit your answer.")

# Theme toggle
state.dark_mode = st.toggle("Dark Mode", value=state.dark_mode)
theme = "dark" if state.dark_mode else "light"

# Sidebar for navigation and file selection
with st.sidebar:
    st.header("Navigation")

    # File selection
    selected_file = st.selectbox(
        "📁 Choose a question set:",
        csv_files,
        key="file_selector"
    )

    # Load new CSV file if selection changes
    if selected_file != state.selected_file:
        file_path = os.path.join(CSV_DIR, selected_file)
        state.df = pd.read_csv(file_path, on_bad_lines='skip')
        state.selected_file = selected_file
        state.current_index = 0
        state.user_answer = ''
        state.wrong_attempts = 0
        state.show_answer = False

    # Question navigation
    if len(state.df) > 0:
        question_num = st.number_input(
            "Go to question:",
            min_value=1,
            max_value=len(state.df),
            value=state.current_index + 1,
            key="question_nav"
        )
        if question_num - 1 != state.current_index:
            state.current_index = question_num - 1
            state.user_answer = ''
            state.show_answer = False
            st.rerun()

    st.markdown("### Shortcuts")
    st.markdown("""
    - `Ctrl+Enter`: Submit answer
    - `Alt+a`: Show answer
    - `Alt+n`: Next question
    - `Alt+p`: Previous question
    """)

# Apply theme styles
if theme == "dark":
    st.markdown("""
    <style>
    .stTextArea textarea {background-color: #2d2d2d !important; color: white !important;}
    .stCodeBlock pre {background-color: #1e1e1e !important;}
    </style>
    """, unsafe_allow_html=True)

# Current question data
df = state.df
index = state.current_index
total = len(df) if not df.empty else 0

if total == 0:
    st.warning("No questions available. Please check your CSV files.")
    st.stop()

if index >= total:
    st.success("🎉 You've completed all questions in this set!")
    st.stop()

row = df.iloc[index]

# Progress and navigation
col1, col2, col3 = st.columns([6, 2, 2])
with col1:
    st.progress((index + 1) / total, text=f"Question {index + 1} of {total}")

with col2:
    if st.button("⬅️ Previous", disabled=index == 0):
        state.current_index -= 1
        state.user_answer = ''
        state.show_answer = False
        st.rerun()

with col3:
    if st.button("Next ➡️", disabled=index == total - 1):
        state.current_index += 1
        state.user_answer = ''
        state.show_answer = False
        st.rerun()

# Display question
st.markdown(
    f"""
    <div style='font-family: monospace; font-size: 16px;
                background-color: {"#2d2d2d" if theme == "dark" else "#f0f2f6"};
                color: {"white" if theme == "dark" else "black"};
                padding: 20px; border-radius: 8px; margin: 10px 0;'>
        <h3 style='color: {"#4fc3f7" if theme == "dark" else "#1a5276"}; margin-top: 0;'>📝 Question {index + 1}</h3>
        <p>{row['question']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Normalize SQL function
def normalize_sql(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

# Form for answer submission
with st.form(key="answer_form"):
    user_input = st.text_area(
        "✍️ Your SQL Answer:",
        value=state.user_answer,
        height=180,
        placeholder="Linux Command ...",
        key="answer_area",
        help="Press Ctrl+Enter to submit"
    )

    col1, col2, col3 = st.columns([2, 2, 6])
    with col1:
        submit = st.form_submit_button("✅ Submit", help="Ctrl+Enter")
    with col2:
        if st.form_submit_button("👀 Show Answer", help="Alt+a"):
            state.show_answer = not state.show_answer

# Keyboard shortcuts
js = """
<script>
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        window.parent.document.querySelector('.stButton button').click();
    }
    else if (e.altKey && e.key === 'a') {
        window.parent.document.querySelectorAll('.stButton button')[1].click();
    }
    else if (e.altKey && e.key === 'n') {
        const nextBtn = window.parent.document.querySelectorAll('.stButton button')[3];
        if (!nextBtn.disabled) nextBtn.click();
    }
    else if (e.altKey && e.key === 'p') {
        const prevBtn = window.parent.document.querySelectorAll('.stButton button')[2];
        if (!prevBtn.disabled) prevBtn.click();
    }
});
</script>
"""
st.components.v1.html(js, height=0, width=0)

# Submit logic
if submit:
    state.user_answer = user_input
    user_clean = normalize_sql(user_input)
    correct_clean = normalize_sql(row['answer'])

    if user_clean == correct_clean:
        st.success("✅ Correct! Well done!")
        st.balloons()
        time.sleep(1)
        state.current_index += 1
        state.user_answer = ''
        state.show_answer = False
        state.wrong_attempts = 0
        st.rerun()
    else:
        st.error("❌ Incorrect. Try again.")
        state.wrong_attempts += 1

# Show answer if requested
if state.show_answer:
    st.markdown(
        f"""
        <div style='font-family: monospace; background-color: {"#1e1e1e" if theme == "dark" else "#e8f4f8"};
                    padding: 15px; border-radius: 8px; margin: 10px 0;'>
            <h4 style='color: {"#4fc3f7" if theme == "dark" else "#1a5276"};'>👀 Answer</h4>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code(row['answer'], language='sql')
    st.markdown(f"**Explanation:** {row.get('explanation', 'No explanation available.')}")

# Wrong attempts counter
if state.wrong_attempts > 0:
    st.caption(f"Attempts: {state.wrong_attempts}")
