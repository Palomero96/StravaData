# StravaData

A Python toolkit to retrieve, analyze, and visualize your **Strava** activity data.

## 📂 Project Structure

- **`app.py`**: Main application script (dashboard/visualization).
- **`strava.py`**: Helper functions to interact with the Strava API.
- **`getToken.py`**: Script to handle OAuth2 authentication and generate access tokens.
- **`testing.ipynb`**: Jupyter Notebook for testing and data experimentation.
- **`data/`**: Directory to store downloaded activity datasets.


## 🔗 Live Demo
You can check a running instance here:
👉 **[stravadata-davidpalomero.streamlit.app](https://stravadata-davidpalomero.streamlit.app/)**
## ⚡ Quick Start

### 1. Prerequisites
* Python 3.8+
* A [Strava Account](https://www.strava.com/)
* **API Credentials:** Go to your [Strava API Settings](https://www.strava.com/settings/api) and create an application to get your `Client ID` and `Client Secret`.

### 2. Installation
Clone the repository and install dependencies:

```bash
git clone [https://github.com/Palomero96/StravaData.git](https://github.com/Palomero96/StravaData.git)
cd StravaData
pip install -r requirements.txt
```
### 3. Authentication
Before fetching data, you need to generate a valid Access Token. Run the authentication script and follow the prompts (or configure your environment variables if supported):

```bash
python getToken.py
```

### 4. Data
After configuring your environment variables, fetch your data:
```bash
python strava.py
```

### 5. Usage
Once authenticated, you can run the main application to visualize your data:
```bash
streamlit run app.py
```