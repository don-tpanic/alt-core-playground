# AltCore: Core functionalities for creating and validating alternative results of experimental studies

<!-- START_STATS -->
Total papers analyzed: <!-- PAPER_COUNT -->
Total alternatives generated: <!-- GEN_COUNT -->
Total evaluations done: <!-- EVAL_COUNT -->
<!-- END_STATS -->

## Premises and mission
The background of the current project is based on previously [published results](https://www.nature.com/articles/s41562-024-02046-9). Two key premises for us are:
1. LLMs can extract key patterns from a noisy scientific literature, 
2. Their predictions are calibrated, which opens the door to assigning probabilities to possible outcomes of studies.

Our big picture objective is to develop automated systems to predict and rank plausible experimental outcomes before scientists conduct resource-intensive experiments. Such tools would generate a comprehensive space of potential results based on preliminary hypotheses and methods, accelerating scientific discovery.

## Current project goal
We aim to explore and validate the idea that it is possible to generate scientifically viable alternative results from published research. We aim to automate the process of generation as well as validation by incorporating both ML-based evaluations and expert feedback to assess feasibility and accuracy.

## Methods
To achieve this, our current idea is using large language models (LLMs) to extract knowledge graphs (KGs) from neuroscience articles. KGs represent key entities (e.g., brain regions) as nodes and represent relationships among nodes in terms of edges. Once we build a KG, we can alter it in several ways to detail a range of alternative results for a study. [Ken](https://github.com/don-tpanic) has made one quick attempt at this ([repo](https://github.com/braingpt-lovelab/knowledge-graph-algo)). It is by no means perfect, but hopefully, you will find inspirations from his attempt and perhaps reuse pieces of his code in your solutions.

## Contributing
This project is inherently exploratory—roles and priorities may shift as we learn! Whether you’re drawn to algorithm design, neuroscience validation, or tool-building, there’s room to collaborate across teams. Early stages will emphasize research, but we’ll gradually transition polished components into engineering streams. We appreciate all contributions. 

To learn about how to make contributions, kindly refer to the contribution page [here](https://github.com/don-tpanic/alt-core-playground/blob/main/CONTRIBUTING.md).

## Ongoing tasks overview
Below is a list of tasks we’re working on and seeking contributors to help with. This provides an overview, but if you're considering contributing, please refer to the contribution page for detailed instructions.

| Team      | Stream   | Feature                                      | Tasks |
|-----------|---------|-------------------------------------------|--------|
| generator | research | develop new algos to create alternative results ([#2](https://github.com/don-tpanic/alt-core-playground/issues/2))                        | [#3](https://github.com/don-tpanic/alt-core-playground/issues/3), [#4](https://github.com/don-tpanic/alt-core-playground/issues/4)      |
| evaluator | research | Validate generated results against ground truth, develop ground truth ([#5](https://github.com/don-tpanic/alt-core-playground/issues/5))             | [#11](https://github.com/don-tpanic/alt-core-playground/issues/11)      |
| evaluator | research | develop automated evaluation pipelines  | [#5](https://github.com/don-tpanic/alt-core-playground/issues/5)      |


## Communications
* GitHub Issues: see [contribution page](https://github.com/don-tpanic/alt-core-playground/blob/main/CONTRIBUTING.md).
* Discord for daily communications, discussions: [![Discord](https://img.shields.io/discord/YOUR_SERVER_ID?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/gfSWCRQR6V)
* Website for new releases: [![Website](https://img.shields.io/badge/Website-BrainGPT-blue?style=flat-square&logo=globe)](https://braingpt.org/)

## The Team
TODO

## License and IP
TODO
