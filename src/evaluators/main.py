"""Main module for running evaluators."""

import argparse
import importlib
import json
from pathlib import Path

from logger import get_logger

logger = get_logger("evaluators.main")


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
                logger.info(f"Successfully read file {paper_path}")
        else:
            logger.error(f"File {paper_path} does not exist")
            return
    else:
        logger.error("Please provide DOI")
        return

    if args.gen_outputs_path:
        gen_outputs_path = Path(args.gen_outputs_path)
        if gen_outputs_path.exists():
            with gen_outputs_path.open() as f:
                gen_outputs_content = json.load(f)
                logger.info(f"Successfully read file {gen_outputs_path}")
        else:
            logger.error(f"File {gen_outputs_path} does not exist")
            return
    else:
        logger.error("Please provide generator outputs path")
        return

    if args.eval_uid:
        uid = args.eval_uid
        try:
            # Import the module dynamically
            module = importlib.import_module(f"evaluators.{uid}")
            logger.info(f"Successfully imported module {uid}")
        except ImportError as e:
            logger.error(f"Module {uid} does not exist: {e}")
            return

        try:
            outputs = module.run(paper_content, gen_outputs_content)
            logger.info(f"Successfully ran module {uid}")
        except Exception:
            logger.exception(f"Error running module {uid}")
            return

        output_path = Path(f"papers/{doi}/eval_{uid}_{gen_outputs_path.name}")
        with output_path.open("w") as f:
            json.dump(outputs, f, indent=4)
            logger.info(f"Successfully saved file {output_path}")
    else:
        logger.error("Please provide evaluator UID")


if __name__ == "__main__":
    main()
