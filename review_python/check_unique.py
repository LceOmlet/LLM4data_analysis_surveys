import re
from collections import defaultdict
import sys

def extract_sections_and_subsections(latex_content):
    """
    提取所有章节和子章节的内容。
    章节使用 \section{...}
    子章节使用 \subsection{...}
    """
    # 正则表达式匹配 \section 和 \subsection
    section_pattern = re.compile(r'\\section\{(.+?)\}')
    subsection_pattern = re.compile(r'\\subsection\{(.+?)\}')

    # 分割内容为章节
    sections = section_pattern.split(latex_content)
    
    # sections 列表中，偶数索引为非章节标题内容，奇数索引为章节标题
    chapters = []
    for i in range(1, len(sections), 2):
        chapter_title = sections[i].strip()
        chapter_content = sections[i+1]
        
        # 在章节内容中分割子章节
        subsections = []
        sub_sec_splits = subsection_pattern.split(chapter_content)
        
        for j in range(1, len(sub_sec_splits), 2):
            subsection_title = sub_sec_splits[j].strip()
            subsection_content = sub_sec_splits[j+1]
            subsections.append({
                'title': subsection_title,
                'content': subsection_content
            })
        
        chapters.append({
            'title': chapter_title,
            'subsections': subsections
        })
    
    return chapters

def extract_citations(text):
    """
    从文本中提取所有引用标签。
    支持 \cite{ref1}, \citep{ref1, ref2}, \citet{ref1, ref2}, 等格式。
    """
    # 支持常见的引用命令
    cite_pattern = re.compile(r'\\cite\w*\{([^}]+)\}')
    citations = set()
    for match in cite_pattern.findall(text):
        refs = [ref.strip() for ref in match.split(',')]
        citations.update(refs)
    return citations

def find_unique_references(chapter2, chapter3):
    """
    找出第二章和第三章中每个子章节独有的参考文献。
    """
    all_subsections = chapter2['subsections'] + chapter3['subsections']
    
    # 提取每个子章节的引用
    for subsec in all_subsections:
        subsec['citations'] = extract_citations(subsec['content'])
    
    # 统计所有引用的出现次数（全局统计）
    citation_counts = defaultdict(int)
    for subsec in all_subsections:
        for cite in subsec['citations']:
            citation_counts[cite] += 1
    
    # 为每个子章节找出独有的引用（引用次数为1）
    unique_references_ch2 = {}
    unique_references_ch3 = {}
    
    for subsec in chapter2['subsections']:
        unique = {cite for cite in subsec['citations'] if citation_counts[cite] == 1}
        unique_references_ch2[subsec['title']] = unique
    
    for subsec in chapter3['subsections']:
        unique = {cite for cite in subsec['citations'] if citation_counts[cite] == 1}
        unique_references_ch3[subsec['title']] = unique
    
    return unique_references_ch2, unique_references_ch3

def main(latex_file):
    try:
        with open(latex_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误: 文件 '{latex_file}' 未找到。")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件时出错: {e}")
        sys.exit(1)
    
    # 提取章节和子章节
    chapters = extract_sections_and_subsections(content)
    
    if len(chapters) < 3:
        print("文档中章节不足3个，无法提取第二章和第三章。")
        sys.exit(1)
    
    # 获取第二章和第三章（索引从0开始）
    chapter2 = chapters[1]
    chapter3 = chapters[2]
    
    # 找出每个子章节独有的引用
    unique_refs_ch2, unique_refs_ch3 = find_unique_references(chapter2, chapter3)
    
    # 输出结果
    print("第二章中每个子章节独有的引用:")
    for subsec_title, unique_refs in unique_refs_ch2.items():
        if unique_refs:
            unique_str = ', '.join(sorted(unique_refs))
            print(f'  子章节 "{subsec_title}" 的独有引用: {unique_str}')
        else:
            print(f'  子章节 "{subsec_title}" 没有独有的引用。')
    
    print("\n第三章中每个子章节独有的引用:")
    for subsec_title, unique_refs in unique_refs_ch3.items():
        if unique_refs:
            unique_str = ', '.join(sorted(unique_refs))
            print(f'  子章节 "{subsec_title}" 的独有引用: {unique_str}')
        else:
            print(f'  子章节 "{subsec_title}" 没有独有的引用。')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python find_unique_references.py your_document.tex")
        sys.exit(1)
    
    latex_file = sys.argv[1]
    main(latex_file)
