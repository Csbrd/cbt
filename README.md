# Streamlit을 활용한 Linux CBT
- 노션에 정리한 리눅스 학습 노트를 바탕으로, `Gemini AI`가 실시간으로 문제를 생성 해주는 학습 애플리케이션이다.
- 리눅스 마스터 자격증을 따기 위해 만들어 봤다.

## 주요 기능
- **Notion API 연동**: 사용자가 노션 페이지에 정리한 텍스트 데이터를 실시간으로 수집한다.
- **AI 문제 생성**: `Gemini 2.5 Flash` 모델을 활용하여 학습 콘텐츠에 어울리는 객관식 퀴즈를 만들어 준다.
- **실시간 채점 및 해설**: 사용자가 선택한 답안을 즉시 채점할 수 있고, 틀린 문제에 대한 해설을 확인할 수 있다.
- **Streamlit UI**: 별도의 프론트엔드 구축 없이 파이썬만으로 깔끔한 웹 인터페이스를 구현했다.
- 
## 구성 환경
- **Language**: Python3.8+
- **Framework**: Streamlit
- **AI Engine**: Google Gemini API(`google-genrativeai`)
- **Data Source**: Notion API

## 파일 구조
- `app.py`: Streamlit 웹 UI 구성 및 세션 관리
- `logic.py`: Notion 데이터 추출 및 Gemini 문제 생성 로직
- `.env`: API 키 등 민감 정보 저장

## 시작하기
### NOTION_TOKEN 발급
[링크]https://www.notion.so/profile/integrations
### GEMINI_API 발급
[링크]https://aistudio.google.com
### 라이브러리 설치
`pip install streamlit google-generativeai requests`
### .env 파일 설정
`cp ./20260205/.env.example ./20260205/.env`로 복사 후 `.env`파일 수정
### 실행하기
`app.py`파일에서 `streamlit run app.py`로 실행
