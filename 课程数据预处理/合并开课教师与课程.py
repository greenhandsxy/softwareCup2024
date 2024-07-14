import json

def remove_duplicates_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        unique_lines = []
        seen = set()
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 1 and parts[1] not in seen:
                unique_lines.append(line)
                seen.add(parts[1])
    return unique_lines

def merge_files(teacher_course_file, course_with_concept_file, output_file):
    unique_teacher_course = remove_duplicates_from_json(teacher_course_file)

    with open(course_with_concept_file, 'r', encoding='utf-8') as file:
        course_lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as output:
        for course_line in course_lines:
            concept = course_line.strip().split('`')[0]  # Assuming the concept is before the '`' symbol
            for teacher_course in unique_teacher_course:
                if concept == teacher_course.strip().split()[1]:
                    output.write(course_line.strip() + '`' + teacher_course.strip().split()[0].split("_")[1] + '\n')

# Example usage
merge_files('teacher-course.json', 'course_with_concept.txt', 'course.txt')
