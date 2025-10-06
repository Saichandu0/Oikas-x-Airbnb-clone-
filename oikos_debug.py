# Oikos - Debugged Airbnb Clone
import streamlit as st
import sqlite3
import hashlib
import json
from datetime import date, timedelta
import pandas as pd
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="Oikos - Find Your Perfect Stay",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
    background-color: #000000 !important;
    color: white !important;
}

.stApp > div:first-child {
    background-color: #000000 !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Floating hamburger menu */
.hamburger-float {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1000;
    background: linear-gradient(135deg, #3498db, #1abc9c);
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
    cursor: pointer;
    transition: all 0.3s ease;
}

.hamburger-float:hover {
    transform: scale(1.1);
    box-shadow: 0 12px 35px rgba(52, 152, 219, 0.4);
}

.hamburger-lines {
    width: 25px;
    height: 3px;
    background: white;
    margin: 5px 0;
    border-radius: 2px;
}

/* Beach background with bright red and sky blue */
.beach-bg {
    background: linear-gradient(135deg, rgba(255, 20, 147, 0.8), rgba(135, 206, 235, 0.8)), 
                url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200') center/cover;
    min-height: 100vh;
    padding: 2rem;
    margin: -1rem;
}

/* Floating animations */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(5deg); }
}

.floating {
    animation: float 8s ease-in-out infinite;
    position: fixed;
    opacity: 0.6;
    z-index: 1;
}

/* Sky Blue and Bright Red Button styling */
.stButton > button {
    background: linear-gradient(135deg, #87CEEB, #FF1493) !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 20, 147, 0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(255, 20, 147, 0.6) !important;
    filter: brightness(1.2) !important;
}

/* Property cards with black background */
.property-card {
    background: #1a1a1a !important;
    color: white !important;
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(255, 20, 147, 0.2);
    transition: all 0.4s ease;
    border: 1px solid #333;
}

.property-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 50px rgba(255, 20, 147, 0.4);
    border-color: #FF1493;
}

