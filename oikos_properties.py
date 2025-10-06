# Oikos Property Management
import streamlit as st
import json
from typing import Dict, List, Optional

class PropertyManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_property(self, host_id: int, title: str, description: str,
                       property_type: str, city: str, country: str, address: str,
                       price_per_night: float, max_guests: int, bedrooms: int,
                       bathrooms: int, amenities: List[str], image_url: str = None) -> bool:
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            amenities_json = json.dumps(amenities)
            
            cursor.execute("""
                INSERT INTO properties (host_id, title, description, property_type,
                                      city, country, address, price_per_night, max_guests,
                                      bedrooms, bathrooms, amenities, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (host_id, title, description, property_type, city, country,
                  address, price_per_night, max_guests, bedrooms, bathrooms,
                  amenities_json, image_url))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error creating property: {e}")
            return False
    
    def get_properties(self, city: str = None, max_price: float = None,
                      min_guests: int = None) -> List[Dict]:
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT p.id, p.host_id, p.title, p.description, p.property_type, 
                   p.city, p.country, p.address, p.price_per_night, p.max_guests,
                   p.bedrooms, p.bathrooms, p.amenities, p.image_url, p.created_at, p.is_available,
                   u.first_name, u.last_name,
                   COALESCE(AVG(CAST(r.rating AS REAL)), 0) as avg_rating,
                   COUNT(r.id) as review_count
            FROM properties p
            JOIN users u ON p.host_id = u.id
            LEFT JOIN reviews r ON p.id = r.property_id
            WHERE p.is_available = TRUE
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
        
        query += " GROUP BY p.id ORDER BY p.created_at DESC"
        
        cursor.execute(query, params)
        properties = cursor.fetchall()
        conn.close()
        
        result = []
        for prop in properties:
            amenities = json.loads(prop[12]) if prop[12] else []
            result.append({
                'id': prop[0],
                'host_id': prop[1],
                'title': prop[2],
                'description': prop[3],
                'property_type': prop[4],
                'city': prop[5],
                'country': prop[6],
                'address': prop[7],
                'price_per_night': prop[8],
                'max_guests': prop[9],
                'bedrooms': prop[10],
                'bathrooms': prop[11],
                'amenities': amenities,
                'image_url': prop[13],
                'host_name': f"{prop[16]} {prop[17]}",
                'avg_rating': round(float(prop[18]), 1) if prop[18] else 0,
                'review_count': prop[19]
            })
        
        return result
    
    def get_property_by_id(self, property_id: int) -> Optional[Dict]:
        properties = self.get_properties()
        for prop in properties:
            if prop['id'] == property_id:
                return prop
        return None

def show_property_listings(property_manager, booking_manager, review_manager):
    # Enhanced Hero Section with Search
    st.markdown("""
    <div class="hero-section" style="animation: fadeInUp 1.2s ease-out;">
        <div class="hero-title" style="animation: bounceIn 1.5s ease-out;">Find Your Perfect Stay</div>
        <div class="hero-subtitle" style="animation: slideInLeft 1s ease-out 0.5s both;">Discover unique accommodations in the world's most amazing destinations</div>
        <div style="display: flex; justify-content: center; gap: 3rem; margin-top: 3rem; animation: fadeInUp 1s ease-out 1s both;">
            <div style="text-align: center; animation: bounceIn 0.8s ease-out 1.2s both;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🌍</div>
                <div style="font-size: 1rem; opacity: 0.9; font-weight: 500;">Global Destinations</div>
            </div>
            <div style="text-align: center; animation: bounceIn 0.8s ease-out 1.4s both;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">⭐</div>
                <div style="font-size: 1rem; opacity: 0.9; font-weight: 500;">Premium Quality</div>
            </div>
            <div style="text-align: center; animation: bounceIn 0.8s ease-out 1.6s both;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🔒</div>
                <div style="font-size: 1rem; opacity: 0.9; font-weight: 500;">Secure Booking</div>
            </div>
            <div style="text-align: center; animation: bounceIn 0.8s ease-out 1.8s both;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">💎</div>
                <div style="font-size: 1rem; opacity: 0.9; font-weight: 500;">Luxury Experience</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced Search Container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        city_filter = st.text_input("", placeholder="🌍 Where are you going?", key="city_search")
    
    with col2:
        max_price = st.number_input("", min_value=0, value=1000, step=50, 
                                  help="💰 Maximum price per night", key="price_search")
    
    with col3:
        min_guests = st.number_input("", min_value=1, value=1, step=1,
                                   help="👥 Number of guests", key="guests_search")
    
    with col4:
        search_btn = st.button("🔍 Search Properties", use_container_width=True, key="search_btn")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get properties based on filters
    properties = property_manager.get_properties(
        city=city_filter if city_filter else None,
        max_price=max_price,
        min_guests=min_guests
    )
    
    if not properties:
        st.info("No properties found matching your criteria. Try adjusting your filters.")
        return
    
    # Display properties with professional cards
    st.markdown("### Featured Properties")
    
    for i in range(0, len(properties), 3):
        cols = st.columns(3)
        
        for j, col in enumerate(cols):
            if i + j < len(properties):
                prop = properties[i + j]
                
                with col:
                    # Create professional property card
                    card_html = f"""
                    <div class="property-card">
                        <div class="property-image">
                            <img src="{prop['image_url'] if prop['image_url'] else 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400'}" 
                                 alt="{prop['title']}" />
                        </div>
                        <div class="property-content">
                            <div class="property-title">{prop['title']}</div>
                            <div class="property-location">📍 {prop['city']}, {prop['country']}</div>
                            <div class="property-details">
                                <span>🏠 {prop['property_type']}</span>
                                <span>🛏️ {prop['bedrooms']} bed</span>
                                <span>🚿 {prop['bathrooms']} bath</span>
                            </div>
                            <div class="property-rating">
                                <span class="rating-stars">{'⭐' * int(prop['avg_rating']) if prop['avg_rating'] > 0 else '⭐'}</span>
                                <span class="rating-text">{prop['avg_rating'] if prop['avg_rating'] > 0 else 'New'} ({prop['review_count']} reviews)</span>
                            </div>
                            <div class="property-footer">
                                <div>
                                    <span class="price-tag">${prop['price_per_night']:.0f}</span>
                                    <span class="price-night"> / night</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """
                    
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Book button
                    if st.button(f"Book Now", key=f"book_{prop['id']}", use_container_width=True):
                        st.session_state.selected_property = prop
                        st.session_state.show_booking = True
                    
                    # Amenities tags
                    if prop['amenities']:
                        amenities_html = ""
                        for amenity in prop['amenities'][:4]:
                            amenities_html += f'<span class="amenity-tag">{amenity}</span>'
                        if len(prop['amenities']) > 4:
                            amenities_html += f'<span class="amenity-tag">+{len(prop["amenities"]) - 4} more</span>'
                        st.markdown(amenities_html, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)

def show_host_property(property_manager):
    st.markdown('<h1 class="main-header">🏡 Host Your Property</h1>', unsafe_allow_html=True)
    
    with st.form("host_property_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Property Title*", placeholder="Beautiful apartment in downtown")
            property_type = st.selectbox("Property Type*", 
                                       ["Apartment", "House", "Condo", "Villa", "Studio", "Other"])
            city = st.text_input("City*")
            country = st.text_input("Country*")
            address = st.text_area("Full Address*")
        
        with col2:
            price_per_night = st.number_input("Price per Night ($)*", min_value=1.0, step=1.0)
            max_guests = st.number_input("Maximum Guests*", min_value=1, step=1)
            bedrooms = st.number_input("Bedrooms*", min_value=0, step=1)
            bathrooms = st.number_input("Bathrooms*", min_value=1, step=1)
            image_url = st.text_input("Image URL (Optional)", 
                                    placeholder="https://example.com/image.jpg")
        
        description = st.text_area("Description*", 
                                 placeholder="Describe your property, its features, and what makes it special...")
        
        # Amenities
        st.markdown("### Amenities")
        amenity_cols = st.columns(4)
        
        amenities = []
        amenity_options = [
            "WiFi", "Kitchen", "Parking", "Pool", "Gym", "Air Conditioning",
            "Heating", "TV", "Washer", "Dryer", "Balcony", "Garden"
        ]
        
        for i, amenity in enumerate(amenity_options):
            with amenity_cols[i % 4]:
                if st.checkbox(amenity):
                    amenities.append(amenity)
        
        submit_btn = st.form_submit_button("List Property", use_container_width=True)
        
        if submit_btn:
            required_fields = [title, property_type, city, country, address, price_per_night, description]
            
            if all(required_fields):
                if property_manager.create_property(
                    st.session_state.user['id'],
                    title, description, property_type, city, country, address,
                    price_per_night, max_guests, bedrooms, bathrooms,
                    amenities, image_url
                ):
                    st.success("Property listed successfully!")
                else:
                    st.error("Failed to list property. Please try again.")
            else:
                st.error("Please fill in all required fields marked with *")
