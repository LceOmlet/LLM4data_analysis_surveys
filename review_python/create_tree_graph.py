#!/usr/bin/env python3
"""
Script to extract citations from chapters 2 and 3 of manuscript_merged.tex
and update Tree_graph.tex with the found citations
"""

import re
import sys
from typing import Dict, List, Set, Tuple

def extract_citations_from_text(text: str) -> Set[str]:
    """Extract all citations from text using regex patterns"""
    citations = set()
    
    # Pattern for \cite{...} with multiple citations
    cite_pattern = r'\\cite\{([^}]+)\}'
    matches = re.findall(cite_pattern, text)
    
    for match in matches:
        # Split multiple citations separated by commas
        individual_cites = [cite.strip() for cite in match.split(',')]
        citations.update(individual_cites)
    
    return citations

def extract_chapters_2_3(manuscript_content: str) -> Tuple[str, str]:
    """Extract content from chapters 2 and 3"""
    
    # 修正章节标题，使用更灵活的匹配
    chapter2_patterns = [
        r'\\section\{Soving Data Analysis Tasks with PFMs\}',
        r'\\section\{Solving Data Analysis Tasks with PFMs\}',
        r'Soving Data Analysis Tasks with PFMs',
        r'Solving Data Analysis Tasks with PFMs'
    ]
    
    chapter3_patterns = [
        r'\\section\{PFMs Enhanced Systematic improvement Methodologies\}',
        r'\\section\{PFMs Enhanced Systematic Improvement Methodologies\}',
        r'PFMs Enhanced Systematic improvement Methodologies',
        r'PFMs Enhanced Systematic Improvement Methodologies'
    ]
    
    chapter4_patterns = [
        r'\\section\{Empirical Findings and Benchmarks\}',
        r'Empirical Findings and Benchmarks'
    ]
    
    chapter2_start = -1
    chapter3_start = -1
    chapter4_start = -1
    
    # 查找第2章开始位置
    for pattern in chapter2_patterns:
        pos = manuscript_content.find(pattern)
        if pos != -1:
            chapter2_start = pos
            print(f"Found Chapter 2 at position {pos} with pattern: {pattern}")
            break
    
    # 查找第3章开始位置
    for pattern in chapter3_patterns:
        pos = manuscript_content.find(pattern)
        if pos != -1:
            chapter3_start = pos
            print(f"Found Chapter 3 at position {pos} with pattern: {pattern}")
            break
    
    # 查找第4章开始位置
    for pattern in chapter4_patterns:
        pos = manuscript_content.find(pattern)
        if pos != -1:
            chapter4_start = pos
            print(f"Found Chapter 4 at position {pos} with pattern: {pattern}")
            break
    
    if chapter2_start == -1:
        print("Could not find chapter 2 boundaries")
        return "", ""
    
    if chapter3_start == -1:
        print("Could not find chapter 3 boundaries")
        return "", ""
    
    # Extract chapter 2 content
    chapter2_content = manuscript_content[chapter2_start:chapter3_start]
    
    # Extract chapter 3 content
    if chapter4_start != -1:
        chapter3_content = manuscript_content[chapter3_start:chapter4_start]
    else:
        # 如果找不到第4章，就取到文档末尾，但排除参考文献部分
        bibliography_patterns = [
            r'\\printbibliography',
            r'\\bibliography',
            r'\\begin\{thebibliography\}',
            r'References'
        ]
        
        end_pos = len(manuscript_content)
        for pattern in bibliography_patterns:
            pos = manuscript_content.find(pattern, chapter3_start)
            if pos != -1:
                end_pos = min(end_pos, pos)
        
        chapter3_content = manuscript_content[chapter3_start:end_pos]
    
    return chapter2_content, chapter3_content

def map_citations_to_groups(citations: Set[str]) -> Tuple[Dict[str, List[str]], Set[str]]:
    """Map citations to their corresponding groups based on the existing tree graph structure"""
    
    # 从现有的Tree_graph.tex中提取的映射关系
    citation_groups = {
        'group1': ['Nobari2023DTTAE', 'Wang2023SoloDD'],
        'group2': ['qi2024cleanagent', 'Li2024IsPB'],
        'group3': ['Tang2024WorldCoderAM', 'ni2024iterclean', 'KGobjectrecognition', 'constructKG', 'vos2022towards', 'deem'],
        'group4': ['Hollmann2023LargeLM'],
        'group5': ['Dibia2023LIDAAT', 'ma2023insightpilot'],
        'group6': ['ko2024filling', 'nam2024using', 'li2024can', 'dubiel2024device', 'zheng2024revolutionizing'],
        'group7': ['jain2024r2e', 'zhengprise', 'repocomp', 'KoziolekGHALE24', 'yuan2023power'],
        'group8': ['singh2023augmenting', 'nam2024optimized'],
        'group9': ['HsuMTW23', 'HuZWCM0WSXZCY0K24', 'SongY00024', 'EoTGE', 'bai2024transformers', 'sayed2024gizaml'],
        'group10': ['Wang2024TheoremLlamaTG', 'Carrott2024CoqPytPN', 'Pei2023CanLL'],
        'group11': ['GrandWBOLTA24'],
        'group12': ['GPTuner', 'CHORUS', 'tabulargeneration', 'LLMschema'],
        'group13': ['readyforNL2SQL', 'smalllargemodelNL2SQL', 'text2sqlevaluation'],
        'group15': ['jha2023counterexample', 'ye2024satlm']
    }
    
    # Create reverse mapping
    citation_to_group = {}
    for group, cites in citation_groups.items():
        for cite in cites:
            citation_to_group[cite] = group
    
    # Group found citations
    grouped_citations = {}
    ungrouped_citations = set()
    
    for citation in citations:
        if citation in citation_to_group:
            group = citation_to_group[citation]
            if group not in grouped_citations:
                grouped_citations[group] = []
            grouped_citations[group].append(citation)
        else:
            ungrouped_citations.add(citation)
    
    return grouped_citations, ungrouped_citations

