"""Main module for running generators."""

import argparse
import importlib
import json
from pathlib import Path


def main() -> None:
    """Main function for running generators."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", type=str, required=True, help="DOI of the paper")
    parser.add_argument("--gen-uid", type=str, required=True, help="UID of the generator")
    parser.add_argument("--algo-name", type=str, required=True, help="Algorithm name")
    parser.add_argument(
        "--alt-index", type=int, required=True, help="Unique index of an alternative result"
    )
    parser.add_argument(
        "--additional-config",
        type=str,
        default="",
        help="Optional additional config for running the algo",
    )

    args = parser.parse_args()

    doi = args.doi
    uid = args.gen_uid
    algo_name = args.algo_name
    alt_index = args.alt_index
    additional_config = args.additional_config

    paper_path = Path(f"papers/{doi}/original_paper.txt")
    if not paper_path.exists():
        print(f"File {paper_path} does not exist")
        return

    with paper_path.open() as f:
        paper_content = f.read()
        print(f"Successfully read file {paper_path}")

    try:
        module = importlib.import_module(f"src.generators.{uid}")
        print(f"Successfully imported module {uid}")
    except ImportError as e:
        print(f"Module {uid} does not exist: {e}")
        return

    try:
        outputs = module.run(paper_content)
        print(f"Successfully ran module {uid}")
    except Exception as e:
        print(f"Error running module {uid}: {e}")
        return

    output_filename = f"gen_{uid}_{algo_name}_alt{alt_index}"
    if additional_config:
        output_filename += f"_{additional_config}"
    output_filename += ".json"
    output_path = Path(f"papers/{doi}/{output_filename}")

    with output_path.open("w") as f:
        json.dump(outputs, f, indent=4)
        print(f"Successfully saved file {output_path}")


if __name__ == "__main__":
    main()
