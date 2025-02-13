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

## Make a contribution
### Find a task to work on
The best place to start is taking a look at opening issues where we publish general directions and specific tasks. We categorize the types of issues following the classic "epic, feature and task" practice.

**epic**: top-level issues stating a general direction and long-term objective.
**feature**: major functional area, help organize related tasks (complete in weeks/months)
**task**: specific, actionable work items (complete in days/weeks)

An issue has title in the format of "[X, Y] Z". Where X \n {epic, feature, task} and Y \in {research, engineering}. And Z is a short description of the issue. 

Issues of different types generally have content in different formats. See examples like [this](https://github.com/don-tpanic/github-playground/issues/1) and [this](https://github.com/don-tpanic/github-playground/issues/3). For generic issue templates, see `ISSUE_TEMPLATE/`.

Do make sure you read the issue description carefully before start working on it! Ask clarification questions (commenting below the issue) is highly encouraged!

### Make a pull request (PR) 
Make a pull request (PR) to submit your solution to a task.

Depending on the exact task you are working on, the required outputs may vary. In general, we expect contributors to briefly explain what they have done in the PR to help us understand their contributions. Here is an example about contributing a new algorithm for creating alternative results ([example](https://github.com/don-tpanic/github-playground/pull/7)).

A general PR template can be found [here](https://github.com/don-tpanic/github-playground/pull/7).

### Code standard
TBD

## A note for contributors
This project is inherently exploratory—roles and priorities may shift as we learn! Whether you’re drawn to algorithm design, neuroscience validation, or tool-building, there’s room to collaborate across teams. Early stages will emphasize research, but we’ll gradually transition polished components into engineering streams.