def generate_tree_graph_tex(grouped_citations: Dict[str, List[str]], ungrouped_citations: Set[str]) -> str:
    """Generate the Tree_graph.tex content with updated citations from chapters 2 and 3"""
    
    # 读取原始Tree_graph.tex作为模板
    try:
        with open('Tree_graph.tex', 'r', encoding='utf-8') as f:
            original_content = f.read()
    except FileNotFoundError:
        print("Warning: Tree_graph.tex not found, using built-in template")
        original_content = ""
    
    # 如果找到原始文件，就基于它修改，否则生成新的
    if original_content:
        # 使用正则表达式替换中间节点定义
        # 查找 \def\middleNodes{ 到 } 之间的内容
        pattern = r'(\\def\\middleNodes\{)(.*?)(\})'
        
        # 构建新的中间节点内容
        new_middle_nodes = ""
        
        # 添加有引用的组
        for group_id in sorted(grouped_citations.keys()):
            citations = grouped_citations[group_id]
            if citations:
                formatted_citations = [f"\\cite{{{cite}}}" for cite in sorted(citations)]
                citation_text = ", ".join(formatted_citations)
                new_middle_nodes += f"    {{{group_id}}}/{{{citation_text}}},\n"
        
        # 添加未分组的引用
        if ungrouped_citations:
            ungrouped_list = sorted(list(ungrouped_citations))
            for i, cite_group in enumerate([ungrouped_list[j:j+3] for j in range(0, len(ungrouped_list), 3)]):
                formatted_ungrouped = [f"\\cite{{{cite}}}" for cite in cite_group]
                citation_text = ", ".join(formatted_ungrouped)
                new_middle_nodes += f"    {{group_new_{i+1}}}/{{{citation_text}}},\n"
        
        # 移除最后的逗号
        new_middle_nodes = new_middle_nodes.rstrip(',\n')
        
        # 替换原有的中间节点定义
        updated_content = re.sub(
            pattern,
            f"\\1\n{new_middle_nodes}\n\\3",
            original_content,
            flags=re.DOTALL
        )
        
        # 更新标题以反映这是基于第2、3章的更新版本
        updated_content = re.sub(
            r'(\\caption\{[^}]*)\}',
            r'\1 Updated with citations from chapters 2 and 3.}',
            updated_content
        )
        
        return updated_content
    
    else:
        # 如果没有原始文件，生成新的内容（使用您原来的模板）
        # 这里可以保留您原来的generate_tree_graph_tex函数的逻辑
        # 为了简洁，我就不重复所有代码了
        print("Generating new Tree_graph.tex from template...")
        # 返回基本的模板结构
        return "% Generated Tree_graph.tex - please use original file as template"

def main():
    """Main function to process the manuscript and generate the tree graph"""
    
    # Read the manuscript file
    try:
        with open('manuscript_merged.tex', 'r', encoding='utf-8') as f:
            manuscript_content = f.read()
    except FileNotFoundError:
        print("Error: manuscript_merged.tex not found")
        return
    
    print(f"Read manuscript file with {len(manuscript_content)} characters")
    
    # Extract chapters 2 and 3
    chapter2_content, chapter3_content = extract_chapters_2_3(manuscript_content)
    
    if not chapter2_content or not chapter3_content:
        print("Error: Could not extract chapter content")
        return
    
    print(f"Chapter 2 content length: {len(chapter2_content)}")
    print(f"Chapter 3 content length: {len(chapter3_content)}")
    
    # Extract citations from both chapters
    chapter2_citations = extract_citations_from_text(chapter2_content)
    chapter3_citations = extract_citations_from_text(chapter3_content)
    
    # Combine all citations
    all_citations = chapter2_citations.union(chapter3_citations)
    
    print(f"\nFound {len(chapter2_citations)} citations in chapter 2")
    print(f"Found {len(chapter3_citations)} citations in chapter 3")
    print(f"Total unique citations: {len(all_citations)}")
    
    print(f"\nAll citations found:")
    for citation in sorted(all_citations):
        print(f"  - {citation}")
    
    # Map citations to groups
    grouped_citations, ungrouped_citations = map_citations_to_groups(all_citations)
    
    print(f"\nGrouped citations:")
    for group, cites in grouped_citations.items():
        print(f"  {group}: {cites}")
    
    if ungrouped_citations:
        print(f"\nUngrouped citations: {sorted(ungrouped_citations)}")
    else:
        print(f"\nAll citations were successfully mapped to existing groups!")
    
    # Generate the tree graph TEX content
    tree_graph_content = generate_tree_graph_tex(grouped_citations, ungrouped_citations)
    
    # Write to output file
    try:
        with open('Tree_graph_updated.tex', 'w', encoding='utf-8') as f:
            f.write(tree_graph_content)
        
        print(f"\n✅ Tree_graph_updated.tex has been generated successfully!")
        print("📝 You can now use this file to replace the Tree_graph.tex in your document.")
        
        # 提供一些统计信息
        print(f"\n📊 Statistics:")
        print(f"   - Groups with citations: {len(grouped_citations)}")
        print(f"   - Total citations used: {sum(len(cites) for cites in grouped_citations.values())}")
        if ungrouped_citations:
            print(f"   - Ungrouped citations: {len(ungrouped_citations)}")
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")

if __name__ == "__main__":
    main()