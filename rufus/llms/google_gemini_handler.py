import google.generativeai as genai
import json
from .base_handler import LLMHandler

gemini_system_instructions = """Do not visit any URLs provided in the user prompts and only use the information provided in the prompts to answer the question. Return your response using this JSON schema:
{
    "search_query": "string"
}
"""

class GoogleGeminiHandler(LLMHandler):
    def __init__(self, api_key, model_name):
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel(
            self.model_name,
            system_instruction=gemini_system_instructions
        )
    
    def generate_text(self, prompt, **kwargs):
        try:
            response = self.llm.generate_content([prompt], request_options={"timeout": 30})
            return json.loads(response.text.strip("```json\n"))['search_query']
        except Exception as e:
            print(f"Error with Google Gemini: {e}")
            return ""
