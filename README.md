# GitHub Actions Workflow Run Data Analysis

This project allows you to **automatically extract, organize, and store detailed information** about GitHub Actions executions (*workflow runs*) from multiple public repositories. It facilitates the creation of datasets for analysis, pipeline debugging, auditing failed runs, and more.

## What does this software do?

The main script (`script.py`) iterates through a list of repositories specified in a `repos.csv` file and:

- Extracts up to `MAX_RUNS` recent executions from each repository.
- Downloads the following elements for each run:
  - General Metadata (`workflow_run.json`)
  - Job Details (`jobs.json`)
  - Workflow YAML file
  - Compressed Logs (`logs.zip`)
- Classifies each execution into organized folders based on its status:
  - All executions
  - Failed executions only
  - Rerun executions only

For further details, please read the documentation in `notebook.ipynb`.

## Expected Project Structure

```text
github-actions-workflow-run-data-extractor/
├── env                      ← Python environment
├── .env                     ← GitHub Token
├── .gitignore               ← Gitignore to protect the token
├── notebook.ipynb           ← Notebook with documentation and script execution
├── README.md                ← Project Readme
├── repos.csv                ← List of repositories to analyze
├── requirements.txt         ← Required libraries
├── script.py                ← Main software script
├── owner1_repo1/            ← Folder for each processed repository
│   ├── all_workflow_runs/
│   ├── failure_workflow_runs/
│   └── retry_workflow_runs/

```

## Steps to Prepare Environment and Run Software

### 1. Create, activate virtual environment, and select kernel

#### On Windows:

```bash
python -m venv env
env\Scripts\activate

```

#### On macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate

```

#### Select kernel in `notebook.ipynb`

### 2. Install Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt

```

> This will install:
> * `requests`: To interact with the GitHub API
> * `python-dotenv`: To load environment variables from `.env`
> * `notebook`: To work with Jupyter Notebook
> 
> 

### 3. Create the `.env` file

In the project root, create a file named `.env` with the following content:

```ini
GITHUB_TOKEN=your_token_here

```

> The token must have permissions to read public repository information (`repo` scope).

### 4. Create the `.gitignore` file

In the project root, create a file named `.gitignore` with the following content:

```text
.env
__pycache__/
*.pyc
env/

```

> This ensures that no sensitive content is uploaded to any repository.

### 5. Verify or edit `repos.csv`

The `repos.csv` file comes with **10 example repositories**, one per line in the following format:

```csv
owner,repo
vercel,next.js
...,...

```

You can **edit this file** to add or remove repositories to process, but it must not be deleted. It **must exist** in the project root and follow the `owner,repo` format.

### 6. Verify or edit the number of workflow runs to extract (`MAX_RUNS`)

In the `script.py` file, you will find a variable at the beginning:

```python
MAX_RUNS = 100

```

You can decrease or increase this value. In its current state, the software will extract 100 workflow runs for each of the repositories listed in `repos.csv`.

## How to execute the script?

Open the `notebook.ipynb` file and execute the cell containing:

```python
!python script.py

```

This will start the extraction and data saving process for all repositories listed in `repos.csv`.

## Contact

David Ibáñez - https://www.linkedin.com/in/davidibanezibanez/

Project Link: https://github.com/davidibanezibanez/github-actions-workflow-run-data-analysis
