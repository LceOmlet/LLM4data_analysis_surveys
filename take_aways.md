# PFMs are benificial to long tail data analysis tasks

[1] Fernandez, R.C., Elmore, A.J., Franklin, M.J., Krishnan, S., & Tan, C. (2023). How Large Language Models Will Disrupt Data Management. Proc. VLDB Endow., 16, 3302-3309.

Tasks has not translated to data integration and other "hard-to-formalize" problems that we consider core to data management and our community.

PFMs offer a new tool to ameliorate the semantic ambiguity problem. 

They will assist in providing code snippets to solve the many "easy” cases at the tail, thus reducing the need for hand-holding and increasing the cases where integration is automated.

# Accessible data needs more

[2] BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval. ICLR 2025

Unstructured retrieval piplines should adopt hybrid methods with both keyword based retrieval and vector retrieval. There are opporunities for researches about reasoning-intensive retrieval to gain higher performance. 

I.e., While more accessible, RAG applications still need a fairly large dataset and an more powerfull infrastructure for the retrieval process.

# The choice of knowledge representation building and selection.

[3] In-depth Analysis of Graph-based RAG in a Unified Framework

Finer granularity boosts performance of retrieving rare patterns, out-of-domain data but can introduce structural error with unessary operations.

# Assessment of PFM based DA.

[4] When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs. Trans. Assoc. Comput. Linguistics 12: 1417-1440 (2024)

PFMs can process intermediate, complex structrued evaluation results, even if they are long tail distributed, e.g. code debugging messages.

# Correction of incomsistencies and incomplete knowledge about the system

[5] Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu, Xian Li, Asli Celikyilmaz, and Jason Weston. 2023. Chain-of-verification reduces hallucination in large language models. arXiv preprint arXiv:2309.11495.

Generated responses include multiple answers, but the feedback generation can be decomposed into easier sub-tasks of verifying each answer. Tasks with decomposable responses are one of the few groups of tasks for which verification is clearly easier than generation, which enables intrinsic self-correction. However, many real-world tasks do not satisfy this property.

# Explorational data analysis.

[6] LLMOPT: Learning to Define and Solve General Optimization Problems from Scratch

PFMs define and optimize problems, which would benifitial to build up more powerful EDA intrastuctures. PFMs that come up with definitions which minimize contradictions with records can be used to boarder applications such as model view creating, index building etc.

# Implementation

[7] Facilitating Multi-turn Function Calling for LLMs via Compositional Instruction Tuning

[8] Attentional Composition Networks for Long-Tailed Human Action Recognition
[9] Revealing the Proximate Long-Tail Distribution in Compositional Zero-Shot
Learning

Compositional tasks are more easier to implement and evaluate, especially for long tail and rare tasks.

