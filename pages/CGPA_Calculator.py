import streamlit as st
import functions

# --- Reset state before rendering if triggered ---
if st.session_state.get("_reset_trigger", False):
    functions.cgpa_reset_all()

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>CGPA Calculator</h1>", unsafe_allow_html=True)

# --- JavaScript to detect screen width and update URL query params ---
st.markdown("""
<script>
const params = new URLSearchParams(window.location.search);
params.set('width', window.innerWidth);
const newUrl = `${window.location.pathname}?${params.toString()}`;
window.history.replaceState({}, '', newUrl);
</script>
""", unsafe_allow_html=True)

# --- Get screen width from query params ---
screen_width = int(st.query_params.get("width", [1080])[0])

# --- Initialize session state ---
if "semesters" not in st.session_state:
    st.session_state.semesters = [0, 1]

# --- Calculate CGPA ---
cgpa = functions.calculate_cgpa(st.session_state.semesters)
st.markdown(
    f"<p style='text-align: center; font-size: 3rem; color: #1f77b4; font-weight: bold;'>{cgpa if cgpa is not None else 0}</p>",
    unsafe_allow_html=True
)

# --- Desktop Layout ---
if screen_width >= 769:
    st.markdown("""
    <div style='display: flex; justify-content: space-around; margin-bottom: 1rem;'>
        <div style='width: 25%; text-align: center;'><h3 style='margin: 0;'>Semester</h3></div>
        <div style='width: 35%; text-align: center;'><h3 style='margin: 0;'>Credits</h3></div>
        <div style='width: 35%; text-align: center;'><h3 style='margin: 0;'>GPA</h3></div>
        <div style='width: 5%; text-align: center;'><h3 style='margin: 0;'>&nbsp;</h3></div>
    </div>
    """, unsafe_allow_html=True)

    for i, semester_id in enumerate(st.session_state.semesters):
        cols = st.columns([2, 3, 3, 1])
        with cols[0]:
            st.markdown(
            f"<p style='text-align: center; font-weight: bold; font-size: 1.5rem;'>{i + 1}.</p>",
            unsafe_allow_html=True
            )

        with cols[1]:
            st.number_input("Credits", key=f"credits_{semester_id}", min_value=0, step=1, label_visibility="collapsed")
        with cols[2]:
            st.number_input("GPA", key=f"gpa_{semester_id}", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed")
        with cols[3]:
            if st.button("Delete", key=f"delete_{semester_id}"):
                functions.delete_semester(semester_id)
    with cols[0]:
        if st.button("Add Semester"):
            functions.add_semester()
    with cols[3]:
        if st.button("Reset All"):
            functions.trigger_reset()
# --- Mobile Layout ---
else:
    for i, semester_id in enumerate(st.session_state.semesters):
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>Semester {i + 1}</p>", unsafe_allow_html=True)
        st.number_input(f"Credits Earned", key=f"credits_{semester_id}", min_value=0, step=1)
        st.number_input(f"GPA", key=f"gpa_{semester_id}", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Delete", key=f"delete_{semester_id}"):
            functions.delete_semester(semester_id)

    # --- Add and Reset buttons ---
    col_left, col_right = st.columns(2)
    with col_left:
        if st.button("Add Semester"):
            functions.add_semester()

    with col_right:
        if st.button("Reset All"):
            functions.trigger_reset()
