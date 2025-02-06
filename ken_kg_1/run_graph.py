import os
import json
import asyncio
import argparse
import numpy as np 

from api_call import ask_gpt4_async, token_cost
from prompts import create_sys_prompts, create_user_prompts
from utils import get_paper_text
from graphs import permute_knowledge_graph


def sampling_permutations(knowledge_graph_permutations_i, num_samples=10):
    """
    Sample a fixed number of permutations.

    Args:
        knowledge_graph_permutations_i (dict): dictionary of permutations for a single experiment
    """
    np.random.seed(42)
    permutes = np.array(list(knowledge_graph_permutations_i.items()))
    if permutes.shape[0] < num_samples:
        return permutes

    permutes = permutes[np.random.choice(permutes.shape[0], num_samples, replace=False)]

    # Sort the order of permutations in increasing order to be
    # consistent with the other permutation-related fields in json.
    permutes = sorted(permutes, key=lambda x: int(x[0]))
    return permutes


def has_n_experiments(knowledge_graph, num_experiments=1):
    """
    Args:
        knowledge_graph (dict): knowledge graph dictionary.
        num_experiment (int): number of experiment to filter by.

    Returns:
        flag (bool): True if the number of experiment is equal to num_experiment.
    """
    return len(knowledge_graph) == num_experiments


def postprocess_json(response_json):
    # 1. Get response
    response_content = response_json["choices"][0]["message"]["content"]
    # 2. Remove code block
    response_content = response_content.strip('```').lstrip('json')
    # 3. Replace escape characters
    response_content = response_content.replace('\\', '\\\\')
    # 4. Load as json
    print('response_content', response_content)
    response_content = json.loads(response_content)
    return response_content


