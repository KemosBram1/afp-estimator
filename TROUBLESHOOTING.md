# Streamlit Cloud Deployment Troubleshooting Guide

## Common Deployment Issues and Solutions

### Issue 1: Outdated Package Versions
**Symptom:** Deployment fails with dependency errors or compatibility issues

**Solution:** ✅ FIXED
- Updated `streamlit` from 1.31.0 to >=1.53.0
- Updated `pandas` from 2.2.0 to >=2.3.0
- Using flexible version constraints (>=) to allow minor updates

### Issue 2: Missing Python Version Specification
**Symptom:** Streamlit Cloud uses wrong Python version

**Solution:** ✅ FIXED
- Added `.python-version` file specifying Python 3.12
- Streamlit Cloud will now use the correct Python version

### Issue 3: Branch Selection
**Symptom:** "app.py does not exist" error

**Solution:** Ensure you're deploying from the correct branch
- Deploy from: `copilot/deploy-to-streamlit-cloud`
- OR merge this PR to `main` and deploy from `main`

### Issue 4: Memory or Resource Limits
**Symptom:** App crashes during startup or runs slowly

**Solution:**
- The current app is lightweight and shouldn't hit limits
- If issues persist, consider:
  - Reducing default data sizes
  - Lazy loading of resources
  - Using `@st.cache_data` for expensive operations

### Issue 5: Import Errors
**Symptom:** ModuleNotFoundError during deployment

**Solution:** ✅ All dependencies are in requirements.txt
- streamlit
- pandas
- Standard library modules (datetime, re) - no installation needed

## Deployment Checklist

Before deploying to Streamlit Cloud:

- [x] **requirements.txt** exists with all dependencies
- [x] **app.py** exists in root directory
- [x] **.python-version** specifies Python version
- [x] **.streamlit/config.toml** for theme configuration
- [x] **No syntax errors** in Python code
- [x] **All imports** are available

## How to Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - **Repository:** KemosBram1/afp-estimator
   - **Branch:** copilot/deploy-to-streamlit-cloud
   - **Main file:** app.py
5. Click "Deploy!"

## Checking Deployment Logs

If deployment still fails:

1. Go to your app on Streamlit Cloud
2. Click the hamburger menu (☰) in the top right
3. Select "Manage app"
4. View the deployment logs for specific error messages

## Common Error Messages

### "Requirements file not found"
- Ensure `requirements.txt` is in the root directory
- Check file name is exactly `requirements.txt` (lowercase)

### "Could not find a version that satisfies the requirement"
- Package name might be misspelled
- Version might not exist
- Try using version ranges instead of exact pins

### "Module has no attribute"
- API might have changed in newer versions
- Check Streamlit documentation for breaking changes
- Current code is compatible with Streamlit 1.53+

### "Python version not supported"
- Streamlit Cloud supports Python 3.8 - 3.12
- We're using Python 3.12 (latest supported)

## Testing Locally

To test the app locally before deploying:

```bash
# Clone the repository
git clone https://github.com/KemosBram1/afp-estimator.git
cd afp-estimator

# Switch to the correct branch
git checkout copilot/deploy-to-streamlit-cloud

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app should open at http://localhost:8501

## Getting Help

If none of these solutions work:

1. Check Streamlit Cloud status page: https://status.streamlit.io
2. Visit Streamlit Community Forum: https://discuss.streamlit.io
3. Check GitHub repository issues
4. Review full deployment logs on Streamlit Cloud

## Recent Changes

- **2026-01-28:** Updated package versions to fix compatibility issues
- **2026-01-28:** Added Python version specification
- **2026-01-27:** Created initial Streamlit application
