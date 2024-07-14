def extract_last_item(file_path):
    teachers = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split('`')
            if len(parts) > 1:
                teachers.add(parts[-1])
    return teachers

def save_to_teacher_file(teachers, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for teacher in teachers:
            output.write(teacher + '\n')

# Example usage
teachers_set = extract_last_item('course.txt')
save_to_teacher_file(teachers_set, 'teacher.txt')
