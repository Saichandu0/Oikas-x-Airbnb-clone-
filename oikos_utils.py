# Oikos Utilities
import streamlit as st

# Professional CSS for modern UI
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding and sidebar */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .css-1d391kg {display: none;}
    .css-1lcbmhc {display: none;}
    .css-1outpf7 {display: none;}
    section[data-testid="stSidebar"] {display: none;}
    .stSidebar {display: none !important;}
    
    /* Hide navigation buttons */
    div[data-testid="column"] button {
        display: none !important;
    }
    
    /* Custom Header */
    .oikos-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .oikos-logo {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9)), 
                    url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=1200') center/cover;
        padding: 4rem 2rem;
        margin: -1rem -1rem 3rem -1rem;
        border-radius: 0 0 30px 30px;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        margin-bottom: 2rem;
        opacity: 0.95;
        animation: fadeInUp 1s ease-out 0.2s both;
    }
    
    /* Search Bar */
    .search-container {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 50px;
        padding: 1.5rem 2rem;
        margin: 2rem auto;
        max-width: 800px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        animation: fadeInUp 1s ease-out 0.4s both;
    }
    
    /* Enhanced Property Cards */
    .property-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem;
        border: 1px solid rgba(0,0,0,0.05);
        animation: fadeInUp 0.8s ease-out;
        position: relative;
    }
    
    .property-card:nth-child(1) { animation-delay: 0.1s; }
    .property-card:nth-child(2) { animation-delay: 0.2s; }
    .property-card:nth-child(3) { animation-delay: 0.3s; }
    .property-card:nth-child(4) { animation-delay: 0.4s; }
    .property-card:nth-child(5) { animation-delay: 0.5s; }
    .property-card:nth-child(6) { animation-delay: 0.6s; }
    
    .property-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 25px 80px rgba(0,0,0,0.25);
        animation: pulse 2s infinite;
    }
    
    .property-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .property-card:hover::before {
        left: 100%;
    }
    
    .property-image {
        position: relative;
        overflow: hidden;
        height: 250px;
    }
    
    .property-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .property-card:hover .property-image img {
        transform: scale(1.05);
    }
    
    .property-content {
        padding: 1.5rem;
    }
    
    .property-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .property-location {
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    .property-details {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #888;
    }
    
    .property-rating {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        margin-bottom: 1rem;
    }
    
    .rating-stars {
        color: #FFD700;
        font-size: 1rem;
    }
    
    .rating-text {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    .property-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 1rem;
        border-top: 1px solid #f0f0f0;
    }
    
    .price-tag {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    .price-night {
        font-size: 0.9rem;
        font-weight: 400;
        color: #666;
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .btn-secondary {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-secondary:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Sidebar */
    .sidebar .stSelectbox > div > div {
        border-radius: 15px;
        border: 2px solid #e1e5e9;
        background: white;
    }
    
    .sidebar .stButton > button {
        width: 100%;
        border-radius: 15px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .sidebar .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Forms - Enhanced visibility */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border-radius: 15px !important;
        border: 2px solid #e1e5e9 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #1a1a1a !important;
        background: white !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2), 0 4px 12px rgba(0,0,0,0.15) !important;
        outline: none !important;
        background: white !important;
        color: #1a1a1a !important;
    }
    
    /* Input placeholder styling */
    .stTextInput > div > div > input::placeholder {
        color: #999 !important;
        font-weight: 400 !important;
    }
    
    /* Auth page specific styling */
    .auth-container {
        background: linear-gradient(135deg, 
            rgba(26, 188, 156, 0.9), 
            rgba(52, 152, 219, 0.9)), 
            url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200') center/cover;
        min-height: 100vh;
        margin: -1rem -1rem -1rem -1rem;
        padding: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .auth-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(25px);
        border-radius: 30px;
        padding: 2.5rem 2rem;
        box-shadow: 
            0 25px 80px rgba(0,0,0,0.15),
            0 0 0 1px rgba(255,255,255,0.3);
        border: 2px solid rgba(255,255,255,0.4);
        max-width: 500px;
        width: 100%;
        animation: slideInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .auth-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s ease-in-out infinite;
        pointer-events: none;
    }
    
    .auth-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 0.8rem;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: textGlow 2s ease-in-out infinite alternate;
        position: relative;
        z-index: 2;
    }
    
    .auth-subtitle {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 500;
        position: relative;
        z-index: 2;
    }
    
    @keyframes textGlow {
        0% { filter: brightness(1) saturate(1); }
        100% { filter: brightness(1.2) saturate(1.3); }
    }
    
    .beach-hero {
        background: 
            linear-gradient(45deg, 
                rgba(255, 107, 107, 0.7) 0%, 
                rgba(78, 205, 196, 0.7) 25%, 
                rgba(69, 183, 209, 0.7) 50%, 
                rgba(150, 206, 180, 0.7) 75%, 
                rgba(255, 234, 167, 0.7) 100%),
            url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200') center/cover;
        background-size: 400% 400%, cover;
        animation: gradientShift 8s ease infinite;
        padding: 6rem 2rem;
        margin: -1rem -1rem 3rem -1rem;
        border-radius: 0 0 40px 40px;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .beach-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        animation: floatingBubbles 12s ease-in-out infinite;
    }
    
    .beach-hero::after {
        content: '✈️🧳📷🧭⭐🌴🐚🏖️🌊🏄‍♂️🌺🐠🌅🥥🦀';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        font-size: 2.5rem;
        display: flex;
        align-items: center;
        justify-content: space-around;
        opacity: 0.4;
        animation: floatingEmojis 25s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes floatingBubbles {
        0%, 100% { 
            transform: translateY(0px) rotate(0deg);
            opacity: 0.7;
        }
        33% { 
            transform: translateY(-20px) rotate(120deg);
            opacity: 0.9;
        }
        66% { 
            transform: translateY(-10px) rotate(240deg);
            opacity: 0.5;
        }
    }
    
    @keyframes floatingEmojis {
        0% { transform: translateX(0); }
        100% { transform: translateX(50%); }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Enhanced Tab styling for auth */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(78, 205, 196, 0.1));
        border-radius: 20px;
        padding: 0.8rem;
        margin-bottom: 2rem;
        border: 2px solid rgba(255,255,255,0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 15px;
        color: #ff6b6b;
        font-weight: 700;
        padding: 1rem 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 1.1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
        transform: translateY(-2px);
    }
    
    /* Enhanced Form Buttons */
    .stForm button[type="submit"] {
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stForm button[type="submit"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(255, 107, 107, 0.4) !important;
        filter: brightness(1.1) !important;
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Enhanced Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(50px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px) rotate(-5deg);
        }
        to {
            opacity: 1;
            transform: translateX(0) rotate(0deg);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px) rotate(5deg);
        }
        to {
            opacity: 1;
            transform: translateX(0) rotate(0deg);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3) rotate(-10deg);
        }
        50% {
            opacity: 1;
            transform: scale(1.05) rotate(2deg);
        }
        70% {
            transform: scale(0.95) rotate(-1deg);
        }
        100% {
            opacity: 1;
            transform: scale(1) rotate(0deg);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }
        50% {
            transform: scale(1.02);
            box-shadow: 0 12px 40px rgba(0,0,0,0.18);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200px 0;
        }
        100% {
            background-position: calc(200px + 100%) 0;
        }
    }
    
    /* Hamburger Navigation */
    .hamburger-menu {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: none;
        border-radius: 15px;
        padding: 12px;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: bounceIn 1s ease-out;
    }
    
    .hamburger-menu:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .hamburger-icon {
        width: 24px;
        height: 18px;
        position: relative;
        transform: rotate(0deg);
        transition: 0.5s ease-in-out;
    }
    
    .hamburger-icon span {
        display: block;
        position: absolute;
        height: 3px;
        width: 100%;
        background: white;
        border-radius: 2px;
        opacity: 1;
        left: 0;
        transform: rotate(0deg);
        transition: 0.25s ease-in-out;
    }
    
    .hamburger-icon span:nth-child(1) {
        top: 0px;
    }
    
    .hamburger-icon span:nth-child(2) {
        top: 7px;
    }
    
    .hamburger-icon span:nth-child(3) {
        top: 14px;
    }
    
    .hamburger-icon.open span:nth-child(1) {
        top: 7px;
        transform: rotate(135deg);
    }
    
    .hamburger-icon.open span:nth-child(2) {
        opacity: 0;
        left: -60px;
    }
    
    .hamburger-icon.open span:nth-child(3) {
        top: 7px;
        transform: rotate(-135deg);
    }
    
    /* Sliding Navigation Panel */
    .nav-panel {
        position: fixed;
        top: 0;
        left: -350px;
        width: 320px;
        height: 100vh;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        z-index: 999;
        transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 5px 0 25px rgba(0,0,0,0.3);
        padding: 80px 20px 20px;
        overflow-y: auto;
    }
    
    .nav-panel.open {
        left: 0;
    }
    
    .nav-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0,0,0,0.5);
        z-index: 998;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
    }
    
    .nav-overlay.open {
        opacity: 1;
        visibility: visible;
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
        transition: all 0.3s ease;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideInLeft 0.6s ease-out;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .nav-item:nth-child(1) { animation-delay: 0.1s; }
    .nav-item:nth-child(2) { animation-delay: 0.2s; }
    .nav-item:nth-child(3) { animation-delay: 0.3s; }
    .nav-item:nth-child(4) { animation-delay: 0.4s; }
    .nav-item:nth-child(5) { animation-delay: 0.5s; }
    
    /* Loading States */
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .search-container {
            margin: 1rem;
            padding: 1rem;
        }
        
        .property-card {
            margin: 1rem 0;
        }
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .error-message {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
        animation: slideInLeft 0.5s ease-out;
    }
    
    /* Amenities Tags */
    .amenity-tag {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Footer */
    .oikos-footer {
        background: #1a1a1a;
        color: white;
        padding: 3rem 2rem 2rem;
        margin: 4rem -1rem -1rem -1rem;
        border-radius: 30px 30px 0 0;
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
    }
    
    .footer-section h3 {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #667eea;
    }
    
    .footer-section a {
        color: #ccc;
        text-decoration: none;
        display: block;
        margin-bottom: 0.5rem;
        transition: color 0.3s ease;
    }
    
    .footer-section a:hover {
        color: #667eea;
    }
    
    .footer-bottom {
        text-align: center;
        padding-top: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #333;
        color: #999;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state management
def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

# Sample data population
def populate_sample_data():
    """Populate the database with sample data for demonstration"""
    from oikos_database import DatabaseManager
    from oikos_auth import UserManager
    from oikos_properties import PropertyManager
    
    db_manager = DatabaseManager()
    user_manager = UserManager(db_manager)
    property_manager = PropertyManager(db_manager)
    
    # Check if data already exists
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM properties")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count > 0:
        return  # Data already exists
    
    # Create sample users
    sample_users = [
        ("john_host", "john@example.com", "password123", "John", "Smith", "+1234567890"),
        ("sarah_host", "sarah@example.com", "password123", "Sarah", "Johnson", "+1234567891"),
        ("mike_host", "mike@example.com", "password123", "Mike", "Brown", "+1234567892"),
    ]
    
    for username, email, password, first_name, last_name, phone in sample_users:
        user_manager.create_user(username, email, password, first_name, last_name, phone)
    
    # Create extensive sample properties for popular cities worldwide
    sample_properties = [
        # New York City
        {
            "host_id": 1, "title": "Manhattan Skyline Penthouse", "description": "Breathtaking penthouse with panoramic city views. Located in the heart of Manhattan with luxury amenities and rooftop terrace.",
            "property_type": "Apartment", "city": "New York", "country": "USA", "address": "123 5th Avenue, New York, NY 10001",
            "price_per_night": 450.0, "max_guests": 6, "bedrooms": 3, "bathrooms": 2,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Balcony", "Gym"], "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400"
        },
        {
            "host_id": 2, "title": "Brooklyn Loft Experience", "description": "Industrial chic loft in trendy Brooklyn neighborhood. Exposed brick walls, high ceilings, and artistic atmosphere.",
            "property_type": "Loft", "city": "New York", "country": "USA", "address": "456 Brooklyn Heights, NY 11201",
            "price_per_night": 180.0, "max_guests": 4, "bedrooms": 2, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Heating", "TV", "Washer"], "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400"
        },
        
        # London
        {
            "host_id": 1, "title": "Covent Garden Luxury Flat", "description": "Elegant Victorian flat in the heart of London's theater district. Walking distance to West End shows and world-class dining.",
            "property_type": "Apartment", "city": "London", "country": "UK", "address": "78 Covent Garden, London WC2E 8RF",
            "price_per_night": 280.0, "max_guests": 4, "bedrooms": 2, "bathrooms": 2,
            "amenities": ["WiFi", "Kitchen", "Heating", "TV", "Washer", "Dryer"], "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400"
        },
        {
            "host_id": 3, "title": "Thames View Riverside Apartment", "description": "Modern apartment with stunning Thames views. Located near Tower Bridge with easy access to London's attractions.",
            "property_type": "Apartment", "city": "London", "country": "UK", "address": "12 Thames Path, London SE1 2AA",
            "price_per_night": 220.0, "max_guests": 3, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Heating", "TV", "Balcony"], "image_url": "https://images.unsplash.com/photo-1520637836862-4d197d17c93a?w=400"
        },
        
        # Paris
        {
            "host_id": 2, "title": "Montmartre Artist's Retreat", "description": "Charming Parisian apartment in historic Montmartre. Cobblestone streets, artistic heritage, and Sacré-Cœur nearby.",
            "property_type": "Apartment", "city": "Paris", "country": "France", "address": "34 Rue des Abbesses, 75018 Paris",
            "price_per_night": 195.0, "max_guests": 2, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Heating", "TV"], "image_url": "https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=400"
        },
        {
            "host_id": 1, "title": "Champs-Élysées Luxury Suite", "description": "Opulent suite on the famous Champs-Élysées. Designer furnishings, marble bathrooms, and concierge service.",
            "property_type": "Suite", "city": "Paris", "country": "France", "address": "101 Avenue des Champs-Élysées, 75008 Paris",
            "price_per_night": 380.0, "max_guests": 4, "bedrooms": 2, "bathrooms": 2,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Gym", "Pool"], "image_url": "https://images.unsplash.com/photo-1549294413-26f195200c16?w=400"
        },
        
        # Tokyo
        {
            "host_id": 3, "title": "Shibuya Modern Capsule", "description": "Ultra-modern micro-apartment in bustling Shibuya. High-tech amenities and authentic Tokyo experience.",
            "property_type": "Studio", "city": "Tokyo", "country": "Japan", "address": "2-1 Shibuya, Tokyo 150-0002",
            "price_per_night": 85.0, "max_guests": 2, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Air Conditioning", "TV"], "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400"
        },
        {
            "host_id": 2, "title": "Traditional Ryokan Experience", "description": "Authentic Japanese ryokan with tatami mats, futon beds, and traditional tea ceremony. Peaceful garden views.",
            "property_type": "Traditional", "city": "Tokyo", "country": "Japan", "address": "5-3 Asakusa, Tokyo 111-0032",
            "price_per_night": 160.0, "max_guests": 4, "bedrooms": 2, "bathrooms": 1,
            "amenities": ["WiFi", "Heating", "TV", "Garden"], "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400"
        },
        
        # Sydney
        {
            "host_id": 1, "title": "Bondi Beach Surf House", "description": "Beachfront house steps from famous Bondi Beach. Surfboard storage, ocean views, and laid-back Australian vibes.",
            "property_type": "House", "city": "Sydney", "country": "Australia", "address": "88 Campbell Parade, Bondi Beach NSW 2026",
            "price_per_night": 320.0, "max_guests": 8, "bedrooms": 4, "bathrooms": 3,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Balcony", "Garden"], "image_url": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
        },
        {
            "host_id": 3, "title": "Harbour Bridge View Apartment", "description": "Stunning apartment with iconic Sydney Harbour Bridge views. Modern amenities in prime location near Circular Quay.",
            "property_type": "Apartment", "city": "Sydney", "country": "Australia", "address": "15 Circular Quay West, Sydney NSW 2000",
            "price_per_night": 275.0, "max_guests": 4, "bedrooms": 2, "bathrooms": 2,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Balcony", "Pool"], "image_url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400"
        },
        
        # Dubai
        {
            "host_id": 2, "title": "Burj Khalifa Sky Suite", "description": "Luxurious suite with views of Burj Khalifa. Premium amenities, infinity pool, and world-class shopping nearby.",
            "property_type": "Suite", "city": "Dubai", "country": "UAE", "address": "Downtown Dubai, Dubai Marina",
            "price_per_night": 520.0, "max_guests": 6, "bedrooms": 3, "bathrooms": 3,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Pool", "Gym", "Balcony"], "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400"
        },
        
        # Rome
        {
            "host_id": 1, "title": "Colosseum Historic Apartment", "description": "Ancient Roman charm meets modern comfort. Stone walls, original frescoes, and walking distance to the Colosseum.",
            "property_type": "Apartment", "city": "Rome", "country": "Italy", "address": "Via del Colosseo, 00184 Roma RM",
            "price_per_night": 210.0, "max_guests": 4, "bedrooms": 2, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV"], "image_url": "https://images.unsplash.com/photo-1515542622106-78bda8ba0e5b?w=400"
        },
        
        # Barcelona
        {
            "host_id": 3, "title": "Gaudí-Inspired Modernist Flat", "description": "Artistic apartment inspired by Antoni Gaudí's architecture. Colorful mosaics, curved walls, and Gothic Quarter location.",
            "property_type": "Apartment", "city": "Barcelona", "country": "Spain", "address": "Carrer del Bisbe, 08002 Barcelona",
            "price_per_night": 165.0, "max_guests": 3, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Balcony"], "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400"
        },
        
        # Amsterdam
        {
            "host_id": 2, "title": "Canal House Floating Hotel", "description": "Unique houseboat experience on Amsterdam's famous canals. Historic charm with modern amenities and bike rental included.",
            "property_type": "Houseboat", "city": "Amsterdam", "country": "Netherlands", "address": "Prinsengracht 263, 1016 GV Amsterdam",
            "price_per_night": 145.0, "max_guests": 2, "bedrooms": 1, "bathrooms": 1,
            "amenities": ["WiFi", "Kitchen", "Heating", "TV"], "image_url": "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=400"
        },
        
        # Singapore
        {
            "host_id": 1, "title": "Marina Bay Infinity Pool Suite", "description": "Spectacular suite overlooking Marina Bay Sands. Infinity pool access, skyline views, and luxury shopping nearby.",
            "property_type": "Suite", "city": "Singapore", "country": "Singapore", "address": "10 Bayfront Avenue, Singapore 018956",
            "price_per_night": 390.0, "max_guests": 4, "bedrooms": 2, "bathrooms": 2,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Pool", "Gym"], "image_url": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=400"
        },
        
        # Los Angeles
        {
            "host_id": 3, "title": "Hollywood Hills Villa", "description": "Glamorous villa in the Hollywood Hills with panoramic city views. Pool, spa, and celebrity neighbor sightings guaranteed.",
            "property_type": "Villa", "city": "Los Angeles", "country": "USA", "address": "1234 Mulholland Drive, Los Angeles, CA 90210",
            "price_per_night": 480.0, "max_guests": 10, "bedrooms": 5, "bathrooms": 4,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Pool", "Gym", "Balcony", "Garden"], "image_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=400"
        },
        
        # Miami
        {
            "host_id": 2, "title": "South Beach Art Deco Suite", "description": "Iconic Art Deco building on South Beach. Pastel colors, ocean views, and vibrant nightlife at your doorstep.",
            "property_type": "Suite", "city": "Miami", "country": "USA", "address": "1001 Ocean Drive, Miami Beach, FL 33139",
            "price_per_night": 285.0, "max_guests": 4, "bedrooms": 2, "bathrooms": 2,
            "amenities": ["WiFi", "Kitchen", "Air Conditioning", "TV", "Pool", "Balcony"], "image_url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400"
        }
    ]
    
    for prop in sample_properties:
        property_manager.create_property(**prop)
