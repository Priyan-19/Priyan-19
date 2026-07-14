#!/usr/bin/env python3
import urllib.request
import json
import re
import sys
import os
from pathlib import Path

USERNAME = "Priyan-19"
README_PATH = Path("README.md")

def fetch_total_repos():
    url = f"https://api.github.com/users/{USERNAME}"
    headers = {"User-Agent": "Mozilla/5.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("public_repos", 0)
    except Exception as e:
        print(f"Error fetching repo count from GitHub API: {e}", file=sys.stderr)
        # fallback
        return 15

def main():
    if not README_PATH.exists():
        print(f"Error: {README_PATH} not found!", file=sys.stderr)
        sys.exit(1)
        
    print("Fetching total public repositories count...")
    repo_count = fetch_total_repos()
    print(f"Total public repositories: {repo_count}")
    
    badge_url = f"https://img.shields.io/badge/Total%20Repositories-{repo_count}-6E40C9?style=for-the-badge&logo=github&logoColor=white"
    dest_url = f"https://github.com/{USERNAME}?tab=repositories"
    badge_html = f'<p align="center">\n  <a href="{dest_url}"><img src="{badge_url}" alt="Total Repositories" /></a>\n</p>'
    
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()
        
    pattern = re.compile(
        r"(<!-- REPOS-BADGE:START -->)(.*?)(<!-- REPOS-BADGE:END -->)",
        re.DOTALL
    )
    
    if not pattern.search(readme_content):
        print("Error: <!-- REPOS-BADGE:START --> and/or <!-- REPOS-BADGE:END --> markers not found in README.md", file=sys.stderr)
        sys.exit(1)
        
    new_content = pattern.sub(
        f"\\1\n{badge_html}\n\\3",
        readme_content
    )
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("README.md successfully updated with latest repository badge count!")

if __name__ == "__main__":
    main()
