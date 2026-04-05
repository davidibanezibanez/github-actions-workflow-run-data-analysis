# Internship: GitHub Actions Workflow Run Data Analysis

**Duration:** First Semester 2025 (264 hours)  
**Contact:** [David Ibáñez](https://www.linkedin.com/in/davidibanezibanez)  
**Project Link:** [GitHub Repository](https://github.com/davidibanezibanez/github-actions-workflow-run-data-analysis)  

---

## Project Context
This internship was conducted at the Universidad de La Frontera under the supervision of a Ph.D. in Computer Science, as part of their broader research project: *GitHub Actions Workflow Run Data Analysis*. The overarching project aims to create a Large Language Model (LLM) capable of interpreting and providing user feedback for specific tasks related to different types of GitHub Actions logs. My role did not involve working directly with the LLM; instead, my contribution focused entirely on the fundamental phase of data extraction and dataset creation.

## Problem Statement and Objectives
Failed step logs and re-runs (retries for runs that failed due to factors external to the code) in GitHub Actions are often extensive and difficult to interpret. This project seeks to develop a tool capable of automatically extracting these logs via the GitHub API. The ultimate goal is to build a dataset that can subsequently be used to train a language model to facilitate the analysis and interpretation of these logs.

### General Objective
Develop a software solution that enables the extraction and structuring of failed step and re-run logs in GitHub Actions, facilitating the creation of a useful dataset to train language models for the automatic interpretation of errors in continuous integration workflows.

### Specific Objectives
* Investigate and document the fundamentals of tools used in machine learning.
* Analyze the *GHALogs* dataset to evaluate its applicability and limitations within the context of the project.
* Develop software for extracting and structuring logs from the GitHub Actions API and creating the dataset.

## Main Activities

1. **Documentation of Basic Data Science Concepts:** Creation of Markdown documents explaining foundational concepts applicable to this and other introductory data science projects, including practical examples and best practices.
2. **Review of the GHALogs Dataset and Associated Paper:** Analysis of the public dataset *"GHALogs: Large-Scale Dataset of GitHub Actions Runs"* (available on Zenodo) and its academic paper. The goal was to understand its structure (data types, metadata, logs), collection methodology, and potential applications. This served to compare approaches and validate or adjust our extraction strategy.
3. **Initial Software Development and Repository Reading:** The initial development phase involved loading environment variables and verifying the `GITHUB_TOKEN` for API authentication. The software then reads a `repos.csv` file, containing a list of repositories in the `owner/repo` format, and validates that each entry has the required fields to proceed.
4. **Collection of All Workflow Runs:** For each repository, the software fetches the latest workflow executions, limited by `MAX_RUNS`. For each run, it saves the metadata (`workflow_run.json`), associated jobs (`jobs.json`), the workflow YAML file, and the compressed logs (`logs.zip`) into an `all_workflow_runs` folder, organized in subdirectories by run ID and name.
5. **Filtering Failed Workflows:** The software reviews each stored workflow run and filters those with a `failure` status. All relevant information (JSON, YAML, and logs) for these cases is copied to a dedicated `failure_workflow_runs` folder, maintaining the file structure to facilitate further analysis.
6. **Detection of Re-runs:** The software identifies workflows that were re-executed. These runs are stored in the `retry_workflow_runs` folder with all their associated files. This enables the study of cases where a workflow initially failed due to external issues but was retried—a specific scenario poorly covered in official documentation.

## Results

A software tool capable of extracting and organizing logs corresponding to various workflows was successfully developed. This component was essential for transitioning from theoretical exploration to the practical application of the studied concepts, enabling the future generation of customized datasets tailored to the project's specific needs.

This project allows you to **automatically extract, organize, and store detailed information** about GitHub Actions executions (*workflow runs*) from multiple public repositories. It facilitates the creation of datasets for analysis, pipeline debugging, auditing failed runs, and more.

---

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

---

## Conclusions and Remarks

* During the initial stage of the internship, a comprehensive review and documentation of machine learning fundamentals and tools were conducted. This work established a solid foundation for understanding the broader technological context of the project.
* The analysis of the *GHALogs: A Large-Scale Dataset of GitHub Actions Runs* dataset was a key stage to not only evaluate the nature of the dataset but also to acquire the necessary knowledge to understand the project's core problem. It was discovered that while the dataset is extensive and valuable, it has limitations regarding the detail of available logs, especially at the level of individual steps. This observation reinforced the need for a custom log extraction tool capable of capturing more specific information to feed future language models.
* One of the main strengths identified during the internship was the ability to successfully integrate theoretical technical analysis with the practical development of software tools.
* Among the challenges encountered, there was an initial complexity in grasping the technical nuances of the problem statement. Furthermore, the log extraction process can be affected by the inherent complexity and variability of GitHub workflows, as well as the constraints and rate limits imposed by the GitHub API.

## References

Moriconi, F., Durieux, T., Falleri, J.-R., Francillon, A., & Troncy, R. (2025). GHALogs: Large-scale dataset of GitHub Actions runs. In *Proceedings of the 21st International Conference on Mining Software Repositories (MSR ’25)*. Association for Computing Machinery.
