#!/bin/bash

# set-git-push.sh
# Monitors a local SharePoint-synced repo and auto-commits/pushes changes to GitHub.
# -------------------------------------------------------------------------------
# QUICK START
# 1) Set REPO_PATH below to your local SharePoint-synced Git repo.
# 2) Make executable: chmod +x ./set-git-push.sh
# 3) Run manually:   ./set-git-push.sh
# -------------------------------------------------------------------------------

REPO_PATH="/path/to/your/local/repo"
BRANCH="main"

# Go to the local GitHub repository directory
cd "$REPO_PATH" || exit 1

# Pull the latest changes from the GitHub repository
git pull origin "$BRANCH"

# Check for changes in the SharePoint sync folder
if [[ -n $(git status --porcelain) ]]; then
  echo "Changes detected. Pushing updates to GitHub."

  # Stage all changes
  git add .

  # Commit changes (auto-generate a message with the current timestamp)
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  git commit -m "Auto-update from SharePoint on $TIMESTAMP"

  # Push the changes to the GitHub repository
  git push origin "$BRANCH"

  echo "Changes successfully pushed to GitHub."
else
  echo "No changes detected. Repository is up-to-date."
fi
