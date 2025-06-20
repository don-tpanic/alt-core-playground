"""Main module for running generators."""

import argparse
import importlib
import json
from pathlib import Path

from logger import get_logger

logger = get_logger("generators.main")


def main() -> None:
    """Main function for running generators."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", type=str, required=True, help="DOI of the paper")
    parser.add_argument("--gen-uid", type=str, required=True, help="UID of the generator")
    parser.add_argument("--algo-name", type=str, required=True, help="Algorithm name")
    parser.add_argument(
        "--max-num-samples",
        type=int,
        default=10,
        help="Maximal number of samples of permutations to generate",
    )
    parser.add_argument(
        "--llm", type=str, default="azure/gpt-4o-2024-08-06", help="LLM to use for processing"
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
    max_num_samples = args.max_num_samples
    llm = args.llm
    additional_config = args.additional_config

    paper_path = Path(f"papers/{doi}/original_paper.txt")
    if not paper_path.exists():
        logger.error(f"File {paper_path} does not exist")
        return

    with paper_path.open("r") as f:
        paper_content = f.read()
        logger.info(f"Successfully read file {paper_path}")

    try:
        module = importlib.import_module(f"generators.{uid}")
        logger.info(f"Successfully imported module {uid}")
    except ImportError as e:
        logger.error(f"Module {uid} does not exist: {e}")
        return

    try:
        outputs = module.run(paper_content, max_num_samples, llm)
        logger.info(f"Successfully ran module {uid}")
    except Exception:
        logger.exception(f"Error running module {uid}")
        return

    output_filename = f"gen_{uid}_{algo_name}_{llm.replace('/', '-')}"
    if additional_config:
        output_filename += f"_{additional_config}"
    output_filename += ".json"
    output_path = Path(f"papers/{doi}/{output_filename}")

    with output_path.open("w") as f:
        json.dump(outputs, f, indent=4)
        logger.info(f"Successfully saved file {output_path}")


if __name__ == "__main__":
    main()
