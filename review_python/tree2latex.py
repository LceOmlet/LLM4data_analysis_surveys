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
        'subparagraph': 6
    }

    section_pattern = re.compile(
        r'\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)'
        r'\s*'
        r'\{((?:[^{}]+|\{[^{}]*\})+)\}'
    )

    # ========= 关键修改 1：优化环境正则表达式 =========
    env_pattern = re.compile(
        r'\\begin{(researchq|lemma)}'                  # 匹配环境类型
        r'(?:\\label{[^}]*})?'                  # 跳过标签
        r'\s*'                                  # 允许空格
        r'([^{}\\\n]*?)\s*'                     # 捕获到环境结束前的内容
        r'(?=\\|\s*$|。|\\end)'                 # 前瞻终止条件
    )

    root = Node("文档根节点", -1)
    stack = [root]

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 处理章节命令...
            
            # ========= 关键修改 2：增强环境处理逻辑 =========
            env_match = env_pattern.search(line)
            if env_match and stack:
                env_type, raw_title = env_match.groups()
                title = raw_title.strip()
                
                # 处理结尾标点（如"Sensitivity analysis." -> "Sensitivity analysis"）
                title = title.rstrip('.').strip()
                
                if title:
                    parent = stack[-1]
                    # 确保层级比父节点深一级（最低为paragraph级别）
                    new_level = max(parent.level + 1, 5)
                    new_node = Node(f"[{env_type.upper()}] {title}", new_level)
                    parent.add_child(new_node)

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