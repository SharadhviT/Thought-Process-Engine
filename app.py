import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Thought Process Engine", layout="wide")

st.title("🧠 Thought Process Reconstruction Engine")
st.markdown("### Modeling student reasoning beyond final answers")

# -------------------------------
# Reference Solution
# -------------------------------
correct_steps = [
    "identify formula",
    "substitute values",
    "simplify equation",
    "calculate final answer"
]

correct_answer = "42"

# -------------------------------
# Sidebar Input
# -------------------------------
st.sidebar.header("📥 Enter Student Data")

student_name = st.sidebar.text_input("Student Name")

steps = []
for i in range(4):
    step = st.sidebar.text_input(f"Step {i+1}")
    steps.append(step.lower())

student_answer = st.sidebar.text_input("Final Answer")
time_taken = st.sidebar.slider("Time Taken (minutes)", 1, 30, 5)

# -------------------------------
# Analysis Function
# -------------------------------
def analyze(student_steps, correct_steps, student_answer, correct_answer):
    score = 0
    changes = 0

    for i in range(len(correct_steps)):
        if i < len(student_steps) and student_steps[i] == correct_steps[i]:
            score += 1
        else:
            changes += 1

    answer_correct = (student_answer == correct_answer)
    confidence = round(score / len(correct_steps), 2)

    # Classification logic
    if score == len(correct_steps) and answer_correct:
        category = "Structured Thinker"
        emoji = "🟢"

    elif score >= len(correct_steps) - 1 and not answer_correct:
        category = "Execution Error"
        emoji = "🟣"

    elif changes > 2:
        category = "Trial-and-Error"
        emoji = "🟡"

    elif score <= 1:
        category = "Conceptual Gap"
        emoji = "🔵"

    elif score >= 2 and changes >= 1:
        category = "Overthinking"
        emoji = "🔴"

    else:
        category = "Mixed Pattern"
        emoji = "⚪"

    return category, emoji, confidence


# -------------------------------
# Store Data
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# -------------------------------
# Run Analysis
# -------------------------------
if st.sidebar.button("Analyze Student"):

    category, emoji, confidence = analyze(
        steps, correct_steps, student_answer, correct_answer
    )

    st.session_state.data.append({
        "Name": student_name,
        "Category": category,
        "Confidence": confidence,
        "Time": time_taken
    })

    st.success(f"{emoji} {student_name} classified as: {category}")
    st.info(f"Confidence Score: {confidence}")

# -------------------------------
# Display Results
# -------------------------------
if st.session_state.data:

    df = pd.DataFrame(st.session_state.data)

    st.subheader("Student Analysis Data")
    st.dataframe(df)

    col1, col2 = st.columns(2)

    # -------------------------------
    # Pie Chart
    # -------------------------------
    with col1:
        st.subheader(" Thinking Pattern Distribution")
        counts = df["Category"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # -------------------------------
    # Time vs Confidence
    # -------------------------------
    with col2:
        st.subheader("⏱️ Time vs Confidence")
        fig2, ax2 = plt.subplots()
        ax2.scatter(df["Time"], df["Confidence"])
        ax2.set_xlabel("Time (minutes)")
        ax2.set_ylabel("Confidence")
        st.pyplot(fig2)

    # -------------------------------
    # Insights
    # -------------------------------
    st.subheader(" Key Insights")

    most_common = df["Category"].value_counts().idxmax()
    avg_time = round(df["Time"].mean(), 2)
    avg_conf = round(df["Confidence"].mean(), 2)

    st.markdown(f"""
    - **Most common thinking pattern:** {most_common}  
    - **Average time taken:** {avg_time} minutes  
    - **Average confidence score:** {avg_conf}  
    """)

    st.subheader(" Interpretation Guide")
    st.markdown("""
    - 🟢 Structured Thinker → Clear logical reasoning  
    - 🟡 Trial-and-Error → Lack of planning  
    - 🔵 Conceptual Gap → Weak understanding  
    - 🔴 Overthinking → Inefficient strategy  
    - 🟣 Execution Error → Minor mistakes despite understanding  
    """)

else:
    st.info(" Enter student data from the sidebar to begin analysis.")
