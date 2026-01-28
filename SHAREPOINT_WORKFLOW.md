# SharePoint to Git Workflow Guide

## Your Situation

You have:
- ✅ Downloaded the app to your local machine
- ✅ Files in SharePoint where you're actively developing
- ❌ Changes in SharePoint don't reflect in your Git repository
- ❓ Want SharePoint to automatically push to Git

## The Reality

**SharePoint cannot directly push to Git automatically.** Here's why:

1. **SharePoint is not a version control system** - It's a document management/collaboration platform
2. **Git requires explicit commits** - You must manually commit and push changes
3. **No native integration** - SharePoint and Git don't have built-in sync functionality
4. **Different purposes** - SharePoint: file sharing; Git: version control

## The Problem with Your Current Workflow

```
SharePoint (Active Development)
       ↓
   ❌ No automatic sync
       ↓
Git Repository (Out of date)
       ↓
Streamlit Cloud (Deploys old code)
```

**This creates version conflicts and deployment issues!**

## Recommended Solutions

### 🥇 Solution 1: Develop Locally with Git (BEST PRACTICE)

This is the **professional, industry-standard approach**.

#### Why This is Best
- ✅ Single source of truth (Git)
- ✅ Full version control
- ✅ Automatic deployment to Streamlit Cloud
- ✅ Proper change tracking
- ✅ Easy rollback if needed
- ✅ Team collaboration support

#### How to Set Up

1. **Stop developing in SharePoint** (use it only for backups/documentation)

2. **Work from your local Git folder:**
```bash
# Navigate to your Git repository
cd /path/to/afp-estimator

# Make changes to files
nano app.py  # or use your preferred editor

# Test locally
streamlit run app.py

# Commit and push
git add .
git commit -m "Description of changes"
git push origin copilot/deploy-to-streamlit-cloud
```

3. **Streamlit Cloud automatically redeploys** (1-3 minutes)

#### Daily Workflow
```
Morning:
├─ git pull              # Get latest changes
├─ Edit files locally    # Make your changes
├─ streamlit run app.py  # Test
└─ git commit + push     # Deploy

Result: ✅ Changes live in 1-3 minutes
```

### 🥈 Solution 2: OneDrive/SharePoint Sync + Git (Hybrid)

If you **must** keep files in SharePoint, use OneDrive Desktop sync.

#### How It Works
```
SharePoint ←→ OneDrive Sync ←→ Local Folder ←→ Git
```

#### Setup Steps

1. **Install OneDrive Desktop** (if not already installed)
   - Windows: Usually pre-installed
   - Mac: Download from Microsoft

2. **Sync your SharePoint folder:**
   - Open SharePoint in browser
   - Click "Sync" button on your document library
   - Choose local folder location

3. **Clone/Move Git repository into synced folder:**
```bash
# Navigate to OneDrive folder
cd ~/OneDrive/YourSharePoint

# Clone repository here
git clone https://github.com/KemosBram1/afp-estimator.git
cd afp-estimator

# Or move existing repo
mv /old/location/afp-estimator ~/OneDrive/YourSharePoint/
```

4. **Work normally with Git:**
```bash
# Files sync to SharePoint automatically via OneDrive
# But you must still manually commit and push to Git

# Edit files
nano app.py

# Test
streamlit run app.py

# Commit to Git (not automatic!)
git add .
git commit -m "Your changes"
git push origin copilot/deploy-to-streamlit-cloud
```

#### Important Notes
⚠️ **You STILL must manually commit and push to Git**
⚠️ OneDrive sync ≠ Git commit
⚠️ Add `.git` folder to OneDrive exclusions to avoid issues

#### OneDrive Exclusions
```bash
# Prevent OneDrive from syncing Git metadata
# Add these to OneDrive exclusions:
- .git/
- __pycache__/
- *.pyc
- .DS_Store
```

### 🥉 Solution 3: Manual Sync Process

If you can't change your workflow immediately, use manual sync.

#### Process

1. **Download files from SharePoint** when you want to deploy
2. **Copy to your local Git repository**
3. **Commit and push to Git**
4. **Repeat regularly** (daily, after major changes)

#### Step-by-Step

