# IMPORTANT: Streamlit Cloud Deployment Instructions

## The Issue

The `app.py` file and all application files are currently on the `copilot/deploy-to-streamlit-cloud` branch, **not** on the `main` branch.

## Solution: Deploy from the Correct Branch

When deploying to Streamlit Cloud, follow these steps:

### Step-by-Step Deployment

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Configure the deployment:
   - **Repository:** `KemosBram1/afp-estimator`
   - **Branch:** `copilot/deploy-to-streamlit-cloud` ⚠️ (NOT main!)
   - **Main file path:** `app.py`
5. Click "Deploy!"

### Important Notes

- ✅ The `app.py` file **EXISTS** on the `copilot/deploy-to-streamlit-cloud` branch
- ❌ The `app.py` file **DOES NOT EXIST** on the `main` branch yet
- Make sure to select the correct branch: `copilot/deploy-to-streamlit-cloud`

### Alternative: Merge to Main Branch

If you want to deploy from the `main` branch instead, you need to merge this pull request first:

1. Merge the `copilot/deploy-to-streamlit-cloud` branch into `main`
2. Then deploy from the `main` branch

## Verification

To verify which branch has the files, check:

- Branch `copilot/deploy-to-streamlit-cloud`: ✅ Has app.py, requirements.txt, .streamlit/config.toml
- Branch `main`: ❌ Only has README.md (unless PR is merged)

## Quick Test

You can verify the app works by cloning this branch:

```bash
git clone https://github.com/KemosBram1/afp-estimator.git
cd afp-estimator
git checkout copilot/deploy-to-streamlit-cloud
pip install -r requirements.txt
streamlit run app.py
```
