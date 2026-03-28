# 🌍 Global Insight Dashboard

Global Insight Dashboard is a Python Streamlit application that lets users explore country-level information, live weather conditions, map-based location context, and recent news in one interactive dashboard.

It was built to combine real-world API integration, clean dashboard design, and practical data presentation in a portfolio-ready project.

---

## Features

- Search for a country and view key national information
- Compare two countries side by side
- Display official country details such as capital, region, population, language, and currency
- Show the national flag
- Visualize the location on an interactive map
- Display live weather metrics including temperature, wind speed, and weather code
- Browse recent country-related news articles
- Save favorite countries
- Track search history
- View quick insight summaries generated from the returned data

---

## Demo Preview

Main dashboard includes:

- search bar with suggestions
- quick insights panel
- country information card
- interactive map
- neighboring countries
- weather details and metrics
- recent news cards
- favorites and search history sidebar

---

## Tech Stack

- **Python**
- **Streamlit**
- **REST Countries API**
- **Open-Meteo API**
- **NewsAPI**
- **Pandas**
- **Requests**
- **Python-dotenv**

---

## APIs Used

### REST Countries API
Used for:
- country name
- official name
- capital
- region
- subregion
- population
- languages
- currencies
- flag

### Open-Meteo API
Used for:
- location geocoding
- coordinates
- live weather data

### NewsAPI
Used for:
- recent news headlines related to the searched country

---

## Project Structure

```text
global-insight-dashboard/
│
├── src/
│   └── api_clients/
│       ├── countries.py
│       ├── weather.py
│       └── news.py
│
├── notebooks/
│   ├── API_Client_Test.ipynb
│   ├── NewsAPI_Client_Test.ipynb
│   └── Weather_Client_Test.ipynb
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
└── .env.example
