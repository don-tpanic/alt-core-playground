import os
import re

def generate_report():
    papers_dir = "papers"
    total_papers = 0
    total_gen = 0
    total_eval = 0

    if os.path.exists(papers_dir):
        for doi in os.listdir(papers_dir):
            doi_path = os.path.join(papers_dir, doi)
            if os.path.isdir(doi_path):
                total_papers += 1
                for fname in os.listdir(doi_path):
                    if fname.startswith("gen_") and fname.endswith(".json"):
                        total_gen += 1
                    elif fname.startswith("eval_") and fname.endswith(".json"):
                        total_eval += 1

    return total_papers, total_gen, total_eval

def update_readme(total_papers, total_gen, total_eval):
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found!")
        return

    # Read the README content
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Create the updated stats block
    new_stats = (
        f"<!-- START_STATS -->\n"
        f"Total papers analyzed: {total_papers}\n"
        f"Total alternatives generated: {total_gen}\n"
        f"Total evaluations done: {total_eval}\n"
        f"<!-- END_STATS -->"
    )

    # Use regex to replace content between markers
    updated_content = re.sub(
        r'<!-- START_STATS -->.*?<!-- END_STATS -->',
        new_stats,
        content,
        flags=re.DOTALL
    )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("README.md updated successfully!")

if __name__ == "__main__":
    papers, gens, evals = generate_report()
    print(f"Total papers: {papers}, Total alternatives: {gens}, Total evaluations: {evals}")
    update_readme(papers, gens, evals)
