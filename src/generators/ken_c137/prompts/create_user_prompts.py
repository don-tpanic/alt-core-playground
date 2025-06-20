"""Create user prompts."""


def summarize_methods(paper_text: str) -> str:
    """Summarize the methods used in the first study/experiment in the paper.

    Args:
        paper_text: The full paper text.

    Returns:
        A string of the prompt.
    """
    prompt = f"""
        Now, you are reading a paper, and you want to summarize the methods used in the first study/experiment in this paper in a few sentences.

        Here is the full paper: {paper_text}

        You should return your answer as a json such as:
        {{
            "methods": your_summary
        }}

        Please summarize the methods:
    """  # noqa: E501
    return prompt


def summarize_results_as_sentences(paper_text: str) -> str:
    """Summarize the results in the paper in a few sentences.

    Args:
        paper_text: The full paper text.

    Returns:
        A string of the prompt.
    """
    prompt = f"""
        Now, you are reading a paper, and you want to summarize the results in this paper in a few sentences.
        Be careful about the granularity of the results, only include the findings presented by the paper.

        Often a paper presents results from multiple experiments, if that is the case, make sure you summarize the results by experiment.

        Here is the full paper: {paper_text}

        You should return your answer as a json such as:
        {{
            "results": {{
                "experiment_1": your summary in a few sentences,
                "experiment_2": your summary in a few sentences,
                ...
            }}
        }}

        Please summarize the results:
    """  # noqa: E501
    return prompt


def create_alternative_results_as_sentences_single_experiment(
    paper_text: str, original_results: str
) -> str:
    """Create alternative results as sentences.

    Args:
        paper_text: The full paper text.
        original_results: The original results as a string.
    """
    prompt = f"""
        Now, you are reading a paper,
        As a critical thinker, you are always curious about whether different results could have been obtained following the same methods and experiments.

        You should come up with alternative patterns of results significantly different, even contradictory to the original results presented in the paper. The alternative results do not have to be the exact opposite of the original results, but they should be different enough. However the alternative results should always  be plausible and consistent with the methods and experiments in the paper.

        Here is the full paper: {paper_text}

        Here are the original results as your reference for style: {original_results}. Write the alternative results in the same way as if they were the original results. Avoid using terms such as "unexpectedly", "surprisingly", "contrary to", etc. State them as if they were the actual results.

        You should return your answer as a json such as:
        {{
            "alternative_results": your summary in a few sentences
        }}
    """  # noqa: E501
    return prompt


class KnowledgeGraphCreator:
    """A series of prompts to create a knowledge graph from a paper.

    Creates prompts to generate a knowledge graph from a paper and perform
    permutations to get sensible alternative results within the search space
    of the paper.

    The process consists of two steps:
        1. create_initial_kg: Create a knowledge graph from the full paper
        2. identify_semantic_groups: Group nodes into semantic groups/categories
           and note the level of granularity of each node
    """

    def __init__(self, paper_text: str) -> None:
        """Initialize the KnowledgeGraphCreator.

        Args:
            paper_text: The full paper text.
        """
        self.paper_text = paper_text

    def create_initial_kg(self) -> str:
        """Create an initial knowledge graph.

        Returns:
            A string of the prompt.
        """
        prompt = f"""
            Now, you are reading a paper, as follows: {self.paper_text}.

            Now you want to construct a knowledge graph of the results of the first study/experiment only.
            Make sure you always label every edge and node.
            It is important to correctly represent the relationships between the nodes.

            You should return your answer as a json such as below, respect the keys.
            {{
                "knowledge_graph": {{
                    "experiment_1": {{
                        "nodes": [{{"id": 1, "label": "node1"}}, {{"id": 2, "label": "node2"}}, ...],
                        "edges": [{{"source": 1, "target": 2, "relation": "edge1"}}, {{"source": 2, "target": 3, "relation": "edge2"}}, ...]
                    }},
                }}
            }}

            Please create the knowledge graph:
        """  # noqa: E501
        return prompt

    def identify_semantic_groups(self, initial_kg: str) -> str:
        """Identify semantic groups.

        Args:
            initial_kg: The initial knowledge graph.

        Returns:
            A string of the prompt.
        """
        prompt = f"""
            Now, you are reading a paper, and you have constructed a knowledge graph for the results of the first study/experiment as follows: {initial_kg}.

            Now focus on all the nodes and group them into semantic groups/categories.
            Notice, nodes belonging to the same group might have hierarchical relationships due to difference in granularity or abstraction level. When grouping, make sure to note the level of granularity of each node.
            The top level is 1 and the level increases as the granularity decreases.

            You should return your answer as a json such as:
            {{
                "semantic_groups": {{
                    "experiment_1": {{
                        "group_name_1": [{{"id": 1, "label": "node1", "level": "granularity_level"}}, {{"id": 2, "label": "node2", "level": "granularity_level"}}, ...],
                        "group_name_2": [{{"id": 1, "label": "node1", "level": "granularity_level"}}, {{"id": 2, "label": "node2", "level": "granularity_level"}}, ...],
                    }}
                }}
            }}
        """  # noqa: E501
        return prompt

    def convert_kg_to_text_single_experiment(
        self, kg: str, orig_results_as_example: str | None = None
    ) -> str:
        """Convert a knowledge graph to text.

        Args:
            kg: The knowledge graph.
            orig_results_as_example: The original results as a string.

        Returns:
            A string of the prompt.
        """
        if (
            orig_results_as_example is None
        ):  # Do not use example; this is when converting orig kg to text
            prompt = f"""
                From this knowledge graph, write a brief paragraph describing the results of main study/experiment.
                Write the paragraph in standard prose, You are describing the results of a scientific paper to others. Do not refer to the knowledge graph in your answer.
                Also only describe the results. Do not provide theoretical interpretations of the results.

                Here is the knowledge graph: {kg}

                You should return your answer as a json such as:
                {{
                    "results": your summary in a few sentences
                }}

                Please convert the knowledge graph back to sentences:
            """  # noqa: E501
        else:  # Use example; this is when converting alternative kg to text
            prompt = f"""
                From this knowledge graph, write a brief paragraph describing the results of main study/experiment.
                Write the paragraph in standard prose, You are describing the results of a scientific paper to others. Do not refer to the knowledge graph in your answer.
                Also only describe the results. Do not provide theoretical interpretations of the results.

                Here is the knowledge graph: {kg}

                Your paragraph should follow a similar writing style but not its content in this example: {orig_results_as_example}.

                You should return your answer as a json such as:
                {{
                    "results": your summary in a few sentences
                }}

                Please convert the knowledge graph back to sentences:
            """  # noqa: E501
        return prompt
