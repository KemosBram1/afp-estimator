# IMPORTANT: Fix for "app.py does not exist" Error

## The Issue

When trying to deploy to Streamlit Cloud from the `main` branch, you get: **"app.py file does not exist"**

This happens because the `app.py` file is currently only on the `copilot/deploy-to-streamlit-cloud` branch, not on the remote `main` branch yet.

## ✅ IMMEDIATE SOLUTION (Recommended)

Deploy from the `copilot/deploy-to-streamlit-cloud` branch instead of `main`:

### Step-by-Step Deployment

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Configure the deployment:
   - **Repository:** `KemosBram1/afp-estimator`
   - **Branch:** `copilot/deploy-to-streamlit-cloud` ⚠️ **← SELECT THIS BRANCH**
   - **Main file path:** `app.py`
5. Click "Deploy!"

The app will deploy successfully because all files exist on this branch.

## 🔄 ALTERNATIVE SOLUTION

If you prefer to deploy from the `main` branch:

1. **Merge this Pull Request** to the `main` branch
   - Go to the GitHub repository
   - Find the pull request for `copilot/deploy-to-streamlit-cloud`
   - Merge it into `main`

2. **Then deploy from `main`**
   - Select branch `main` in Streamlit Cloud
   - The `app.py` file will now be available

## Verification

Current status of branches on GitHub:

- ✅ **Branch `copilot/deploy-to-streamlit-cloud`**: Has all files (app.py, requirements.txt, etc.) - **READY TO DEPLOY**
- ❌ **Branch `main`**: Only has README.md - **NOT READY** (until PR is merged)

## Why This Happened

The application was developed on the `copilot/deploy-to-streamlit-cloud` branch as part of a pull request workflow. To deploy, you need to either:
- Use the development branch directly, OR
- Merge the changes to main first

## Quick Test (Optional)

You can test the app locally from the correct branch:

```bash
git clone https://github.com/KemosBram1/afp-estimator.git
cd afp-estimator
git checkout copilot/deploy-to-streamlit-cloud
pip install -r requirements.txt
streamlit run app.py
```
