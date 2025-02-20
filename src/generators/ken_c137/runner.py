"""Runner for the Ken C137 generator."""


def run(paper_content: str) -> dict:
    """Run the generator.

    Args:
        paper_content: The content of the paper.

    Returns:
        A dictionary containing the outputs.
    """
    outputs = {
        "doi": "",
        "llm": "",
        "methods": "",
        "results": paper_content,
        "knowledge_graph": "",
        "knowledge_graph_permutations": {},
        "results_permutations": {},
        "num_permutations": 0,
    }
    return outputs
