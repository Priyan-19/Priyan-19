#!/usr/bin/env python3
import urllib.request
import json
import re
import sys
from pathlib import Path

USERNAME = "Priyan-19"
README_PATH = Path("README.md")

PROJECTS = [
    {
        "name": "Reborn Motors Website 🚗",
        "repo": "RBM-Covai",
        "description": "A sleek website for Reborn Motors, showcasing modern automotive services.",
        "tech": ["JavaScript", "HTML5", "CSS3"]
    },
    {
        "name": "Tanzi Task Manager ⏰",
        "repo": "TANZI",
        "description": "A reminder-based task management system to keep your daily schedules on track.",
        "tech": ["React", "JavaScript", "Tailwind CSS"]
    },
    {
        "name": "Mospee Speedometer 📱",
        "repo": "MOSPEE",
        "description": "A reliable mobile speedometer app to track real-time velocity and trip distance.",
        "tech": ["Java", "Android Studio"]
    },
    {
        "name": "DictHero 📖",
        "repo": "DictHero",
        "description": "An interactive vocabulary builder to learn and store new words effortlessly.",
        "tech": ["HTML5", "CSS3", "JavaScript"]
    },
    {
        "name": "MonsterVerse Extension 👾",
        "repo": "Monsterverse_Extention",
        "description": "A MonsterVerse-themed extension bringing custom themes and tools to VS Code.",
        "tech": ["TypeScript", "VS Code API"]
    },
    {
        "name": "WiFi Radar 📶",
        "repo": "WiFi_Radar",
        "description": "A WiFi scanner using ESP32 to map and analyze nearby wireless signals.",
        "tech": ["Python", "ESP32"]
    }
]

TECH_BADGES = {
    "React": "https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB",
    "JavaScript": "https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black",
    "TypeScript": "https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white",
    "HTML5": "https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white",
    "CSS3": "https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white",
    "Tailwind CSS": "https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white",
    "Java": "https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white",
    "Android Studio": "https://img.shields.io/badge/Android_Studio-3DDC84?style=flat-square&logo=android-studio&logoColor=white",
    "Python": "https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white",
    "ESP32": "https://img.shields.io/badge/ESP32-E7352C?style=flat-square&logo=espressif&logoColor=white",
    "VS Code API": "https://img.shields.io/badge/VS_Code-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white"
}

def fetch_total_repos():
    url = f"https://api.github.com/users/{USERNAME}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("public_repos", 0)
    except Exception as e:
        print(f"Error fetching repo count from GitHub API: {e}", file=sys.stderr)
        # fallback
        return 15

def generate_projects_html(repo_count):
    badge_url = f"https://img.shields.io/badge/Total%20Repositories-{repo_count}-6E40C9?style=for-the-badge&logo=github&logoColor=white"
    dest_url = f"https://github.com/{USERNAME}?tab=repositories"
    badge_html = f'<a href="{dest_url}"><img src="{badge_url}" alt="Total Repositories" /></a>'
    
    html = "<table width=\"90%\" align=\"center\">\n"
    
    # 2 columns x 3 rows
    for i in range(0, len(PROJECTS), 2):
        html += "  <tr>\n"
        for j in range(2):
            if i + j < len(PROJECTS):
                proj = PROJECTS[i+j]
                name = proj["name"]
                repo = proj["repo"]
                desc = proj["description"]
                techs = proj["tech"]
                
                badges_html = " ".join([f'<img src="{TECH_BADGES.get(t, "")}" alt="{t}" />' for t in techs if t in TECH_BADGES])
                
                html += f'    <td width="50%" valign="top">\n'
                html += f'      <h4>{name}</h4>\n'
                html += f'      <p><font size="2">{desc}</font></p>\n'
                html += f'      <p>\n'
                html += f'        {badges_html}\n'
                html += f'      </p>\n'
                html += f'      <a href="https://github.com/{USERNAME}/{repo}"><font size="2">Explore Repository →</font></a>\n'
                html += f'    </td>\n'
        html += "  </tr>\n"
        
    html += "</table>\n\n"
    html += f'<p align="center">\n  {badge_html}\n</p>'
    return html

def main():
    if not README_PATH.exists():
        print(f"Error: {README_PATH} not found!", file=sys.stderr)
        sys.exit(1)
        
    print("Fetching total public repositories count...")
    repo_count = fetch_total_repos()
    print(f"Total public repositories: {repo_count}")
    
    projects_html = generate_projects_html(repo_count)
    
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()
        
    pattern = re.compile(
        r"(<!-- TOP-PROJECTS:START -->)(.*?)(<!-- TOP-PROJECTS:END -->)",
        re.DOTALL
    )
    
    if not pattern.search(readme_content):
        print("Error: <!-- TOP-PROJECTS:START --> and/or <!-- TOP-PROJECTS:END --> markers not found in README.md", file=sys.stderr)
        sys.exit(1)
        
    new_content = pattern.sub(
        f"\\1\n{projects_html}\n\\3",
        readme_content
    )
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("README.md successfully updated with latest projects and repository badge!")

if __name__ == "__main__":
    main()
