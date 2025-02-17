# Contributor roles
As an exploratory and evolving project, we expect the structure of contributor roles to adapt over time. Below, we outline the key roles and areas of specialization to help contributors identify where they can best contribute. We also recognize that roles may overlap, and we encourage contributors to engage in one or more areas of the project as appropriate.

## Two teams: Generator and Evaluator
* Team-Generator: Experts in machine learning and LLMs to develop novel methods for generating experimental outcomes from neuroscience studies. The first task is to extract a KG from papers. A second, more demanding, task is to generate a set of alternative results.

* Team-Evaluator: Neuroscience specialists to validate the feasibility and scientific accuracy of the generated outcomes. This team will develop a test set (akin to BrainBench) and supporting code to evaluate the Generators’ results.
 
## Two streams: Research and Engineering
In addition to the two teams, contributor activities can generally be grouped into two streams:

### Research Stream:
- Typical Tasks: Develop novel algorithms, consult relevant literature for new ideas, or conduct exploratory studies.
- Deliverables: These tasks typically result in self-contained directories (such as Jupyter notebooks) that address specific research problems or propose innovative solutions.

### Engineering Stream:
- Typical Tasks: Focus on improving code quality and efficiency, particularly when algorithms from the Research stream need to be implemented as part of a stable software release for end users.
- Deliverables: This stream produces code that is production-ready, ensuring that research outputs are efficiently translated into stable, functional systems.

# Make a contribution
## Find an existing task to work on
We organize tasks to work on using issues. These issues are treated as announcements which describe a general direction or specifc tasks that requirement investigation. We categorize annoucement issues as **epics**, **features**, or **tasks**.

* **epic**: top-level issues stating a general direction and long-term objective.
* **feature**: major functional area, help organize related tasks (complete in weeks/months)
* **task**: specific, actionable work items (complete in days/weeks)

Each issue title follows the format: `[X, Y] Z` where:
- `X ∈ {epic, feature, task}`
- `Y ∈ {research, engineering}`
- `Z` is a short description of the issue.

For example, [this](https://github.com/don-tpanic/github-playground/issues/1) is an epic and [this](https://github.com/don-tpanic/github-playground/issues/3) is a task. 

Do make sure you read the issue description carefully before start working on it! Ask clarification questions (commenting below the issue) is highly encouraged!

## Opening new epics, features or tasks
Most contributors won't need to create epics or features, though their input is welcome. Instead, they are more likely to create tasks and we ask contributors to ensure issues are placed in the correct hierarchy.

## Opening new issues for all other purposes
For bugs, questions, or issues related to existing code or materials, file them as you would in any GitHub repo. Whenever possible, create them under specific tasks (see example TODO).

Issue templates can be found in `ISSUE_TEMPLATE/`.

## Make a pull request (PR) 
Make a pull request (PR) to submit your solution to a task.

Depending on the exact task you are working on, the required outputs may vary. In general, we expect contributors to briefly explain what they have done in the PR to help us understand their contributions. Here is an example about contributing a new algorithm for creating alternative results ([example](https://github.com/don-tpanic/github-playground/pull/7)).

PR templates can be found in `PULL_REQUEST_TEMPLATE/`.

## On-going tasks
| Team      | Stream   | Task                                      | Issues | PR Template |
|-----------|---------|-------------------------------------------|--------|-------------|
| generator | research | develop new algos                        | #      | [Template](#) |
| evaluator | research | develop ground truth labels             | #      | [Template](#) |
| evaluator | research | develop automated evaluation pipelines  | #      | [Template](#) |

## Structure your code
```
.
├── papers
│   └── <doi>
│       ├── eval_<eval_uid>_<algo_id>_<alt_id>_<etc>.json
│       ├── gen_<gen_uid>_<algo_id>_<alt_id>.json
│       └── original_paper.txt
└── src
    ├── generators
    │   ├── <gen_uid>
    │   │   └── __init__.py
    │   └── main.py
    └── evaluators
        ├── <eval_uid>
        │   └── __init__.py
        └── main.py
```
Above is the general structure of this code base. Your code should be self-contained and placed under the right team, i.e., `src/generators/` or `src/evaluators/`. Do make sure your code can be executed according to required procedure and the outputs produced by your code are formated, named and saved according to requirements (see corresponding task issues for details). 

As an entry-point, 

* For generator contributions, `python -m src.generators.main --doi <doi> --gen-uid <gen-uid>` should produce outputs in the required format and save outputs under `papers/<doi>/` with the correct naming requirements.
* For evaluator contributions `python -m src.evaluators.main --doi <doi> --eval-uid <eval-uid> --gen-outputs-path <gen-outputs-path>` should produce outputs in the required format and saves outputs under `paper/<doi>` with the correct naming requirements.

## Code standard
TODO

# A note for contributors
This project is inherently exploratory—roles and priorities may shift as we learn! Whether you’re drawn to algorithm design, neuroscience validation, or tool-building, there’s room to collaborate across teams. Early stages will emphasize research, but we’ll gradually transition polished components into engineering streams.
