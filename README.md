# AFP Quote Estimator

A professional quote estimation tool built with Streamlit for generating accurate project quotes.

## Features

- 💰 Comprehensive cost breakdown (labor, materials, equipment, travel, misc)
- 📊 Real-time quote calculations with markup
- 📥 Export quotes as text or CSV files
- 🎨 Clean, professional interface
- 📱 Responsive design

## Deployment to Streamlit Cloud

This application is ready to deploy on Streamlit Cloud:

1. Fork or push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select this repository, branch `main`, and the `app.py` file
6. Click "Deploy"

See `DEPLOYMENT.md` for detailed deployment instructions.

## Updating After Deployment

**Yes, you can update your app after deployment!** Changes pushed to GitHub will automatically trigger redeployment.

```bash
# 1. Make changes and test locally
streamlit run app.py

# 2. Commit and push
git add .
git commit -m "Your change description"
git push origin copilot/deploy-to-streamlit-cloud

# 3. Wait 1-3 minutes for automatic redeployment
```

📖 **See [UPDATE_WORKFLOW.md](UPDATE_WORKFLOW.md)** for comprehensive update guide
📖 **See [QUICK_UPDATE_GUIDE.md](QUICK_UPDATE_GUIDE.md)** for quick reference

## Local Development

To run the application locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

1. Enter project information in the sidebar (project name, client name, date)
2. Fill in cost estimates:
   - Labor hours and hourly rate
   - Material costs
   - Equipment/tools costs
   - Travel expenses
   - Miscellaneous costs
3. Adjust markup percentage
4. Review the quote summary
5. Download the quote as a text file or CSV

## Documentation

- 📘 [UPDATE_WORKFLOW.md](UPDATE_WORKFLOW.md) - How to update your deployed app
- 📗 [QUICK_UPDATE_GUIDE.md](QUICK_UPDATE_GUIDE.md) - Quick reference for updates
- 📙 [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- 📕 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions

## Requirements

- Python 3.8+
- Streamlit
- Pandas

See `requirements.txt` for specific versions.
