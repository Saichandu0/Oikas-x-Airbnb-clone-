# Oikos Authentication System
import streamlit as st
import hashlib
import sqlite3
from typing import Dict, Optional

class UserManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str, 
                   first_name: str, last_name: str, phone: str = None) -> bool:
        try:
            conn = self.db.get_connection()
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
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute("""
            SELECT id, username, email, first_name, last_name, is_host
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
                'last_name': user[4],
                'is_host': user[5]
            }
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, first_name, last_name, phone, is_host
            FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'first_name': user[3],
                'last_name': user[4],
                'phone': user[5],
                'is_host': user[6]
            }
        return None

# Authentication UI
def show_auth_page():
    from oikos_database import DatabaseManager
    
    # Beautiful Beach/Resort Hero Section with Travel Theme
    st.markdown("""
    <div style="background: linear-gradient(rgba(255, 107, 107, 0.6), rgba(78, 205, 196, 0.6)), url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600"><defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:%2387CEEB;stop-opacity:1" /><stop offset="50%" style="stop-color:%2340E0D0;stop-opacity:1" /><stop offset="100%" style="stop-color:%23FFE4B5;stop-opacity:1" /></linearGradient></defs><rect width="1200" height="600" fill="url(%23bg)"/><circle cx="100" cy="100" r="30" fill="%23FFF" opacity="0.3"/><circle cx="300" cy="150" r="20" fill="%23FFF" opacity="0.2"/><circle cx="500" cy="80" r="25" fill="%23FFF" opacity="0.25"/><circle cx="700" cy="120" r="35" fill="%23FFF" opacity="0.15"/><circle cx="900" cy="90" r="28" fill="%23FFF" opacity="0.3"/><circle cx="1100" cy="140" r="22" fill="%23FFF" opacity="0.2"/></svg>') center/cover; min-height: 500px; display: flex; align-items: center; justify-content: center; padding: 6rem 2rem; margin: -1rem -1rem 3rem -1rem; border-radius: 0 0 40px 40px; text-align: center; color: white; position: relative; overflow: hidden;">
        
        <div style="position: absolute; top: 10%; left: 10%; animation: float 6s ease-in-out infinite; z-index: 1; opacity: 0.4; font-size: 3rem;">✈️</div>
        <div style="position: absolute; top: 20%; right: 15%; animation: float 8s ease-in-out infinite 2s; z-index: 1; opacity: 0.4; font-size: 2.5rem;">📷</div>
        <div style="position: absolute; bottom: 20%; left: 20%; animation: float 7s ease-in-out infinite 1s; z-index: 1; opacity: 0.4; font-size: 2.8rem;">🧭</div>
        <div style="position: absolute; bottom: 15%; right: 10%; animation: float 9s ease-in-out infinite 3s; z-index: 1; opacity: 0.4; font-size: 2.2rem;">🧳</div>
        
        <div style="position: relative; z-index: 2; width: 100%; max-width: 1000px;">
            <div style="font-size: 3.5rem; font-weight: 800; text-shadow: 0 4px 20px rgba(0,0,0,0.5); margin-bottom: 1rem; line-height: 1.2; background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">🏖️ Welcome to Oikos</div>
            <div style="font-size: 1.3rem; margin-bottom: 2rem; line-height: 1.4; text-shadow: 0 2px 10px rgba(0,0,0,0.3); opacity: 0.95;">Your gateway to paradise • Luxury resorts • Beach villas • Mountain retreats</div>
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                <div style="text-align: center; animation: bounceIn 1s ease-out 0.2s both;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">🏖️</div>
                    <div style="font-size: 0.9rem; opacity: 0.95; font-weight: 600; text-shadow: 0 1px 3px rgba(0,0,0,0.3);">Beach Resorts</div>
                </div>
                <div style="text-align: center; animation: bounceIn 1s ease-out 0.4s both;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">🏔️</div>
                    <div style="font-size: 0.9rem; opacity: 0.95; font-weight: 600; text-shadow: 0 1px 3px rgba(0,0,0,0.3);">Mountain Lodges</div>
                </div>
                <div style="text-align: center; animation: bounceIn 1s ease-out 0.6s both;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">🏝️</div>
                    <div style="font-size: 0.9rem; opacity: 0.95; font-weight: 600; text-shadow: 0 1px 3px rgba(0,0,0,0.3);">Island Villas</div>
                </div>
                <div style="text-align: center; animation: bounceIn 1s ease-out 0.8s both;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">🏨</div>
                    <div style="font-size: 0.9rem; opacity: 0.95; font-weight: 600; text-shadow: 0 1px 3px rgba(0,0,0,0.3);">Luxury Hotels</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the authentication card
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="auth-title">🌺 Join Paradise</div>
        <div class="auth-subtitle">Start your journey to extraordinary stays</div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🏖️ Login", "🌴 Sign Up"])
    
        db_manager = DatabaseManager()
        user_manager = UserManager(db_manager)
    
        with tab1:
            st.markdown("### 🔐 Welcome Back")
            st.markdown("Sign in to access your bookings and continue your journey")
            
            with st.form("login_form"):
                st.markdown("**Username**")
                username = st.text_input("Username", placeholder="Enter your username", key="login_username", label_visibility="collapsed")
                
                st.markdown("**Password**")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password", label_visibility="collapsed")
                
                st.markdown("")
                login_btn = st.form_submit_button("🏖️ Sign In to Paradise", use_container_width=True, type="primary")
                
                if login_btn:
                    if username and password:
                        user = user_manager.authenticate_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.markdown('<div class="success-message">🌺 Welcome back! Redirecting to your dashboard...</div>', unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown('<div class="error-message">❌ Invalid credentials. Please try again.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">⚠️ Please fill in all fields</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**Demo Accounts:** Try `john_host` / `password123`")
        
        with tab2:
            st.markdown("### 🌴 Join Our Community")
            st.markdown("Create your account and discover amazing places worldwide")
            
            with st.form("signup_form"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**First Name**")
                    first_name = st.text_input("First Name", placeholder="Your first name", key="signup_first", label_visibility="collapsed")
                    
                    st.markdown("**Username**")
                    username = st.text_input("Username", placeholder="Choose username", key="signup_username", label_visibility="collapsed")
                    
                    st.markdown("**Email**")
                    email = st.text_input("Email", placeholder="your@email.com", key="signup_email", label_visibility="collapsed")
                
                with col2:
                    st.markdown("**Last Name**")
                    last_name = st.text_input("Last Name", placeholder="Your last name", key="signup_last", label_visibility="collapsed")
                    
                    st.markdown("**Phone (Optional)**")
                    phone = st.text_input("Phone", placeholder="+1 (555) 123-4567", key="signup_phone", label_visibility="collapsed")
                    
                    st.markdown("**Password**")
                    password = st.text_input("Password", type="password", placeholder="Create password", key="signup_password", label_visibility="collapsed")
                
                st.markdown("")
                signup_btn = st.form_submit_button("🌺 Create Paradise Account", use_container_width=True, type="primary")
                
                if signup_btn:
                    if all([first_name, last_name, username, email, password]):
                        if user_manager.create_user(username, email, password, first_name, last_name, phone):
                            st.markdown('<div class="success-message">🎉 Account created! Welcome to paradise. Please login above.</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-message">❌ Username or email already exists</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">⚠️ Please fill in all required fields</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close auth-card
