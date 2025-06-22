import streamlit as st

def add_course():
    new_id = max(st.session_state.courses) + 1 if st.session_state.courses else 0
    st.session_state.courses.append(new_id)
    st.rerun()

def delete_course(course_id):
    if course_id in st.session_state.courses:
        st.session_state.courses.remove(course_id)
    st.rerun()

def trigger_reset():
    st.session_state._reset_trigger = True
    st.rerun()

def sgpa_reset_all():
    # Clear all course inputs
    for key in list(st.session_state.keys()):
        if key.startswith("credits_") or key.startswith("grade_"):
            del st.session_state[key]

    # Reset course list to 4 fresh IDs
    st.session_state.courses = [0, 1, 2, 3, 4]

    # Remove previous flags
    st.session_state.add_course_flag = False
    st.session_state.delete_course_flag = None
    st.session_state._reset_trigger = False

    # Reset course input states to ensure blank fields
    for cid in st.session_state.courses:
        st.session_state[f"credits_{cid}"] = 0
        st.session_state[f"grade_{cid}"] = "-Select a grade-"

    st.rerun()

def calculate_total_credits(courses):
    total_credits = 0

    for course_id in courses:
        course_credits = st.session_state.get(f"credits_{course_id}",0)

        if course_credits > 0:
            total_credits += course_credits

    if total_credits > 0:
        return total_credits
    else:
        return 0
    
def calculate_sgpa(courses, grade_points):
    total_credits = 0
    weighted_sum = 0

    for course_id in courses:
        grade_credits = st.session_state.get(f"credits_{course_id}", 0)
        grade = st.session_state.get(f"grade_{course_id}", None)

        if grade and grade != "-Select a grade-" and grade_credits > 0:
            gp = grade_points.get(grade, 0)
            weighted_sum += gp * grade_credits
            total_credits += grade_credits

    if total_credits > 0:
        raw_gpa = weighted_sum/total_credits
        sgpa = round(raw_gpa, 2)
        return sgpa
    else:
        return None

def calculate_cgpa(semesters):
    total_credits = 0
    total_weighted_gpa = 0

    for semester_id in semesters:
        gpa = st.session_state.get(f"gpa_{semester_id}", 0)
        sem_credits = st.session_state.get(f"credits_{semester_id}", 0)

        if gpa > 0 and sem_credits > 0:
            total_weighted_gpa += gpa * sem_credits
            total_credits += sem_credits

    if total_credits > 0:
        return round(total_weighted_gpa / total_credits, 2)
    return None

def add_semester():
    new_id = max(st.session_state.semesters) + 1 if st.session_state.semesters else 0
    st.session_state.semesters.append(new_id)
    st.rerun()

def delete_semester(semester_id):
    if semester_id in st.session_state.semesters:
        st.session_state.semesters.remove(semester_id)
    st.rerun()

def cgpa_reset_all():
    # Clear semester inputs
    for key in list(st.session_state.keys()):
        if key.startswith("credits_") or key.startswith("gpa_"):
            del st.session_state[key]

    # Reset to 2 default semesters
    st.session_state.semesters = [0, 1]

    # Clear flags
    st.session_state._reset_trigger = False

    for sid in st.session_state.semesters:
        st.session_state[f"credits_{sid}"] = 0
        st.session_state[f"gpa_{sid}"] = 0.00

    st.rerun()
