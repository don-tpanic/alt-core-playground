"""Main module for running evaluators."""

import argparse
import importlib
import json
from pathlib import Path


def main() -> None:
    """Main function for running evaluators."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", type=str, help="DOI of the paper")
    parser.add_argument("--eval-uid", type=str, help="UID of the evaluator")
    parser.add_argument("--gen-outputs-path", type=str, help="Path to the generator outputs")
    args = parser.parse_args()

    if args.doi:
        doi = args.doi
        paper_path = Path(f"papers/{doi}/original_paper.txt")
        if paper_path.exists():
            with paper_path.open() as f:
                paper_content = f.read()
                print(f"Successfully read file {paper_path}")
        else:
            print(f"File {paper_path} does not exist")
            return
    else:
        print("Please provide DOI")
        return

    if args.gen_outputs_path:
        gen_outputs_path = Path(args.gen_outputs_path)
        if gen_outputs_path.exists():
            with gen_outputs_path.open() as f:
                gen_outputs_content = json.load(f)
                print(f"Successfully read file {gen_outputs_path}")
        else:
            print(f"File {gen_outputs_path} does not exist")
            return
    else:
        print("Please provide generator outputs path")
        return

    if args.eval_uid:
        uid = args.eval_uid
        try:
            # Import the module dynamically
            module = importlib.import_module(f"evaluators.{uid}")
            print(f"Successfully imported module {uid}")
        except ImportError as e:
            print(f"Module {uid} does not exist: {e}")
            return

        try:
            outputs = module.run(paper_content, gen_outputs_content)
            print(f"Successfully ran module {uid}")
        except Exception as e:
            print(f"Error running module {uid}: {e}")
            return

        output_path = Path(f"papers/{doi}/eval_{uid}_{gen_outputs_path.name}")
        with output_path.open("w") as f:
            json.dump(outputs, f, indent=4)
            print(f"Successfully saved file {output_path}")
    else:
        print("Please provide evaluator UID")


if __name__ == "__main__":
    main()
