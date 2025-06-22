import streamlit as st
import functions

# --- Reset state before rendering if triggered ---
if st.session_state.get("_reset_trigger", False):
    functions.cgpa_reset_all()

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>CGPA Calculator</h1>", unsafe_allow_html=True)

# --- Initialize session state ---
if "semesters" not in st.session_state:
    st.session_state.semesters = [0, 1]  # Start with 2 semesters

# --- Calculate CGPA ---
cgpa = functions.calculate_cgpa(st.session_state.semesters)
st.markdown(
    f"<p style='text-align: center; font-size: 3rem; color: #1f77b4; font-weight: bold;'>{cgpa if cgpa is not None else 0}</p>",
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
    <div style='width: 25%; text-align: center;'><h3 style='margin: 0;'>Semester</h3></div>
    <div style='width: 35%; text-align: center;'><h3 style='margin: 0;'>Credits Earned</h3></div>
    <div style='width: 35%; text-align: center;'><h3 style='margin: 0;'>GPA</h3></div>
    <div style='width: 5%; text-align: center;'><h3 style='margin: 0;'>&nbsp;</h3></div>
</div>
""", unsafe_allow_html=True)

# --- Input Rows ---
for semester_id in st.session_state.semesters:
    cols = st.columns([2, 3, 3, 1])

    with cols[0]:
        st.markdown(
            f"<p style='text-align: center; font-weight: bold; font-size: 1.2rem;'>{st.session_state.semesters.index(semester_id)+1}.</p>",
            unsafe_allow_html=True
        )
    with cols[1]:
        st.number_input("Credits Earned", key=f"credits_{semester_id}", min_value=0, step=1, label_visibility="collapsed")
    with cols[2]:
        st.number_input("GPA", key=f"gpa_{semester_id}", min_value=0.0, max_value=10.0, step=0.01, format="%.2f", label_visibility="collapsed")
    with cols[3]:
        if st.button("Delete", key=f"delete_{semester_id}"):
            functions.delete_semester(semester_id)

# --- Bottom Buttons ---
if st.button("Add Semester"):
    functions.add_semester()

if st.button("Reset All"):
    functions.trigger_reset()
