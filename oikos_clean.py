# Oikos - Professional Airbnb Clone
# Complete application in a single file for reliability

import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import datetime
from datetime import date, timedelta
import json
import plotly.express as px

# Configure Streamlit
st.set_page_config(
    page_title="Oikos - Find Your Perfect Stay",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS with Beach Theme
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    
    /* Beach Hero Background */
    .beach-hero {
        background: 
            linear-gradient(45deg, 
                rgba(255, 107, 107, 0.8) 0%, 
                rgba(78, 205, 196, 0.8) 25%, 
                rgba(69, 183, 209, 0.8) 50%, 
                rgba(150, 206, 180, 0.8) 75%, 
                rgba(255, 234, 167, 0.8) 100%),
            url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200') center/cover;
        background-size: 400% 400%, cover;
        animation: gradientShift 10s ease infinite;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        margin: -1rem -1rem -1rem -1rem;
        position: relative;
        overflow: hidden;
    }
    
    /* Floating Travel Elements */
    .floating-element {
        position: absolute;
        animation: float 8s ease-in-out infinite;
        opacity: 0.6;
        font-size: 3rem;
        z-index: 1;
    }
    
    .floating-element:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
    .floating-element:nth-child(2) { top: 20%; right: 15%; animation-delay: 2s; }
    .floating-element:nth-child(3) { bottom: 20%; left: 20%; animation-delay: 1s; }
    .floating-element:nth-child(4) { bottom: 15%; right: 10%; animation-delay: 3s; }
    .floating-element:nth-child(5) { top: 50%; left: 5%; animation-delay: 4s; }
    .floating-element:nth-child(6) { top: 60%; right: 5%; animation-delay: 1.5s; }
    
    /* Auth Card */
    .auth-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 3rem 2.5rem;
        box-shadow: 0 30px 100px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.5);
        max-width: 500px;
        width: 100%;
        animation: slideInUp 1s ease-out;
        position: relative;
        z-index: 10;
    }
    
    .auth-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: textPulse 2s ease-in-out infinite alternate;
    }
    
    .auth-subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Form Styling */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        border: 2px solid #e1e5e9 !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #1a1a1a !important;
        background: white !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2) !important;
        outline: none !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Property Cards */
    .property-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        transition: all 0.4s ease;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .property-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    }
    
    /* Animations */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(10deg); }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes textPulse {
        0% { filter: brightness(1); }
        100% { filter: brightness(1.2); }
    }
    
    /* Hamburger Menu */
    .hamburger {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
        border: none;
        border-radius: 15px;
        padding: 15px;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        transition: all 0.3s ease;
    }
    
    .hamburger:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4);
    }
    
    .hamburger-lines {
        width: 25px;
        height: 3px;
        background: white;
        margin: 5px 0;
        transition: 0.3s;
        border-radius: 2px;
    }
    
    /* Navigation Panel */
    .nav-panel {
        position: fixed;
        top: 0;
        left: -350px;
        width: 320px;
        height: 100vh;
        background: linear-gradient(180deg, #ff6b6b 0%, #4ecdc4 100%);
        z-index: 999;
        transition: left 0.4s ease;
        padding: 80px 20px 20px;
        box-shadow: 5px 0 25px rgba(0,0,0,0.3);
    }
    
    .nav-panel.open {
        left: 0;
    }
    
    .nav-item {
        display: block;
        color: white;
        text-decoration: none;
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 15px;
        font-weight: 600;
        font-size: 1.1rem;
        background: rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(10px);
    }
    </style>
    """, unsafe_allow_html=True)

# Database Management
class Database:
    def __init__(self):
        self.db_path = "oikos_clean.db"
        self.init_db()
    
    def get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        conn = self.get_conn()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Properties table
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
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (host_id) REFERENCES users (id)
            )
        """)
        
        # Bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                guest_id INTEGER NOT NULL,
                check_in_date DATE NOT NULL,
                check_out_date DATE NOT NULL,
                total_price REAL NOT NULL,
                guest_count INTEGER NOT NULL,
                status TEXT DEFAULT 'confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties (id),
                FOREIGN KEY (guest_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()

# User Management
class UserManager:
    def __init__(self, db):
        self.db = db
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password, first_name, last_name, phone=None):
        try:
            conn = self.db.get_conn()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, first_name, last_name, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, first_name, last_name, phone))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def authenticate_user(self, username, password):
        conn = self.db.get_conn()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute("""
            SELECT id, username, email, first_name, last_name
            FROM users 
            WHERE username = ? AND password_hash = ?
        """, (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'first_name': user[3],
                'last_name': user[4]
            }
        return None

# Property Management
class PropertyManager:
    def __init__(self, db):
        self.db = db
    
    def get_properties(self, city=None, max_price=None, min_guests=None):
        conn = self.db.get_conn()
        cursor = conn.cursor()
        
        query = """
            SELECT p.*, u.first_name, u.last_name
            FROM properties p
            JOIN users u ON p.host_id = u.id
            WHERE 1=1
        """
        
        params = []
        
        if city:
            query += " AND LOWER(p.city) LIKE LOWER(?)"
            params.append(f"%{city}%")
        
        if max_price:
            query += " AND p.price_per_night <= ?"
            params.append(max_price)
        
        if min_guests:
            query += " AND p.max_guests >= ?"
            params.append(min_guests)
        
        query += " ORDER BY p.created_at DESC"
        
        cursor.execute(query, params)
        properties = cursor.fetchall()
        conn.close()
        
        result = []
        for prop in properties:
            amenities = json.loads(prop[12]) if prop[12] else []
            result.append({
                'id': prop[0],
                'title': prop[2],
                'description': prop[3],
                'property_type': prop[4],
                'city': prop[5],
                'country': prop[6],
                'price_per_night': prop[8],
                'max_guests': prop[9],
                'bedrooms': prop[10],
                'bathrooms': prop[11],
                'amenities': amenities,
                'image_url': prop[13],
                'host_name': f"{prop[15]} {prop[16]}"
            })
        
        return result

# Initialize Database and Managers
@st.cache_resource
def get_managers():
    db = Database()
    user_manager = UserManager(db)
    property_manager = PropertyManager(db)
    return db, user_manager, property_manager

# Populate Sample Data
def populate_sample_data():
    db, user_manager, property_manager = get_managers()
    
    # Check if data exists
    conn = db.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM properties")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count > 0:
        return
    
    # Create sample users
    sample_users = [
        ("john_host", "john@example.com", "password123", "John", "Smith"),
        ("sarah_host", "sarah@example.com", "password123", "Sarah", "Johnson"),
        ("mike_host", "mike@example.com", "password123", "Mike", "Brown"),
    ]
    
    for username, email, password, first_name, last_name in sample_users:
        user_manager.create_user(username, email, password, first_name, last_name)
    
    # Create global properties
    global_properties = [
        # New York
        {
            "host_id": 1, "title": "Manhattan Skyline Penthouse", 
            "description": "Breathtaking penthouse with panoramic city views in the heart of Manhattan.",
            "property_type": "Penthouse", "city": "New York", "country": "USA",
            "address": "123 5th Avenue, New York, NY", "price_per_night": 450.0,
            "max_guests": 6, "bedrooms": 3, "bathrooms": 2,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Balcony", "Gym"],
            "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400"
        },
        # London
        {
            "host_id": 2, "title": "Covent Garden Luxury Flat",
            "description": "Elegant Victorian flat in London's theater district with modern amenities.",
            "property_type": "Apartment", "city": "London", "country": "UK",
            "address": "78 Covent Garden, London", "price_per_night": 280.0,
            "max_guests": 4, "bedrooms": 2, "bathrooms": 2,
            "amenities": ["WiFi", "Kitchen", "Heating", "TV", "Washer"],
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400"
        },
        # Paris
        {
            "host_id": 3, "title": "Montmartre Artist's Retreat",
            "description": "Charming Parisian apartment in historic Montmartre near Sacré-Cœur.",
            "property_type": "Apartment", "city": "Paris", "country": "France",
            "address": "34 Rue des Abbesses, Paris", "price_per_night": 195.0,
            "max_guests": 2, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Heating", "TV"],
            "image_url": "https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400"
        },
        # Tokyo
        {
            "host_id": 1, "title": "Shibuya Modern Capsule",
            "description": "Ultra-modern micro-apartment in bustling Shibuya with high-tech amenities.",
            "property_type": "Studio", "city": "Tokyo", "country": "Japan",
            "address": "2-1 Shibuya, Tokyo", "price_per_night": 85.0,
            "max_guests": 2, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Air Conditioning", "TV"],
            "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400"
        },
        # Sydney
        {
            "host_id": 2, "title": "Bondi Beach Surf House",
            "description": "Beachfront house steps from famous Bondi Beach with ocean views.",
            "property_type": "House", "city": "Sydney", "country": "Australia",
            "address": "88 Campbell Parade, Bondi Beach", "price_per_night": 320.0,
            "max_guests": 8, "bedrooms": 4, "bathrooms": 3,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Balcony", "Garden"],
            "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
        },
        # Dubai
        {
            "host_id": 3, "title": "Burj Khalifa Sky Suite",
            "description": "Luxurious suite with views of Burj Khalifa and Dubai Marina.",
            "property_type": "Suite", "city": "Dubai", "country": "UAE",
            "address": "Downtown Dubai, Dubai Marina", "price_per_night": 520.0,
            "max_guests": 6, "bedrooms": 3, "bathrooms": 3,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Pool", "Gym", "Balcony"],
            "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400"
        },
        # Barcelona
        {
            "host_id": 1, "title": "Gaudí-Inspired Modernist Flat",
            "description": "Artistic apartment inspired by Antoni Gaudí in the Gothic Quarter.",
            "property_type": "Apartment", "city": "Barcelona", "country": "Spain",
            "address": "Carrer del Bisbe, Barcelona", "price_per_night": 165.0,
            "max_guests": 3, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Balcony"],
            "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400"
        },
        # Amsterdam
        {
            "host_id": 2, "title": "Canal House Floating Hotel",
            "description": "Unique houseboat experience on Amsterdam's famous canals.",
            "property_type": "Houseboat", "city": "Amsterdam", "country": "Netherlands",
            "address": "Prinsengracht 263, Amsterdam", "price_per_night": 145.0,
            "max_guests": 2, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Heating", "TV"],
            "image_url": "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=400"
        }
    ]
    
    # Insert properties
    conn = db.get_conn()
    cursor = conn.cursor()
    
    for prop in global_properties:
        amenities_json = json.dumps(prop['amenities'])
        cursor.execute("""
            INSERT INTO properties (host_id, title, description, property_type, city, country,
                                  address, price_per_night, max_guests, bedrooms, bathrooms,
                                  amenities, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (prop['host_id'], prop['title'], prop['description'], prop['property_type'],
              prop['city'], prop['country'], prop['address'], prop['price_per_night'],
              prop['max_guests'], prop['bedrooms'], prop['bathrooms'], amenities_json,
              prop['image_url']))
    
    conn.commit()
    conn.close()

# Session State Management
def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

# Authentication Page
def show_auth_page():
    db, user_manager, property_manager = get_managers()
    
    # Beach Hero Section with Floating Elements
    st.markdown("""
    <div class="beach-hero">
        <div class="floating-element">✈️</div>
        <div class="floating-element">📷</div>
        <div class="floating-element">🧭</div>
        <div class="floating-element">🧳</div>
        <div class="floating-element">🌴</div>
        <div class="floating-element">⭐</div>
        
        <div class="auth-card">
            <div class="auth-title">🏖️ Join Paradise</div>
            <div class="auth-subtitle">Start your journey to extraordinary stays</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### 🔐 Welcome Back")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        login_btn = st.form_submit_button("🏖️ Sign In to Paradise", use_container_width=True)
        
        if login_btn:
            if username and password:
                user = user_manager.authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success("🌺 Welcome back! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            else:
                st.error("⚠️ Please fill in all fields")
    
    st.markdown("---")
    
    # Signup Form
    with st.form("signup_form", clear_on_submit=False):
        st.markdown("### 🌴 Create Account")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Your first name")
            username = st.text_input("Username", placeholder="Choose username")
            email = st.text_input("Email", placeholder="your@email.com")
        
        with col2:
            last_name = st.text_input("Last Name", placeholder="Your last name")
            phone = st.text_input("Phone (Optional)", placeholder="+1 (555) 123-4567")
            password = st.text_input("Password", type="password", placeholder="Create password")
        
        signup_btn = st.form_submit_button("🌺 Create Paradise Account", use_container_width=True)
        
        if signup_btn:
            if all([first_name, last_name, username, email, password]):
                if user_manager.create_user(username, email, password, first_name, last_name, phone):
                    st.success("🎉 Account created! Please login above.")
                else:
                    st.error("❌ Username or email already exists")
            else:
                st.error("⚠️ Please fill in all required fields")
    
    st.info("**Demo Account:** Username: `john_host` | Password: `password123`")

# Property Listings Page
def show_property_listings():
    db, user_manager, property_manager = get_managers()
    
    # Hamburger Navigation
    st.markdown("""
    <div class="hamburger" onclick="toggleNav()">
        <div class="hamburger-lines"></div>
        <div class="hamburger-lines"></div>
        <div class="hamburger-lines"></div>
    </div>
    
    <div class="nav-panel" id="navPanel">
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 2rem; color: white;">🏠 Oikos</div>
            <div style="color: rgba(255,255,255,0.8);">Welcome, """ + st.session_state.user['first_name'] + """!</div>
        </div>
        <div class="nav-item">🏠 Browse Properties</div>
        <div class="nav-item">📋 My Bookings</div>
        <div class="nav-item">🏡 Host Property</div>
        <div class="nav-item">📊 Dashboard</div>
        <div class="nav-item" style="margin-top: 20px;">🚪 Logout</div>
    </div>
    
    <script>
        function toggleNav() {
            document.getElementById('navPanel').classList.toggle('open');
        }
    </script>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b, #4ecdc4); padding: 4rem 2rem; margin: -1rem -1rem 3rem -1rem; border-radius: 0 0 30px 30px; text-align: center; color: white;">
        <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem;">🌍 Find Your Perfect Stay</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Discover unique accommodations in amazing destinations worldwide</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        city_filter = st.text_input("🌍 City", placeholder="Where are you going?")
    
    with col2:
        max_price = st.number_input("💰 Max Price/Night", min_value=0, value=1000, step=50)
    
    with col3:
        min_guests = st.number_input("👥 Guests", min_value=1, value=1, step=1)
    
    with col4:
        st.write("")
        search_btn = st.button("🔍 Search Properties", use_container_width=True)
    
    # Get and display properties
    properties = property_manager.get_properties(
        city=city_filter if city_filter else None,
        max_price=max_price,
        min_guests=min_guests
    )
    
    if not properties:
        st.info("🏖️ No properties found. Try different search criteria!")
        return
    
    st.markdown("### 🏠 Featured Properties")
    
    # Display properties in grid
    for i in range(0, len(properties), 3):
        cols = st.columns(3)
        
        for j, col in enumerate(cols):
            if i + j < len(properties):
                prop = properties[i + j]
                
                with col:
                    # Property card
                    st.markdown(f"""
                    <div class="property-card">
                        <img src="{prop['image_url']}" style="width: 100%; height: 200px; object-fit: cover;" />
                        <div style="padding: 1.5rem;">
                            <h3 style="margin-bottom: 0.5rem; color: #1a1a1a;">{prop['title']}</h3>
                            <p style="color: #666; margin-bottom: 1rem;">📍 {prop['city']}, {prop['country']}</p>
                            <p style="color: #888; font-size: 0.9rem; margin-bottom: 1rem;">
                                🏠 {prop['property_type']} • 🛏️ {prop['bedrooms']} bed • 🚿 {prop['bathrooms']} bath
                            </p>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <span style="font-size: 1.4rem; font-weight: 700; color: #1a1a1a;">${prop['price_per_night']:.0f}</span>
                                    <span style="color: #666;"> / night</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Book Now", key=f"book_{prop['id']}", use_container_width=True):
                        st.success(f"🎉 Booking initiated for {prop['title']}!")
                    
                    # Amenities
                    if prop['amenities']:
                        amenities_html = ""
                        for amenity in prop['amenities'][:4]:
                            amenities_html += f'<span style="display: inline-block; background: rgba(255, 107, 107, 0.1); color: #ff6b6b; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; margin: 0.2rem;">{amenity}</span>'
                        st.markdown(amenities_html, unsafe_allow_html=True)

# Main Application
def main():
    load_css()
    init_session_state()
    populate_sample_data()
    
    if st.session_state.user is None:
        show_auth_page()
    else:
        show_property_listings()

if __name__ == "__main__":
    main()
