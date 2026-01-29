#!/bin/bash

# set-git-push.sh
# Monitors a local SharePoint-synced repo and auto-commits/pushes changes to GitHub.
# -------------------------------------------------------------------------------
# QUICK START
# 1) Set REPO_PATH below to your local SharePoint-synced Git repo.
# 2) Make executable: chmod +x ./set-git-push.sh
# 3) Run manually:   ./set-git-push.sh
# -------------------------------------------------------------------------------

REPO_PATH="/Users/bramuelkemoli/Library/CloudStorage/OneDrive-AssociatedFireProtection/SLM - Sales & Marketing (2025) - src"
BRANCH="main"

# Optional notifications (requires mail to be configured on your Mac)
EMAIL_TO="bkemoli@associatedfire.net"
MAIL_BIN="/usr/bin/mail"

# Log file location for launchd runs
LOG_FILE="/tmp/com.afp.git-sync.log"

log() {
  local msg="$1"
  local ts
  ts=$(date "+%Y-%m-%d %H:%M:%S")
  echo "[$ts] $msg" | tee -a "$LOG_FILE"
}

notify() {
  local subject="$1"
  local body="$2"
  if [[ -n "$EMAIL_TO" && -x "$MAIL_BIN" ]]; then
    echo "$body" | "$MAIL_BIN" -s "$subject" "$EMAIL_TO"
  fi
}

# Go to the local GitHub repository directory
cd "$REPO_PATH" || exit 1

# Pull the latest changes from the GitHub repository
stashed=0
if [[ -n $(git status --porcelain) ]]; then
  log "Local changes detected before pull; stashing."
  git stash push -u -m "auto-sync-$(date "+%Y-%m-%d %H:%M:%S")" >/dev/null
  stashed=1
fi

if ! git pull --rebase origin "$BRANCH"; then
  log "Pull failed. Resolve conflicts manually."
  notify "Git Sync Error: pull failed" "Pull/rebase failed in $REPO_PATH. Manual intervention required."
  exit 1
fi

if [[ $stashed -eq 1 ]]; then
  if ! git stash pop; then
    log "Stash pop produced conflicts. Resolve manually."
    notify "Git Sync Warning: stash conflicts" "Stash pop produced conflicts in $REPO_PATH. Manual intervention required."
    exit 1
  fi
fi

# Check for changes in the SharePoint sync folder
if [[ -n $(git status --porcelain) ]]; then
  log "Changes detected. Committing and pushing."

  # Stage all changes
  git add .

  # Commit changes (auto-generate a message with the current timestamp)
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  git commit -m "Auto-update from SharePoint on $TIMESTAMP"

  # Push the changes to the GitHub repository
  if ! git push origin "$BRANCH"; then
    log "Push failed. Resolve manually."
    notify "Git Sync Error: push failed" "Push failed in $REPO_PATH. Manual intervention required."
    exit 1
  fi

  log "Changes successfully pushed to GitHub."
  notify "Git Sync Success" "Changes detected and pushed from $REPO_PATH."
else
  log "No changes detected. Repository is up-to-date."
fi
