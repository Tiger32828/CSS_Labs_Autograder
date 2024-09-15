# modules/grading.py

import re

class Grader:
    def __init__(self, openai_api, rubric):
        self.openai_api = openai_api
        self.rubric = rubric

    def grade_answers(self, answers):
        total_score = 0
        deductions = []
        for question_key, student_answer in answers.items():
            question_rubric = self.rubric.get_question_rubric(question_key)
            if question_rubric:
                max_score = question_rubric['max_score']
                description = question_rubric['description']
                prompt = f"""Please grading based on the rubric below：

Grading rubric：
{description}
max score：{max_score}

student answer：
{student_answer}

Please grade using this format：
Studentpoint：X
deductreasons：XXXX

if there is no deduct point for this answer, the deduct reason needs to be 'None'”。"""

                grading_result = self.openai_api.grade_answer(prompt)
                
                score_match = re.search(r'StudentPoint[:：]\s*(\d+)', grading_result)
                reason_match = re.search(r'deductreason[:：]\s*(.*)', grading_result)
                if score_match:
                    score = int(score_match.group(1))
                    total_score += score
                    if reason_match and score < max_score:
                        deductions.append({
                            'question': question_key,
                            'reason': reason_match.group(1)
                        })
                else:
                    # if cannot parse, generate error
                    deductions.append({
                        'question': question_key,
                        'reason': '!!!!!Can not parse grading, need manually check whether the answer is empty or the format is incorrect。'
                    })
            else:
                # if the problem is not in rubric TBD: dangerous, make warning
                continue
        return total_score, deductions
