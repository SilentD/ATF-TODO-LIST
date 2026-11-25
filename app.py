import streamlit as st 
from repositories.todo_repository import TodoRepository 

st.set_page_config(page_title="ATF Cohort 1 - Team TODO Workspace", 
                   page_icon="📝", 
                   layout="centered") 
repo = TodoRepository()
st.title("📝 ATF Project Task Board")
st.caption("Modular Streamlit + MongoDB Warm-Up App")
# --- TASK CREATION FORM ---
with st.form("new_task_form", clear_on_submit=True): 
    col1, col2 = st.columns([3, 1]) 
    with col1: 
        task_title = st.text_input("Task Description", placeholder="e.g. Verify profile progress for team members") 
    with col2:
        category = st.selectbox("Category", ["AI Agents", "Database", "UI/UX", "Security", "Admin/Pitch"]) 
    assignee = st.selectbox("Assignee", ["Final Year CS", "Advanced Diploma CS", "Junior CS", "Honors EE", "Management Eng"]) 
    submitted = st.form_submit_button("Add Task") 
    if submitted and task_title.strip(): 
        repo.create_task(title=task_title.strip(), category=category, assignee=assignee)
        st.success("Task added!")
        st.rerun()
st.divider() 
# --- TASK LIST RENDER --- 
tasks = repo.get_all_tasks() 
if not tasks:
    st.info("No tasks registered yet. Add your first task above!") 
else: 
    for task in tasks: 
        col_check, col_details, col_del = st.columns([0.5, 4, 0.5])
        with col_check: 
            is_done = st.checkbox("", value=task["completed"], key=f"chk {task['_id']}")
            if is_done != task["completed"]: 
                repo.toggle_task(task["_id"], task["completed"]) 
                st.rerun()
        with col_details:
            title_fmt = f"{task['title']}" if task["completed"] else f"{task['title']}"
            st.markdown(f"{title_fmt} `{task['category']}` — Assignee: {task['assignee']}")
            with col_del: 
                if st.button("🗑️", key=f"del {task['_id']}"): 
                    repo.delete_task(task["_id"]) 
                    st.rerun()