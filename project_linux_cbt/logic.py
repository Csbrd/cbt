import requests
import google.generativeai as genai
import json
import re

class QuizGenerator:
    def __init__(self, notion_token, gemini_key):
        self.notion_headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28"
        }
        genai.configure(api_key=gemini_key)
        
        # [핵심 수정] 사용 가능한 모델 중 'gemini-1.5-flash'가 포함된 모델을 자동으로 찾음
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
        
        self.model = genai.GenerativeModel(target_model)
        print(f"연결된 모델: {target_model}") # 터미널에서 확인용

    def get_notion_text(self, page_id):
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        res = requests.get(url, headers=self.notion_headers)
        blocks = res.json().get("results", [])
        
        content = ""
        for block in blocks:
            b_type = block.get("type")
            if b_type in ["paragraph", "bulleted_list_item"]:
                rich_text = block[b_type].get("rich_text", [])
                content += "".join([t["plain_text"] for t in rich_text]) + "\n"
        return content

    def create_quizzes(self, context):
        # 중괄호 에러 방지를 위해 f-string 대신 .format() 또는 직접 결합 사용
        prompt = """
        당신은 리눅스 전문가입니다. 다음 내용을 바탕으로 CBT 객관식 문제 3개를 생성하세요.
        응답은 반드시 마크다운 기호 없이 순수 JSON 배열 형식으로만 출력하세요.
        JSON 구조: [{"question": "문제", "options": ["A", "B", "C", "D"], "answer": "정답"}]
        
        내용: """ + context
        
        response = self.model.generate_content(prompt)
        clean_json = re.sub(r'```json|```', '', response.text).strip()
        return json.loads(clean_json)