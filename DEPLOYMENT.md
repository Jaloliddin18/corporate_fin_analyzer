# 🚀 Deployment Guide

## Quick Deployment to Streamlit Cloud

### Prerequisites

- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Step-by-Step Instructions

#### 1. Initialize Git Repository (if not already done)

```bash
cd /Users/khonimkulovjaloliddin/Desktop/team10_project
git init
```

#### 2. Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click the **"+"** icon → **"New repository"**
3. Name it (e.g., `financial-health-analyzer`)
4. Choose **Public** (required for free Streamlit Cloud)
5. **Do NOT** initialize with README (we already have files)
6. Click **"Create repository"**

#### 3. Push Code to GitHub

```bash
# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Corporate Financial Health Analyzer"

# Add remote (replace YOUR_USERNAME and YOUR_REPO with your details)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### 4. Deploy on Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in"** and authenticate with GitHub
3. Click **"New app"** button
4. Fill in the deployment form:
   - **Repository**: Select your repository (e.g., `YOUR_USERNAME/YOUR_REPO`)
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain
5. Click **"Deploy!"**

#### 5. Wait for Deployment

- Deployment typically takes 2-5 minutes
- You'll see a build log showing progress
- Once complete, your app will be live!

### Your App URL

Your app will be available at:

```
https://YOUR-APP-NAME.streamlit.app
```

## 🔄 Updating Your Deployed App

Any time you push changes to GitHub, Streamlit Cloud will automatically redeploy:

```bash
# Make your changes to app.py or other files

# Commit and push
git add .
git commit -m "Description of changes"
git push
```

The app will automatically update within a few minutes!

## 🐛 Troubleshooting

### App Won't Start

- Check the logs in Streamlit Cloud dashboard
- Verify all dependencies are in `requirements.txt`
- Ensure Python version compatibility

### Data Fetching Issues

- Yahoo Finance API may have rate limits
- Some tickers may not have complete financial data
- Try using different ticker symbols

### Performance Issues

- Consider reducing the number of companies in benchmark (currently 8)
- Use caching effectively (already implemented with `@st.cache_data`)

## 📊 Monitoring Your App

- View app analytics in Streamlit Cloud dashboard
- Monitor usage, errors, and performance
- Set up email notifications for app issues

## 🔒 Security Notes

- This app uses public data from Yahoo Finance
- No sensitive data is stored
- All processing happens in real-time

## 💡 Tips for Better Performance

1. **Use caching**: Already implemented with `@st.cache_data(ttl=3600)`
2. **Limit API calls**: Benchmark uses max 8 companies by default
3. **Monitor usage**: Check Streamlit Cloud dashboard regularly

## 📞 Support

If you encounter issues:

1. Check Streamlit Cloud logs
2. Review [Streamlit documentation](https://docs.streamlit.io)
3. Open an issue on GitHub

---

**Happy Deploying! 🎉**
