import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

# --- PAGE SETUP ---
st.set_page_config(page_title="Owner Analytics Dashboard", layout="wide")

# --- MOCK DATA ENGINE (Simulating your Database) ---
@st.cache_data
def load_data():
    dates = pd.date_range(start="2024-01-01", periods=90, freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Visits': np.random.randint(100, 500, size=90),
        'Saves': np.random.randint(10, 60, size=90),
        'Directions': np.random.randint(20, 100, size=90),
        'Calls': np.random.randint(5, 40, size=90),
        'Orders': np.random.randint(30, 150, size=90),
        'Spam_Score': np.random.choice(['Real', 'Bot/Spam'], size=90, p=[0.9, 0.1])
    })
    return data

df = load_data()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972161.png", width=80)
    st.title("CityGuide Admin")
    selected = option_menu(
        "Main Menu", 
        ["Dashboard", "Customer Insights", "Operations", "Location Logic"],
        icons=['speedometer2', 'chat-heart', 'shop', 'geo-alt'], 
        menu_icon="cast", default_index=0
    )
    st.markdown("---")
    st.write("Logged in as: **The Pizza House**")
    if st.sidebar.button("System Alert: Check Reductions"):
        st.error("Traffic decreased by 12% on Tuesdays.")

# --- 1. DASHBOARD TAB ---
if selected == "Dashboard":
    st.title("📊 Business Performance")
    
    # KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Visits", df['Visits'].sum(), "+15%")
    m2.metric("Place Saved", df['Saves'].sum(), "+8%")
    m3.metric("Direction Clicks", df['Directions'].sum(), "-2%")
    m4.metric("Call Clicks", df['Calls'].sum(), "+5%")

    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Growth & Order Analysis")
        fig_growth = px.line(df, x='Date', y=['Visits', 'Orders'], 
                             title="Visits vs App Orders Over Time",
                             color_discrete_sequence=["#007BFF", "#28A745"])
        st.plotly_chart(fig_growth, use_container_width=True)

    with col_right:
        st.subheader("🍕 Top Items Ordered")
        items = pd.DataFrame({
            'Item': ['Margherita', 'Pepperoni', 'Veggie Supreme', 'Coke', 'Garlic Bread'],
            'Count': [450, 600, 300, 800, 200]
        }).sort_values('Count')
        fig_items = px.bar(items, x='Count', y='Item', orientation='h', color='Count', color_continuous_scale='Blues')
        st.plotly_chart(fig_items, use_container_width=True)

# --- 2. CUSTOMER INSIGHTS ---
elif selected == "Customer Insights":
    st.title("🤖 Chatbot & Engagement")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Chatbot Response Accuracy")
        labels = ['Helpful', 'Neutral', 'Spam/Irrelevant', 'Human Needed']
        values = [65, 15, 10, 10]
        fig_chat = px.pie(names=labels, values=values, hole=0.6, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_chat, use_container_width=True)

    with c2:
        st.subheader("Real vs. Spam Engagement")
        fig_spam = px.histogram(df, x='Spam_Score', color='Spam_Score', 
                                color_discrete_map={'Real': '#28A745', 'Bot/Spam': '#DC3545'})
        st.plotly_chart(fig_spam, use_container_width=True)

    st.subheader("⭐ Rating Analysis")
    ratings = [4, 5, 5, 4, 3, 5, 4, 2, 5, 5, 4, 5]
    fig_rate = px.histogram(x=ratings, nbins=5, labels={'x': 'Star Rating'}, title="User Review Distribution")
    st.plotly_chart(fig_rate, use_container_width=True)

# --- 3. OPERATIONS ---
elif selected == "Operations":
    st.title("⏰ Operational Efficiency")
    
    st.subheader("Popular Visiting Hours (Heatmap)")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = [f"{i}:00" for i in range(24)]
    heat_data = np.random.randint(5, 100, size=(7, 24))
    fig_heat = px.imshow(heat_data, x=hours, y=days, color_continuous_scale='YlGnBu', aspect="auto")
    st.plotly_chart(fig_heat, use_container_width=True)

    st.divider()
    
    st.subheader("Engagement During Closing Hours")
    st.info("Users are checking your menu at 11:00 PM (Closed). Consider late-night delivery!")
    closing_data = pd.DataFrame({'Hour': ['10PM', '11PM', '12AM', '1AM'], 'Clicks': [45, 80, 30, 10]})
    fig_closing = px.area(closing_data, x='Hour', y='Clicks', title="Lost Engagement Potential")
    st.plotly_chart(fig_closing, use_container_width=True)

# --- 4. LOCATION LOGIC ---
elif selected == "Location Logic":
    st.title("📍 Location Based Analysis")
    st.write("Where are users located when they search for you?")
    
    map_data = pd.DataFrame({
        'lat': np.random.uniform(40.7, 40.8, 50),
        'lon': np.random.uniform(-74.0, -73.9, 50),
        'weight': np.random.randint(1, 10, 50)
    })
    st.map(map_data)
    st.success("Targeting suggestion: Most users are within 2km of your location.")