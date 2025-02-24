"""Knowledge graph pipeline."""

import json
from typing import Any

import numpy as np

from llm.caller import ask_llm, ask_llm_with_schema
from logger import get_logger

from .graphs import permute_knowledge_graph
from .prompts import create_sys_prompts, create_user_prompts
from .prompts.response_models import SummarizeMethods

logger = get_logger(__name__)


def sampling_permutations(
    knowledge_graph_permutations_i: dict, max_num_samples: int = 10
) -> np.ndarray:
    """
    Sample a fixed number of permutations.

    Args:
        knowledge_graph_permutations_i (dict): Dictionary of permutations for a single experiment.
        max_num_samples (int): Max number of samples to select.

    Returns:
        np.ndarray: Array of tuples (permutation key, permutation value) sampled and sorted.
    """
    np.random.seed(42)
    permutes = np.array(list(knowledge_graph_permutations_i.items()))
    if permutes.shape[0] < max_num_samples:
        return permutes

    permutes = permutes[np.random.choice(permutes.shape[0], max_num_samples, replace=False)]
    # Sort the order of permutations in increasing order for consistency.
    permutes = np.array(sorted(permutes, key=lambda x: int(x[0])))
    return permutes


def has_n_experiments(knowledge_graph: dict, num_experiments: int = 1) -> bool:
    """
    Check if the knowledge graph contains exactly num_experiments experiments.

    Args:
        knowledge_graph (dict): Knowledge graph dictionary.
        num_experiments (int): Expected number of experiments.

    Returns:
        bool: True if the number of experiments equals num_experiments.
    """
    return len(knowledge_graph) == num_experiments


def postprocess_json(response_json: dict) -> dict:
    """
    Process the JSON output from the LLM call.

    Args:
        response_json (dict): JSON response from ask_llm.

    Returns:
        dict: Parsed response content.
    """
    response_content = response_json["choices"][0]["message"]["content"]

    # Find the first occurrence of '{' and the last occurrence of '}'
    start_idx = response_content.find("{")
    end_idx = response_content.rfind("}")

    if start_idx != -1 and end_idx != -1:
        response_content = response_content[start_idx : end_idx + 1]

    # Remove code block markers if present
    response_content = response_content.removeprefix("```json").removesuffix("```")
    # Replace escape characters as needed
    response_content = response_content.replace("\\", "\\\\")
    logger.debug("response_content %s", response_content)
    return json.loads(response_content)


def run(paper_text: str, max_num_samples: int = 10, llm: str = "azure/gpt-4o-2024-08-06") -> dict:
    """
    Process the provided paper text through several NLP steps and return the results.

    This function:
      1. Summarizes the paper methods.
      2. Creates an initial knowledge graph from the paper.
      3. Converts the KG to text.
      4. Identifies semantic groups.
      5. Creates permuted knowledge graphs.
      6. Converts the permuted KGs to text.
      7. Aggregates token usage cost metrics.

    Args:
        paper_text (str): Full text of the paper.
        max_num_samples (int): Max number of permutations to sample.
        llm (str): LLM model to use for processing.

    Returns:
        dict: Dictionary of outputs containing methods summary, knowledge graph,
              semantic groups, conversion results, and token cost details.
    """
    outputs: dict[str, Any] = {}
    outputs["llm"] = llm
    total_cost = {}

    # Create system prompt.
    sys_prompt = create_sys_prompts.prompts()

    # Summarize methods.
    logger.info("Summarizing methods for paper...")
    user_prompt = create_user_prompts.summarize_methods(paper_text)
    summarize_methods, cost = ask_llm_with_schema(llm, sys_prompt, user_prompt, SummarizeMethods)
    outputs["methods"] = summarize_methods.methods
    total_cost["methods"] = cost

    # Step 1: Create initial knowledge graph conditioned on the full paper.
    logger.info("Creating initial knowledge graph for paper...")
    kg_creator = create_user_prompts.KnowledgeGraphCreator(paper_text)
    user_prompt = kg_creator.create_initial_kg()
    response, cost = ask_llm(llm, sys_prompt, user_prompt)
    response_json = json.loads(response)
    response_content = postprocess_json(response_json)
    outputs["knowledge_graph"] = response_content.get("knowledge_graph")
    total_cost["res_to_kg"] = cost

    # Only proceed if there is exactly one experiment in the knowledge graph.
    if has_n_experiments(outputs["knowledge_graph"], num_experiments=1):
        # Step 2: Convert original KG to text (per experiment).
        logger.info("Converting knowledge graph to text...")
        outputs["results"] = {}
        kg_to_text_cost = 0.0
        for experiment_i in range(1, len(outputs["knowledge_graph"]) + 1):
            key = f"experiment_{experiment_i}"
            user_prompt = kg_creator.convert_kg_to_text_single_experiment(
                outputs["knowledge_graph"][key]
            )
            response, cost = ask_llm(llm, sys_prompt, user_prompt)
            response_json = json.loads(response)
            response_content = postprocess_json(response_json)
            kg_to_text_cost += cost
            outputs["results"][key] = response_content.get("results")
        total_cost["kg_to_text"] = kg_to_text_cost

        # Step 3: Identify semantic groups.
        logger.info("Identifying semantic groups...")
        user_prompt = kg_creator.identify_semantic_groups(outputs["knowledge_graph"])
        response, cost = ask_llm(llm, sys_prompt, user_prompt)
        response_json = json.loads(response)
        response_content = postprocess_json(response_json)
        outputs["semantic_groups"] = response_content.get("semantic_groups")
        total_cost["kg_to_semantic_groups"] = cost

        # Step 4: Create permuted knowledge graphs.
        logger.info("Creating permuted knowledge graphs...")
        (knowledge_graph_permutations, node_swaps_tracker, triple_deviation_pct) = (
            permute_knowledge_graph.create_permutations(
                outputs["knowledge_graph"], outputs["semantic_groups"]
            )
        )
        outputs["knowledge_graph_permutations"] = knowledge_graph_permutations
        outputs["node_swaps_tracker"] = node_swaps_tracker
        outputs["triple_deviation_pct"] = triple_deviation_pct

        # Step 5: Convert permuted KGs to text.
        logger.info("Converting permuted knowledge graphs to text...")
        outputs["results_permutations"] = {}
        kg_permutes_to_text_cost = 0.0
        num_graph_permutations: dict[int | str, int] = {}
        for experiment_i, kg_perms in knowledge_graph_permutations.items():
            outputs["results_permutations"][experiment_i] = {}
            num_graph_permutations[experiment_i] = len(kg_perms)

            for permutation_i, kg in sampling_permutations(kg_perms, max_num_samples):
                logger.info(f"Converting permutation {permutation_i} for {experiment_i}...")
                user_prompt = kg_creator.convert_kg_to_text_single_experiment(
                    kg, orig_results_as_example=outputs["results"][experiment_i]
                )
                response, cost = ask_llm(llm, sys_prompt, user_prompt)
                response_json = json.loads(response)
                response_content = postprocess_json(response_json)
                kg_permutes_to_text_cost += cost
                outputs["results_permutations"][experiment_i][permutation_i] = response_content.get(
                    "results"
                )

        # Record number of permutations.
        num_graph_permutations["total"] = sum(num_graph_permutations.values())
        outputs["num_graph_permutations"] = num_graph_permutations

        # Calculate and record token costs.
        total_cost["kg_permutes_to_text"] = kg_permutes_to_text_cost
        total_cost["total"] = sum(total_cost.values())
        outputs["token_cost"] = total_cost
    else:
        logger.info("Paper has more than 1 experiment, processing is skipped.")

    return outputs
