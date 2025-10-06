# Oikos Booking Management
import streamlit as st
import datetime
from datetime import date, timedelta
from typing import Dict, List

class BookingManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_booking(self, property_id: int, guest_id: int, check_in_date: date,
                      check_out_date: date, guest_count: int) -> bool:
        try:
            # Check availability
            if not self.is_property_available(property_id, check_in_date, check_out_date):
                return False
            
            # Calculate total price
            from oikos_properties import PropertyManager
            property_manager = PropertyManager(self.db)
            property_data = property_manager.get_property_by_id(property_id)
            if not property_data:
                return False
            
            nights = (check_out_date - check_in_date).days
            total_price = nights * property_data['price_per_night']
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO bookings (property_id, guest_id, check_in_date,
                                    check_out_date, total_price, guest_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (property_id, guest_id, check_in_date, check_out_date,
                  total_price, guest_count))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error creating booking: {e}")
            return False
    
    def is_property_available(self, property_id: int, check_in: date, check_out: date) -> bool:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM bookings
            WHERE property_id = ? AND status = 'confirmed'
            AND NOT (check_out_date <= ? OR check_in_date >= ?)
        """, (property_id, check_in, check_out))
        
        conflicts = cursor.fetchone()[0]
        conn.close()
        
        return conflicts == 0
    
    def get_user_bookings(self, user_id: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT b.*, p.title, p.city, p.country, p.image_url
            FROM bookings b
            JOIN properties p ON b.property_id = p.id
            WHERE b.guest_id = ?
            ORDER BY b.created_at DESC
        """, (user_id,))
        
        bookings = cursor.fetchall()
        conn.close()
        
        result = []
        for booking in bookings:
            result.append({
                'id': booking[0],
                'property_id': booking[1],
                'check_in_date': datetime.datetime.strptime(booking[3], '%Y-%m-%d').date(),
                'check_out_date': datetime.datetime.strptime(booking[4], '%Y-%m-%d').date(),
                'total_price': booking[5],
                'guest_count': booking[6],
                'status': booking[7],
                'property_title': booking[9],
                'city': booking[10],
                'country': booking[11],
                'image_url': booking[12]
            })
        
        return result

def show_booking_modal(property_data, booking_manager):
    st.markdown(f"### Book {property_data['title']}")
    
    with st.form(f"booking_form_{property_data['id']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            check_in = st.date_input("Check-in Date", 
                                   min_value=date.today(),
                                   value=date.today())
        
        with col2:
            check_out = st.date_input("Check-out Date",
                                    min_value=date.today() + timedelta(days=1),
                                    value=date.today() + timedelta(days=2))
        
        guest_count = st.number_input("Number of Guests", 
                                    min_value=1, 
                                    max_value=property_data['max_guests'],
                                    value=1)
        
        if check_in >= check_out:
            st.error("Check-out date must be after check-in date")
            return
        
        nights = (check_out - check_in).days
        total_price = nights * property_data['price_per_night']
        
        st.markdown(f"**Total: ${total_price:.2f}** ({nights} nights × ${property_data['price_per_night']:.0f})")
        
        book_btn = st.form_submit_button("Confirm Booking", use_container_width=True)
        
        if book_btn:
            if booking_manager.is_property_available(property_data['id'], check_in, check_out):
                if booking_manager.create_booking(
                    property_data['id'], 
                    st.session_state.user['id'],
                    check_in, 
                    check_out, 
                    guest_count
                ):
                    st.success("Booking confirmed! Check your bookings page for details.")
                else:
                    st.error("Failed to create booking. Please try again.")
            else:
                st.error("Property is not available for selected dates.")

def show_user_bookings(booking_manager, review_manager):
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1a1a1a; margin-bottom: 0.5rem;">📋 My Bookings</h1>
        <p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">Manage your reservations and travel history</p>
    </div>
    """, unsafe_allow_html=True)
    
    bookings = booking_manager.get_user_bookings(st.session_state.user['id'])
    
    if not bookings:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 20px; margin: 2rem 0;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">🌟 Ready for your first adventure?</h3>
            <p style="color: #666; margin-bottom: 2rem;">You don't have any bookings yet. Discover amazing places to stay!</p>
            <a href="#" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; border-radius: 25px; text-decoration: none; font-weight: 600;">Browse Properties</a>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for booking in bookings:
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                if booking['image_url']:
                    st.image(booking['image_url'], width=200)
                else:
                    st.image("https://via.placeholder.com/200x150?text=Property", width=200)
            
            with col2:
                st.markdown(f"### {booking['property_title']}")
                st.markdown(f"📍 {booking['city']}, {booking['country']}")
                st.markdown(f"📅 {booking['check_in_date']} → {booking['check_out_date']}")
                st.markdown(f"👥 {booking['guest_count']} guests")
                st.markdown(f"💰 Total: ${booking['total_price']:.2f}")
                
                status_color = {"confirmed": "🟢", "cancelled": "🔴", "completed": "🔵"}
                st.markdown(f"Status: {status_color.get(booking['status'], '⚪')} {booking['status'].title()}")
            
            with col3:
                if booking['status'] == 'confirmed' and booking['check_out_date'] < date.today():
                    if st.button(f"Leave Review", key=f"review_{booking['id']}"):
                        st.session_state.selected_booking = booking
                        st.session_state.show_review = True
            
            st.divider()
