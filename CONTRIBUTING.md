## Premises and mission
The background of the current project is based on previously [published results](https://www.nature.com/articles/s41562-024-02046-9). Two key premises for us are:
1. LLMs can extract key patterns from a noisy scientific literature, 
2. Their predictions are calibrated, which opens the door to assigning probabilities to possible outcomes of studies.

Our big picture objective is to develop automated systems to predict and rank plausible experimental outcomes before scientists conduct resource-intensive experiments. Such tools would generate a comprehensive space of potential results based on preliminary hypotheses and methods, accelerating scientific discovery.

## Current project goal
We aim to explore and validate the idea that it is possible to generate scientifically viable alternative results from published research. We aim to automate the process of generation as well as validation by incorporating both ML-based evaluations and expert feedback to assess feasibility and accuracy.

## Methods
To achieve this, our current idea is using large language models (LLMs) to extract knowledge graphs (KGs) from neuroscience articles. KGs represent key entities (e.g., brain regions) as nodes and represent relationships among nodes in terms of edges. Once we build a KG, we can alter it in several ways to detail a range of alternative results for a study. [Ken](https://github.com/don-tpanic) has made one quick attempt at this ([repo](https://github.com/braingpt-lovelab/knowledge-graph-algo)). It is by no means perfect, but hopefully, you will find inspirations from his attempt and perhaps reuse pieces of his code in your solutions.

## Contributor roles
As an exploratory and evolving project, we expect the structure of contributor roles to adapt over time. Below, we outline the key roles and areas of specialization to help contributors identify where they can best contribute. We also recognize that roles may overlap, and we encourage contributors to engage in one or more areas of the project as appropriate.

### Two teams: Generator and Evaluator
* Team-Generator: Experts in machine learning and LLMs to develop novel methods for generating experimental outcomes from neuroscience studies. The first task is to extract a KG from papers. A second, more demanding, task is to generate a set of alternative results.

* Team-Evaluator: Neuroscience specialists to validate the feasibility and scientific accuracy of the generated outcomes. This team will develop a test set (akin to BrainBench) and supporting code to evaluate the Generators’ results.
 
### Two streams: Research and Engineering
In addition to the two teams, contributor activities can generally be grouped into two streams:

#### Research Stream:
- Typical Tasks: Develop novel algorithms, consult relevant literature for new ideas, or conduct exploratory studies.
- Deliverables: These tasks typically result in self-contained directories (such as Jupyter notebooks) that address specific research problems or propose innovative solutions.

#### Engineering Stream:
- Typical Tasks: Focus on improving code quality and efficiency, particularly when algorithms from the Research stream need to be implemented as part of a stable software release for end users.
- Deliverables: This stream produces code that is production-ready, ensuring that research outputs are efficiently translated into stable, functional systems.

## A note for contributors
This project is inherently exploratory—roles and priorities may shift as we learn! Whether you’re drawn to algorithm design, neuroscience validation, or tool-building, there’s room to collaborate across teams. Early stages will emphasize research, but we’ll gradually transition polished components into engineering streams.
