import streamlit as st
import functions

# --- Reset state before rendering if triggered ---
if st.session_state.get("_reset_trigger", False):
    functions.cgpa_reset_all()

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>CGPA Calculator</h1>", unsafe_allow_html=True)

# --- Initialize session state ---
if "semesters" not in st.session_state:
    st.session_state.semesters = [0, 1]

# --- Input Rows (Simplified, No Borders) ---
for i, semester_id in enumerate(st.session_state.semesters):
    st.markdown(
        f"<h3 style='text-align:center; font-size: 1.5rem; margin-bottom: 0.5rem;'>Semester {i + 1}</h3>",
        unsafe_allow_html=True
    )
    st.number_input("Credits Earned", key=f"credits_{semester_id}", min_value=0, step=1)
    st.number_input("GPA", key=f"gpa_{semester_id}", min_value=0.0, step=0.01, format="%.2f")
    if st.button("Delete semester", key=f"delete_{semester_id}"):
        functions.delete_semester(semester_id)
    st.markdown("<hr>", unsafe_allow_html=True)  # optional divider
# --- Calculate CGPA ---
cgpa = functions.calculate_cgpa(st.session_state.semesters)
st.markdown(
    f"<p style='text-align: center; font-size: 3rem; color: #1f77b4; font-weight: bold;'>CGPA: {cgpa if cgpa is not None else 0}</p>",
    unsafe_allow_html=True
)

# --- Add and Reset Buttons ---
if st.button("Add Semester"):
    functions.add_semester()

if st.button("Reset All"):
    functions.trigger_reset()
