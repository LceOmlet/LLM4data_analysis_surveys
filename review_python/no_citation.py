import re
from collections import defaultdict

class Node:
    def __init__(self, title, level):
        self.title = title
        self.level = level
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def get_leaf_count(self):
        if not self.children:
            return 1
        return sum(child.get_leaf_count() for child in self.children)

    def get_max_depth(self, current_depth=1):
        if not self.children:
            return current_depth
        return max(child.get_max_depth(current_depth + 1) for child in self.children)

def parse_latex_structure(file_path):
    section_commands = {
        'part': 0,
        'chapter': 1,
        'section': 2,
        'subsection': 3,
        'subsubsection': 4,
        'paragraph': 5,
        'subparagraph': 6,
        # ========= 修改 2：添加 researchq 和 lemma 的级别 =========
        'researchq': 6,
        'lemma': 6
    }

    section_pattern = re.compile(
        r'\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)'
        r'\s*'  # 允许命令后有空格
        r'\{((?:[^{}]+|\{[^{}]*\})+)\}'  # 匹配包含嵌套括号的内容
    )

    root = Node("文档根节点", -1)
    stack = [root]
    current_env = None  # 跟踪当前环境状态

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            section_match = section_pattern.search(line)
            if section_match:
                current_env = None  # 遇到 section 命令时重置环境状态
                command, title = section_match.groups()
                level = section_commands[command]

                while stack and stack[-1].level >= level:
                    stack.pop()
                parent = stack[-1] if stack else root

                new_node = Node(title.strip(), level)
                parent.add_child(new_node)
                stack.append(new_node)
                continue

            # ========= 修改 2：处理 researchq/lemma 环境 =========
            env_start_match = re.match(r'\\begin{(researchq|lemma)}', line)
            if env_start_match:
                env_type = env_start_match.group(1)
                current_env = env_type
                remaining = line[env_start_match.end():].lstrip()
                remaining = re.sub(r'\\label\{[^}]+\}', '', remaining).strip()
                if remaining:
                    parts = re.split(r'([.?!\n])', remaining, 1)
                    title_part = parts[0]
                    if len(parts) > 1 and parts[1] in ('.', '?', '!'):
                        title_part += parts[1]
                    title = title_part.strip()
                    level = section_commands[env_type]
                    while stack and stack[-1].level >= level:
                        stack.pop()
                    parent = stack[-1]
                    new_node = Node(title, level)
                    parent.add_child(new_node)
                    stack.append(new_node)
                    current_env = None
                continue

            if current_env:
                line = re.sub(r'\\label\{[^}]+\}', '', line).strip()
                if line:
                    parts = re.split(r'([.?!\n])', line, 1)
                    title_part = parts[0]
                    if len(parts) > 1 and parts[1] in ('.', '?', '!'):
                        title_part += parts[1]
                    title = title_part.strip()
                    level = section_commands[current_env]
                    while stack and stack[-1].level >= level:
                        stack.pop()
                    parent = stack[-1]
                    new_node = Node(title, level)
                    parent.add_child(new_node)
                    stack.append(new_node)
                    current_env = None

    return root

# ...（后续 generate_table_rows 和 create_latex_table 函数保持不变）...

def generate_table_rows(node, current_path, table_rows, max_depth):
    if node.title != "文档根节点":
        current_path = current_path.copy()
        current_path.append(node)

    if not node.children:
        row = []
        for i in range(max_depth):
            if i < len(current_path):
                row.append(current_path[i])
            else:
                row.append(None)
        table_rows.append(row)
    else:
        for child in node.children:
            generate_table_rows(child, current_path, table_rows, max_depth)

def create_latex_table(file_path, output_table_path):
    tree = parse_latex_structure(file_path)
    max_depth = tree.get_max_depth()

    table_rows = []
    generate_table_rows(tree, [], table_rows, max_depth)

    num_columns = max_depth

    multirow_tracker = [0] * max_depth

    latex_table = r"""
\begin{table}[ht]
    \centering
    \caption{论文结构}
    \label{tab:structure}
    \begin{tabular}{""" + "l" * num_columns + r"""}
    \toprule
"""

    for row in table_rows:
        latex_row = []
        for i in range(max_depth):
            if multirow_tracker[i] > 0:
                latex_row.append("")
                multirow_tracker[i] -= 1
            else:
                node = row[i]
                if node:
                    leaf_count = node.get_leaf_count()
                    if leaf_count > 1:
                        cell = f"\\multirow{{{leaf_count}}}{{*}}{{{node.title}}}"
                        latex_row.append(cell)
                        multirow_tracker[i] = leaf_count - 1
                    else:
                        latex_row.append(node.title)
                else:
                    latex_row.append("")

        escaped_row = [cell.replace('&', '\\&').replace('%', '\\%') for cell in latex_row]
        latex_table += " & ".join(escaped_row) + r" \\" + "\n"

        eligible = [multirow_tracker[i] == 0 for i in range(max_depth)]
        dashline_ranges = []
        start = None
        for idx, is_eligible in enumerate(eligible):
            if is_eligible:
                if start is None:
                    start = idx + 1
            else:
                if start is not None:
                    dashline_ranges.append((start, idx))
                    start = None
        if start is not None:
            dashline_ranges.append((start, num_columns))

        for start, end in dashline_ranges:
            if start <= end:
                latex_table += f"\\cdashline{{{start}-{end}}}\n"

    latex_table += r"""\bottomrule
    \end{tabular}
\end{table}
"""

    with open(output_table_path, 'w', encoding='utf-8') as f_out:
        f_out.write(latex_table)

    print(f"已成功生成LaTeX表格并保存到 '{output_table_path}'。")

if __name__ == "__main__":
    input_file = "/mnt/c/Users/Administrator/Desktop/review_python/appendix.tex"
    output_table_file = "appendix_structure_table.tex"
    create_latex_table(input_file, output_table_file)