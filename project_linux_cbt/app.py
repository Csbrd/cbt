import streamlit as st
from logic import QuizGenerator
import os
from dotenv import load_dotenv

load_dotenv()

# 객체 생성
quiz_tool = QuizGenerator(os.getenv("NOTION_TOKEN"), os.getenv("GEMINI_API_KEY"))

st.title("🐧 My Linux CBT Study")

if "quizzes" not in st.session_state:
    st.session_state.quizzes = None

if st.button("노션에서 새로운 문제 가져오기"):
    with st.spinner("문제를 생성 중입니다..."):
        content = quiz_tool.get_notion_text(os.getenv("NOTION_PAGE_ID"))
        st.session_state.quizzes = quiz_tool.create_quizzes(content)
        st.rerun()

# [핵심 수정] 문제가 있을 때만 렌더링
if st.session_state.quizzes:
    for i, q in enumerate(st.session_state.quizzes):
        with st.container(border=True):
            st.write(f"**Q{i+1}. {q['question']}**")
            
            # key를 다르게 주어 각 문제의 선택지를 독립적으로 관리
            choice = st.radio("보기 선택", q['options'], key=f"ans_{i}")
            
            # 버튼 클릭 시에만 결과를 보여줌으로써 NameError 방지
            if st.button("정답 확인", key=f"check_{i}"):
                if q['answer'].strip() in choice.strip() or choice.strip() in q['answer'].strip():
                    st.success("정답입니다!")
                else:
                    st.error(f"오답입니다. 정답은 {q['answer']}입니다.")
            
            if st.button("AI 해설 보기", key=f"expl_{i}"):
                with st.spinner("해설 작성 중..."):
                    res = quiz_tool.model.generate_content(f"문제: {q['question']}, 정답: {q['answer']}. 이 내용에 대해 설명해줘.")
                    st.info(res.text)