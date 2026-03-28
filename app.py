import os
import streamlit as st
from dotenv import load_dotenv
import folium
from streamlit_folium import st_folium
import json

from src.api_clients.countries import get_country_by_name, get_countries_by_codes
from src.api_clients.weather import geocode_location, get_current_weather
from src.api_clients.news import get_news

load_dotenv()

st.set_page_config(page_title="Global Insight Dashboard", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "search_input" not in st.session_state:
    st.session_state.search_input = "Portugal"
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "Search"
if "current_search_results" not in st.session_state:
    st.session_state.current_search_results = None
if "last_search_term" not in st.session_state:
    st.session_state.last_search_term = None

# Modern CSS Styling (same as before)
st.markdown("""
    <style>
        :root {
            --primary-color: #0066FF;
            --secondary-color: #00D9FF;
            --accent-color: #FF6B6B;
            --dark-bg: #0F1419;
            --card-bg: #1A1F2E;
            --text-primary: #FFFFFF;
            --text-secondary: #B0B5CC;
            --border-color: #2A2F3E;
        }

        .stApp {
            background: linear-gradient(135deg, #0F1419 0%, #1A1F2E 100%);
        }

        .header-container {
            background: linear-gradient(135deg, #0066FF 0%, #00D9FF 100%);
            padding: 40px 20px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 102, 255, 0.3);
        }

        .header-title {
            color: white;
            font-size: 3em;
            font-weight: 600;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .header-subtitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1em;
            margin: 10px 0 0 0;
            font-weight: 300;
        }

        .modern-card {
            background: rgba(26, 31, 46, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .modern-card:hover {
            border-color: rgba(0, 102, 255, 0.5);
            box-shadow: 0 12px 32px rgba(0, 102, 255, 0.2);
            transform: translateY(-2px);
        }

        .section-title {
            color: #00D9FF;
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 2px solid rgba(0, 102, 255, 0.3) !important;
            border-radius: 12px !important;
            color: #000000 !important;
            font-size: 1.1em !important;
            padding: 12px 16px !important;
            transition: all 0.3s ease !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: #666666 !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #0066FF 0%, #00D9FF 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 32px !important;
            font-size: 1.05em !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 102, 255, 0.3) !important;
        }

        .stButton > button:hover {
            box-shadow: 0 8px 25px rgba(0, 102, 255, 0.4) !important;
            transform: translateY(-2px) !important;
        }

        .stMetric {
            background: rgba(0, 217, 255, 0.05);
            border: 1px solid rgba(0, 217, 255, 0.2);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .stMetric > div {
            color: white !important;
        }

        .stMetric > div > div {
            color: white !important;
        }

        .stMetric label {
            color: white !important;
        }

        .stMetric p {
            color: white !important;
        }

        .stInfo {
            background: rgba(0, 102, 255, 0.1) !important;
            border: 1px solid rgba(0, 102, 255, 0.3) !important;
            border-left: 4px solid #0066FF !important;
            border-radius: 12px !important;
            padding: 15px !important;
        }

        .stWarning {
            background: rgba(255, 107, 107, 0.1) !important;
            border: 1px solid rgba(255, 107, 107, 0.3) !important;
            border-left: 4px solid #FF6B6B !important;
            border-radius: 12px !important;
        }

        .data-item {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .data-item:last-child {
            border-bottom: none;
        }

        .data-label {
            color: #00D9FF;
            font-weight: 600;
            margin-right: 8px;
        }

        .data-value {
            color: #FFFFFF;
        }

        .news-article {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }

        .news-article:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(0, 217, 255, 0.3);
            transform: translateX(5px);
        }

        .news-title {
            color: #00D9FF;
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .news-meta {
            color: #B0B5CC;
            font-size: 0.9em;
            margin-bottom: 10px;
        }

        .news-link {
            display: inline-block;
            color: #0066FF;
            text-decoration: none;
            font-weight: 600;
            margin-top: 10px;
            transition: all 0.2s ease;
        }

        .news-link:hover {
            color: #00D9FF;
            text-decoration: underline;
        }

        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0, 102, 255, 0.3), transparent);
            margin: 30px 0;
        }

        .column-title {
            color: #00D9FF;
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .favorite-btn {
            background: rgba(255, 107, 107, 0.2) !important;
            border: 1px solid rgba(255, 107, 107, 0.5) !important;
            color: #FF6B6B !important;
        }

        .favorite-btn:hover {
            background: rgba(255, 107, 107, 0.3) !important;
        }

        .stats-card {
            background: linear-gradient(135deg, rgba(0, 102, 255, 0.15), rgba(0, 217, 255, 0.15));
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .stats-card:hover {
            background: linear-gradient(135deg, rgba(0, 102, 255, 0.25), rgba(0, 217, 255, 0.25));
            border-color: rgba(0, 217, 255, 0.6);
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 102, 255, 0.2);
        }

        .stats-label {
            color: #B0B5CC;
            font-size: 0.9em;
            font-weight: 500;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stats-value {
            color: #00D9FF;
            font-size: 1.8em;
            font-weight: 700;
        }

        .stats-value-large {
            color: #FFFFFF;
            font-size: 2em;
            font-weight: 700;
        }

        .neighboring-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .neighboring-tag {
            background: rgba(0, 102, 255, 0.2);
            border: 1px solid rgba(0, 102, 255, 0.4);
            border-radius: 20px;
            padding: 6px 12px;
            color: #00D9FF;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .neighboring-tag:hover {
            background: rgba(0, 102, 255, 0.4);
            border-color: rgba(0, 102, 255, 0.8);
            transform: translateY(-2px);
        }

        h3 {
            color: #FFFFFF !important;
        }

        .stSidebar h3 {
            color: #000000 !important;
        }

        .stTextInput label {
            color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for Favorites and History
st.sidebar.markdown("### 🌟 Favorites & History")
with st.sidebar.expander("⭐ Favorites", expanded=False):
    if st.session_state.favorites:
        for fav in st.session_state.favorites:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(fav, key=f"fav_{fav}"):
                    st.session_state.search_input = fav
                    st.session_state.app_mode = "Search"
                    st.rerun()
            with col2:
                if st.button("✕", key=f"remove_fav_{fav}"):
                    st.session_state.favorites.remove(fav)
                    st.rerun()
    else:
        st.write("No favorites yet!")

with st.sidebar.expander("📜 Search History", expanded=False):
    if st.session_state.search_history:
        for hist in reversed(st.session_state.search_history[-10:]):
            if st.button(hist, key=f"hist_{hist}"):
                st.session_state.search_input = hist
                st.session_state.app_mode = "Search"
                st.rerun()
    else:
        st.write("No history yet!")

st.sidebar.markdown("---")

# Mode selection
st.sidebar.markdown("### 🎮 App Mode")
mode = st.sidebar.radio("Select mode:", ["Search", "Compare Countries", "Favorites Overview"], 
                        key="mode_radio",
                        index=0 if st.session_state.app_mode == "Search" else (1 if st.session_state.app_mode == "Compare" else 2))

if st.session_state.app_mode != mode:
    st.session_state.current_search_results = None
    
st.session_state.app_mode = mode

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🌍 Global Insight Dashboard</h1>
        <p class="header-subtitle">Discover comprehensive information about countries, weather, and global news</p>
    </div>
""", unsafe_allow_html=True)

# Common country names for autocomplete
COUNTRIES_LIST = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia",
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Central African",
    "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba",
    "Cyprus", "Czech", "Denmark", "Djibouti", "Dominica", "Dominican", "Ecuador", "Egypt",
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland",
    "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
    "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan",
    "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
    "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar",
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius",
    "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
    "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
    "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine",
    "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar",
    "Romania", "Russia", "Rwanda", "Saint Kitts", "Saint Lucia", "Saint Vincent", "Samoa",
    "San Marino", "Sao Tome", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
    "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea",
    "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria",
    "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor", "Togo", "Tonga", "Trinidad", "Tunisia",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab", "United Kingdom",
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican", "Venezuela", "Vietnam", "Yemen",
    "Zambia", "Zimbabwe"
]

