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
    
    # Find chapter 2 (starts with \section{Soving Data Analysis Tasks with PFMs})
    chapter2_start = manuscript_content.find(r'\section{Soving Data Analysis Tasks with PFMs}')
    
    # Find chapter 3 (starts with \section{PFMs Enhanced Systematic improvement Methodologies})
    chapter3_start = manuscript_content.find(r'\section{PFMs Enhanced Systematic improvement Methodologies}')
    
    # Find chapter 4 or end of chapter 3
    chapter4_start = manuscript_content.find(r'\section{Empirical Findings and Benchmarks}')
    
    if chapter2_start == -1 or chapter3_start == -1:
        print("Could not find chapter boundaries")
        return "", ""
    
    # Extract chapter 2 content
    chapter2_content = manuscript_content[chapter2_start:chapter3_start]
    
    # Extract chapter 3 content
    if chapter4_start != -1:
        chapter3_content = manuscript_content[chapter3_start:chapter4_start]
    else:
        chapter3_content = manuscript_content[chapter3_start:]
    
    return chapter2_content, chapter3_content

def map_citations_to_groups(citations: Set[str]) -> Tuple[Dict[str, List[str]], Set[str]]:
    """Map citations to their corresponding groups based on the existing tree graph structure"""
    
    # Define the mapping based on the existing tree graph
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
    """Generate the Tree_graph.tex content with updated citations"""
    
    # Base template for the tree graph
    tex_content = r"""\begin{figure*}[h]
    \centering
\begin{tikzpicture}[
  auto,
  emptyNode/.style={
    draw=none,
    fill=none,
    minimum height=0.8cm,
    inner sep=0pt,
    align=center,
    scale=1.1
  },
  baseNode/.style={
    rectangle,
    draw,
    rounded corners,
    minimum height=0.8cm,
    inner sep=2pt,
    font=\small
  },
  leftParentNode/.style={
    emptyNode,
    text width=\leftParentNodeWidth,
    text=black,
    font=\bfseries,
  },
  rightParentNode/.style={
    emptyNode,
    text width=\rightParentNodeWidth,
    text=black,
    font=\bfseries
  },
  middleNode/.style={
    baseNode,
    text width=\middleNodeWidth,
    fill=gray!20,
    draw=gray!50,
    text=black,
    font=\tiny,
    minimum height=\middleNodeHeight
  },
  >=stealth'
]
 % Define colors for left column subsections
  \definecolor{DataManagementColor}{RGB}{31,119,180}
  \definecolor{ExploratoryDataAnalysisColor}{RGB}{44,160,44}
  \definecolor{ImplementationColor}{RGB}{255,127,14}
  \definecolor{AssessmentColor}{RGB}{148,103,189}
  
  % Define colors for right column subsections
  \definecolor{DSLUnderstandingColor}{RGB}{214,39,40}
  \definecolor{DataQualityOptimizationColor}{RGB}{140,86,75}
  \definecolor{AutoMLColor}{RGB}{23,190,207}
  \definecolor{AccessibilityColor}{RGB}{227,119,194}
  
  % Define left column parent node
  \node[leftParentNode] (left_parent) at (0,-2) {Task Solving};
  
  % Define right column parent node
  \node[rightParentNode] (right_parent) at ($(left_parent)+(\horizontalSpacing,0)$) {Optimizations};
  
  % Middle reference node starting point
  \coordinate (middleStart) at ($(left_parent)!0.5!(right_parent)$);
  
  % Left column child nodes
  \node[baseNode, fill=DataManagementColor!20, draw=DataManagementColor, text width=\leftNodeWidth, below=\leftVerticalSpacing of left_parent] (data_management) {Data Preparation};
  \node[baseNode, fill=ExploratoryDataAnalysisColor!20, draw=ExploratoryDataAnalysisColor, text width=\leftNodeWidth, below=\leftVerticalSpacing of data_management] (exploratory_data_analysis) {Exploratory DA};
  \node[baseNode, fill=ImplementationColor!20, draw=ImplementationColor, text width=\leftNodeWidth, below=\leftVerticalSpacing of exploratory_data_analysis] (implementing_methods) {Implementation};
  \node[baseNode, fill=AssessmentColor!20, draw=AssessmentColor, text width=\leftNodeWidth, below=\leftVerticalSpacing of implementing_methods] (assessing_results) {Assessment};
  
  % Right column child nodes
  \node[baseNode, fill=DSLUnderstandingColor!20, draw=DSLUnderstandingColor, text width=\rightNodeWidth, below=\rightVerticalSpacing of right_parent] (dsl_understanding) {Reasoning};
  \node[baseNode, fill=DataQualityOptimizationColor!20, draw=DataQualityOptimizationColor, text width=\rightNodeWidth, below=\rightVerticalSpacing of dsl_understanding] (PFM_quality) {Data Quality};
  \node[baseNode, fill=AutoMLColor!20, draw=AutoMLColor, text width=\rightNodeWidth, below=\rightVerticalSpacing of PFM_quality] (automated_ml) {Automation};
  \node[baseNode, fill=AccessibilityColor!20, draw=AccessibilityColor, text width=\rightNodeWidth, below=\rightVerticalSpacing of automated_ml] (accessible_models) {Accessibility};
  
  % Define middle nodes with citations
  \def\middleNodes{
"""

    # Add grouped citations to middle nodes
    all_citations_found = set()
    for group_id in sorted(grouped_citations.keys()):
        citations = grouped_citations[group_id]
        if citations:
            all_citations_found.update(citations)
            # Format citations with \cite{}
            formatted_citations = [f"\\cite{{{cite}}}" for cite in sorted(citations)]
            citation_text = ", ".join(formatted_citations)
            tex_content += f"    {{{group_id}}}/{{{citation_text}}},\n"
    
    # Add any ungrouped citations as new groups if needed
    if ungrouped_citations:
        ungrouped_list = sorted(list(ungrouped_citations))
        # Split into groups of 3-4 citations each for readability
        for i, cite_group in enumerate([ungrouped_list[j:j+3] for j in range(0, len(ungrouped_list), 3)]):
            formatted_ungrouped = [f"\\cite{{{cite}}}" for cite in cite_group]
            citation_text = ", ".join(formatted_ungrouped)
            tex_content += f"    {{group_new_{i+1}}}/{{{citation_text}}},\n"
    
    # Remove the last comma and continue with the rest of the template
    tex_content = tex_content.rstrip(',\n') + '\n'
    
    tex_content += r"""  }
  
  % Place middle column nodes
  \def\yShift{-1cm}
  
  \foreach \name/\text in \middleNodes {
    \node[middleNode] (\name) at ($(middleStart)-(0,\yShift+\leftVerticalSpacing)$) {\text};
    \pgfmathparse{\yShift+\middleVerticalSpacing}
    \xdef\yShift{\pgfmathresult}
  }
  
  % Draw smooth connecting lines with corresponding theme colors
  % Group connections based on the relationships in the tree
  \draw[->, thin, draw=DataManagementColor] (data_management.east) to [out=0, in=180] (group1.west);
  \draw[->, thin, draw=DSLUnderstandingColor] (group1.east) to [out=0, in=180] (dsl_understanding.west);
  
  \draw[->, thin, draw=DataManagementColor] (data_management.east) to [out=0, in=180] (group2.west);
  \draw[->, thin, draw=AssessmentColor] (assessing_results.east) to [out=0, in=180] (group2.west);
  \draw[->, thin, draw=DSLUnderstandingColor] (group2.east) to [out=0, in=180] (dsl_understanding.west);
  
  % Add more connections based on existing groups
  \draw[->, thin, draw=DataManagementColor] (data_management.east) to [out=0, in=180] (group3.west);
  \draw[->, thin, draw=DataQualityOptimizationColor] (group3.east) to [out=0, in=180] (PFM_quality.west);
  
  \draw[->, thin, draw=DataManagementColor] (data_management.east) to [out=0, in=180] (group4.west);
  \draw[->, thin, draw=AutoMLColor] (group4.east) to [out=0, in=180] (automated_ml.west);
  
  \draw[->, thin, draw=ExploratoryDataAnalysisColor] (exploratory_data_analysis.east) to [out=0, in=180] (group5.west);
  \draw[->, thin, draw=DSLUnderstandingColor] (group5.east) to [out=0, in=180] (dsl_understanding.west);
  
  \draw[->, thin, draw=ExploratoryDataAnalysisColor] (exploratory_data_analysis.east) to [out=0, in=180] (group6.west);
  \draw[->, thin, draw=AccessibilityColor] (group6.east) to [out=0, in=180] (accessible_models.west);
  
  \draw[->, thin, draw=ImplementationColor] (implementing_methods.east) to [out=0, in=180] (group7.west);
  \draw[->, thin, draw=DSLUnderstandingColor] (group7.east) to [out=0, in=180] (dsl_understanding.west);
  
  \draw[->, thin, draw=ImplementationColor] (implementing_methods.east) to [out=0, in=180] (group8.west);
  \draw[->, thin, draw=AccessibilityColor] (group8.east) to [out=0, in=180] (accessible_models.west);
  
  \draw[->, thin, draw=ImplementationColor] (implementing_methods.east) to [out=0, in=180] (group9.west);
  \draw[->, thin, draw=AutoMLColor] (group9.east) to [out=0, in=180] (automated_ml.west);
  
  \draw[->, thin, draw=AssessmentColor] (assessing_results.east) to [out=0, in=180] (group10.west);
  \draw[->, thin, draw=DSLUnderstandingColor] (group10.east) to [out=0, in=180] (dsl_understanding.west);
  
  \draw[->, thin, draw=ExploratoryDataAnalysisColor] (exploratory_data_analysis.east) to [out=0, in=180] (group11.west);
  \draw[->, thin, draw=ImplementationColor] (implementing_methods.east) to [out=0, in=180] (group11.west);
  \draw[->, thin, draw=DSLUnderstandingColor] (group11.east) to [out=0, in=180] (dsl_understanding.west);
  \draw[->, thin, draw=AccessibilityColor] (group11.east) to [out=0, in=180] (accessible_models.west);
  
  \draw[->, thin, draw=DataManagementColor] (data_management.east) to [out=0, in=180] (group12.west);
  \draw[->, thin, draw=AccessibilityColor] (group12.east) to [out=0, in=180] (accessible_models.west);
  
  \draw[->, thin, draw=ExploratoryDataAnalysisColor] (exploratory_data_analysis.east) to [out=0, in=180] (group13.west);
  \draw[->, thin, draw=AccessibilityColor] (group13.east) to [out=0, in=180] (accessible_models.west);
  
  \draw[->, thin, draw=AssessmentColor] (assessing_results.east) to [out=0, in=180] (group15.west);
  \draw[->, thin, draw=DSLUnderstandingColor] (group15.east) to [out=0, in=180] (dsl_understanding.west);
  
  \end{tikzpicture}
  \caption{\textbf{An Overview of How PFMs Improve Data Analysis.} Updated figure showing the relationships between data analysis tasks and PFM-enabled optimizations with citations from chapters 2 and 3.}
  
  \end{figure*}"""
    
    return tex_content

