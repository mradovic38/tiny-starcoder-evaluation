import os
import random
import csv
from typing import List, Dict

class SplitGenerator():
    def __init__(self, directory: str = 'code_examples', max_chars: int = 256) -> None:
        self.files = [os.path.join(root, file) for root, _, files in os.walk(directory)
                      for file in files if file.endswith('.py')]
        self.max_chars = max_chars

    def split_code(self, code: str, fname: str) -> List[Dict[str, str]]:
        """Generate prefix, middle, and suffix examples by splitting code into lines."""
        examples = []
        lines = code.splitlines()

        # Initialize the variables to track the current chunk
        current_chunk = []
        current_length = 0

        for line in lines:
            line_length = len(line) + 1  # +1 for the newline character
            # Check if adding this line exceeds the max character limit
            if current_length + line_length > self.max_chars:
                # We reached the limit, now we can make a random split
                if len(current_chunk) > 1:  # Ensure we have at least two lines to split
                    prefix_end = random.randint(1, len(current_chunk) - 1)  # Avoid empty prefix
                    suffix_start = random.randint(prefix_end, len(current_chunk))  # Avoid empty suffix

                    # Build the prefix, middle, and suffix with newline characters
                    prefix = '\n'.join(current_chunk[:prefix_end]) + '\n'
                    middle = '\n'.join(current_chunk[prefix_end:suffix_start]) + '\n'
                    suffix = '\n'.join(current_chunk[suffix_start:]) + '\n'

                    # Ensure none of the sections are empty
                    if prefix.strip() and middle.strip() and suffix.strip():
                        examples.append({"fname": fname, "prefix": prefix, "middle": middle, "suffix": suffix})

                # Reset for the next chunk
                current_chunk = []
                current_length = 0
            
            # Add the line to the current chunk
            current_chunk.append(line)
            current_length += line_length

        # Handle any remaining lines in the current chunk after the loop
        if current_chunk and len(current_chunk) > 1:
            prefix_end = random.randint(1, len(current_chunk) - 1)
            suffix_start = random.randint(prefix_end, len(current_chunk))

            # Build the prefix, middle, and suffix with newline characters
            prefix = '\n'.join(current_chunk[:prefix_end]) + '\n'
            middle = '\n'.join(current_chunk[prefix_end:suffix_start]) + '\n'
            suffix = '\n'.join(current_chunk[suffix_start:]) + '\n'

            # Ensure none of the sections are empty
            if prefix.strip() and middle.strip() and suffix.strip():
                examples.append({"fname": fname, "prefix": prefix, "middle": middle, "suffix": suffix})

        return examples

    def generate(self, save_path: str, num_examples: int = 40) -> None:
        """Generates a dataset of code completion examples from python files."""
        dataset = []

        for file in self.files:
            with open(file, 'r') as f:
                code = f.read()
                examples = self.split_code(code, file)
                dataset.extend(examples)

                if examples:
                    print(f"Generated {len(examples)} examples for file: {file}")

        # If dataset is empty, skip writing to CSV
        if not dataset:
            print("No examples were generated.")
            return

        data_cut = random.sample(dataset, min(num_examples, len(dataset)))

        if os.path.exists(save_path):
            os.remove(save_path)

        # Save data_cut to a CSV file using a vertical bar as the delimiter
        with open(save_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerow(['fname', 'prefix', 'middle', 'suffix'])  # Write header
            
            for row in data_cut:
                # Ensure we only write rows with valid data
                if isinstance(row, dict) and all(field in row for field in ['fname', 'prefix', 'middle', 'suffix']):
                    writer.writerow([row['fname'], row['prefix'], row['middle'], row['suffix']])  # Write each example
