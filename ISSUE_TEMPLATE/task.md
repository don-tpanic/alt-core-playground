### General method 
To obtain possible alternative results of an experiment, one idea is to construct a knowledge graph (KG) that captures key entities such as brain regions (as nodes) and relationships such as effects (as edges) of a study. Once we build a KG, we can alter it in several ways to detail a range of alternative results for a study. 

For altering nodes (e.g., swapping brain regions in the conclusion, similar to a number of [BrainBench](https://github.com/braingpt-lovelab/brainbench_testcases/tree/89869dab3be1ec096dc38931ea33e43268c65d30) test cases). Current idea is to rely on LLMs to identify nodes from a KG that belongs to the same semantic group (e.g., brain regions, test treatments) and permute nodes within the same group.

### Task
Taking the general method as a rough guidance, develop algorithms that automatically builds KGs from published neuroscience papers. Alternate the KGs and obtain alternative results in natural language.

### Validation
<State what methods will be used to validate the output of this task>

### Expected outputs
<Make clear what is the expected output and its format.>

### Submit your solution via a PR
<optional: if you have provided a solution to this task, you could point other contributors to your PR as an example!>