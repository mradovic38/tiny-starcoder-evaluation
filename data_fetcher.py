import os
import shutil
import git


# Function to clone a public GitHub repository
def clone_repo(repo_url: str, clone_dir: str = "repo") -> None:
    """
    Clones the given GitHub repository into the clone_dir folder.
    
    Args:
        repo_url (str): URL of the GitHub repository
        clone_dir (str): Directory to clone the repository into
    """
    if os.path.exists(clone_dir):
        return

    print(f"Cloning repository from {repo_url} into {clone_dir}...")
    git.Repo.clone_from(repo_url, clone_dir)
    print("Repository cloned successfully.")

# Function to collect all Python files and store them in the dataset folder
def collect_python_files(source_dir: str, target_dir:str = "code_examples") -> None:
    """
    Collects all Python (.py) files from the source_dir and stores them in the target_dir.
    
    Args:
        source_dir (str): Directory to search for Python files
        target_dir (str): Directory to store the collected Python files
    """
    if os.path.exists(target_dir):
        return
    
    os.makedirs(target_dir, exist_ok=True)

    print(f"Collecting Python files from {source_dir} into {target_dir}...")

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".py") and file != '__init__.py':
                full_path = os.path.join(root, file)
                target_path = os.path.join(target_dir, file)
                shutil.copy(full_path, target_path)
                print(f"Copied: {full_path} -> {target_path}")

    print(f"Python file collection complete. Files are saved in {target_dir}.")

if __name__ == "__main__":
    repo_url = "https://github.com/mradovic38/football_analysis"

    # Clone the repository
    clone_repo(repo_url, clone_dir="repo")

    # Collect all Python files from the cloned repository
    collect_python_files("repo", target_dir="code_examples")
