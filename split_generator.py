import os
import random
import csv
from typing import Dict, List
from transformers import AutoTokenizer

class SplitGenerator():
    def __init__(self, tokenizer: AutoTokenizer, directory: str = 'code_examples', prefix_length: int = 30,
                   middle_length: int = 30, suffix_length: int = 30) -> None:
        """Initialize the SplitGenerator with the tokenizer, file directory, and lengths for prefix, middle, and suffix.

        Args:
            tokenizer (AutoTokenizer): The tokenizer to be used for splitting code.
            directory (str): The directory containing Python files for code examples.
            prefix_length (int): The number of tokens in the prefix.
            middle_length (int): The number of tokens in the middle section.
            suffix_length (int): The number of tokens in the suffix.
        """
        
        self.files = [os.path.join(root, file) for root, _, files in os.walk(directory)
                      for file in files if file.endswith('.py')]
        self.tokenizer = tokenizer
        self.prefix_length = prefix_length
        self.middle_length = middle_length
        self.suffix_length = suffix_length

    def split_code(self, code: str, fname: str) -> List[Dict[str, str]]:
        """Split the given code into prefix, middle, and suffix segments.

        Args:
            code (str): The complete code as a string.
            fname (str): The filename from which the code was read.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each containing the filename, prefix, middle, and suffix.
        """


        # Tokenize the code
        tokens = self.tokenizer.tokenize(code)
        total_tokens = len(tokens)

        # Check if the code is long enough
        if total_tokens < (self.prefix_length + self.middle_length + self.suffix_length):
            return []

        splits = []
        current_position = 0

        while current_position + self.prefix_length + self.middle_length + self.suffix_length <= total_tokens:
            # Get the prefix, middle, and suffix based on the current position
            prefix = tokens[current_position:current_position + self.prefix_length]
            middle = tokens[current_position + self.prefix_length:current_position 
                            + self.prefix_length + self.middle_length]
            suffix = tokens[current_position + self.prefix_length + self.middle_length:current_position + 
                            self.prefix_length + self.middle_length + self.suffix_length]

            # Convert tokens back to text
            prefix_text = self.tokenizer.convert_tokens_to_string(prefix)
            middle_text = self.tokenizer.convert_tokens_to_string(middle)
            suffix_text = self.tokenizer.convert_tokens_to_string(suffix)

            # Add the split to the result list
            splits.append({
                "fname": fname,
                "prefix": prefix_text,
                "middle": middle_text,
                "suffix": suffix_text
            })

            # Move the current position to the end of the suffix for the next split
            current_position += self.prefix_length + self.middle_length + self.suffix_length

        return splits


    def generate(self,  save_path: str, num_examples: int = 40) -> None:
        """Generate a dataset of code completion examples from Python files.

        Args:
            save_path (str): The path where the generated dataset will be saved as a CSV file.
            num_examples (int): The number of examples to generate. If there are fewer examples available, all will be used.
        """
        
        dataset = []

        for file in self.files:
            with open(file, 'r') as f:
                code = f.read()
                examples = self.split_code(code, file)
                if len(examples) > 0:
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
