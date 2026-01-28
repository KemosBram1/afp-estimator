# Quick Reference: Updating Your Deployed App

## TL;DR

**Question:** Will updates work after deployment?

**Answer:** YES! Just push changes to GitHub and Streamlit Cloud auto-redeploys in 1-3 minutes.

## Three-Step Update Process

```bash
# 1. Test locally
streamlit run app.py

# 2. Commit and push
git add .
git commit -m "Your change description"
git push origin copilot/deploy-to-streamlit-cloud

# 3. Wait 1-3 minutes
# Your app will automatically redeploy!
```

## Common Update Commands

### Fix a Bug
```bash
# Edit the file
nano app.py

# Test it
streamlit run app.py

# Deploy it
git add app.py
git commit -m "Fix: description of bug fix"
git push origin copilot/deploy-to-streamlit-cloud
```

### Add a Feature
```bash
# Edit files
nano app.py

# Test thoroughly
streamlit run app.py

# Deploy
git add .
git commit -m "Feature: description of new feature"
git push origin copilot/deploy-to-streamlit-cloud
```

### Update Dependencies
```bash
# Edit requirements
nano requirements.txt

# Test with new versions
pip install -r requirements.txt
streamlit run app.py

# Deploy
git add requirements.txt
git commit -m "Update: upgrade packages"
git push origin copilot/deploy-to-streamlit-cloud
```

### Undo Last Change
```bash
# Revert last commit
git revert HEAD

# Push the revert
git push origin copilot/deploy-to-streamlit-cloud
```

## Key Differences: Local vs Cloud

| Aspect | Local Development | Streamlit Cloud |
|--------|------------------|-----------------|
| **Update trigger** | Save file | Git push |
| **Update speed** | Instant | 1-3 minutes |
| **Update method** | Auto-detect | Auto-redeploy |
| **Testing** | Same machine | Live production |
| **Rollback** | Undo/redo | Git revert |

## Before Every Push

✅ **Checklist:**
- [ ] Tested locally with `streamlit run app.py`
- [ ] All calculations verified
- [ ] No Python syntax errors
- [ ] Requirements up to date (if changed)
- [ ] Commit message is descriptive

## If Something Breaks

### Quick Fix
```bash
# Fix the issue
nano app.py

# Test
streamlit run app.py

# Deploy fix immediately
git add .
git commit -m "Hotfix: description"
git push origin copilot/deploy-to-streamlit-cloud
```

### Rollback
```bash
# Go back to previous version
git revert HEAD
git push origin copilot/deploy-to-streamlit-cloud
```

### Check Logs
1. Go to your app on Streamlit Cloud
2. Click hamburger menu (☰)
3. Select "Manage app"
4. View deployment logs

## Pro Tips

💡 **Always test locally first** - Catch errors before they go live

💡 **Use descriptive commit messages** - Makes it easy to track changes

💡 **Make small changes** - Easier to debug and rollback

💡 **Monitor after deployment** - Visit app after each update

💡 **Keep main branch stable** - Use feature branches for experiments

## Need More Details?

See `UPDATE_WORKFLOW.md` for comprehensive documentation including:
- Detailed workflow explanations
- Rollback procedures
- Branch management
- Common scenarios
- Troubleshooting guide

## Support

- Full docs: `UPDATE_WORKFLOW.md`
- Streamlit docs: https://docs.streamlit.io
- Deployment guide: `DEPLOYMENT.md`
- Troubleshooting: `TROUBLESHOOTING.md`
