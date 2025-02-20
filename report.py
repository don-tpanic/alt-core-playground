"""Report module for generating and updating reports."""

import re
from pathlib import Path


def generate_report() -> tuple[int, int, int]:
    """Generate a report of the number of papers, alternatives, and evaluations."""
    papers_dir = Path("papers")
    total_papers = 0
    total_gen = 0
    total_eval = 0

    if papers_dir.exists():
        for doi in papers_dir.iterdir():
            if doi.is_dir():
                total_papers += 1
                total_gen += len(list(doi.glob("gen_*.json")))
                total_eval += len(list(doi.glob("eval_*.json")))

    return total_papers, total_gen, total_eval


def update_readme(total_papers: int, total_gen: int, total_eval: int) -> None:
    """Update the README.md file with the new stats."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("README.md not found!")
        return

    # Read the README content
    with readme_path.open(encoding="utf-8") as f:
        content = f.read()

    # Create the updated stats block in a table format
    new_stats = (
        "<!-- START_STATS -->\n"
        "| Metric                          | Count |\n"
        "|---------------------------------|-------|\n"
        f"| Total papers analyzed           | {total_papers} |\n"
        f"| Total alternatives generated    | {total_gen} |\n"
        f"| Total evaluations done          | {total_eval} |\n"
        "<!-- END_STATS -->"
    )

    # Use regex to replace content between markers
    updated_content = re.sub(
        r"<!-- START_STATS -->.*?<!-- END_STATS -->", new_stats, content, flags=re.DOTALL
    )

    with readme_path.open("w", encoding="utf-8") as f:
        f.write(updated_content)
    print("README.md updated successfully!")


if __name__ == "__main__":
    papers, gens, evals = generate_report()
    print(f"Total papers: {papers}, Total alternatives: {gens}, Total evaluations: {evals}")
    update_readme(papers, gens, evals)
