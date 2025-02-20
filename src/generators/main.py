import argparse
import importlib
import json
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--doi', type=str, required=True, help='DOI of the paper')
    parser.add_argument('--gen-uid', type=str, required=True, help='UID of the generator')
    parser.add_argument('--algo-name', type=str, required=True, help='Algorithm name')
    parser.add_argument('--max-num-samples', type=int, default=10, help='Maximal number of samples of permutations to generate')
    parser.add_argument('--llm', type=str, default='gpt-4o-2024-08-06', help='LLM to use for processing')
    parser.add_argument('--additional-config', type=str, default='', help='Optional additional config for running the algo')
    
    args = parser.parse_args()

    doi = args.doi
    uid = args.gen_uid
    algo_name = args.algo_name
    max_num_samples = args.max_num_samples
    llm = args.llm
    additional_config = args.additional_config

    paper_path = f'papers/{doi}/original_paper.txt'
    if not os.path.exists(paper_path):
        print(f"File {paper_path} does not exist")
        return

    with open(paper_path, 'r') as f:
        paper_content = f.read()
        print(f"Successfully read file {paper_path}")
    
    try:
        module = importlib.import_module(f"src.generators.{uid}")
        print(f"Successfully imported module {uid}")
    except ImportError as e:
        print(f"Module {uid} does not exist: {e}")
        return
    
    try:
        outputs = module.run(paper_content, max_num_samples, llm)
        print(f"Successfully ran module {uid}")
    except Exception as e:
        print(f"Error running module {uid}: {e}")
        return
    
    output_filename = f'gen_{uid}_algo{algo_name}_{llm}'
    if additional_config:
        output_filename += f'_{additional_config}'
    output_filename += '.json'
    output_path = f'papers/{doi}/{output_filename}'

    with open(output_path, 'w') as f:
        json.dump(outputs, f, indent=4)
        print(f"Successfully saved file {output_path}")


if __name__ == '__main__':
    main()
