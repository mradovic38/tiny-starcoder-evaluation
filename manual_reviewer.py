import pandas as pd
import csv
import os
import time
from typing import Tuple

class ManualReviewer():
    def __init__(self) -> None:
        self.labels = []
        self.comments = []

    # Function to display an example and ask for label and comment
    def review_example(self, row) -> Tuple[str, str]:
        print("\n--- Review Example ---")
        print(f"Prefix:\n{row['prefix']}")
        print('*'*75)
        print(f"\nMiddle Prediction:\n{row['mid_pred']}")
        print('*'*75)
        print(f"\nMiddle Truth:\n{row['middle']}")
        print('*'*75)
        print(f"\nSuffix:\n{row['suffix']}")
        print('_'*100)

        time.sleep(0.2)
        
        # Ask for label
        while True:
            label = int(input("\nAssign label (0 (correct)/ 1 (partially correct) / 2 (incorrect)): "))
            if label in [0, 1, 2]:
                break
            else:
                print("Invalid input. Please enter '0', '1', or '2'.")

        # Ask for a comment
        comment = input("\nComment on this example: ").strip()
        
        return label, comment

    def review(self, df: pd.DataFrame, output_path: str = None) -> pd.DataFrame:
        df = df.copy()

        # Iterate through each row and review the example
        for _, row in df.iterrows():
            label, comment = self.review_example(row)
            self.labels.append(label)
            self.comments.append(comment)

        # Add the labels and comments to the DataFrame
        df['label'] = self.labels
        df['comment'] = self.comments


        # Save the DataFrame to csv
        df.to_csv(output_path, sep='|', index=False, quoting=csv.QUOTE_MINIMAL)

        print(f"Review process completed and saved to {output_path}.")

        return df