def format_list(values):
    if not values:
        return "N/A"
    return ", ".join(values)

def build_summary_list(country_data, location_data, weather_data, news_data):
    parts = []
    if location_data:
        parts.append(f"📍 Location: {location_data['name']}")
    if weather_data:
        parts.append(f"🌡️ Current temperature is {weather_data['temperature']}°C with wind speed {weather_data['wind_speed']} km/h")
    if country_data:
        parts.append(f"🏛️ {country_data['name']} is in {country_data['region']} with a population of {country_data['population']:,}")
    if news_data:
        parts.append(f"📰 {len(news_data)} recent news articles were found")
    return parts

def create_map(lat, lon, country_name):
    m = folium.Map(
        location=[lat, lon],
        zoom_start=4,
        tiles="CartoDB positron"
    )
    folium.Marker(
        location=[lat, lon],
        popup=country_name,
        tooltip=country_name,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    return m

def display_country_info(country_data, location_data, weather_data, news_data, show_map=True):
    """Display country information with optional map"""
    
    # Quick Insights
    summary_parts = build_summary_list(country_data, location_data, weather_data, news_data)
    if summary_parts:
        summary_html = "<ul style='margin-left: 20px; line-height: 1.8;'>"
        for part in summary_parts:
            summary_html += f"<li style='color: #B0B5CC; font-size: 1.05em;'>{part}</li>"
        summary_html += "</ul>"
        st.markdown(f"""
            <div class="modern-card">
                <div class="section-title">⚡ Quick Insights</div>
                {summary_html}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Country Info and Map Side by Side
    if show_map and location_data:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="column-title">🏳️ Country Information</div>', unsafe_allow_html=True)
            if country_data:
                st.markdown("""
                <div class="modern-card">
                <div class="data-item"><span class="data-label">Name:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Official Name:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Capital:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Region:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Subregion:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Population:</span><span class="data-value">{:,}</span></div>
                <div class="data-item"><span class="data-label">Languages:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Currencies:</span><span class="data-value">{}</span></div>
                </div>
                """.format(
                    country_data['name'],
                    country_data['official_name'],
                    country_data['capital'],
                    country_data['region'],
                    country_data['subregion'],
                    country_data['population'],
                    format_list(country_data['languages']),
                    format_list(country_data['currencies'])
                ), unsafe_allow_html=True)
                
                if country_data.get("flag"):
                    st.image(country_data["flag"], width=120, use_container_width=False)
            else:
                st.markdown('<div class="stWarning">No country data found.</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="column-title">🗺️ Map</div>', unsafe_allow_html=True)
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            map_obj = create_map(location_data['latitude'], location_data['longitude'], country_data['name'] if country_data else location_data['name'])
            st_folium(map_obj, use_container_width=True, height=500)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="column-title">🏳️ Country Information</div>', unsafe_allow_html=True)
            if country_data:
                st.markdown("""
                <div class="modern-card">
                <div class="data-item"><span class="data-label">Name:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Official Name:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Capital:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Region:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Subregion:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Population:</span><span class="data-value">{:,}</span></div>
                <div class="data-item"><span class="data-label">Languages:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Currencies:</span><span class="data-value">{}</span></div>
                </div>
                """.format(
                    country_data['name'],
                    country_data['official_name'],
                    country_data['capital'],
                    country_data['region'],
                    country_data['subregion'],
                    country_data['population'],
                    format_list(country_data['languages']),
                    format_list(country_data['currencies'])
                ), unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="column-title">🌤️ Weather Information</div>', unsafe_allow_html=True)
            if location_data and weather_data:
                st.markdown("""
                <div class="modern-card">
                <div class="data-item"><span class="data-label">Location:</span><span class="data-value">{}</span></div>
                <div class="data-item"><span class="data-label">Coordinates:</span><span class="data-value">{:.2f}°, {:.2f}°</span></div>
                <div class="data-item"><span class="data-label">Local Time:</span><span class="data-value">{}</span></div>
                </div>
                """.format(
                    location_data['name'],
                    location_data['latitude'],
                    location_data['longitude'],
                    weather_data['time']
                ), unsafe_allow_html=True)

                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("🌡️ Temperature", f"{weather_data['temperature']}°C")
                with m2:
                    st.metric("💨 Wind Speed", f"{weather_data['wind_speed']} km/h")
                with m3:
                    st.metric("📊 Weather Code", weather_data['weather_code'])
    
    st.markdown("---")
    
    # Neighboring Countries
    if country_data and country_data.get('borders'):
        st.markdown('<div class="section-title">🌍 Neighboring Countries</div>', unsafe_allow_html=True)
        try:
            borders_codes = country_data['borders']
            neighbors_info = get_countries_by_codes(borders_codes)
            
            neighbors_html = '<div class="neighboring-list">'
            for code, name in neighbors_info.items():
                neighbors_html += f'<div class="neighboring-tag">{name}</div>'
            neighbors_html += '</div>'
            
            st.markdown(f"""
                <div class="modern-card">
                    {neighbors_html}
                </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown('<div class="modern-card"><p style="color: #B0B5CC;">No neighboring countries data available</p></div>', unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Weather Section with Local Time
    if location_data and weather_data:
        st.markdown('<div class="section-title">🌤️ Weather Details</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="modern-card">
        <div class="data-item"><span class="data-label">📍 Location:</span><span class="data-value">{location_data['name']}</span></div>
        <div class="data-item"><span class="data-label">🧭 Coordinates:</span><span class="data-value">{location_data['latitude']:.2f}°, {location_data['longitude']:.2f}°</span></div>
        <div class="data-item"><span class="data-label">🕐 Local Time:</span><span class="data-value">{weather_data['time']}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("🌡️ Temperature", f"{weather_data['temperature']}°C")
        with m2:
            st.metric("💨 Wind Speed", f"{weather_data['wind_speed']} km/h")
        with m3:
            st.metric("📊 Weather Code", weather_data['weather_code'])
        
        st.markdown("---")
    
    # News Section
    st.markdown('<div class="section-title">📰 Recent News</div>', unsafe_allow_html=True)
    if news_data:
        for article in news_data:
            st.markdown(f"""
                <div class="news-article">
                    <div class="news-title">📌 {article['title']}</div>
                    <div class="news-meta">
                        <strong>Source:</strong> {article['source']} | <strong>Published:</strong> {article['published_at']}
                    </div>
                    <a href="{article['url']}" target="_blank" class="news-link">Read Full Article →</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="stWarning">No news articles found.</div>', unsafe_allow_html=True)

# SEARCH MODE
if st.session_state.app_mode == "Search":
    col1, col2, col3 = st.columns([4, 0.5, 0.5])
    
    with col1:
        search_term = st.text_input("", placeholder="Search for a country or city...", label_visibility="collapsed", value=st.session_state.search_input)
    
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    
    with col3:
        if search_term in st.session_state.search_history or (search_term in st.session_state.favorites):
            fav_button = st.button("★ Favorite", use_container_width=True, key="fav_toggle")
        else:
            fav_button = st.button("☆ Favorite", use_container_width=True, key="fav_toggle")
    
    if fav_button and search_term:
        if search_term in st.session_state.favorites:
            st.session_state.favorites.remove(search_term)
        else:
            st.session_state.favorites.append(search_term)
        st.rerun()
    
    if search_term and len(search_term) > 1:
        matching_countries = [c for c in COUNTRIES_LIST if c.lower().startswith(search_term.lower())]
        if matching_countries:
            st.markdown('<p style="font-size: 0.9em; color: #00D9FF; margin-top: -10px; margin-bottom: 10px;">Suggestions:</p>', unsafe_allow_html=True)
            suggestion_cols = st.columns(min(5, len(matching_countries)))
            for idx, country in enumerate(matching_countries[:5]):
                with suggestion_cols[idx]:
                    if st.button(country, use_container_width=True, key=f"suggestion_{country}"):
                        st.session_state.search_input = country
                        search_term = country
                        search_button = True
                        st.rerun()
    
    st.session_state.search_input = search_term
    
    if search_button and search_term:
        if search_term not in st.session_state.search_history:
            st.session_state.search_history.append(search_term)
        
        country_data = None
        location_data = None
        weather_data = None
        news_data = []
        
        try:
            country_data = get_country_by_name(search_term)
        except Exception:
            country_data = None
        
        country_name_for_location = country_data['name'] if country_data else search_term
        
        try:
            location_data = geocode_location(country_name_for_location)
            if location_data:
                weather_data = get_current_weather(location_data["latitude"], location_data["longitude"])
        except Exception:
            location_data = None
            weather_data = None
        
        try:
            api_key = os.getenv("NEWS_API_KEY")
            if api_key:
                news_data = get_news(country_name_for_location, api_key)
        except Exception:
            news_data = []
        
        # Store results in session state
        st.session_state.current_search_results = {
            "country_data": country_data,
            "location_data": location_data,
            "weather_data": weather_data,
            "news_data": news_data
        }
    
    # Display stored results if they exist
    if st.session_state.current_search_results:
        st.markdown("---")
        results = st.session_state.current_search_results
        display_country_info(
            results["country_data"],
            results["location_data"],
            results["weather_data"],
            results["news_data"],
            show_map=True
        )

# COMPARE MODE
elif st.session_state.app_mode == "Compare Countries":
    st.markdown("### Compare Two Countries")
    col1, col2 = st.columns(2)
    
    with col1:
        search1 = st.text_input("First country:", value="Portugal", key="compare_1")
    with col2:
        search2 = st.text_input("Second country:", value="Spain", key="compare_2")
    
    if st.button("🔄 Compare", use_container_width=True):
        country1_data = location1_data = weather1_data = news1_data = None
        country2_data = location2_data = weather2_data = news2_data = None
        
        try:
            country1_data = get_country_by_name(search1)
        except:
            pass
        try:
            location1_data = geocode_location(country1_data['name'] if country1_data else search1)
            if location1_data:
                weather1_data = get_current_weather(location1_data["latitude"], location1_data["longitude"])
        except:
            pass
        try:
            api_key = os.getenv("NEWS_API_KEY")
            if api_key and country1_data:
                news1_data = get_news(country1_data['name'], api_key)
        except:
            pass
        
        try:
            country2_data = get_country_by_name(search2)
        except:
            pass
        try:
            location2_data = geocode_location(country2_data['name'] if country2_data else search2)
            if location2_data:
                weather2_data = get_current_weather(location2_data["latitude"], location2_data["longitude"])
        except:
            pass
        try:
            api_key = os.getenv("NEWS_API_KEY")
            if api_key and country2_data:
                news2_data = get_news(country2_data['name'], api_key)
        except:
            pass
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {country1_data['name'] if country1_data else search1}")
            display_country_info(country1_data, location1_data, weather1_data, news1_data, show_map=False)
        
        with col2:
            st.markdown(f"### {country2_data['name'] if country2_data else search2}")
            display_country_info(country2_data, location2_data, weather2_data, news2_data, show_map=False)

# FAVORITES OVERVIEW
elif st.session_state.app_mode == "Favorites Overview":
    st.markdown("### Your Favorite Countries")
    if st.session_state.favorites:
        for country in st.session_state.favorites:
            with st.expander(f"📍 {country}"):
                try:
                    country_data = get_country_by_name(country)
                    location_data = geocode_location(country_data['name'] if country_data else country)
                    weather_data = location_data and get_current_weather(location_data["latitude"], location_data["longitude"])
                    
                    api_key = os.getenv("NEWS_API_KEY")
                    news_data = []
                    if api_key and country_data:
                        news_data = get_news(country_data['name'], api_key)
                    
                    display_country_info(country_data, location_data, weather_data, news_data, show_map=False)
                except Exception as e:
                    st.error(f"Error loading data for {country}")
    else:
        st.info("Add countries to your favorites to see them here!")
