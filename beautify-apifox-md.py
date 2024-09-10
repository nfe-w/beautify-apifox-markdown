# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Description: 美化 Apifox 生成的 Markdown 文档
#
# @Author: nfe-w
# @Time: 2024-09-10 16:36
import os
import re
import sys


def main():
    # 从命令行获取文件名的路径
    if len(sys.argv) < 2:
        raise Exception('未指定文件名')
    file_name = sys.argv[1]
    if not file_name.endswith('.md'):
        raise Exception('文件名不是markdown文件')
    handle(file_name)


def handle(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines: list[str] = f.readlines()
    if len(lines) == 0:
        raise Exception('markdown文件为空')

    # 遍历数组，将所有满足正则表达式 \(#.*?\) 的行号记录，并将其 (#id) 中的id提取出来，保存到字典中，key为行号，value为提取出来的id
    line_id_dict: [int, str] = {}
    for i in range(len(lines)):
        p_id: re.Pattern = re.compile('\(#.*?\)')
        if len(re.findall(p_id, lines[i])) > 0:
            line_id_dict[i] = re.findall(p_id, lines[i])[0].split('(#')[1].split(')')[0]
    if len(line_id_dict) == 0:
        raise Exception('未找到匹配的行')

    # 遍历原数组，如果命中id所在的<a>标签，找到<a>标签前最近的<h2>标签的内容，将id和<h2>标签内容保存到字典中，key为id，value为<h2>标签内容
    id_h2_dict: [str, str] = {}
    all_id_list: list[str] = list(line_id_dict.values())
    for i in range(len(lines)):
        a_tag_prefix = '<a id="'
        if not lines[i].startswith(a_tag_prefix):
            continue
        a_tag_id = lines[i].split(a_tag_prefix)[1].split('"></a>')[0]
        if a_tag_id not in all_id_list:
            continue
        # 已命中id所在的<a>标签
        h2_tag_prefix = '<h2 id="'
        h2_tag_content = ''
        for j in range(i - 1, -1, -1):
            if lines[j].startswith(h2_tag_prefix):
                # 找到<h2>标签的内容，记录
                h2_tag_content = lines[j].split('>')[1].split('<')[0]
                # 将<h2>标签还原为 ## 的形式
                lines[j] = f'## {h2_tag_content}'
                break

        id_h2_dict[a_tag_id] = h2_tag_content

    # 遍历 line_id_dict 字典，将 key 所在行的 value，根据 id_h2_dict 字典中的 value，替换为 h2
    for k, v in line_id_dict.items():
        lines[k] = lines[k].replace(f"(#{v})", f"(#{id_h2_dict[v]})")

    # 删除所有 <a> 标签所在的行
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith('<a id="'):
            del lines[i]

    # 将修改后的数组写入到新文件中
    new_file_name = file_name.split('.')[0] + '_new.md'
    if os.path.exists(new_file_name):
        raise Exception('已存在同名新文件')
    with open(new_file_name, 'w', encoding='utf-8') as f:
        f.writelines(lines)


if __name__ == '__main__':
    main()
