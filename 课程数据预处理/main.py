import json
import re

# 读取JSON文件
with open('course.json', 'r', encoding='utf-8') as file:
    data = file.read()

# 定义要删除的字符组合的正则表达式模式
pattern = r'[\n\t\r<p></p><span></span>br&b;]+'

# 将每行数据转换为JSON对象并提取所需内容
courses = []
for line in data.splitlines():
    try:
        course_data = json.loads(line)
        about_data = course_data.get('about', '')

        # 删除指定字符组合
        about_data_cleaned = re.sub(pattern, '', about_data)

        course_tuple = (
            course_data.get('id', ''),
            course_data.get('name', ''),
            course_data.get('prerequisites', ''),
            about_data_cleaned  # 使用处理后的"about"数据
        )
        courses.append(course_tuple)
    except json.JSONDecodeError:
        pass  # 忽略无法解析的行

# 写入course.txt
with open('course.txt', 'w', encoding='utf-8') as outfile:
    for course in courses:
        outfile.write('`'.join(course) + '\n')
