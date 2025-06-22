import streamlit as st
import json
import functions

# --- Reset state before rendering if triggered ---
if st.session_state.get("_reset_trigger", False):
    functions.cgpa_reset_all()

st.set_page_config(layout="wide")

# --- App title ---
st.markdown("<h1 style='text-align: center;'>CGPA Calculator</h1>", unsafe_allow_html=True)

# --- Initialize session state ---
if "semesters" not in st.session_state:
    st.session_state.semesters = [0, 1]  # 2 semesters on first load

if "add_semester_flag" not in st.session_state:
    st.session_state.add_semester_flag = False

if "delete_semester_flag" not in st.session_state:
    st.session_state.delete_semester_flag = None

# --- Calculate SGPA ---
cgpa = functions.calculate_cgpa(st.session_state.semesters)

if cgpa is not None:
    st.markdown(
        f"<p style='text-align: center; font-size: 3rem; color: #1f77b4; font-weight: bold;'>{cgpa}</p>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<p style='text-align: center; font-size: 3rem; color: gray; font-weight: bold;'>0</p>",
        unsafe_allow_html=True
    )

# --- Column headers ---
col1, col2, col3, col4 = st.columns([2, 3, 3, 1])

with col1:
    st.markdown("<h3 style='text-align: center;'>Semester</h3>", unsafe_allow_html=True)
with col2:
    st.markdown("<h3 style='text-align: center;'>Total Credits</h3>", unsafe_allow_html=True)
with col3:
    st.markdown("<h3 style='text-align: center;'>GPA</h3>", unsafe_allow_html=True)
with col4:
    st.markdown("<h3 style='text-align: center;'>&nbsp;</h3>", unsafe_allow_html=True)

# --- Input rows ---
if st.session_state.semesters:
    for semester_id in st.session_state.semesters:

        with col1:
            st.markdown(
                f"""
                <div style='text-align: center; margin-top: 0.6rem;'>
                    <p style='font-weight: bold; font-size: 1.2rem;'>{st.session_state.semesters.index(semester_id)+1}.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.number_input("Credits Earned", key=f"credits_{semester_id}", min_value=0, step=1, label_visibility="collapsed")

        with col3:
            st.number_input("GPA", key=f"gpa_{semester_id}", min_value=0.00, step=0.01, label_visibility="collapsed")

        with col4:
            if st.button("Delete", key=f"delete_{semester_id}"):
                st.session_state.delete_semester_flag = semester_id
                functions.delete_semester(semester_id)
                
else:
    st.info("No semesters. Click 'Add semester' to begin.")

# --- Add course button ---
with col1:
    if st.button("Add semester"):
        st.session_state.add_semester_flag = True
        functions.add_semester()

# --- Reset all button ---
with col4:
    if st.button("Reset All"):
        functions.trigger_reset()
