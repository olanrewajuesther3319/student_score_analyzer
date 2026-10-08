import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Score Analyzer",
    page_icon=None,
    layout="wide"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 18px;
            color: #666666;
            margin-bottom: 30px;
        }

        .section-title {
            font-size: 25px;
            font-weight: 600;
            margin-top: 25px;
            margin-bottom: 15px;
        }

        .footer {
            text-align: center;
            color: #777777;
            font-size: 14px;
            padding: 30px 0 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Student Score Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze student performance, grades, rankings, and class results.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("About")

    st.write(
        "Student Score Analyzer is a simple academic analytics "
        "tool designed to help teachers understand student "
        "performance and make data-driven decisions."
    )

    st.divider()

    st.subheader("Technologies")

    st.write("Python")
    st.write("Pandas")
    st.write("Streamlit")

    st.divider()

    st.subheader("Features")

    st.write("• Student score management")
    st.write("• Automatic grading")
    st.write("• Student ranking")
    st.write("• Class performance analysis")
    st.write("• Individual student analysis")
    st.write("• Performance insights")
    st.write("• CSV results download")


# ============================================================
# GRADE FUNCTION
# ============================================================

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


# ============================================================
# SESSION STATE
# ============================================================

if "students" not in st.session_state:
    st.session_state.students = {}


# ============================================================
# ADD STUDENT
# ============================================================

st.markdown(
    '<div class="section-title">Add Student</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

with col2:

    math_score = st.number_input(
        "Mathematics Score",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )


col3, col4 = st.columns(2)

with col3:

    english_score = st.number_input(
        "English Score",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )

with col4:

    biology_score = st.number_input(
        "Biology Score",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )


# ============================================================
# ADD STUDENT BUTTON
# ============================================================

if st.button("Add Student", type="primary"):

    cleaned_name = " ".join(name.strip().split())

    if cleaned_name == "":

        st.warning("Please enter a student name.")

    else:

        # Make student names case-insensitive
        existing_names = [
            student.lower()
            for student in st.session_state.students.keys()
        ]

        if cleaned_name.lower() in existing_names:

            st.warning(
                "This student has already been added."
            )

        else:

            st.session_state.students[cleaned_name] = {
                "Mathematics": math_score,
                "English": english_score,
                "Biology": biology_score
            }

            st.success(
                f"{cleaned_name} added successfully!"
            )


# ============================================================
# ANALYSIS
# ============================================================

if st.session_state.students:

    # --------------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------------

    data = pd.DataFrame.from_dict(
        st.session_state.students,
        orient="index"
    )

    data.index.name = "Student"

    data = data.reset_index()


    # --------------------------------------------------------
    # SUBJECTS
    # --------------------------------------------------------

    subjects = [
        "Mathematics",
        "English",
        "Biology"
    ]


    # --------------------------------------------------------
    # CALCULATE AVERAGE
    # --------------------------------------------------------

    data["Average"] = data[subjects].mean(axis=1)


    # --------------------------------------------------------
    # GRADE
    # --------------------------------------------------------

    data["Grade"] = data["Average"].apply(
        get_grade
    )


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    data["Status"] = data["Average"].apply(
        lambda score:
        "Pass" if score >= 40 else "Fail"
    )


    # --------------------------------------------------------
    # RANK
    # --------------------------------------------------------

    data["Rank"] = (
        data["Average"]
        .rank(
            ascending=False,
            method="min"
        )
        .astype(int)
    )


    # --------------------------------------------------------
    # ROUND AVERAGE
    # --------------------------------------------------------

    data["Average"] = data["Average"].round(2)


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    data = data.sort_values(
        "Rank"
    )


    # ========================================================
    # STUDENT TABLE
    # ========================================================

    st.markdown(
        '<div class="section-title">Student Performance</div>',
        unsafe_allow_html=True
    )

    display_columns = [
        "Rank",
        "Student",
        "Mathematics",
        "English",
        "Biology",
        "Average",
        "Grade",
        "Status"
    ]

    st.dataframe(
        data[display_columns],
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # INDIVIDUAL STUDENT ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Individual Student Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    selected_student = st.selectbox(
        "Select a student",
        data["Student"].tolist()
    )


    student_data = data[
        data["Student"] == selected_student
    ].iloc[0]


    # --------------------------------------------------------
    # STUDENT METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Average",
            f"{student_data['Average']:.2f}"
        )

    with col2:

        st.metric(
            "Grade",
            student_data["Grade"]
        )

    with col3:

        st.metric(
            "Rank",
            int(student_data["Rank"])
        )

    with col4:

        st.metric(
            "Status",
            student_data["Status"]
        )


    # --------------------------------------------------------
    # STUDENT SUBJECT SCORES
    # --------------------------------------------------------

    student_scores = pd.DataFrame(
        {
            "Subject": subjects,
            "Score": [
                student_data["Mathematics"],
                student_data["English"],
                student_data["Biology"]
            ]
        }
    )


    st.write(
        f"**{selected_student}'s Subject Scores**"
    )

    st.bar_chart(
        student_scores.set_index("Subject")
    )


    # --------------------------------------------------------
    # BEST / WEAKEST SUBJECT
    # --------------------------------------------------------

    best_subject = student_scores.loc[
        student_scores["Score"].idxmax(),
        "Subject"
    ]

    best_score = student_scores["Score"].max()


    weakest_subject = student_scores.loc[
        student_scores["Score"].idxmin(),
        "Subject"
    ]

    weakest_score = student_scores["Score"].min()


    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"Best Subject: **{best_subject}** "
            f"({best_score}/100)"
        )

    with col2:

        st.warning(
            f"Needs Improvement: **{weakest_subject}** "
            f"({weakest_score}/100)"
        )


    # ========================================================
    # CLASS RESULTS
    # ========================================================

    st.markdown(
        '<div class="section-title">Class Results</div>',
        unsafe_allow_html=True
    )


    class_average = data["Average"].mean()


    highest_student = data.loc[
        data["Average"].idxmax(),
        "Student"
    ]

    highest_score = data["Average"].max()


    lowest_student = data.loc[
        data["Average"].idxmin(),
        "Student"
    ]

    lowest_score = data["Average"].min()


    passed_students = (
        data["Status"] == "Pass"
    ).sum()


    failed_students = (
        data["Status"] == "Fail"
    ).sum()


    total_students = len(data)


    pass_rate = (
        passed_students / total_students
    ) * 100


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Class Average",
            f"{class_average:.2f}"
        )

    with col2:

        st.metric(
            "Highest Average",
            f"{highest_score:.2f}"
        )

        st.caption(
            highest_student
        )

    with col3:

        st.metric(
            "Students Passed",
            passed_students
        )

    with col4:

        st.metric(
            "Pass Rate",
            f"{pass_rate:.1f}%"
        )


    # ========================================================
    # TOP STUDENTS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Top Performing Students'
        '</div>',
        unsafe_allow_html=True
    )


    top_students = data[
        data["Rank"] <= 3
    ][
        [
            "Rank",
            "Student",
            "Average",
            "Grade"
        ]
    ]


    st.dataframe(
        top_students,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # SUBJECT PERFORMANCE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Subject Performance'
        '</div>',
        unsafe_allow_html=True
    )


    subject_averages = (
        data[subjects]
        .mean()
        .round(2)
    )


    st.bar_chart(
        subject_averages
    )


    # ========================================================
    # CLASS STUDENT AVERAGES
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Student Average Scores'
        '</div>',
        unsafe_allow_html=True
    )


    chart_data = (
        data
        .set_index("Student")[["Average"]]
    )


    st.bar_chart(
        chart_data
    )


    # ========================================================
    # GRADE DISTRIBUTION
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Grade Distribution'
        '</div>',
        unsafe_allow_html=True
    )


    grade_distribution = (
        data["Grade"]
        .value_counts()
        .reindex(
            ["A", "B", "C", "D", "E", "F"],
            fill_value=0
        )
    )


    st.bar_chart(
        grade_distribution
    )


    # ========================================================
    # PERFORMANCE INSIGHTS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Performance Insights'
        '</div>',
        unsafe_allow_html=True
    )


    best_class_subject = (
        subject_averages.idxmax()
    )

    weakest_class_subject = (
        subject_averages.idxmin()
    )


    st.success(
        f"The class performed best in "
        f"**{best_class_subject}**, with an average score "
        f"of **{subject_averages[best_class_subject]:.2f}**."
    )


    st.warning(
        f"**{weakest_class_subject}** had the lowest class "
        f"average of "
        f"**{subject_averages[weakest_class_subject]:.2f}**."
    )


    if pass_rate >= 70:

        st.success(
            f"The class has a strong overall performance "
            f"with a pass rate of **{pass_rate:.1f}%**."
        )

    elif pass_rate >= 50:

        st.info(
            f"The class has a moderate pass rate of "
            f"**{pass_rate:.1f}%**."
        )

    else:

        st.error(
            f"The class has a low pass rate of "
            f"**{pass_rate:.1f}%**. Additional academic "
            f"support may be needed."
        )


    # ========================================================
    # DOWNLOAD RESULTS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Download Results'
        '</div>',
        unsafe_allow_html=True
    )


    csv_data = data.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="Download Results as CSV",
        data=csv_data,
        file_name="student_results.csv",
        mime="text/csv"
    )


    # ========================================================
    # CLEAR DATA
    # ========================================================

    st.divider()


    if st.button(
        "Clear All Students"
    ):

        st.session_state.students = {}

        st.rerun()


else:

    st.info(
        "Add students above to begin analyzing "
        "class performance."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Student Score Analyzer · Built with Python, Pandas & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)