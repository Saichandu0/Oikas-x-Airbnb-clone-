# Oikos - Simple Working Airbnb Clone
import streamlit as st
import sqlite3
import hashlib
import json
from datetime import date

# Configure page
st.set_page_config(
    page_title="Oikos - Find Your Perfect Stay",
    page_icon="🏠",
    layout="wide"
)

# Simple but beautiful CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Beach background for auth */
.auth-page {
    background: linear-gradient(135deg, rgba(52, 152, 219, 0.8), rgba(26, 188, 156, 0.8)), 
                url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200') center/cover;
    min-height: 100vh;
    padding: 2rem;
    margin: -1rem;
}

/* Floating animations */
.floating {
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Property cards */
.property-card {
    background: white;
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.property-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.2);
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
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# Database setup
def init_database():
    conn = sqlite3.connect('oikos_simple.db')
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
    
    conn.commit()
    conn.close()

# User functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, first_name, last_name):
    try:
        conn = sqlite3.connect('oikos_simple.db')
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
    conn = sqlite3.connect('oikos_simple.db')
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

# Property functions
def get_properties(city=None, max_price=None):
    conn = sqlite3.connect('oikos_simple.db')
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

def populate_sample_data():
    conn = sqlite3.connect('oikos_simple.db')
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
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password_hash, first_name, last_name))
    
    # Global properties
    global_properties = [
        (1, "Manhattan Skyline Penthouse", "Breathtaking penthouse with panoramic city views.", "Penthouse", "New York", "USA", 450.0, 6, 3, 2, '["WiFi", "Kitchen", "AC", "TV", "Balcony"]', "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400"),
        (2, "Covent Garden Luxury Flat", "Elegant Victorian flat in London's theater district.", "Apartment", "London", "UK", 280.0, 4, 2, 2, '["WiFi", "Kitchen", "Heating", "TV"]', "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400"),
        (3, "Montmartre Artist Retreat", "Charming Parisian apartment in historic Montmartre.", "Apartment", "Paris", "France", 195.0, 2, 1, 1, '["WiFi", "Kitchen", "Heating"]', "https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400"),
        (1, "Shibuya Modern Capsule", "Ultra-modern apartment in bustling Shibuya.", "Studio", "Tokyo", "Japan", 85.0, 2, 1, 1, '["WiFi", "AC", "TV"]', "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400"),
        (2, "Bondi Beach Surf House", "Beachfront house steps from famous Bondi Beach.", "House", "Sydney", "Australia", 320.0, 8, 4, 3, '["WiFi", "Kitchen", "AC", "Balcony"]', "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),
        (3, "Burj Khalifa Sky Suite", "Luxurious suite with views of Burj Khalifa.", "Suite", "Dubai", "UAE", 520.0, 6, 3, 3, '["WiFi", "Kitchen", "AC", "Pool", "Gym"]', "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400"),
        (1, "Gaudi Modernist Flat", "Artistic apartment inspired by Antoni Gaudí.", "Apartment", "Barcelona", "Spain", 165.0, 3, 1, 1, '["WiFi", "Kitchen", "AC"]', "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400"),
        (2, "Canal House Floating Hotel", "Unique houseboat on Amsterdam's canals.", "Houseboat", "Amsterdam", "Netherlands", 145.0, 2, 1, 1, '["WiFi", "Kitchen", "Heating"]', "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=400"),
    ]
    
    for prop in global_properties:
        cursor.execute("""
            INSERT INTO properties (host_id, title, description, property_type, city, country,
                                  price_per_night, max_guests, bedrooms, bathrooms, amenities, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, prop)
    
    conn.commit()
    conn.close()

# Initialize session state
def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'browse'
    if 'selected_property' not in st.session_state:
        st.session_state.selected_property = None

# Authentication page
def show_auth_page():
    # Beach background
    st.markdown('<div class="auth-page">', unsafe_allow_html=True)
    
    # Floating elements
    st.markdown("""
    <div style="position: fixed; top: 10%; left: 10%; font-size: 3rem; opacity: 0.6; animation: float 6s ease-in-out infinite;">✈️</div>
    <div style="position: fixed; top: 20%; right: 15%; font-size: 2.5rem; opacity: 0.6; animation: float 8s ease-in-out infinite 2s;">📷</div>
    <div style="position: fixed; bottom: 20%; left: 20%; font-size: 2.8rem; opacity: 0.6; animation: float 7s ease-in-out infinite 1s;">🧭</div>
    <div style="position: fixed; bottom: 15%; right: 10%; font-size: 2.2rem; opacity: 0.6; animation: float 9s ease-in-out infinite 3s;">🧳</div>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 4rem; color: white; text-shadow: 0 4px 20px rgba(0,0,0,0.5); margin-bottom: 1rem;">🏖️ Welcome to Oikos</h1>
        <p style="font-size: 1.3rem; color: white; opacity: 0.9; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">Your gateway to paradise • Luxury resorts • Beach villas • Mountain retreats</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the forms
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create tabs
        tab1, tab2 = st.tabs(["🏖️ Login", "🌴 Sign Up"])
        
        with tab1:
            st.markdown("### 🔐 Welcome Back")
            st.markdown("Sign in to access your bookings and continue your journey")
            
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
            st.markdown("Join our community and discover amazing places")
            
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

# Property listings page
def show_property_listings():
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3498db, #1abc9c); padding: 2rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 20px 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h1 style="color: white; font-size: 2rem; margin: 0;">🏠 Oikos</h1>
            <div style="color: white;">Welcome, """ + st.session_state.user['first_name'] + """! ✨</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Browse", use_container_width=True):
            st.session_state.page = 'home'
    
    with col2:
        if st.button("📋 Bookings", use_container_width=True):
            st.session_state.page = 'bookings'
    
    with col3:
        if st.button("🏡 Host", use_container_width=True):
            st.session_state.page = 'host'
    
    with col4:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
    
    with col5:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    st.markdown("---")
    
    # Search section
    st.markdown("### 🔍 Find Your Perfect Stay")
    
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
                    # Property card
                    st.markdown(f"""
                    <div class="property-card">
                        <img src="{prop[13]}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 1rem;" />
                        <h4 style="margin-bottom: 0.5rem; color: #1a1a1a;">{prop[2]}</h4>
                        <p style="color: #666; margin-bottom: 0.5rem;">📍 {prop[5]}, {prop[6]}</p>
                        <p style="color: #888; font-size: 0.9rem; margin-bottom: 1rem;">
                            🏠 {prop[4]} • 🛏️ {prop[10]} bed • 🚿 {prop[11]} bath
                        </p>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.3rem; font-weight: 700; color: #3498db;">${prop[7]:.0f}</span>
                                <span style="color: #666;"> / night</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Book {prop[2]}", key=f"book_{prop[0]}", use_container_width=True):
                        st.success(f"🎉 Booking initiated for {prop[2]}!")
                    
                    # Show amenities safely
                    if prop[12] and prop[12].strip():
                        try:
                            amenities = json.loads(prop[12])
                            amenities_text = " • ".join(amenities[:3])
                            if len(amenities) > 3:
                                amenities_text += f" • +{len(amenities) - 3} more"
                            st.markdown(f"🏷️ {amenities_text}")
                        except:
                            st.markdown("🏷️ WiFi • Kitchen • TV")

# Main application
def main():
    init_database()
    init_session_state()
    populate_sample_data()
    
    if st.session_state.user is None:
        show_auth_page()
    else:
        show_property_listings()

if __name__ == "__main__":
    main()