def main():
    """Main function to process the manuscript and generate the tree graph"""
    
    # Read the manuscript file
    try:
        with open('manuscript_merged.tex', 'r', encoding='utf-8') as f:
            manuscript_content = f.read()
    except FileNotFoundError:
        print("Error: manuscript_merged.tex not found")
        return
    
    # Extract chapters 2 and 3
    chapter2_content, chapter3_content = extract_chapters_2_3(manuscript_content)
    
    if not chapter2_content or not chapter3_content:
        print("Error: Could not extract chapter content")
        return
    
    # Extract citations from both chapters
    chapter2_citations = extract_citations_from_text(chapter2_content)
    chapter3_citations = extract_citations_from_text(chapter3_content)
    
    # Combine all citations
    all_citations = chapter2_citations.union(chapter3_citations)
    
    print(f"Found {len(all_citations)} unique citations in chapters 2 and 3:")
    for citation in sorted(all_citations):
        print(f"  - {citation}")
    
    # Map citations to groups
    grouped_citations, ungrouped_citations = map_citations_to_groups(all_citations)
    
    print(f"\nGrouped citations:")
    for group, cites in grouped_citations.items():
        print(f"  {group}: {cites}")
    
    if ungrouped_citations:
        print(f"\nUngrouped citations: {sorted(ungrouped_citations)}")
    
    # Generate the tree graph TEX content
    tree_graph_content = generate_tree_graph_tex(grouped_citations, ungrouped_citations)
    
    # Write to output file
    try:
        with open('Tree_graph_updated.tex', 'w', encoding='utf-8') as f:
            f.write(tree_graph_content)
        
        print(f"\nTree_graph_updated.tex has been generated successfully!")
        print("You can now use this file to replace the Tree_graph.tex in your document.")
        
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    main()