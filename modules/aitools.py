# modules/aitools.py

import openai
from config import config

class OpenAIAPI:
    def __init__(self):
        openai.api_key = config.OPENAI_API_KEY

    def grade_answer(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Please grade each short answer of each student against the rubric. DOn't be too harsh."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
