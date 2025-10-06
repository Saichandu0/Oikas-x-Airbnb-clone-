# Oikos Dashboard
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

def show_dashboard(property_manager, booking_manager):
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.5rem;">📊 Travel Dashboard</h1>
        <p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">Your travel insights and booking analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user's bookings for analytics
    bookings = booking_manager.get_user_bookings(st.session_state.user['id'])
    
    if not bookings:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 20px; margin: 2rem 0;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">📈 Start Your Journey</h3>
            <p style="color: #666; margin-bottom: 2rem;">Make your first booking to see your travel analytics here!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Professional metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_spent = sum(booking['total_price'] for booking in bookings)
    completed_bookings = [b for b in bookings if b['check_out_date'] < date.today()]
    upcoming_bookings = [b for b in bookings if b['check_in_date'] > date.today()]
    
    metrics = [
        ("📋", "Total Bookings", len(bookings), "#667eea"),
        ("💰", "Total Spent", f"${total_spent:.0f}", "#764ba2"),
        ("✅", "Completed", len(completed_bookings), "#4CAF50"),
        ("🔮", "Upcoming", len(upcoming_bookings), "#FF9800")
    ]
    
    for i, (icon, label, value, color) in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}, {color}dd); color: white; padding: 2rem 1rem; border-radius: 20px; text-align: center; box-shadow: 0 8px 30px rgba(0,0,0,0.12); margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">{value}</div>
                <div style="font-size: 0.9rem; opacity: 0.9; font-weight: 500;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Booking timeline chart
    if bookings:
        st.markdown("### Booking Timeline")
        
        # Prepare data for chart
        booking_dates = []
        booking_amounts = []
        
        for booking in bookings:
            booking_dates.append(booking['check_in_date'])
            booking_amounts.append(booking['total_price'])
        
        # Create DataFrame for plotting
        df = pd.DataFrame({
            'Date': booking_dates,
            'Amount': booking_amounts
        })
        
        # Create line chart
        fig = px.line(df, x='Date', y='Amount', 
                     title='Booking Spending Over Time',
                     markers=True)
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Amount ($)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