```bash
# 1. Download updated files from SharePoint
#    (Use SharePoint web interface or OneDrive)

# 2. Copy to Git repository
cp ~/Downloads/app.py ~/path/to/afp-estimator/app.py

# 3. Check what changed
cd ~/path/to/afp-estimator
git status
git diff app.py

# 4. Test locally
streamlit run app.py

# 5. Commit and push
git add .
git commit -m "Sync from SharePoint - [describe changes]"
git push origin copilot/deploy-to-streamlit-cloud

# 6. Wait for Streamlit Cloud to redeploy
```

#### Pros and Cons
✅ Simple, no setup required
✅ Works with any file storage
❌ Manual, time-consuming
❌ Easy to forget
❌ High risk of version conflicts
❌ Not professional for production code

### 🔧 Solution 4: Automation Script (Advanced)

For advanced users, create a script to automate the sync.

#### PowerShell Script (Windows)
```powershell
# sync-to-git.ps1
$SharePointFolder = "C:\Users\YourName\OneDrive\SharePoint\AppFiles"
$GitRepo = "C:\Users\YourName\Projects\afp-estimator"

# Copy files
Copy-Item "$SharePointFolder\*.py" -Destination $GitRepo -Force
Copy-Item "$SharePointFolder\requirements.txt" -Destination $GitRepo -Force

# Git operations
cd $GitRepo
git add .
$message = "Auto-sync from SharePoint - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git commit -m $message
git push origin copilot/deploy-to-streamlit-cloud

Write-Host "Sync complete! Streamlit Cloud will redeploy in 1-3 minutes."
```

#### Bash Script (Mac/Linux)
```bash
#!/bin/bash
# sync-to-git.sh

SHAREPOINT_FOLDER="$HOME/OneDrive/SharePoint/AppFiles"
GIT_REPO="$HOME/Projects/afp-estimator"

# Copy files
cp "$SHAREPOINT_FOLDER"/*.py "$GIT_REPO/"
cp "$SHAREPOINT_FOLDER/requirements.txt" "$GIT_REPO/"

# Git operations
cd "$GIT_REPO"
git add .
git commit -m "Auto-sync from SharePoint - $(date '+%Y-%m-%d %H:%M')"
git push origin copilot/deploy-to-streamlit-cloud

echo "Sync complete! Streamlit Cloud will redeploy in 1-3 minutes."
```

#### Usage
```bash
# Run manually when you want to sync
./sync-to-git.sh

# Or schedule with cron (Mac/Linux)
# Run every hour during work hours (9 AM - 5 PM)
0 9-17 * * 1-5 /path/to/sync-to-git.sh

# Or Task Scheduler (Windows)
# Create scheduled task to run script
```

⚠️ **Warning:** Automated scripts can cause issues if:
- You're working directly in Git repo at the same time
- Files have conflicts
- SharePoint has old versions

## Comparison of Solutions

| Solution | Ease of Setup | Maintenance | Professional | Recommended |
|----------|---------------|-------------|--------------|-------------|
| **Local Git Only** | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐⭐ Low | ⭐⭐⭐⭐⭐ Yes | ✅ **BEST** |
| **OneDrive + Git** | ⭐⭐⭐ Medium | ⭐⭐⭐ Medium | ⭐⭐⭐ OK | ✅ If needed |
| **Manual Sync** | ⭐⭐⭐⭐⭐ Easy | ⭐ High | ⭐ No | ❌ Temporary only |
| **Automation Script** | ⭐⭐ Hard | ⭐⭐⭐ Medium | ⭐⭐⭐ OK | ⚠️ Advanced users |

## Step-by-Step Migration to Best Practice

### Week 1: Transition Period
1. **Keep SharePoint** as backup
2. **Start working in local Git** repository
3. **Manually backup to SharePoint** after major changes
4. Get comfortable with Git workflow

### Week 2-3: Git Primary
1. **Git becomes your primary** development location
2. **Test and deploy** through Git
3. **Occasional backups** to SharePoint
4. Build confidence in Git workflow

### Week 4+: Git Only
1. **Stop actively developing in SharePoint**
2. **Use SharePoint** only for:
   - Documentation
   - Design files
   - Requirements documents
   - Final release backups
3. **All code development** in Git

## Understanding the Workflow

### Current (Problematic) Workflow
```
You edit in SharePoint
        ↓
    ❌ No sync
        ↓
Git repository out of date
        ↓
Streamlit Cloud deploys old code
        ↓
Your changes not visible!
```

