import json
from collections import Counter

# 读取course.txt文件中的数据并存储到字典中
courses_data = {}
with open('course.txt', 'r', encoding='utf-8') as course_file:
    for line in course_file:
        course_id, course_name, course_prerequisites, course_introduction = line.strip().split('`')
        courses_data[course_id] = {
            'name': course_name,
            'prerequisites': course_prerequisites,
            'introduction': course_introduction
        }

# 读取course-concept.json文件并处理数据
with open('course-concept.json', 'r', encoding='utf-8') as concept_file:
    concept_data = concept_file.readlines()

# 处理数据并附加内容到course.txt中的相应课程条目
for concept_entry in concept_data:
    entry_fields = concept_entry.strip().split('\t')
    if len(entry_fields) != 2:
        continue  # 跳过格式不正确的条目

    course_id, concept = entry_fields
    concept_key = concept.split('_')[2]  # 提取第二个下划线后的内容作为键
    if course_id in courses_data:
        courses_data[course_id]['concept_key'] = concept_key

# 将附加了内容的数据写入到新的文件course_with_concept.txt中
with open('course_with_concept.txt', 'w', encoding='utf-8') as outfile:
    for course_id, course_info in courses_data.items():
        course_name = course_info['name']
        course_prerequisites = course_info['prerequisites']
        course_introduction = course_info['introduction']
        concept_key = course_info.get('concept_key', '')  # 获取附加的内容，如果不存在则为空字符串
        outfile.write(f'{course_id}`{course_name}`{course_prerequisites}`{course_introduction}`{concept_key}\n')
