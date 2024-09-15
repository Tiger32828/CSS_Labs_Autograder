# main.py

import os
import zipfile
import csv
from modules.aitools import OpenAIAPI
from modules.rubric import Rubric
from modules.notebook import NotebookParser
from modules.grading import Grader
from utils import extract_student_id_from_filename, clean_temp_files

def process_assignments(zip_file_path, rubric_file, output_total_csv, output_deductions_csv):
    # init
    openai_api = OpenAIAPI()
    rubric = Rubric(rubric_file)
    grader = Grader(openai_api, rubric)

    total_scores = []
    all_deductions = []

    temp_extract_folder = 'temp_extracted'

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_extract_folder)

    # find .ipynb for each student
    for root, dirs, files in os.walk(temp_extract_folder):
        for file in files:
            if file.endswith('.ipynb'):
                student_id = extract_student_id_from_filename(file)
                notebook_file = os.path.join(root, file)
                # print(notebook_file)
                notebook_parser = NotebookParser(notebook_file)
                answers = notebook_parser.get_answers()
                total_score, deductions = grader.grade_answers(answers)
                total_scores.append({'student_id': student_id, 'total_score': total_score})
                for deduction in deductions:
                    deduction['student_id'] = student_id  # add student ID
                    all_deductions.append(deduction)

    
    clean_temp_files(temp_extract_folder)

    # write total scores to CSV
    with open(output_total_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['student_id', 'total_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in total_scores:
            writer.writerow(data)

    # write grading explaination to another CSV
    with open(output_deductions_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['student_id', 'question', 'reason']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in all_deductions:
            writer.writerow(data)

if __name__ == '__main__':
    process_assignments(
        zip_file_path='students_submissions.zip',    
        rubric_file='rubric.txt',                   
        output_total_csv='total_scores.csv',        
        output_deductions_csv='deductions.csv'      
    )
