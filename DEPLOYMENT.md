# Streamlit Cloud Deployment Guide

## Quick Start

Your AFP Quote Estimator is now ready to deploy on Streamlit Cloud!

## Steps to Deploy

1. **Ensure this repository is pushed to GitHub**
   - The repository is at: `KemosBram1/afp-estimator`
   - All necessary files have been committed

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select the repository: `KemosBram1/afp-estimator`
   - **IMPORTANT:** Select the branch: `copilot/deploy-to-streamlit-cloud` 
     (The app files are on this branch. If deploying from `main`, ensure the PR is merged first)
   - Set the main file path: `app.py`
   - Click "Deploy!"

3. **Wait for deployment**
   - Streamlit Cloud will automatically install dependencies from `requirements.txt`
   - The app will be live in a few minutes
   - You'll get a URL like: `https://[your-app-name].streamlit.app`

## What's Included

✅ `app.py` - Main Streamlit application
✅ `requirements.txt` - Python dependencies (streamlit, pandas)
✅ `.streamlit/config.toml` - Streamlit configuration
✅ `.gitignore` - Ignores unnecessary files
✅ `README.md` - Documentation and usage instructions

## Application Features

- Professional quote estimation interface
- Cost breakdown for labor, materials, equipment, travel, and misc
- Real-time calculations with adjustable markup
- Export quotes as text or CSV files
- Clean, responsive design

## Troubleshooting

### "app.py file does not exist" error

If you get this error when deploying:
- **Make sure you selected the branch `copilot/deploy-to-streamlit-cloud`** (not `main`)
- The application files are currently on the `copilot/deploy-to-streamlit-cloud` branch
- If you want to deploy from `main`, merge the pull request first

### Other issues

If deployment fails:
- Check that `requirements.txt` has all necessary dependencies
- Ensure `app.py` is in the root directory
- Verify that the Python version is compatible (3.8+)
- Check Streamlit Cloud logs for specific errors

## Next Steps

After deployment, you can:
- Share the URL with your team
- Customize the app further
- Add authentication if needed
- Connect to databases for saving quotes
- Add more features as requirements grow

## Support

For Streamlit Cloud support:
- Documentation: https://docs.streamlit.io/streamlit-community-cloud
- Community Forum: https://discuss.streamlit.io
