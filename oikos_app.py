# Oikos - Airbnb Clone Application
# Main application file

import streamlit as st
from oikos_database import DatabaseManager
from oikos_auth import UserManager, show_auth_page
from oikos_properties import PropertyManager, show_property_listings, show_host_property
from oikos_bookings import BookingManager, show_user_bookings, show_booking_modal
from oikos_reviews import ReviewManager, show_review_form
from oikos_dashboard import show_dashboard
from oikos_utils import load_css, init_session_state, populate_sample_data

# Configure Streamlit page
st.set_page_config(
    page_title="Oikos - Find Your Perfect Stay",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
@st.cache_resource
def get_managers():
    db_manager = DatabaseManager()
    user_manager = UserManager(db_manager)
    property_manager = PropertyManager(db_manager)
    booking_manager = BookingManager(db_manager)
    review_manager = ReviewManager(db_manager)
    
    return db_manager, user_manager, property_manager, booking_manager, review_manager

# Main application UI
def show_main_app():
    _, user_manager, property_manager, booking_manager, review_manager = get_managers()
    
    # Initialize navigation state
    if 'nav_open' not in st.session_state:
        st.session_state.nav_open = False
    
    # Hamburger Navigation
    st.markdown(f"""
    <div class="hamburger-menu" onclick="toggleNav()">
        <div class="hamburger-icon" id="hamburger">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
    
    <div class="nav-overlay" id="navOverlay" onclick="toggleNav()"></div>
    
    <div class="nav-panel" id="navPanel">
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 2rem; color: white; margin-bottom: 10px;">🏠 Oikos</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Welcome, {st.session_state.user['first_name']}! ✨</div>
        </div>
        
        <a href="#" class="nav-item" onclick="setPage('home')">🏠 Browse Properties</a>
        <a href="#" class="nav-item" onclick="setPage('bookings')">📋 My Bookings</a>
        <a href="#" class="nav-item" onclick="setPage('host')">🏡 Host Property</a>
        <a href="#" class="nav-item" onclick="setPage('dashboard')">📊 Dashboard</a>
        <a href="#" class="nav-item" onclick="logout()" style="margin-top: 20px; background: rgba(255,255,255,0.2);">🚪 Logout</a>
    </div>
    
    <script>
        function toggleNav() {{
            const panel = document.getElementById('navPanel');
            const overlay = document.getElementById('navOverlay');
            const hamburger = document.getElementById('hamburger');
            
            panel.classList.toggle('open');
            overlay.classList.toggle('open');
            hamburger.classList.toggle('open');
        }}
        
        function setPage(page) {{
            // This would trigger Streamlit rerun with new page
            toggleNav();
        }}
        
        function logout() {{
            // This would trigger logout
            toggleNav();
        }}
    </script>
    """, unsafe_allow_html=True)
    
    # Navigation functionality (hidden buttons for Streamlit functionality)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠", key="nav_home_hidden", help="Browse Properties"):
            st.session_state.page = 'home'
            st.rerun()
    
    with col2:
        if st.button("📋", key="nav_bookings_hidden", help="My Bookings"):
            st.session_state.page = 'bookings'
            st.rerun()
    
    with col3:
        if st.button("🏡", key="nav_host_hidden", help="Host Property"):
            st.session_state.page = 'host'
            st.rerun()
    
    with col4:
        if st.button("📊", key="nav_dashboard_hidden", help="Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    with col5:
        if st.button("🚪", key="logout_hidden", help="Logout"):
            st.session_state.user = None
            st.session_state.page = 'home'
            st.rerun()
    
    # Hide the navigation buttons with CSS
    st.markdown("""
    <style>
    div[data-testid="column"] button {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main content based on selected page
    if st.session_state.page == 'home':
        show_property_listings(property_manager, booking_manager, review_manager)
        
        # Handle booking modal
        if hasattr(st.session_state, 'show_booking') and st.session_state.show_booking:
            from oikos_bookings import show_booking_modal
            show_booking_modal(st.session_state.selected_property, booking_manager)
            st.session_state.show_booking = False
            
    elif st.session_state.page == 'bookings':
        show_user_bookings(booking_manager, review_manager)
        
        # Handle review modal
        if hasattr(st.session_state, 'show_review') and st.session_state.show_review:
            from oikos_reviews import show_review_form
            show_review_form(st.session_state.selected_booking, review_manager)
            st.session_state.show_review = False
    elif st.session_state.page == 'host':
        show_host_property(property_manager)
    elif st.session_state.page == 'dashboard':
        show_dashboard(property_manager, booking_manager)
    
    # Professional Footer
    st.markdown("""
    <div class="oikos-footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>🏠 Oikos</h3>
                <p style="color: #ccc; line-height: 1.6;">Your gateway to extraordinary accommodations worldwide. Experience the world like a local with our curated selection of unique stays.</p>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <a href="#">About Us</a>
                <a href="#">How It Works</a>
                <a href="#">Safety & Trust</a>
                <a href="#">Help Center</a>
            </div>
            <div class="footer-section">
                <h3>Host</h3>
                <a href="#">Become a Host</a>
                <a href="#">Host Resources</a>
                <a href="#">Community Guidelines</a>
                <a href="#">Host Protection</a>
            </div>
            <div class="footer-section">
                <h3>Support</h3>
                <a href="#">Contact Us</a>
                <a href="#">Terms of Service</a>
                <a href="#">Privacy Policy</a>
                <a href="#">Accessibility</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 Oikos. All rights reserved. Made with ❤️ for travelers worldwide.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main application
def main():
    load_css()
    init_session_state()
    
    # Populate sample data on first run
    populate_sample_data()
    
    if st.session_state.user is None:
        show_auth_page()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
