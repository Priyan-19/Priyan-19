#!/bin/bash
# Auto-fetches ALL public repos for the user via GitHub API

set -e

echo "Starting LOC counting process..."

WORKSPACE_DIR="$(pwd)"
OUTPUT_FILE="$WORKSPACE_DIR/loc/loc-data.json"
TEMP_DIR=$(mktemp -d)

# GitHub username — change this if you fork this script
GITHUB_USER="${GITHUB_USER:-Priyan-19}"

echo "Workspace: $WORKSPACE_DIR"
echo "Temporary directory: $TEMP_DIR"
echo "Fetching all public repos for: $GITHUB_USER"

# Fetch all public repos from GitHub API (handles pagination up to 10 pages)
ALL_REPOS=()
PAGE=1
while true; do
    RESPONSE=$(curl -s \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        "https://api.github.com/users/$GITHUB_USER/repos?type=public&per_page=100&page=$PAGE")

    COUNT=$(echo "$RESPONSE" | jq 'length')
    echo "  Page $PAGE: found $COUNT repos"

    if [ "$COUNT" -eq 0 ]; then
        break
    fi

    while IFS= read -r repo; do
        ALL_REPOS+=("$repo")
    done < <(echo "$RESPONSE" | jq -r '.[].full_name')

    PAGE=$((PAGE + 1))
done

echo "Total repos found: ${#ALL_REPOS[@]}"

cd "$TEMP_DIR"

echo "Cloning repositories..."
for repo in "${ALL_REPOS[@]}"; do
    echo "  Cloning $repo..."
    git clone --depth 1 "https://github.com/$repo.git" "$(basename $repo)" 2>/dev/null || echo "  Failed to clone $repo, skipping."
done

echo "Running tokei to count lines of code..."
tokei . --output json --exclude '*.md,*.txt,README*,LICENSE*' > "$OUTPUT_FILE"

echo "Cleaning up temporary directory..."
cd "$WORKSPACE_DIR"
rm -rf "$TEMP_DIR"

echo "LOC counting complete! Results saved to $OUTPUT_FILE"

cat "$OUTPUT_FILE" | jq '.'
