# Airbnb x Oikas

Single-file Streamlit app that lets users browse properties, view details, book with a simple checkout, host new listings, and see a dashboard — all with a pitch-black backdrop and sky blue / bright red theme.

## Features

### 🔐 User Authentication
- User registration and login
- Secure password hashing
- Session management

### 🏡 Property Management
- Property listing creation for hosts
- Advanced search and filtering
- Property details with images and amenities
- Host information and ratings

### 📅 Booking System
- Date selection with availability checking
- Guest count validation
- Price calculation
- Booking confirmation and management

### ⭐ Review System
- Guest reviews and ratings
- Property rating aggregation
- Review display on property listings

### 📊 Dashboard & Analytics
- User booking history
- Spending analytics
- Booking timeline visualization
- Metrics and statistics

## Run locally

```bash
pip install -r requirements.txt
streamlit run "Airbnb x Oikas.py"
```

Open: http://localhost:8501

## Usage

1. **Sign Up/Login**: Create an account or login with existing credentials
2. **Browse Properties**: Search and filter properties by location, price, and guest count
3. **Make Bookings**: Select dates and book your perfect stay
4. **Host Properties**: List your own properties for rent
5. **Manage Bookings**: View and manage your booking history
6. **Leave Reviews**: Rate and review properties after your stay
7. **View Dashboard**: Track your booking analytics and spending

## Sample Data

The application comes pre-loaded with sample properties and users for demonstration:

- **Sample Users**: john_host, sarah_host, mike_host (password: password123)
- **Sample Properties**: Various properties in New York, Miami, Aspen, San Francisco, and Boston

## File structure

- `Airbnb x Oikas.py` — the entire app in one file
- `oikos_debug.db` — SQLite database (auto-created)

## Technologies Used

- **Streamlit** - Web application framework
- **SQLite** - Database for data persistence
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive charts and visualizations
- **Python** - Backend logic and data processing

## Features Highlights

### Beautiful UI/UX
- Modern, responsive design
- Airbnb-inspired color scheme and layout
- Interactive components and smooth navigation
- Mobile-friendly interface

### Robust Backend
- SQLite database with proper relationships
- Data validation and error handling
- Secure authentication with password hashing
- Efficient query optimization

### Real-time Features
- Live availability checking
- Dynamic price calculation
- Instant booking confirmation
- Real-time search and filtering

Enjoy using Oikos for your property rental needs! 🏠✨
