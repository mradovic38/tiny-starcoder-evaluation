# Tiny Starcoder FIM Code Completion Model Evaluation

## [Generating the dataset](data_fetcher.py)
To generate the dataset, I first cloned the public repository of my [Football Analysis]("https://github.com/mradovic38/football_analysis") project using the `clone_repo()` function. This function clones the repository into a specified directory, ensuring the code is available locally. After cloning, I used the `collect_python_files()` function to gather all Python files (except `__init__.py` files) from the repository into a target directory. This function searches for .py files and stores them in a designated folder for further processing. I applied this process to gather all Python files from the cloned repository.

## [Splitting scripts into prefix, middle and suffix](split_generator.py)
To prepare the dataset for the model, I implemented the `SplitGenerator` class, which splits Python files into three sections: **prefix**, **middle**, and **suffix**. The prefix and suffix sections each contain 200 tokens, providing ample context for predicting the middle segment, which is 40 tokens long. 

The process works as follows:
- **Tokenization**: The code is tokenized using a provided tokenizer.
```python
tokens = self.tokenizer.tokenize(code)
```
- **Splitting**: The tokens are divided into prefix, middle, and suffix, ensuring that each part fits the specified lengths.
```python
prefix = tokens[current_position:current_position + self.prefix_length]
middle = tokens[current_position + self.prefix_length:current_position +
                           self.prefix_length + self.middle_length]
suffix = tokens[current_position + self.prefix_length + self.middle_length:current_position +
                         self.prefix_length + self.middle_length + self.suffix_length]
```
- **Splits Dataset Generation**: I used the `generate()` method to create a CSV file with 40 examples, each containing a filename, prefix, middle, and suffix.

## [Running Tiny Starcoder](tiny_starcoder_evaluation.ipynb)
The `get_completion` function generates predictions for the middle part of a code snippet. It takes the prefix and suffix as inputs, tokenizes them, and prepares them for the model. The model generates a completion based on the input, which is then decoded to extract the middle portion of the text.
We apply this function to each row in our DataFrame to obtain predictions for the dataset.

## [Manual scoring](manual_reviewer.py)
The `ManualReviewer` class enables the manual evaluation of code completion examples. It displays each example to the reviewer, allowing them to assign a label (0 for correct, 1 for partially correct, and 2 for incorrect) and provide comments on why the example got the given score. The reviews are stored in a DataFrame, which can be saved to a CSV file for further analysis.

## [Proposing some automatic metrics](tiny_starcoder_evaluation.ipynb)
I have proposed several automatic metrics to evaluate the performance of the Fill-in-the-Middle (FIM) code completion model. The selected metrics include Exact Match, chrF, BLEU and some ROUGE metrics, each providing unique insights into the quality of the generated outputs.

1. **Exact Match**
This metric evaluates whether the predicted output matches the reference output exactly. It returns a binary score (True or False).

2. **chrF (Character F-score)**
chrF measures the F-score at the character level, allowing for sensitivity to small variations in the output, such as syntax and formatting differences. It could be particularly beneficial for code completion tasks, where minor changes can significantly affect functionality, thus providing a more nuanced evaluation.

3. **BLEU** (Bilingual Evaluation Understudy)
BLEU measures the overlap of n-grams between the predicted output and reference completions. It ranges from 0 to 1, where higher scores indicate better alignment with the references.
 - **Why did I choose BLEU?**: BLEU could be useful for assessing the precision of code snippets, because it identifies how closely the model's outputs match expected patterns.

4. **ROUGE** (Recall-Oriented Understudy for Gisting Evaluation)
ROUGE calculates the recall of n-grams between the reference and predicted texts, with several variants (ROUGE-1, ROUGE-2, ROUGE-L) measuring unigram, bigram, and longest common subsequence matches, respectively.
 - **Why did I choose ROUGE?**: It could provide insights into the completeness and relevance of the generated code, making it effective for understanding how well the model captures key elements of the reference completions.

## [Calculating which metrics align the most with manual evaluations](tiny_starcoder_evaluation.ipynb)
In evaluating the performance of the Tiny Starcoder model, several metrics were analyzed for their correlation with manual labels. I have computed the Pearson and Spearman correlations between the manually created labels and various metrics.
### Insights:
Most metrics exhibited negative correlations, which can be attributed to the labeling system where 0 indicates correctness and 2 indicates incorrectness.
1. **Exact Match has no meaningful correlation with the manual labels**, since there are no exact matches.

2. **chrf has a moderate correlation**, indicating that this metric aligns reasonably well with manual evaluations.

3. **BLEU demonstrates the strongest correlation with manual labels**, making it the most reliable metric in this evaluation.

4. **ROUGE-1 and ROUGE-2 and ROUGE-L also show moderate positive correlations**, indicating moderate agreement with manual labels.


## 🏆 Acknowledgements
* [Tiny Starcoder](https://huggingface.co/bigcode/tiny_starcoder_py)
* Lin, Chin-Yew. 2004. ROUGE: a Package for Automatic Evaluation of Summaries. In Pro-ceedings of the Workshop on Text Summari-zation  Branches  Out  (WAS  2004),  Barce-lona, Spain, July 25 - 26, 2004
* Kishore  Papineni  and  Salim  Roukos  and Todd  Ward  and  Wei-jing  Zhu  BLEU:  a Method  for  Automatic  Evaluation  of  Ma-chine Translation /  Proceedings of the 40th Annual Meeting of the Association for Com-putational  Linguistics  (ACL),  Philadelphia, July 2002, pp. 311-318.
