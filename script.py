import os
import re
import json
import requests
import base64
import shutil
import time
import csv
import logging
from pathlib import Path
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global configuration

load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN not found. Make sure you have a .env file with the variable defined.")

MAX_RUNS = 100
REPOS_CSV = "repos.csv"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Utility functions

def read_repositories(csv_path):
    repos = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            owner = row.get("owner")
            repo = row.get("repo")
            if owner and repo:
                repos.append((owner.strip(), repo.strip()))
    return repos

def sanitize_filename(name, max_length=100):
    name = re.sub(r"[^a-zA-Z0-9 \-_]", "", name)
    return name.strip().replace(" ", "_")[:max_length]

def create_run_dir(base_dir, run_id, run_name):
    dir_path = base_dir / f"{run_id}_{sanitize_filename(run_name)}"
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_text(data, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

def save_logs_zip(run_id, output_path, base_api_url):
    url = f"{base_api_url}/actions/runs/{run_id}/logs"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60)
        if resp.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(resp.content)
            return True
        else:
            logger.error(f"Could not download logs for run {run_id}. Status code: {resp.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading logs for run {run_id}: {e}")
    return False

def get_file_content(owner, repo, path, ref=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": ref} if ref else {}
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("encoding") == "base64":
                return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching YAML file {path}: {e}")
    return None

def get_workflow_runs(base_api_url, max_runs=None):
    runs = []
    page = 1
    while True:
        url = f"{base_api_url}/actions/runs"
        params = {"per_page": 100, "page": page}
        try:
            resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
            if resp.status_code != 200:
                logger.error(f"Error on page {page}. Status code: {resp.status_code}")
                break
            data = resp.json().get("workflow_runs", [])
            if not data:
                break
            runs.extend(data)
            if max_runs and len(runs) >= max_runs:
                break
            page += 1
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching workflow runs: {e}")
            break
    return runs[:max_runs] if max_runs else runs

def get_jobs_json(base_api_url, run_id):
    url = f"{base_api_url}/actions/runs/{run_id}/jobs"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        else:
            logger.error(f"Could not fetch jobs for run {run_id}. Status code: {resp.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching jobs for run {run_id}: {e}")
    return None

def get_run_detail(base_api_url, run_id):
    url = f"{base_api_url}/actions/runs/{run_id}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        else:
            logger.error(f"Could not fetch run details for run {run_id}. Status code: {resp.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching run details for run {run_id}: {e}")
    return None

# Main execution

if not GITHUB_TOKEN:
    raise EnvironmentError("Environment variable GITHUB_TOKEN is not defined.")

repositories = read_repositories(REPOS_CSV)

for owner, repo in repositories:
    logger.info(f"==> Processing repository: {owner}/{repo}")
    base_api_url = f"https://api.github.com/repos/{owner}/{repo}"
    output_dir = Path(f"{owner}_{repo}")
    all_dir = output_dir / "all_workflow_runs"
    failure_dir = output_dir / "failure_workflow_runs"
    retry_dir = output_dir / "retry_workflow_runs"

    all_dir.mkdir(parents=True, exist_ok=True)
    failure_dir.mkdir(parents=True, exist_ok=True)
    retry_dir.mkdir(parents=True, exist_ok=True)

    workflow_runs = get_workflow_runs(base_api_url, max_runs=MAX_RUNS)
    logger.info(f"{len(workflow_runs)} workflow runs found.")

    for run in workflow_runs:
        run_id = run["id"]
        run_name = run["name"]
        run_attempt = run.get("run_attempt", 1)
        run_conclusion = run.get("conclusion", "")

        logger.info(
            f"Processing run {run_id} - {run_name} "
            f"(attempt: {run_attempt}, conclusion: {run_conclusion})"
        )

        run_detail = get_run_detail(base_api_url, run_id)
        jobs_data = get_jobs_json(base_api_url, run_id)

        if not run_detail or not jobs_data:
            logger.error("Run skipped due to metadata error.")
            continue

        workflow_path = run_detail.get("path")
        head_sha = run_detail.get("head_sha")
        yaml_content = get_file_content(owner, repo, workflow_path, head_sha) if workflow_path else None
        yaml_filename = os.path.basename(workflow_path) if workflow_path else None

        run_all_dir = create_run_dir(all_dir, run_id, run_name)
        save_json(run_detail, run_all_dir / "workflow_run.json")
        save_json(jobs_data, run_all_dir / "jobs.json")

        if yaml_content and yaml_filename:
            save_text(yaml_content, run_all_dir / yaml_filename)

        logs_zip_path = run_all_dir / "logs.zip"
        if not save_logs_zip(run_id, logs_zip_path, base_api_url):
            logger.error("logs.zip not saved, run skipped for additional copies.")
            continue

        if run_conclusion == "failure":
            run_failure_dir = create_run_dir(failure_dir, run_id, run_name)
            shutil.copytree(run_all_dir, run_failure_dir, dirs_exist_ok=True)

        if run_attempt > 1:
            run_retry_dir = create_run_dir(retry_dir, run_id, run_name)
            shutil.copytree(run_all_dir, run_retry_dir, dirs_exist_ok=True)

        time.sleep(1)

logger.info("Extraction completed for all repositories.")
