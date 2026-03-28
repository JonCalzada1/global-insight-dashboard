# 🌍 Global Insight Dashboard

Global Insight Dashboard is a Python Streamlit application that lets users explore country-level information, compare two countries side by side, view live weather conditions, interact with map-based location context, and browse recent news in one interactive dashboard.

This project combines multiple real-world APIs into a polished interactive dashboard where users can search for a country, compare two countries side by side, monitor live weather, explore map context, and track country-related news.

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

- single-country search mode
- country comparison mode
- favorites overview
- search bar with suggestions
- quick insights panels
- country information cards
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
