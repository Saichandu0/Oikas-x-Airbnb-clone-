# Oikos - Complete Airbnb Clone with Full Functionality
import streamlit as st
import sqlite3
import hashlib
import json
from datetime import date, timedelta
import plotly.express as px
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Oikos - Find Your Perfect Stay",
    page_icon="🏠",
    layout="wide"
)

# Beautiful CSS with Beach Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Beach background */
.beach-bg {
    background: linear-gradient(135deg, rgba(52, 152, 219, 0.8), rgba(26, 188, 156, 0.8)), 
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

/* Property cards */
.property-card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    transition: all 0.4s ease;
    animation: fadeInUp 0.8s ease-out;
}

.property-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3498db, #1abc9c) !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4) !important;
}

/* Payment card */
.payment-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 15px 40px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

/* Metrics */
.metric-card {
    background: linear-gradient(135deg, #3498db, #1abc9c);
    color: white;
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
    margin: 1rem 0;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# Database functions
def init_database():
    conn = sqlite3.connect('oikos_final.db')
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
            property_title TEXT NOT NULL,
            property_city TEXT NOT NULL,
            property_country TEXT NOT NULL,
            property_image TEXT,
            check_in_date DATE NOT NULL,
            check_out_date DATE NOT NULL,
            total_price REAL NOT NULL,
            guest_count INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (property_id) REFERENCES properties (id),
            FOREIGN KEY (guest_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, first_name, last_name):
    try:
        conn = sqlite3.connect('oikos_final.db')
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password_hash, first_name, last_name))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    conn = sqlite3.connect('oikos_final.db')
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
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

