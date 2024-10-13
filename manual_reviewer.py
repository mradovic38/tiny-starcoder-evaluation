import pandas as pd
import csv
import os
import time
from typing import Tuple

class ManualReviewer:
    def __init__(self) -> None:
        """
        Initializes the ManualReviewer with empty lists for labels and comments.
        """
        self.labels = []
        self.comments = []

    def review_example(self, row: pd.Series) -> Tuple[int, str]:
        """
        Displays an example for review and collects user input for labeling and commenting.

        Args:
            row (pd.Series): A row from the DataFrame containing 'prefix', 'mid_pred', 'middle', and 'suffix'.

        Returns:
            Tuple[int, str]: A tuple containing the assigned label (0, 1, or 2) and the user's comment.
        """
        print("\n--- Review Example ---")
        print(f"Prefix:\n{row['prefix']}")
        print('*' * 75)
        print(f"\nMiddle Prediction:\n{row['mid_pred']}")
        print('*' * 75)
        print(f"\nMiddle Truth:\n{row['middle']}")
        print('*' * 75)
        print(f"\nSuffix:\n{row['suffix']}")
        print('_' * 100)

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
        """
        Iterates through the provided DataFrame, allowing the user to review each example.

        Args:
            df (pd.DataFrame): DataFrame containing the examples to be reviewed.
            output_path (str, optional): Path to save the reviewed DataFrame. Defaults to None.

        Returns:
            pd.DataFrame: The updated DataFrame with labels and comments added.
        """
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
        if output_path:
            if os.path.exists(output_path):
                os.remove(output_path)
            df.to_csv(output_path, sep='|', index=False, quoting=csv.QUOTE_MINIMAL)

        print(f"Review process completed and saved to {output_path}.")
        
        return df
