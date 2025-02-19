#!/usr/bin/env python3
import os

def main():
    papers_dir = "papers"
    if not os.path.exists(papers_dir):
        print("No papers/ folder found.")
        return

    total_papers = 0
    total_gen = 0
    total_eval = 0

    for doi in os.listdir(papers_dir):
        doi_path = os.path.join(papers_dir, doi)
        if os.path.isdir(doi_path):
            total_papers += 1
            for fname in os.listdir(doi_path):
                if fname.startswith("gen_") and fname.endswith(".json"):
                    total_gen += 1
                elif fname.startswith("eval_") and fname.endswith(".json"):
                    total_eval += 1

    # Print the report
    print("=== Quick Report ===")
    print(f"Total number of papers: {total_papers}")
    print(f"Total number of generated outputs: {total_gen}")
    print(f"Total number of evaluations: {total_eval}")

if __name__ == "__main__":
    main()
