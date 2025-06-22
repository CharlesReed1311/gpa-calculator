import streamlit as st
import json
import functions

# --- Reset state before rendering if triggered ---
if st.session_state.get("_reset_trigger", False):
    functions.sgpa_reset_all()

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>SGPA Calculator</h1>", unsafe_allow_html=True)

# --- Load grade mapping from JSON ---
with open("grademap.json", "r") as f:
    grade_points = json.load(f)

gradelist = list(grade_points.keys())

# --- Initialize session state ---
if "courses" not in st.session_state:
    st.session_state.courses = [0, 1, 2, 3, 4]

# --- Calculate SGPA ---
sgpa = functions.calculate_sgpa(st.session_state.courses, grade_points)
st.markdown(
    f"<p style='text-align: center; font-size: 3rem; color: #1f77b4; font-weight: bold;'>{sgpa if sgpa is not None else 0}</p>",
    unsafe_allow_html=True
)

# --- Column headers ---
st.markdown("""
<style>
@media (max-width: 768px) {
    .header-row {
        flex-direction: column;
        align-items: center;
    }
    .header-row > div {
        width: 100% !important;
        margin-bottom: 0.5rem;
    }
}
</style>

<div class="header-row" style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
    <div style='width: 25%; text-align: center;'><h3 style='margin: 0;'>Course</h3></div>
    <div style='width: 35%; text-align: center;'><h3 style='margin: 0;'>Credits</h3></div>
    <div style='width: 35%; text-align: center;'><h3 style='margin: 0;'>Grade</h3></div>
    <div style='width: 5%; text-align: center;'><h3 style='margin: 0;'>&nbsp;</h3></div>
</div>
""", unsafe_allow_html=True)

# --- Input Rows ---
for course_id in st.session_state.courses:
    cols = st.columns([2, 3, 3, 1])
    
    with cols[0]:
        st.markdown(
            f"<p style='text-align: center; font-weight: bold; font-size: 1.2rem;'>{st.session_state.courses.index(course_id)+1}.</p>",
            unsafe_allow_html=True
        )
    with cols[1]:
        st.number_input("Credits", key=f"credits_{course_id}", min_value=0, step=1, label_visibility="collapsed")
    with cols[2]:
        st.selectbox("Grade", options=gradelist, key=f"grade_{course_id}", label_visibility="collapsed")
    with cols[3]:
        if st.button("Delete", key=f"delete_{course_id}"):
            functions.delete_course(course_id)

# --- Total Credits ---
total_credits = functions.calculate_total_credits(st.session_state.courses)
st.markdown(
    f"<p style='text-align: center; font-size: 1.2rem; color: gray;'>Total Credits: {total_credits}</p>",
    unsafe_allow_html=True
)

if st.button("Add Course"):
    functions.add_course()

if st.button("Reset All"):
    functions.trigger_reset()