/* Text inputs with black theme */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
.stNumberInput > div > div > input {
    background-color: #1a1a1a !important;
    color: white !important;
    border: 2px solid #333 !important;
    border-radius: 15px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus,
.stNumberInput > div > div > input:focus {
    border-color: #87CEEB !important;
    box-shadow: 0 0 0 2px rgba(135, 206, 235, 0.2) !important;
}

/* Metrics with sky blue and bright red theme */
.stMetric {
    background: linear-gradient(135deg, #87CEEB, #FF1493) !important;
    color: white !important;
    padding: 1rem !important;
    border-radius: 15px !important;
    box-shadow: 0 8px 25px rgba(255, 20, 147, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'browse'
if 'selected_property' not in st.session_state:
    st.session_state.selected_property = None
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

# Database functions
def init_database():
    conn = sqlite3.connect('oikos_debug.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            property_type TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            address TEXT NOT NULL,
            price_per_night REAL NOT NULL,
            max_guests INTEGER NOT NULL,
            bedrooms INTEGER NOT NULL,
            bathrooms INTEGER NOT NULL,
            amenities TEXT,
            image_url TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id INTEGER NOT NULL,
            guest_id INTEGER NOT NULL,
            property_title TEXT NOT NULL,
            property_city TEXT NOT NULL,
            property_country TEXT NOT NULL,
            property_image TEXT,
            check_in_date TEXT NOT NULL,
            check_out_date TEXT NOT NULL,
            total_price REAL NOT NULL,
            guest_count INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT DEFAULT 'confirmed'
        )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, first_name, last_name):
    try:
        conn = sqlite3.connect('oikos_debug.db')
        cursor = conn.cursor()
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password_hash, first_name, last_name))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def authenticate_user(username, password):
    conn = sqlite3.connect('oikos_debug.db')
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute("""
        SELECT id, username, email, first_name, last_name
        FROM users WHERE username = ? AND password_hash = ?
    """, (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {'id': user[0], 'username': user[1], 'email': user[2], 'first_name': user[3], 'last_name': user[4]}
    return None

def get_properties(city=None, max_price=None):
    conn = sqlite3.connect('oikos_debug.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM properties WHERE 1=1"
    params = []
    
    if city:
        query += " AND LOWER(city) LIKE LOWER(?)"
        params.append(f"%{city}%")
    
    if max_price:
        query += " AND price_per_night <= ?"
        params.append(max_price)
    
    cursor.execute(query, params)
    properties = cursor.fetchall()
    conn.close()
    return properties

def create_booking(property_id, guest_id, property_title, property_city, property_country,
                  property_image, check_in_date, check_out_date, total_price, guest_count, payment_method):
    conn = sqlite3.connect('oikos_debug.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (property_id, guest_id, property_title, property_city, property_country,
                            property_image, check_in_date, check_out_date, total_price, guest_count, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (property_id, guest_id, property_title, property_city, property_country,
          property_image, str(check_in_date), str(check_out_date), total_price, guest_count, payment_method))
    conn.commit()
    conn.close()
    return True

def get_user_bookings(user_id):
    conn = sqlite3.connect('oikos_debug.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE guest_id = ? ORDER BY id DESC", (user_id,))
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def populate_sample_data():
    conn = sqlite3.connect('oikos_debug.db')
    cursor = conn.cursor()
    
    # Check if data exists
    cursor.execute("SELECT COUNT(*) FROM properties")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Create sample users
    sample_users = [
        ("john_host", "john@example.com", "password123", "John", "Smith"),
        ("sarah_host", "sarah@example.com", "password123", "Sarah", "Johnson"),
        ("mike_host", "mike@example.com", "password123", "Mike", "Brown"),
    ]
    
    for username, email, password, first_name, last_name in sample_users:
        password_hash = hash_password(password)
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name)
                VALUES (?, ?, ?, ?, ?)
            """, (username, email, password_hash, first_name, last_name))
        except:
            pass
    
    # Global properties
    global_properties = [
        (1, "Manhattan Skyline Penthouse", "Breathtaking penthouse with panoramic city views.", "Penthouse", "New York", "USA", "123 5th Avenue, New York", 450.0, 6, 3, 2, '["WiFi", "Kitchen", "AC", "TV", "Balcony", "Gym"]', "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400"),
        (2, "Covent Garden Luxury Flat", "Elegant Victorian flat in London's theater district.", "Apartment", "London", "UK", "78 Covent Garden, London", 280.0, 4, 2, 2, '["WiFi", "Kitchen", "Heating", "TV"]', "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400"),
        (3, "Montmartre Artist Retreat", "Charming Parisian apartment in historic Montmartre.", "Apartment", "Paris", "France", "34 Rue des Abbesses, Paris", 195.0, 2, 1, 1, '["WiFi", "Kitchen", "Heating"]', "https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400"),
        (1, "Shibuya Modern Capsule", "Ultra-modern apartment in bustling Shibuya.", "Studio", "Tokyo", "Japan", "2-1 Shibuya, Tokyo", 85.0, 2, 1, 1, '["WiFi", "AC", "TV"]', "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400"),
        (2, "Bondi Beach Surf House", "Beachfront house steps from famous Bondi Beach.", "House", "Sydney", "Australia", "88 Campbell Parade, Bondi", 320.0, 8, 4, 3, '["WiFi", "Kitchen", "AC", "Balcony"]', "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        (3, "Burj Khalifa Sky Suite", "Luxurious suite with views of Burj Khalifa.", "Suite", "Dubai", "UAE", "Downtown Dubai Marina", 520.0, 6, 3, 3, '["WiFi", "Kitchen", "AC", "Pool", "Gym"]', "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400"),
        (1, "Gaudi Modernist Flat", "Artistic apartment inspired by Antoni Gaudí.", "Apartment", "Barcelona", "Spain", "Carrer del Bisbe, Barcelona", 165.0, 3, 1, 1, '["WiFi", "Kitchen", "AC"]', "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400"),
        (2, "Canal House Floating Hotel", "Unique houseboat on Amsterdam's canals.", "Houseboat", "Amsterdam", "Netherlands", "Prinsengracht 263, Amsterdam", 145.0, 2, 1, 1, '["WiFi", "Kitchen", "Heating"]', "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=400"),
    ]
    
    for prop in global_properties:
        cursor.execute("""
            INSERT INTO properties (host_id, title, description, property_type, city, country,
                                  address, price_per_night, max_guests, bedrooms, bathrooms, amenities, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, prop)
    
    conn.commit()
    conn.close()

# Authentication page
def show_auth_page():
    # Beach background
    st.markdown("""
    <div class="beach-bg">
        <div class="floating" style="top: 10%; left: 10%; font-size: 3rem;">✈️</div>
        <div class="floating" style="top: 20%; right: 15%; font-size: 2.5rem; animation-delay: 2s;">📷</div>
        <div class="floating" style="bottom: 20%; left: 20%; font-size: 2.8rem; animation-delay: 1s;">🧭</div>
        <div class="floating" style="bottom: 15%; right: 10%; font-size: 2.2rem; animation-delay: 3s;">🧳</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: white; padding: 2rem 0;">
        <h1 style="font-size: 7rem; font-weight: 900; margin: 0; text-shadow: 0 8px 40px rgba(0,0,0,0.8); letter-spacing: 4px;">🏖️ Welcome to Oikos</h1>
        <p style="font-size: 1.8rem; margin-top: 2rem; opacity: 0.95; text-shadow: 0 4px 20px rgba(0,0,0,0.6);">Your gateway to paradise • Luxury resorts • Beach villas • Mountain retreats</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Forms
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🏖️ Login", "🌴 Sign Up"])
        
        with tab1:
            st.markdown("### 🔐 Welcome Back")
            
            username = st.text_input("Username", placeholder="Enter your username", key="login_user")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
            
            if st.button("🏖️ Sign In to Paradise", key="login_btn", use_container_width=True):
                if username and password:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.success("🌺 Welcome back!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.error("⚠️ Please fill in all fields")
        
        with tab2:
            st.markdown("### 🌴 Create Account")
            
            col_a, col_b = st.columns(2)
            with col_a:
                first_name = st.text_input("First Name", key="signup_first")
                username = st.text_input("Username", key="signup_user")
                email = st.text_input("Email", key="signup_email")
            
            with col_b:
                last_name = st.text_input("Last Name", key="signup_last")
                phone = st.text_input("Phone (Optional)", key="signup_phone")
                password = st.text_input("Password", type="password", key="signup_pass")
            
            if st.button("🌺 Create Paradise Account", key="signup_btn", use_container_width=True):
                if all([first_name, last_name, username, email, password]):
                    if create_user(username, email, password, first_name, last_name):
                        st.success("🎉 Account created! Please login.")
                    else:
                        st.error("❌ Username or email already exists")
                else:
                    st.error("⚠️ Please fill in all required fields")
    
    st.info("**Demo Account:** Username: `john_host` | Password: `password123`")

# Main application
def show_main_app():
    # Beautiful header with sky blue and bright red theme
    st.markdown("""
    <div style="background: linear-gradient(135deg, #87CEEB, #FF1493); padding: 4rem 2rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 30px 30px; text-align: center; position: relative; overflow: hidden;">
        <h1 style="font-size: 8rem; font-weight: 900; color: white; text-shadow: 0 10px 50px rgba(0,0,0,0.8); letter-spacing: 8px; margin: 0;">🏠 Oikos</h1>
        <p style="color: white; font-size: 1.4rem; font-weight: 500; margin-top: 1rem; opacity: 0.95;">Your Gateway to Paradise</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple navigation with buttons
    st.markdown("### 🧭 Navigation")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Browse Properties", key="nav_browse", use_container_width=True):
            st.session_state.current_page = 'browse'
    
    with col2:
        if st.button("📋 My Bookings", key="nav_bookings", use_container_width=True):
            st.session_state.current_page = 'bookings'
    
    with col3:
        if st.button("🏡 Host Property", key="nav_host", use_container_width=True):
            st.session_state.current_page = 'host'
    
    with col4:
        if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
    
    with col5:
        if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_page = 'browse'
    
    # Current page indicator
    page_names = {
        'browse': '🏠 Browse Properties',
        'bookings': '📋 My Bookings', 
        'host': '🏡 Host Property',
        'dashboard': '📊 Dashboard',
        'property_details': '🏠 Property Details',
        'payment': '💳 Payment'
    }
    
    current_page_name = page_names.get(st.session_state.current_page, '🏠 Browse Properties')
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <span style="background: linear-gradient(135deg, #87CEEB, #FF1493); color: white; padding: 0.8rem 2rem; border-radius: 30px; font-weight: 700; font-size: 1.1rem; box-shadow: 0 6px 20px rgba(255, 20, 147, 0.4);">
            {current_page_name}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Route to different pages
    if st.session_state.current_page == 'browse':
        show_browse_page()
    elif st.session_state.current_page == 'bookings':
        show_bookings_page()
    elif st.session_state.current_page == 'host':
        show_host_page()
    elif st.session_state.current_page == 'dashboard':
        show_dashboard_page()
    elif st.session_state.current_page == 'property_details':
        show_property_details_page()
    elif st.session_state.current_page == 'payment':
        show_payment_page()

# Browse properties page
def show_browse_page():
    st.markdown("### 🔍 Find Your Perfect Stay")
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        city_filter = st.text_input("🌍 City", placeholder="Enter city name")
    
    with col2:
        max_price = st.number_input("💰 Max Price/Night", min_value=0, value=1000, step=50)
    
    with col3:
        st.write("")
        search_btn = st.button("🔍 Search", use_container_width=True)
    
    # Get properties
    properties = get_properties(city=city_filter if city_filter else None, max_price=max_price)
    
    if not properties:
        st.info("🏖️ No properties found matching your criteria.")
        return
    
    st.markdown("### 🏠 Available Properties")
    
    # Display properties
    for i in range(0, len(properties), 3):
        cols = st.columns(3)
        
        for j, col in enumerate(cols):
            if i + j < len(properties):
                prop = properties[i + j]
                
                with col:
                    with st.container():
                        st.image(prop[13], use_column_width=True)
                        st.markdown(f"### {prop[2]}")
                        st.markdown(f"📍 {prop[5]}, {prop[6]}")
                        st.markdown(f"🏠 {prop[4]} • 🛏️ {prop[10]} bed • 🚿 {prop[11]} bath")
                        st.markdown(f"**${prop[8]:.0f}** / night")
                        
                        if st.button(f"View Details", key=f"view_{prop[0]}", use_container_width=True):
                            st.session_state.selected_property = prop
                            st.session_state.current_page = 'property_details'
                        
                        # Show amenities safely
                        if prop[12]:
                            try:
                                amenities = json.loads(prop[12])
                                amenities_text = " • ".join(amenities[:3])
                                if len(amenities) > 3:
                                    amenities_text += f" • +{len(amenities) - 3} more"
                                st.markdown(f"🏷️ {amenities_text}")
                            except:
                                st.markdown("🏷️ WiFi • Kitchen • TV")

# Property details page
def show_property_details_page():
    if not st.session_state.selected_property:
        st.error("No property selected")
        return
    
    prop = st.session_state.selected_property
    
    if st.button("← Back to Browse", key="back_to_browse"):
        st.session_state.current_page = 'browse'
    
    st.markdown(f"# {prop[2]}")
    st.markdown(f"📍 {prop[5]}, {prop[6]}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.image(prop[13], use_column_width=True)
        st.markdown("### 📝 Description")
        st.markdown(prop[3])
        
        if prop[12]:
            try:
                amenities = json.loads(prop[12])
                st.markdown("### 🏷️ Amenities")
                for amenity in amenities:
                    st.markdown(f"✅ {amenity}")
            except:
                st.markdown("✅ WiFi ✅ Kitchen ✅ TV")
    
    with col2:
        st.markdown(f"### ${prop[8]:.0f} / night")
        st.markdown(f"🏠 {prop[4]}")
        st.markdown(f"🛏️ {prop[10]} bedrooms")
        st.markdown(f"🚿 {prop[11]} bathrooms")
        st.markdown(f"👥 Up to {prop[9]} guests")
        
        if st.button("💳 Book This Property", key="book_property", use_container_width=True):
            st.session_state.current_page = 'payment'

# Payment page
def show_payment_page():
    if not st.session_state.selected_property:
        st.error("No property selected")
        return
    
    prop = st.session_state.selected_property
    
    if st.button("← Back to Property Details", key="back_to_details"):
        st.session_state.current_page = 'property_details'
    
    st.markdown("### 💳 Complete Your Booking")
    st.markdown(f"**Property:** {prop[2]} in {prop[5]}, {prop[6]}")
    
    # Booking form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        check_in = st.date_input("Check-in Date", min_value=date.today(), value=date.today())
    
    with col2:
        check_out = st.date_input("Check-out Date", min_value=date.today() + timedelta(days=1), 
                                value=date.today() + timedelta(days=2))
    
    with col3:
        guest_count = st.number_input("Number of Guests", min_value=1, max_value=prop[9], value=1)
    
    if check_in >= check_out:
        st.error("Check-out date must be after check-in date")
        return
    
    # Calculate pricing
    nights = (check_out - check_in).days
    subtotal = nights * prop[8]
    service_fee = subtotal * 0.12
    taxes = subtotal * 0.08
    total_price = subtotal + service_fee + taxes
    
    st.markdown("### 💰 Price Breakdown")
    st.markdown(f"**${prop[8]:.0f} × {nights} nights:** ${subtotal:.2f}")
    st.markdown(f"**Service fee (12%):** ${service_fee:.2f}")
    st.markdown(f"**Taxes (8%):** ${taxes:.2f}")
    st.markdown(f"**Total:** ${total_price:.2f}")
    
    # Payment method
    payment_method = st.selectbox("Payment Method", 
                                ["Credit Card", "PayPal", "Apple Pay", "Google Pay"])
    
    if payment_method == "Credit Card":
        col1, col2 = st.columns(2)
        with col1:
            card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            expiry = st.text_input("Expiry Date", placeholder="MM/YY")
        with col2:
            cardholder = st.text_input("Cardholder Name", placeholder="John Smith")
            cvv = st.text_input("CVV", placeholder="123", type="password")
    
    # Pay button
    if st.button("💳 Pay Now & Confirm Booking", key="pay_btn", use_container_width=True):
        if create_booking(prop[0], st.session_state.user['id'], prop[2], prop[5], prop[6],
                        prop[13], check_in, check_out, total_price, guest_count, payment_method):
            st.success("🎉 Booking Confirmed! Payment successful.")
            st.balloons()
            
            st.markdown(f"""
            ### ✅ Booking Confirmation
            
            **Property:** {prop[2]}  
            **Location:** {prop[5]}, {prop[6]}  
            **Dates:** {check_in} → {check_out}  
            **Guests:** {guest_count}  
            **Total Paid:** ${total_price:.2f}  
            **Payment Method:** {payment_method}  
            
            🎊 Your booking is confirmed!
            """)
            
            # Navigation after booking
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 View My Bookings", key="goto_bookings", use_container_width=True):
                    st.session_state.current_page = 'bookings'
            
            with col2:
                if st.button("🏠 Browse More Properties", key="goto_browse", use_container_width=True):
                    st.session_state.current_page = 'browse'
        else:
            st.error("❌ Booking failed. Please try again.")

# Bookings page
def show_bookings_page():
    st.markdown("### 📋 My Bookings")
    
    bookings = get_user_bookings(st.session_state.user['id'])
    
    if not bookings:
        st.info("🏖️ You don't have any bookings yet. Browse properties to make your first booking!")
        return
    
    for booking in bookings:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if booking[6]:
                st.image(booking[6], width=200)
            else:
                st.image("https://via.placeholder.com/200x150?text=Property", width=200)
        
        with col2:
            st.markdown(f"### {booking[3]}")
            st.markdown(f"📍 {booking[4]}, {booking[5]}")
            st.markdown(f"📅 {booking[7]} → {booking[8]}")
            st.markdown(f"👥 {booking[10]} guests")
            st.markdown(f"💰 Total: ${booking[9]:.2f}")
            st.markdown(f"💳 Payment: {booking[11]}")
        
        with col3:
            st.markdown(f"Status: 🟢 {booking[12].title()}")
        
        st.divider()

# Host page
def show_host_page():
    st.markdown("### 🏡 Host Your Property")
    
    with st.form("host_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Property Title*")
            property_type = st.selectbox("Property Type*", ["Apartment", "House", "Villa", "Studio", "Suite"])
            city = st.text_input("City*")
            country = st.text_input("Country*")
            address = st.text_area("Address*")
        
        with col2:
            price_per_night = st.number_input("Price per Night ($)*", min_value=1.0, step=1.0)
            max_guests = st.number_input("Maximum Guests*", min_value=1, step=1)
            bedrooms = st.number_input("Bedrooms*", min_value=0, step=1)
            bathrooms = st.number_input("Bathrooms*", min_value=1, step=1)
            image_url = st.text_input("Image URL")
        
        description = st.text_area("Description*")
        
        # Amenities
        amenity_cols = st.columns(4)
        amenities = []
        amenity_options = ["WiFi", "Kitchen", "Parking", "Pool", "Gym", "AC", "Heating", "TV"]
        
        for i, amenity in enumerate(amenity_options):
            with amenity_cols[i % 4]:
                if st.checkbox(amenity):
                    amenities.append(amenity)
        
        submit_btn = st.form_submit_button("🏡 List My Property", use_container_width=True)
        
        if submit_btn:
            if all([title, property_type, city, country, address, price_per_night, description]):
                conn = sqlite3.connect('oikos_debug.db')
                cursor = conn.cursor()
                amenities_json = json.dumps(amenities)
                cursor.execute("""
                    INSERT INTO properties (host_id, title, description, property_type, city, country,
                                          address, price_per_night, max_guests, bedrooms, bathrooms, amenities, image_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (st.session_state.user['id'], title, description, property_type, city, country, address,
                      price_per_night, max_guests, bedrooms, bathrooms, amenities_json, image_url))
                conn.commit()
                conn.close()
                st.success("🎉 Property listed successfully!")
                st.balloons()
            else:
                st.error("⚠️ Please fill in all required fields")

# Dashboard page
def show_dashboard_page():
    st.markdown("### 📊 Travel Dashboard")
    
    bookings = get_user_bookings(st.session_state.user['id'])
    
    if not bookings:
        st.info("📈 Make your first booking to see your travel analytics!")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_spent = sum(booking[9] for booking in bookings)
    total_bookings = len(bookings)
    avg_booking = total_spent / total_bookings if total_bookings > 0 else 0
    unique_cities = len(set(booking[4] for booking in bookings))
    
    with col1:
        st.metric("📋 Total Bookings", total_bookings)
    
    with col2:
        st.metric("💰 Total Spent", f"${total_spent:.0f}")
    
    with col3:
        st.metric("📊 Avg Booking", f"${avg_booking:.0f}")
    
    with col4:
        st.metric("🌍 Cities Visited", unique_cities)
    
    # Chart
    if bookings:
        st.markdown("### 💰 Spending Timeline")
        dates = [booking[7] for booking in bookings]
        amounts = [booking[9] for booking in bookings]
        df = pd.DataFrame({'Date': dates, 'Amount': amounts})
        fig = px.bar(df, x='Date', y='Amount', title='Booking Spending')
        st.plotly_chart(fig, use_container_width=True)

# Main application
def main():
    init_database()
    populate_sample_data()
    
    if st.session_state.user is None:
        show_auth_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
