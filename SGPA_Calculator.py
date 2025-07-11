import streamlit as st
import json
import functions

# --- Reset state before rendering if triggered ---
if st.session_state.get("_reset_trigger", False):
    functions.sgpa_reset_all()

st.set_page_config(layout="wide", page_title="SGPA Calculator")

st.markdown("<h1 style='text-align: center;'>SGPA Calculator</h1>", unsafe_allow_html=True)

# --- Load grade mapping from JSON ---
with open("grademap.json", "r") as f:
    grade_points = json.load(f)

gradelist = list(grade_points.keys())

# --- Initialize session state ---
if "courses" not in st.session_state:
    st.session_state.courses = [0, 1, 2, 3, 4]

# --- Input Rows (Unified layout with vertical labels, no headers) ---
for i, course_id in enumerate(st.session_state.courses):
    st.markdown(
        f"<h3 style='text-align:center; font-size: 1.5rem; margin-bottom: 0.5rem;'>Course {i + 1}</h3>",
        unsafe_allow_html=True
    )
    st.number_input("Credits", key=f"credits_{course_id}", min_value=0, step=1)
    st.selectbox("Grade", options=gradelist, key=f"grade_{course_id}")
    if st.button("Delete Course", key=f"delete_{course_id}"):
        functions.delete_course(course_id)
    st.markdown("<hr>", unsafe_allow_html=True)  # Optional divider

# --- Add Course Button ---
if st.button("Add Course"):
    functions.add_course()

# --- SGPA Result ---
sgpa = functions.calculate_sgpa(st.session_state.courses, grade_points)
st.markdown(
    f"<p style='text-align: center; font-size: 3rem; color: #1f77b4; font-weight: bold;'>SGPA: {sgpa if sgpa is not None else 0}</p>",
    unsafe_allow_html=True
)

# --- Total Credits Display ---
total_credits = functions.calculate_total_credits(st.session_state.courses)
st.markdown(
    f"<p style='text-align: center; font-size: 1.2rem; color: gray;'>Total Credits: {total_credits}</p>",
    unsafe_allow_html=True
)

# --- Reset Button ---
if st.button("Reset All"):
    functions.trigger_reset()
