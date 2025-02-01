# AltCore: Core functionalities for creating and validating alternative results of experimental studies

## Premises and mission
The background of the current project is based on previously [published results](https://www.nature.com/articles/s41562-024-02046-9). Two key premises for us are:
1. LLMs can extract key patterns from a noisy scientific literature, 
2. Their predictions are calibrated, which opens the door to assigning probabilities to possible outcomes of studies.

Our big picture objective is to develop automated systems to predict and rank plausible experimental outcomes before scientists conduct resource-intensive experiments. Such tools would generate a comprehensive space of potential results based on preliminary hypotheses and methods, accelerating scientific discovery.

## Current project goal
We aim to explore and validate the idea that it is possible to generate scientifically viable alternative results from published research. We aim to automate the process of generation as well as validation by incorporating both ML-based evaluations and expert feedback to assess feasibility and accuracy.

## Methods
To achieve this, our current idea is using large language models (LLMs) to extract knowledge graphs (KGs) from neuroscience articles. KGs represent key entities (e.g., brain regions) as nodes and represent relationships among nodes in terms of edges. Once we build a KG, we can alter it in several ways to detail a range of alternative results for a study. [Ken](https://github.com/don-tpanic) has made one quick attempt at this ([repo](https://github.com/braingpt-lovelab/knowledge-graph-algo)). It is by no means perfect, but hopefully, you will find inspirations from his attempt and perhaps reuse pieces of his code in your solutions.
