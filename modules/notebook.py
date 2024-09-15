import nbformat
import re

class NotebookParser:
    def __init__(self, notebook_file):
        self.answers = self.parse_notebook(notebook_file)

    def parse_notebook(self, notebook_file):
        nb = nbformat.read(notebook_file, as_version=4)
        answers = {}
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'markdown':
                # match '#### Short answer' or '### Reflection'，no matter whether number exists
                short_answer_match = re.search(r'#+\s*(Short answer|Reflection)(.*)', cell.source, re.IGNORECASE)
                if short_answer_match:
                    answer_type = short_answer_match.group(1).strip().lower().replace(' ', '_')
                    # extract number if exists
                    answer_num_match = re.search(r'(\d+)', short_answer_match.group(2))
                    if answer_num_match:
                        answer_num = answer_num_match.group(1)
                        question_key = f'{answer_type}_{answer_num}'
                    else:
                        # if there is no number, using index to distinguish among questons
                        question_key = f'{answer_type}_{i}'
                    # look at the next markdown cell for student answer
                    student_answer = ''
                    for j in range(1, 3):
                        if i + j < len(nb.cells):
                            next_cell = nb.cells[i + j]
                            if next_cell.cell_type == 'markdown':
                                if '🤔 **Write your response here:**' in next_cell.source:
                                    student_answer = next_cell.source.replace('🤔 **Write your response here:**', '').strip()
                                    break
                    if student_answer:
                        answers[question_key] = student_answer
        return answers

    def get_answers(self):
        print(self.answers)
        return self.answers
