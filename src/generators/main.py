import argparse
import importlib
import json
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--doi', type=str, help='DOI of the paper')
    parser.add_argument('--gen-uid', type=str, help='UID of the generator')
    args = parser.parse_args()

    if args.doi:
        doi = args.doi
        path = f'papers/{doi}/original_paper.txt'
        if os.path.exists(path):
            with open(path, 'r') as f:
                paper_content = f.read()
                print(f"Successfully read file {path}")
        else:
            print(f"File {path} does not exist")
    else:
        print("Please provide DOI")

    if args.gen_uid:
        uid = args.gen_uid
        try:
            # Import the module dynamically
            module = importlib.import_module(f"src.generators.{uid}")
            print(f"Successfully imported module {uid}")
        except ImportError as e:
            print(f"Module {uid} does not exist: {e}")

        try:
            outputs = module.run(paper_content)
            print(f"Successfully ran module {uid}")
        except Exception as e:
            print(f"Error running module {uid}: {e}")

        path = f'papers/{doi}/gen_{uid}_algo1_alt1.json'
        with open(path, 'w') as f:
            json.dump(outputs, f, indent=4)
            print(f"Successfully saved file {path}")
    else:
        print("Please provide generator UID")


if __name__ == '__main__':
    main()