async def process_paper(fname, txt_dir, outputs_dir, num_samples):
    fpath = os.path.join(txt_dir, fname)
    paper_text = get_paper_text.load(fpath)

    outputs = {}
    outputs_fpath = os.path.join(outputs_dir, fname.replace('.txt', '.json'))

    if os.path.exists(outputs_fpath):
        print(f"Skipping {fname}, because outputs already exists")
        return

    total_cost = {}
    sys_prompt = create_sys_prompts.prompts()

    # Summarize methods
    print(f"\n# Summarizing methods for {fname}..")
    user_prompt = create_user_prompts.summarize_methods(paper_text)
    response_json = json.loads(await ask_gpt4_async(sys_prompt, user_prompt))
    response_content = postprocess_json(response_json)
    n_input_tokens = int(response_json["usage"]["prompt_tokens"])
    n_output_tokens = int(response_json["usage"]["completion_tokens"])
    outputs["methods"] = response_content["methods"]
    
    # Step 1: Create initial knowledge graph conditioned on full paper.
    print(f"\n# Creating initial knowledge graph for {fname}..")
    kg_creator = create_user_prompts.KnowledgeGraphCreator(paper_text)
    user_prompt = kg_creator.create_initial_kg()
    response_json = json.loads(await ask_gpt4_async(sys_prompt, user_prompt))
    response_content = postprocess_json(response_json)
    n_input_tokens = int(response_json["usage"]["prompt_tokens"])
    n_output_tokens = int(response_json["usage"]["completion_tokens"])
    outputs["knowledge_graph"] = response_content["knowledge_graph"]
    cost = token_cost(n_input_tokens, n_output_tokens)
    total_cost["res_to_kg"] = cost

    # Step 2-5: Convert KG to text, identify semantic groups, and permute KGs
    # For now, we only proceed with papers have 1 experiment.
    if has_n_experiments(outputs["knowledge_graph"], num_experiments=1):
        # Step 2: Convert original KG to text (per experiment)
        print(f"\n# Converting knowledge graph to text for {fname}..")
        outputs["results"] = {}
        n_input_tokens = 0
        n_output_tokens = 0
        for experiment_i in range(1, len(outputs["knowledge_graph"]) + 1):
            user_prompt = kg_creator.convert_kg_to_text_single_experiment(
                outputs["knowledge_graph"][f'experiment_{experiment_i}'], 
            )
            response_json = json.loads(await ask_gpt4_async(sys_prompt, user_prompt))
            response_content = postprocess_json(response_json)
            n_input_tokens += int(response_json["usage"]["prompt_tokens"])
            n_output_tokens += int(response_json["usage"]["completion_tokens"])
            outputs["results"][f'experiment_{experiment_i}'] = response_content["results"]
        cost = token_cost(n_input_tokens, n_output_tokens)
        total_cost["kg_to_text"] = cost

        # Step 3: Identify semantic groups
        print(f"\n# Identifying semantic groups for {fname}..")
        user_prompt = kg_creator.identify_semantic_groups(
            outputs["knowledge_graph"], 
        )
        response_json = json.loads(await ask_gpt4_async(sys_prompt, user_prompt))
        response_content = postprocess_json(response_json)
        n_input_tokens = int(response_json["usage"]["prompt_tokens"])
        n_output_tokens = int(response_json["usage"]["completion_tokens"])
        outputs["semantic_groups"] = response_content["semantic_groups"]
        cost = token_cost(n_input_tokens, n_output_tokens)
        total_cost["kg_to_semantic_groups"] = cost

        # Step 4: Create permuted knowledge graphs
        print(f"\n# Creating permuted knowledge graphs for {fname}..")
        knowledge_graph_permutations, node_swaps_tracker, triple_deviation_pct \
            = permute_knowledge_graph.create_permutations(
                outputs["knowledge_graph"], 
                outputs["semantic_groups"],
            )
        outputs["knowledge_graph_permutations"] = knowledge_graph_permutations
        outputs["node_swaps_tracker"] = node_swaps_tracker
        outputs["triple_deviation_pct"] = triple_deviation_pct

        # Step 5: Convert permuted KGs to text (per experiment and per permutation)
        print(f"\n# Converting permuted knowledge graphs to text for {fname}..")
        outputs["results_permutations"] = {}
        n_input_tokens_kg_to_text = 0
        n_output_tokens_kg_to_text = 0
        num_graph_permutations = {}
        for experiment_i, knowledge_graph_permutations_i in knowledge_graph_permutations.items():
            outputs["results_permutations"][experiment_i] = {}
            num_graph_permutations[experiment_i] = len(knowledge_graph_permutations_i)

            for permutation_i, knowledge_graph_i in sampling_permutations(knowledge_graph_permutations_i, num_samples):
                print(f"  Converting permutation {permutation_i} for {experiment_i}, {fname}..")
                user_prompt = kg_creator.convert_kg_to_text_single_experiment(
                    knowledge_graph_i,
                    orig_results_as_example=outputs["results"][experiment_i]
                )
                response_json = json.loads(await ask_gpt4_async(sys_prompt, user_prompt))
                response_content = postprocess_json(response_json)
                n_input_tokens_kg_to_text += int(response_json["usage"]["prompt_tokens"])
                n_output_tokens_kg_to_text += int(response_json["usage"]["completion_tokens"])
                outputs["results_permutations"][experiment_i][permutation_i] = response_content["results"]
    
        # Record number of permutations
        num_graph_permutations["total"] = sum(num_graph_permutations.values())
        outputs["num_graph_permutations"] = num_graph_permutations

        # Calculate costs
        kg_to_text_cost = token_cost(n_input_tokens_kg_to_text, n_output_tokens_kg_to_text)
        total_cost["kg_permutes_to_text"] = kg_to_text_cost
        total_cost["total"] = sum(total_cost.values())
        outputs["token_cost"] = total_cost

        with open(outputs_fpath, 'w') as f:
            json.dump(outputs, f, indent=4)    
    else:
        print(f"{fname} has more than 1 experiments, ignored.")


async def main():
    txt_dir = 'data/txt_articles'
    outputs_dir = 'outputs/'

    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    async_tasks = []
    for fname in os.listdir(txt_dir):
        if not fname.endswith('.txt'):
            print(f"Skipping {fname}")
            continue
        async_tasks.append(
            process_paper(
                fname, 
                txt_dir, 
                outputs_dir, 
                num_samples
            )
        )

    await asyncio.gather(*async_tasks)


if __name__ == '__main__':
    num_samples = 10
    asyncio.run(main())