import os

def extract_student_id_from_filename(filename):
    student_id = filename.split('_')[0]
    return student_id

def clean_temp_files(temp_folder='temp_extracted'):
    if os.path.exists(temp_folder):
        os.system(f'rm -rf {temp_folder}')
