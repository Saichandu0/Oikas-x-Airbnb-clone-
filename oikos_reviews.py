# Oikos Review Management
import streamlit as st
from typing import Dict, List

class ReviewManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_review(self, property_id: int, guest_id: int, booking_id: int,
                     rating: int, comment: str) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO reviews (property_id, guest_id, booking_id, rating, comment)
                VALUES (?, ?, ?, ?, ?)
            """, (property_id, guest_id, booking_id, rating, comment))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error creating review: {e}")
            return False
    
    def get_property_reviews(self, property_id: int) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.*, u.first_name, u.last_name
            FROM reviews r
            JOIN users u ON r.guest_id = u.id
            WHERE r.property_id = ?
            ORDER BY r.created_at DESC
        """, (property_id,))
        
        reviews = cursor.fetchall()
        conn.close()
        
        result = []
        for review in reviews:
            result.append({
                'id': review[0],
                'rating': review[4],
                'comment': review[5],
                'created_at': review[6],
                'guest_name': f"{review[7]} {review[8]}"
            })
        
        return result

def show_review_form(booking, review_manager):
    st.markdown(f"### Leave a Review for {booking['property_title']}")
    
    with st.form(f"review_form_{booking['id']}"):
        rating = st.select_slider("Rating", options=[1, 2, 3, 4, 5], value=5,
                                format_func=lambda x: "⭐" * x)
        
        comment = st.text_area("Your Review", placeholder="Share your experience...")
        
        submit_btn = st.form_submit_button("Submit Review", use_container_width=True)
        
        if submit_btn:
            if review_manager.create_review(
                booking['property_id'],
                st.session_state.user['id'],
                booking['id'],
                rating,
                comment
            ):
                st.success("Review submitted successfully!")
            else:
                st.error("Failed to submit review. Please try again.")
