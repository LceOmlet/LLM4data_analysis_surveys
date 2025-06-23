import re
from collections import defaultdict

class Node:
    def __init__(self, title, level):
        self.title = title
        self.level = level
        self.children = []
        self.citations = set()  # 使用集合来存储唯一的引用

    def add_child(self, node):
        self.children.append(node)

    def add_citation(self, citation):
        self.citations.add(citation)

    def print_tree(self, indent=0):
        indent_str = '  ' * indent
        print(f"{indent_str}{self.title}")
        if self.citations:
            citations_str = ', '.join(f"\\cite{{{cite}}}" for cite in sorted(self.citations))
            print(f"{indent_str}  引用: {citations_str}")
        for child in self.children:
            child.print_tree(indent + 1)

def parse_latex_structure(file_path):
    # 定义章节命令及其对应的层级
    section_commands = {
        'part': 0,
        'chapter': 1,
        'section': 2,
        'subsection': 3,
        'subsubsection': 4,
        'paragraph': 5,
        'subparagraph': 6
    }

    # 编译正则表达式
    section_pattern = re.compile(r'\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\{([^}]+)\}')
    cite_pattern = re.compile(r'\\cite\{([^}]+)\}')

    root = Node("文档根节点", -1)
    stack = [root]

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 检测章节命令
            section_match = section_pattern.search(line)
            if section_match:
                command, title = section_match.groups()
                level = section_commands[command]

                # 找到适当的父节点
                while stack and stack[-1].level >= level:
                    stack.pop()
                parent = stack[-1] if stack else root

                # 创建新节点并添加到树中
                new_node = Node(title, level)
                parent.add_child(new_node)
                stack.append(new_node)
                continue  # 章节命令不同时进行引用检测

            # 检测引用命令
            cite_matches = cite_pattern.findall(line)
            if cite_matches and stack:
                current_node = stack[-1]
                for match in cite_matches:
                    # 处理多个引用，如 \cite{ref1, ref2}
                    cites = [cite.strip() for cite in match.split(',')]
                    for cite in cites:
                        current_node.add_citation(cite)

    return root

if __name__ == "__main__":
    # 示例LaTeX内容保存为example.tex

    # 解析LaTeX结构
    file_path = "/home/liangchen/review/section_3.tex"

    tree = parse_latex_structure(file_path)

    # 打印树状结构及引用
    tree.print_tree()
