# modules/rubric.py

import re

class Rubric:
    def __init__(self, rubric_file):
        self.rubric = self.read_rubric(rubric_file)

    def read_rubric(self, rubric_file):
        rubric = {}
        with open(rubric_file, 'r', encoding='utf-8') as f:
            content = f.read()
        # using re
        criteria_matches = re.findall(
            r'This criterion is linked to a Learning Outcome(.*?)\n(\d+) pts\nFull Marks\n(.*?)\n0 pts\nNo Marks\n\2 pts',
            content, re.DOTALL)
        for match in criteria_matches:
            question_name = match[0].strip()
            max_score = int(match[1])
            full_marks_description = match[2].strip()
            question_key = question_name.lower().replace(' ', '_')
            rubric[question_key] = {
                'max_score': max_score,
                'description': full_marks_description
            }
        return rubric

    def get_question_rubric(self, question_key):
        return self.rubric.get(question_key, None)
