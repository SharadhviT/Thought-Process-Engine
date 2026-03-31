import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Thought Process Reconstruction Engine", layout="wide")

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
st.sidebar.header("📥 Enter / Edit Student Data")

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
# Initialize session state
# -------------------------------
if "data" not in st.session_state:
    st.session_state.data = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

# -------------------------------
# Add / Edit Student
# -------------------------------
if st.sidebar.button(" Add / Update Student"):
    category, emoji, confidence = analyze(steps, correct_steps, student_answer, correct_answer)
    
    student_record = {
        "Name": student_name,
        "Steps": steps,
        "Final Answer": student_answer,
        "Time": time_taken,
        "Category": category,
        "Confidence": confidence
    }

    if st.session_state.edit_index is not None:
        st.session_state.data[st.session_state.edit_index] = student_record
        st.session_state.edit_index = None
        st.success(f" Student {student_name} updated")
    else:
        st.session_state.data.append(student_record)
        st.success(f"{emoji} {student_name} classified as: {category} (Confidence: {confidence})")

# -------------------------------
# Clear all data
# -------------------------------
if st.sidebar.button("🗑️ Clear All Data"):
    st.session_state.data = []
    st.session_state.edit_index = None
    st.experimental_rerun()

# -------------------------------
# Display Student Data
# -------------------------------
if st.session_state.data:
    st.subheader(" Student Analysis Data")
    
    df = pd.DataFrame(st.session_state.data)
    
    # Edit and Delete buttons
    for i, row in df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,2,1,1])
        col1.write(row["Name"])
        col2.write(row["Category"])
        col3.write(row["Confidence"])
        col4.write(row["Time"])
        col5.button("✏️", key=f"edit_{i}", on_click=lambda i=i: edit_student(i))
        col6.button("❌", key=f"delete_{i}", on_click=lambda i=i: delete_student(i))
    
    # Visualization
  
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Thinking Pattern Distribution")
        counts = df["Category"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
        st.pyplot(fig)
        
    with col2:
        st.subheader(" Time vs Confidence")
        fig2, ax2 = plt.subplots()
        ax2.scatter(df["Time"], df["Confidence"])
        ax2.set_xlabel("Time (minutes)")
        ax2.set_ylabel("Confidence")
        st.pyplot(fig2)
    

    # Download CSV
   
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Download Data as CSV",
        data=csv,
        file_name='student_analysis.csv',
        mime='text/csv'
    )


# Functions

def edit_student(index):
    student = st.session_state.data[index]
    st.session_state.edit_index = index
    st.session_state.student_name = student["Name"]
    st.session_state.student_steps = student["Steps"]
    st.session_state.student_answer = student["Final Answer"]
    st.session_state.student_time = student["Time"]
    st.experimental_rerun()

def delete_student(index):
    st.session_state.data.pop(index)
    st.experimental_rerun()
