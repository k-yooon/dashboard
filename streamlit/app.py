import streamlit as st
import os

st.sidebar.title("📊 대시보드 리스트")

APPS_DIR = "apps"
apps = [f for f in os.listdir(APPS_DIR) if f.endswith(".py")]

app_selection = st.sidebar.selectbox("대시보드를 선택하세요", apps)

if app_selection:
    app_path = os.path.join(APPS_DIR, app_selection)
    with open(app_path, 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code, globals())