### Recommended Workflow
```
You edit locally in Git folder
        ↓
Test with: streamlit run app.py
        ↓
Commit: git add . && git commit -m "..."
        ↓
Push: git push origin copilot/...
        ↓
Streamlit Cloud auto-redeploys (1-3 min)
        ↓
Your changes are LIVE! ✅
```

## Common Questions

### Q: Can I link SharePoint to automatically push to Git?
**A:** No, SharePoint doesn't have this capability. Git requires explicit commits.

### Q: Why can't SharePoint just sync like Google Drive?
**A:** SharePoint can sync files (via OneDrive), but that's different from Git commits. Git needs:
- Commit messages
- Change descriptions
- Manual approval of each change
- Proper version tracking

### Q: What if multiple people work on the code?
**A:** This is exactly why you should use Git! Git handles:
- Multiple developers
- Merge conflicts
- Branch management
- Code review
- Proper collaboration

SharePoint will create confusion with multiple versions.

### Q: I'm more comfortable with SharePoint. Can I keep using it?
**A:** For code development? No, not recommended. Use SharePoint for:
- Documentation (Word, PowerPoint)
- Requirements and specifications
- Design mockups
- Final release archives
- Non-code project files

Use Git for:
- All Python code (.py files)
- Configuration files
- Requirements.txt
- Any file that needs version control

### Q: What if I forget to push to Git?
**A:** Your changes won't be deployed. This is actually a **feature**, not a bug! You want manual control over what goes to production. Always:
1. Test locally
2. Review your changes
3. Commit with good message
4. Push when ready

### Q: How do I know if my Git push worked?
**A:** 
1. Check your Git repository on GitHub
2. Look for your latest commit
3. Go to Streamlit Cloud dashboard
4. Watch deployment status
5. Visit your live app URL

## Setting Up Your Ideal Workflow

### One-Time Setup
```bash
# 1. Clone repository (if not already done)
git clone https://github.com/KemosBram1/afp-estimator.git
cd afp-estimator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test it works
streamlit run app.py

# 4. Configure Git (if first time)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 5. You're ready!
```

### Daily Development
```bash
# Morning routine
cd ~/path/to/afp-estimator
git pull                    # Get latest changes

# During the day
# - Edit files with your favorite editor
# - Test frequently: streamlit run app.py

# When ready to deploy
git status                  # See what changed
git add .                   # Stage changes
git commit -m "Your changes"  # Commit
git push origin copilot/deploy-to-streamlit-cloud  # Deploy!

# Wait 1-3 minutes, then check your live app
```

## Troubleshooting

### Issue: "I made changes in SharePoint but they're not live"
**Solution:** SharePoint changes don't automatically go to Git. Follow one of the solutions above.

### Issue: "My local files are different from SharePoint"
**Solution:** Decide on single source of truth:
- **Recommended:** Git is the source, backup to SharePoint
- **Not recommended:** SharePoint is source, manually sync to Git

### Issue: "OneDrive sync conflicts with Git"
**Solution:** 
- Exclude `.git` folder from OneDrive sync
- Don't edit files in both places simultaneously
- Use Git for version control, not OneDrive

### Issue: "I want teammates to access files in SharePoint"
**Solution:**
- **For code:** Use GitHub, not SharePoint
- **For documents:** Use SharePoint
- **For both:** Give teammates Git access + SharePoint for docs

## Best Practices Summary

✅ **DO:**
- Develop locally with Git as your source of truth
- Test before committing
- Use meaningful commit messages
- Push regularly (daily or after major changes)
- Use SharePoint for documents, not code

❌ **DON'T:**
- Develop code in SharePoint
- Expect automatic sync between SharePoint and Git
- Edit the same files in multiple locations
- Skip testing before pushing
- Ignore Git commit messages

## Getting Help

If you're stuck:
1. Review [UPDATE_WORKFLOW.md](UPDATE_WORKFLOW.md) for Git basics
2. Check [QUICK_UPDATE_GUIDE.md](QUICK_UPDATE_GUIDE.md) for quick commands
3. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

## Next Steps

1. **Choose your solution** (Recommended: Local Git Only)
2. **Set up your workflow** following the instructions above
3. **Test the process** with a small change
4. **Make it your daily routine**

**Remember:** Professional developers use Git for code, not SharePoint. Make the transition and you'll have a much smoother development experience! 🚀