def get_properties(city=None, max_price=None):
    conn = sqlite3.connect('oikos_final.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM properties WHERE 1=1"
    params = []
    
    if city:
        query += " AND LOWER(city) LIKE LOWER(?)"
        params.append(f"%{city}%")
    
    if max_price:
        query += " AND price_per_night <= ?"
        params.append(max_price)
    
    query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    properties = cursor.fetchall()
    conn.close()
    
    return properties

def create_property(host_id, title, description, property_type, city, country, address, 
                   price_per_night, max_guests, bedrooms, bathrooms, amenities, image_url):
    conn = sqlite3.connect('oikos_final.db')
    cursor = conn.cursor()
    
    amenities_json = json.dumps(amenities)
    cursor.execute("""
        INSERT INTO properties (host_id, title, description, property_type, city, country,
                              address, price_per_night, max_guests, bedrooms, bathrooms,
                              amenities, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (host_id, title, description, property_type, city, country, address,
          price_per_night, max_guests, bedrooms, bathrooms, amenities_json, image_url))
    
    conn.commit()
    conn.close()
    return True

def create_booking(property_id, guest_id, property_title, property_city, property_country,
                  property_image, check_in_date, check_out_date, total_price, guest_count, payment_method):
    conn = sqlite3.connect('oikos_final.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO bookings (property_id, guest_id, property_title, property_city, property_country,
                            property_image, check_in_date, check_out_date, total_price, guest_count, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (property_id, guest_id, property_title, property_city, property_country,
          property_image, check_in_date, check_out_date, total_price, guest_count, payment_method))
    
    conn.commit()
    conn.close()
    return True

def get_user_bookings(user_id):
    conn = sqlite3.connect('oikos_final.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM bookings WHERE guest_id = ? ORDER BY created_at DESC
    """, (user_id,))
    
    bookings = cursor.fetchall()
    conn.close()
    return bookings

def populate_sample_data():
    conn = sqlite3.connect('oikos_final.db')
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
        except sqlite3.IntegrityError:
            pass  # User already exists
    
    # Global properties with proper JSON
    global_properties = [
        (1, "Manhattan Skyline Penthouse", "Breathtaking penthouse with panoramic city views in Manhattan.", "Penthouse", "New York", "USA", "123 5th Avenue, New York", 450.0, 6, 3, 2, '["WiFi", "Kitchen", "AC", "TV", "Balcony", "Gym"]', "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400"),
        (2, "Covent Garden Luxury Flat", "Elegant Victorian flat in London's theater district.", "Apartment", "London", "UK", "78 Covent Garden, London", 280.0, 4, 2, 2, '["WiFi", "Kitchen", "Heating", "TV", "Washer"]', "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400"),
        (3, "Montmartre Artist Retreat", "Charming Parisian apartment in historic Montmartre.", "Apartment", "Paris", "France", "34 Rue des Abbesses, Paris", 195.0, 2, 1, 1, '["WiFi", "Kitchen", "Heating", "TV"]', "https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400"),
        (1, "Shibuya Modern Capsule", "Ultra-modern apartment in bustling Shibuya district.", "Studio", "Tokyo", "Japan", "2-1 Shibuya, Tokyo", 85.0, 2, 1, 1, '["WiFi", "AC", "TV"]', "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400"),
        (2, "Bondi Beach Surf House", "Beachfront house steps from famous Bondi Beach.", "House", "Sydney", "Australia", "88 Campbell Parade, Bondi", 320.0, 8, 4, 3, '["WiFi", "Kitchen", "AC", "TV", "Balcony"]', "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        (3, "Burj Khalifa Sky Suite", "Luxurious suite with views of Burj Khalifa.", "Suite", "Dubai", "UAE", "Downtown Dubai Marina", 520.0, 6, 3, 3, '["WiFi", "Kitchen", "AC", "Pool", "Gym"]', "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400"),
        (1, "Gaudi Modernist Flat", "Artistic apartment inspired by Antoni Gaudí.", "Apartment", "Barcelona", "Spain", "Carrer del Bisbe, Barcelona", 165.0, 3, 1, 1, '["WiFi", "Kitchen", "AC", "Balcony"]', "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400"),
        (2, "Canal House Floating Hotel", "Unique houseboat on Amsterdam's famous canals.", "Houseboat", "Amsterdam", "Netherlands", "Prinsengracht 263, Amsterdam", 145.0, 2, 1, 1, '["WiFi", "Kitchen", "Heating"]', "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=400"),
        (3, "Hollywood Hills Villa", "Glamorous villa with panoramic city views.", "Villa", "Los Angeles", "USA", "1234 Mulholland Drive, LA", 480.0, 10, 5, 4, '["WiFi", "Kitchen", "AC", "Pool", "Gym"]', "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=400"),
        (1, "Marina Bay Infinity Suite", "Spectacular suite overlooking Marina Bay Sands.", "Suite", "Singapore", "Singapore", "10 Bayfront Avenue, Singapore", 390.0, 4, 2, 2, '["WiFi", "Kitchen", "AC", "Pool"]', "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=400"),
    ]
    
    for prop in global_properties:
        cursor.execute("""
            INSERT INTO properties (host_id, title, description, property_type, city, country,
                                  address, price_per_night, max_guests, bedrooms, bathrooms, amenities, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, prop)
    
    conn.commit()
    conn.close()

# Session state
def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'browse'
    if 'selected_property' not in st.session_state:
        st.session_state.selected_property = None

# Authentication page
def show_auth_page():
    st.markdown('<div class="beach-bg">', unsafe_allow_html=True)
    
    # Floating elements
    st.markdown("""
    <div class="floating" style="top: 10%; left: 10%; font-size: 3rem;">✈️</div>
    <div class="floating" style="top: 20%; right: 15%; font-size: 2.5rem; animation-delay: 2s;">📷</div>
    <div class="floating" style="bottom: 20%; left: 20%; font-size: 2.8rem; animation-delay: 1s;">🧭</div>
    <div class="floating" style="bottom: 15%; right: 10%; font-size: 2.2rem; animation-delay: 3s;">🧳</div>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 4rem; color: white; text-shadow: 0 4px 20px rgba(0,0,0,0.5);">🏖️ Welcome to Oikos</h1>
        <p style="font-size: 1.3rem; color: white; opacity: 0.9;">Your gateway to paradise • Luxury resorts • Beach villas • Mountain retreats</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Forms
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🏖️ Login", "🌴 Sign Up"])
        
        with tab1:
            st.markdown("### 🔐 Welcome Back")
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_btn = st.form_submit_button("🏖️ Sign In to Paradise", use_container_width=True)
                
                if login_btn:
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
            
            with st.form("signup_form"):
                col_a, col_b = st.columns(2)
                with col_a:
                    first_name = st.text_input("First Name")
                    username = st.text_input("Username")
                    email = st.text_input("Email")
                
                with col_b:
                    last_name = st.text_input("Last Name")
                    phone = st.text_input("Phone (Optional)")
                    password = st.text_input("Password", type="password")
                
                signup_btn = st.form_submit_button("🌺 Create Paradise Account", use_container_width=True)
                
                if signup_btn:
                    if all([first_name, last_name, username, email, password]):
                        if create_user(username, email, password, first_name, last_name):
                            st.success("🎉 Account created! Please login.")
                        else:
                            st.error("❌ Username or email already exists")
                    else:
                        st.error("⚠️ Please fill in all required fields")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.info("**Demo Account:** Username: `john_host` | Password: `password123`")

# Navigation header
def show_navigation():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #3498db, #1abc9c); padding: 1.5rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 20px 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h1 style="color: white; font-size: 2rem; margin: 0;">🏠 Oikos</h1>
            <div style="color: white; font-weight: 500;">Welcome, {st.session_state.user['first_name']}! ✨</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Browse Properties", key="nav_browse", use_container_width=True):
            st.session_state.page = 'browse'
            st.rerun()
    
    with col2:
        if st.button("📋 My Bookings", key="nav_bookings", use_container_width=True):
            st.session_state.page = 'bookings'
            st.rerun()
    
    with col3:
        if st.button("🏡 Host Property", key="nav_host", use_container_width=True):
            st.session_state.page = 'host'
            st.rerun()
    
    with col4:
        if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    with col5:
        if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = 'browse'
            st.rerun()

# Browse properties page
def show_browse_page():
    show_navigation()
    
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
                    st.markdown(f"""
                    <div class="property-card">
                        <img src="{prop[13]}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 15px; margin-bottom: 1rem;" />
                        <h4 style="margin-bottom: 0.5rem; color: #1a1a1a;">{prop[2]}</h4>
                        <p style="color: #666; margin-bottom: 0.5rem;">📍 {prop[5]}, {prop[6]}</p>
                        <p style="color: #888; font-size: 0.9rem; margin-bottom: 1rem;">
                            🏠 {prop[4]} • 🛏️ {prop[10]} bed • 🚿 {prop[11]} bath
                        </p>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.4rem; font-weight: 700; color: #3498db;">${prop[8]:.0f}</span>
                                <span style="color: #666;"> / night</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View Details", key=f"view_{prop[0]}", use_container_width=True):
                        st.session_state.selected_property = prop
                        st.session_state.page = 'payment'
                        st.rerun()
                    
                    # Show amenities
                    if prop[12]:
                        try:
                            amenities = json.loads(prop[12])
                            amenities_text = " • ".join(amenities[:3])
                            if len(amenities) > 3:
                                amenities_text += f" • +{len(amenities) - 3} more"
                            st.markdown(f"🏷️ {amenities_text}")
                        except:
                            st.markdown("🏷️ WiFi • Kitchen • TV")

# Host property page
def show_host_page():
    show_navigation()
    
    st.markdown("### 🏡 Host Your Property")
    st.markdown("List your space and start earning money as a host")
    
    with st.form("host_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Property Title*", placeholder="Amazing apartment in downtown")
            property_type = st.selectbox("Property Type*", ["Apartment", "House", "Villa", "Studio", "Suite", "Other"])
            city = st.text_input("City*")
            country = st.text_input("Country*")
            address = st.text_area("Full Address*")
        
        with col2:
            price_per_night = st.number_input("Price per Night ($)*", min_value=1.0, step=1.0)
            max_guests = st.number_input("Maximum Guests*", min_value=1, step=1)
            bedrooms = st.number_input("Bedrooms*", min_value=0, step=1)
            bathrooms = st.number_input("Bathrooms*", min_value=1, step=1)
            image_url = st.text_input("Image URL", placeholder="https://example.com/image.jpg")
        
        description = st.text_area("Description*", placeholder="Describe your property...")
        
        # Amenities
        st.markdown("### Amenities")
        amenity_cols = st.columns(4)
        
        amenities = []
        amenity_options = ["WiFi", "Kitchen", "Parking", "Pool", "Gym", "AC", "Heating", "TV", "Washer", "Balcony"]
        
        for i, amenity in enumerate(amenity_options):
            with amenity_cols[i % 4]:
                if st.checkbox(amenity):
                    amenities.append(amenity)
        
        submit_btn = st.form_submit_button("🏡 List My Property", use_container_width=True)
        
        if submit_btn:
            required_fields = [title, property_type, city, country, address, price_per_night, description]
            
            if all(required_fields):
                if create_property(st.session_state.user['id'], title, description, property_type,
                                 city, country, address, price_per_night, max_guests, bedrooms,
                                 bathrooms, amenities, image_url):
                    st.success("🎉 Property listed successfully!")
                else:
                    st.error("❌ Failed to list property")
            else:
                st.error("⚠️ Please fill in all required fields marked with *")

# Bookings page
def show_bookings_page():
    show_navigation()
    
    st.markdown("### 📋 My Bookings")
    st.markdown("Manage your reservations and travel history")
    
    bookings = get_user_bookings(st.session_state.user['id'])
    
    if not bookings:
        st.info("🏖️ You don't have any bookings yet. Browse properties to make your first booking!")
        return
    
    for booking in bookings:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if booking[6]:  # property_image
                st.image(booking[6], width=200)
            else:
                st.image("https://via.placeholder.com/200x150?text=Property", width=200)
        
        with col2:
            st.markdown(f"### {booking[3]}")  # property_title
            st.markdown(f"📍 {booking[4]}, {booking[5]}")  # city, country
            st.markdown(f"📅 {booking[7]} → {booking[8]}")  # dates
            st.markdown(f"👥 {booking[10]} guests")  # guest_count
            st.markdown(f"💰 Total: ${booking[9]:.2f}")  # total_price
            st.markdown(f"💳 Payment: {booking[11]}")  # payment_method
        
        with col3:
            status_color = {"confirmed": "🟢", "cancelled": "🔴", "completed": "🔵"}
            st.markdown(f"Status: {status_color.get(booking[12], '⚪')} {booking[12].title()}")
        
        st.divider()

# Dashboard page
def show_dashboard_page():
    show_navigation()
    
    st.markdown("### 📊 Travel Dashboard")
    st.markdown("Your travel insights and booking analytics")
    
    bookings = get_user_bookings(st.session_state.user['id'])
    
    if not bookings:
        st.info("📈 Make your first booking to see your travel analytics!")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_spent = sum(booking[9] for booking in bookings)  # total_price
    total_bookings = len(bookings)
    avg_booking = total_spent / total_bookings if total_bookings > 0 else 0
    unique_cities = len(set(booking[4] for booking in bookings))  # unique cities
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📋</div>
            <div style="font-size: 2rem; font-weight: 700;">{total_bookings}</div>
            <div style="opacity: 0.9;">Total Bookings</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💰</div>
            <div style="font-size: 2rem; font-weight: 700;">${total_spent:.0f}</div>
            <div style="opacity: 0.9;">Total Spent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div style="font-size: 2rem; font-weight: 700;">${avg_booking:.0f}</div>
            <div style="opacity: 0.9;">Avg Booking</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌍</div>
            <div style="font-size: 2rem; font-weight: 700;">{unique_cities}</div>
            <div style="opacity: 0.9;">Cities Visited</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Spending chart
    if bookings:
        st.markdown("### 💰 Spending Timeline")
        
        # Prepare data
        dates = [booking[13] for booking in bookings]  # created_at
        amounts = [booking[9] for booking in bookings]  # total_price
        
        df = pd.DataFrame({'Date': dates, 'Amount': amounts})
        fig = px.line(df, x='Date', y='Amount', title='Booking Spending Over Time', markers=True)
        st.plotly_chart(fig, use_container_width=True)

# Payment page
def show_payment_page():
    show_navigation()
    
    if not st.session_state.selected_property:
        st.error("No property selected")
        return
    
    prop = st.session_state.selected_property
    
    st.markdown("### 💳 Complete Your Booking")
    
    # Property details
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(prop[13], use_column_width=True)
    
    with col2:
        st.markdown(f"## {prop[2]}")
        st.markdown(f"📍 {prop[5]}, {prop[6]}")
        st.markdown(f"🏠 {prop[4]} • 🛏️ {prop[10]} bed • 🚿 {prop[11]} bath")
        st.markdown(f"👥 Up to {prop[9]} guests")
        
        # Show amenities
        if prop[12]:
            try:
                amenities = json.loads(prop[12])
                st.markdown("### 🏷️ Amenities")
                for amenity in amenities:
                    st.markdown(f"✅ {amenity}")
            except:
                st.markdown("✅ WiFi ✅ Kitchen ✅ TV")
    
    st.markdown("---")
    st.markdown(prop[3])  # description
    st.markdown("---")
    
    # Booking form
    with st.form("booking_form"):
        st.markdown("### 📅 Select Your Dates")
        
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
        service_fee = subtotal * 0.12  # 12% service fee
        taxes = subtotal * 0.08  # 8% taxes
        total_price = subtotal + service_fee + taxes
        
        st.markdown("### 💰 Price Breakdown")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**${prop[8]:.0f} × {nights} nights**")
            st.markdown("**Service fee**")
            st.markdown("**Taxes**")
            st.markdown("---")
            st.markdown("**Total**")
        
        with col2:
            st.markdown(f"${subtotal:.2f}")
            st.markdown(f"${service_fee:.2f}")
            st.markdown(f"${taxes:.2f}")
            st.markdown("---")
            st.markdown(f"**${total_price:.2f}**")
        
        # Payment method
        st.markdown("### 💳 Payment Method")
        payment_method = st.selectbox("Choose Payment Method", 
                                    ["Credit Card", "PayPal", "Apple Pay", "Google Pay", "Bank Transfer"])
        
        if payment_method == "Credit Card":
            col1, col2 = st.columns(2)
            with col1:
                card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
                expiry = st.text_input("Expiry Date", placeholder="MM/YY")
            with col2:
                cardholder = st.text_input("Cardholder Name", placeholder="John Smith")
                cvv = st.text_input("CVV", placeholder="123", type="password")
        
        # Pay button
        pay_btn = st.form_submit_button("💳 Pay Now & Confirm Booking", use_container_width=True)
        
        if pay_btn:
            # Create booking
            if create_booking(prop[0], st.session_state.user['id'], prop[2], prop[5], prop[6],
                            prop[13], check_in, check_out, total_price, guest_count, payment_method):
                st.success("🎉 Booking Confirmed! Payment successful.")
                st.balloons()
                
                # Show confirmation
                st.markdown(f"""
                ### ✅ Booking Confirmation
                
                **Property:** {prop[2]}  
                **Location:** {prop[5]}, {prop[6]}  
                **Dates:** {check_in} → {check_out}  
                **Guests:** {guest_count}  
                **Total Paid:** ${total_price:.2f}  
                **Payment Method:** {payment_method}  
                
                🎊 Your booking is confirmed! Check your bookings page for details.
                """)
                
                # Booking completed message
                st.markdown("---")
                st.markdown("### 🎊 What's Next?")
                st.markdown("- Check your email for booking confirmation")
                st.markdown("- View your booking details in the 'My Bookings' section")
                st.markdown("- Contact your host if you have any questions")
            else:
                st.error("❌ Booking failed. Please try again.")

# Main application logic
def main():
    init_database()
    init_session_state()
    populate_sample_data()
    
    if st.session_state.user is None:
        show_auth_page()
    else:
        # Route to different pages
        if st.session_state.page == 'browse':
            show_browse_page()
        elif st.session_state.page == 'host':
            show_host_page()
        elif st.session_state.page == 'bookings':
            show_bookings_page()
        elif st.session_state.page == 'dashboard':
            show_dashboard_page()
        elif st.session_state.page == 'payment':
            show_payment_page()

if __name__ == "__main__":
    main()
