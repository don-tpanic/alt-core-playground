# Contributor Guide

## Table of Contents

- [Contributor roles](#contributor-roles)
  - [Two teams: Generator and Evaluator](#two-teams-generator-and-evaluator)
  - [Two streams: Research and Engineering](#two-streams-research-and-engineering)
    - [Research Stream](#research-stream)
    - [Engineering Stream](#engineering-stream)
- [Make a contribution](#make-a-contribution)
  - [Find an existing task to work on](#find-an-existing-task-to-work-on)
  - [Opening new epics, features or tasks](#opening-new-epics-features-or-tasks)
  - [Opening new issues for all other purposes](#opening-new-issues-for-all-other-purposes)
  - [Make a pull request (PR)](#make-a-pull-request-pr)
  - [On-going tasks](#on-going-tasks)
  - [Codebase Walkthrough](#codebase-walkthrough)
  - [Code standard](#code-standard)
- [Quickstart](#quickstart)
  - [Setup a virtual environment](#setup-a-virtual-environment)
  - [End-to-end examples](#end-to-end-examples)
- [A note for contributors](#a-note-for-contributors)

# Contributor roles

As an exploratory and evolving project, we expect the structure of contributor roles to adapt over time. Below, we outline the key roles and areas of specialization to help contributors identify where they can best contribute. We also recognize that roles may overlap, and we encourage contributors to engage in one or more areas of the project as appropriate.

## Two teams: Generator and Evaluator

- Team-Generator: Experts in machine learning and LLMs to develop novel methods for generating experimental outcomes from neuroscience studies. The first task is to extract a KG from papers. A second, more demanding, task is to generate a set of alternative results.

- Team-Evaluator: Neuroscience specialists to validate the feasibility and scientific accuracy of the generated outcomes. This team will develop a test set (akin to [BrainBench](https://huggingface.co/datasets/BrainGPT/BrainBench_Human_v0.1.csv)) and supporting code to evaluate the Generators' results.

## Two streams: Research and Engineering

In addition to the two teams, contributor activities can generally be grouped into two streams:

### Research Stream:

- Typical Tasks: Develop novel algorithms, consult relevant literature for new ideas, or conduct exploratory studies.
- Deliverables: These tasks typically result in self-contained directories that address specific research problems or propose innovative solutions.

### Engineering Stream:

- Typical Tasks: Focus on improving code quality and efficiency, particularly when algorithms from the Research stream need to be implemented as part of a stable software release for end users.
- Deliverables: This stream produces code that is production-ready, ensuring that research outputs are efficiently translated into stable, functional systems.

# Make a contribution

## Find an existing task to work on

We organize tasks to work on using issues. These issues are treated as announcements which describe a general direction or specifc tasks that requirement investigation. We categorize annoucement issues as **epics**, **features**, or **tasks**.

- **epic**: top-level issues stating a general direction and long-term objective.
- **feature**: major functional area, help organize related tasks (complete in weeks/months)
- **task**: specific, actionable work items (complete in days/weeks)

Each issue title follows the format: `[X, Y] Z` where:

- `X ∈ {epic, feature, task}`
- `Y ∈ {research, engineering}`
- `Z` is a short description of the issue.

For example, [this](https://github.com/don-tpanic/alt-core-playground/issues/1) is an epic and [this](https://github.com/don-tpanic/alt-core-playground/issues/3) is a task.

Do make sure you read the issue description carefully before start working on it! Ask clarification questions (commenting below the issue) is highly encouraged!

## Opening new epics, features or tasks

Most contributors won't need to create epics or features, though their input is welcome. Instead, they are more likely to create tasks and we ask contributors to ensure issues are placed in the correct hierarchy.

## Opening new issues for all other purposes

For bugs, questions, or issues related to existing code or materials, file them as you would in any GitHub repo. Whenever possible, create them under specific tasks (see example TODO).

Issue templates can be found in `/github/ISSUE_TEMPLATE/`.

## Make a pull request (PR)

Make a pull request (PR) to submit your work addressing task.

Depending on the exact task you are working on, the required outputs may vary. In general, we expect contributors to briefly explain what they have done in the PR to help us understand their contributions. Here is an example about contributing a new algorithm for creating alternative results ([example](https://github.com/don-tpanic/alt-core-playground/pull/7)).

PR templates can be found in `/github/PULL_REQUEST_TEMPLATE/`.

## On-going tasks

| Team      | Stream   | Feature                                                                                                                                  | Tasks                                                                                                                              |
| --------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| generator | research | develop new algos to create alternative results ([#2](https://github.com/don-tpanic/alt-core-playground/issues/2))                       | [#3](https://github.com/don-tpanic/alt-core-playground/issues/3), [#4](https://github.com/don-tpanic/alt-core-playground/issues/4) |
| evaluator | research | Validate generated results against ground truth, develop ground truth ([#5](https://github.com/don-tpanic/alt-core-playground/issues/5)) | [#11](https://github.com/don-tpanic/alt-core-playground/issues/11)                                                                 |
| evaluator | research | develop automated evaluation pipelines                                                                                                   | [#5](https://github.com/don-tpanic/alt-core-playground/issues/5)                                                                   |

## Codebase walkthrough

```
.
├── papers
│   └── <doi>
│       ├── eval_<eval_uid>_<algo_id>_<model_id>_<etc>.json
│       ├── gen_<gen_uid>_<algo_id>_<model_id>_<etc>.json
│       ├── original_paper.txt
│       ├── label_<uid>_kg_original.json
|       └── label_<uid>_kg_perm_<index>.json
└── src
    ├── generators
    │   ├── <gen_uid>
    │   │   └── __init__.py
    │   └── main.py
    ├── llm
    │   ├── __init__.py
    │   └── caller.py
    └── evaluators
        ├── <eval_uid>
        │   └── __init__.py
        └── main.py
```

### [papers/](https://github.com/don-tpanic/alt-core-playground/tree/main/papers/)

- `original_paper.txt`: the original paper content.
- `label_*.json`: manually created KGs of original or alternative results by human experts.
- `gen_*.json`: generated content by running alternative results generation algorithms developed in `src/generators/`
- `eval_*.json`: generated or manually created content which are evaluation results produced by algorithms in `src/evaluators/` or feedback provided manually by experts.
  All `label_*.json`, `gen_*.json` and `eval_*.json` files are assigned unique identifiers that allow us to track down contributors, their teams, the version of their algorithms and the specific alternative results.

### [src/generators/](https://github.com/don-tpanic/alt-core-playground/tree/main/src/generators)

- `<gen_uid>`: A self-contained contributor directory where all code being developed to generate alternative results lives. Each contributor has its own directory with `uid` created by themselves.
- `main.py`: Entry-point for running any contributor's solutions on given papers. For generator contributions,
  ```
  python -m generators.main \
    --doi <doi> \
    --gen-uid <your-unique-team-generator-id> \
    --algo-name <algo-name> \
    --llm <llm-name>
  ```
  - The above command should produce outputs in the required format and save outputs under `papers/<doi>/` with the correct naming requirements.
  - See an end-to-end toy example below, under [quickstart](#quickstart)

### [src/llm/](https://github.com/don-tpanic/alt-core-playground/tree/main/src/llm)

- `caller.py`: A module for calling LLMs.

### [src/evaluators/](https://github.com/don-tpanic/alt-core-playground/tree/main/src/evaluators)

- `<eval_uid>`: A self-contained contributor directory where all code being developed to evaluate alternative results lives. Each contributor has its own directory with `uid` created by themselves.
- `main.py`: Entry-point for running any contributor's solutions on given papers and their generated alternative results. For evaluator contributions,
  ```
  python -m evaluators.main \
    --doi <doi> \
    --eval-uid <eval-uid> \
    --gen-outputs-path <gen-outputs-path>
  ```
  - The above command should produce outputs in the required format and saves outputs under `paper/<doi>/` with the correct naming requirements.
  - `<gen-outputs-path>` represent existing generated outputs produced by team-generator contributors. \*
  - Any existing outputs can be found in `paper/<doi>/gen_*.json` and you should replace `<gen-outputs-path>` with an actual `gen_*.json`. This way, each evaluation is uniquely
    coded by a generator contributor & evaluator contributor.

Do make sure your code can be executed according to required procedure and the outputs produced by your code are formated, named and saved according to requirements (see corresponding task issues for details).

## Code standard

When making LLM calls, we strongly encourage using Pydantic schemas to validate and structure responses. This approach:

- Reduces the need for response parsing/cleaning
- Minimizes the chance of receiving malformed data
- Makes the expected response format explicit

You can:

1. Use existing schemas from `src/generators/ken_c137/prompts/response_models.py`
2. Create new Pydantic classes for your specific needs
3. Make direct LLM calls without schemas (not recommended)

Example using a schema:

```python
from llm.caller import ask_llm_with_schema
from .prompts.response_models import KGAsText

response, cost = ask_llm_with_schema(
    llm="azure/gpt-4",
    sys_prompt="You are a helpful assistant",
    user_prompt="Summarize this text...",
    output_class=KGAsText
)
# response will be a KGAsText object with validated fields
```

Example without a schema:

```python
from llm.caller import ask_llm

response, cost = ask_llm(
    llm="azure/gpt-4",
    sys_prompt="You are a helpful assistant",
    user_prompt="Summarize this text..."
)
# response will be a raw string that needs parsing
```

# Quickstart

## Setup a virtual environment

1. Create and activate a virtual environment:

```
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

2. Install the package with development dependencies:

```
pip install -e ".[dev]"
```

3. Set up environment variables for LLM access:

```
cp .env.example .env
```

Then edit `.env` to add your API key(s). You only need to configure the variables for the LLM you plan to use with the `--llm` argument:

- For OpenAI models (e.g., `--llm openai/gpt-4`):

  - `OPENAI_API_KEY`: Your OpenAI API key

- For Azure models (e.g., `--llm azure/gpt-4`):
  - `AZURE_API_KEY`: Your Azure API key
  - `AZURE_API_BASE`: Your Azure API base URL
  - `AZURE_API_VERSION`: Your Azure API version

Without the appropriate environment variables configured, you won't be able to make API calls to your chosen LLM.

## End-to-end examples 
### Example 1: contributing ground truth labels as domain experts.
1. Read through [README.md](https://github.com/don-tpanic/alt-core-playground/blob/main/README.md) and [CONTRIBUTING.md](https://github.com/don-tpanic/alt-core-playground/blob/main/CONTRIBUTING.md) to get basic information.
2. Decide to work on task [#11](https://github.com/don-tpanic/alt-core-playground/issues/11) and understand the expected outputs and formating requirements.
3. Fork the repo and create a local branch to work on the task.
   ```
   git clone git@github.com:don-tpanic/alt-core-playground.git
   ```
   ```
   git checkout -b <your-unique-branch-name>
   ```
4. Find a paper you want to work on. If you want to work on an existing paper, simply go to `papers/<doi>`. If you want to introduce a new paper,
   ```
   cd papers
   mkdir <paper-doi>
   ```
5. Save your work:
   The KG corresponds to the paper's original result should be saved as `label_<uid>_kg_original.json` and KGs represent alternative patterns of results should be saved as `label_<uid>_kg_perm_<index>.json` where `index` is to identify different    possible alternative patterns.
6. Make a pull request (PR) to submit your work!

### Example 2: contributing code for KG generation algorithm as ML researchers/engineers.
1. Read through [README.md](https://github.com/don-tpanic/alt-core-playground/blob/main/README.md) and [CONTRIBUTING.md](https://github.com/don-tpanic/alt-core-playground/blob/main/CONTRIBUTING.md) to get basic information.
2. Decide to work on task [#3](https://github.com/don-tpanic/alt-core-playground/issues/3) and understand the expected outputs and formating requirements.
3. Fork the repo and create a local branch to work on the task.
   ```
   git clone git@github.com:don-tpanic/alt-core-playground.git
   ```
   ```
   git checkout -b <your-unique-branch-name>
   ```
   
4. Create a self-contained contributor directory:
   ```
   cd src/generators
   mkdir <your-unique-team-generator-id>
   ```
   e.g., `mkdir ken_c137` (which already exists)
5. Choose a paper to work on from `papers/<doi>/`, e.g., `10.1016:j.cognition.2020.104244`
6. Develop your code inside of `<your-unique-team-generator-id>/`. Make sure you expose a `run` function which will execute your code and return formated outputs. Import `run` in `<your-unique-team-generator-id>/__init__.py`.
   For a concrete example, check out `ken_c137/__init__.py`

   ```python
    from .kg_pipeline import run

    __all__ = ["run"]
   ```

7. Execute your code to obtain and save results
   ```
   python -m generators.main \
    --doi <doi> \
    --gen-uid <your-unique-team-generator-id> \
    --algo-name <algo-name> \
    --llm <llm-name>
   ```
   e.g., `python -m generators.main --doi 10.1016:j.cognition.2020.104244 --gen-uid ken_c137 --algo-name algo1 --llm openai/gpt-4o-2024-08-06` (will execute the toy example).
8. By executing the command above, you save your results in desired format at the right location, e.g., `papers/10.1016:j.cognition.2020.104244/gen_ken_c137_algo1_openai-gpt-4o-2024-08-06.json`
9. Make a pull request (PR) to submit the work.

# A note for contributors

This project is inherently exploratory—roles and priorities may shift as we learn! Whether you're drawn to algorithm design, neuroscience validation, or tool-building, there's room to collaborate across teams. Early stages will emphasize research, but we'll gradually transition polished components into engineering streams.
