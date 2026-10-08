import streamlit as st
import pandas as pd

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("🎓 Student Score Analyzer")

st.write("Enter student scores and analyze their performance.")


# -----------------------------
# GRADE FUNCTION
# -----------------------------

def get_grade(score):

    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    elif score >= 40:
        return "E"
    else:
        return "F"


# -----------------------------
# STORE STUDENTS
# -----------------------------

if "students" not in st.session_state:
    st.session_state.students = {}


# -----------------------------
# INPUT SECTION
# -----------------------------

st.subheader("Add Student")

name = st.text_input("Student Name")

score = st.number_input(
    "Student Score",
    min_value=0,
    max_value=100,
    step=1
)


# -----------------------------
# ADD STUDENT
# -----------------------------

if st.button("Add Student"):

    if name.strip() == "":
        st.warning("Please enter a student name.")

    elif name in st.session_state.students:
        st.warning("This student has already been added.")

    else:
        st.session_state.students[name] = score
        st.success(f"{name} added successfully!")


# -----------------------------
# ANALYSIS SECTION
# -----------------------------

if st.session_state.students:

    st.subheader("📋 Student Scores")

    # Convert dictionary to DataFrame
    data = pd.DataFrame(
        list(st.session_state.students.items()),
        columns=["Student", "Score"]
    )

    # Add grades
    data["Grade"] = data["Score"].apply(get_grade)

    # Add pass/fail status
    data["Status"] = data["Score"].apply(
        lambda score: "Pass" if score >= 40 else "Fail"
    )

    # Display table
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


    # -----------------------------
    # CALCULATE RESULTS
    # -----------------------------

    average_score = (
        sum(st.session_state.students.values())
        / len(st.session_state.students)
    )

    highest_student = max(
        st.session_state.students,
        key=st.session_state.students.get
    )

    lowest_student = min(
        st.session_state.students,
        key=st.session_state.students.get
    )


    # -----------------------------
    # RESULTS
    # -----------------------------

    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Score",
            f"{average_score:.2f}"
        )

    with col2:
        st.metric(
            "Highest Score",
            st.session_state.students[highest_student]
        )
        st.caption(highest_student)

    with col3:
        st.metric(
            "Lowest Score",
            st.session_state.students[lowest_student]
        )
        st.caption(lowest_student)


    # -----------------------------
    # CLASS SUMMARY
    # -----------------------------

    passed_students = sum(data["Status"] == "Pass")
    failed_students = sum(data["Status"] == "Fail")

    st.subheader("📚 Class Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Students Passed",
            passed_students
        )

    with col2:
        st.metric(
            "Students Failed",
            failed_students
        )


    # -----------------------------
    # PERFORMANCE CHART
    # -----------------------------

    st.subheader("📈 Student Performance")

    chart_data = data.set_index("Student")[["Score"]]

    st.bar_chart(chart_data)


    # -----------------------------
    # CLEAR ALL STUDENTS
    # -----------------------------

    if st.button("🗑️ Clear All Students"):

        st.session_state.students = {}

        st.rerun()