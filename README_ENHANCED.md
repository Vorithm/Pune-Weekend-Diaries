# 🗓️ Pune Weekend Diaries

A comprehensive travel suggestion app with **extended destination types** that helps you discover amazing places around Pune for your weekend adventures! 

## ✨ Enhanced Features

- **🎯 Extended Categories**: 7 main categories with 40+ specific types
- **🏷️ Smart Filtering**: Filter by main category and specific subcategory
- **🎨 Beautiful UI**: Modern, responsive design with gradient cards and animations
- **🗺️ Interactive Map**: Visualize all destinations on an interactive map
- **🔐 Secret Travel Tips**: Get randomized local travel tips and secrets
- **📱 Mobile Friendly**: Works perfectly on all devices
- **⚡ Fast Performance**: Optimized data loading and caching
- **📊 Category Breakdown**: Visual statistics and insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd Pune_Weekend_Diaries
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the enhanced app**
   ```bash
   streamlit run app_enhanced.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, manually navigate to the URL

## 📁 Project Structure

```
Pune_Weekend_Diaries/
├── app_enhanced.py          # Main Streamlit application
├── flask_api.py            # Flask API backend
├── places.csv              # Original dataset (50 places)
├── places_extended.csv     # Enhanced dataset with categories
├── requirements.txt        # Python dependencies
├── README_ENHANCED.md      # This documentation
└── venv/                   # Virtual environment (created automatically)
```

## 🎮 How to Use

### 1. Welcome Message
The app opens with a friendly greeting: "Hey Ghumakkad! What's up? Ready to plan your next adventure? 🌍✨"

### 2. Enhanced Filtering
Use the sidebar to select:
- **🏷️ Main Categories**: Choose from 7 broad categories
- **🎪 Specific Types**: Filter by detailed subcategories
- **📏 Distance Filter**: Set maximum distance from Pune
- **👻 Spooky Preference**: Filter for spooky or non-spooky places

### 3. Explore Places
Each destination is displayed in a beautiful card showing:
- 📍 Name and Category (with icons)
- 🎪 Subcategory type
- 📖 Description and Location
- 📅 Best time to visit
- 🧠 Interesting facts
- ⚠️ Rules and guidelines
- 👻 Spooky status
- 📏 Distance from Pune
- 🗺️ Clickable map link

### 4. Interactive Map
All filtered destinations are displayed on an interactive map using coordinates.

### 5. Secret Tips
Click the buttons to get randomized travel tips from Ghumakkad! 🔐

## 🏷️ Extended Destination Categories

### 🏞️ Nature & Outdoors
- **Mountains**: Hill stations, viewpoints, trekking spots
- **Trekking**: Adventure trails, hiking routes
- **Waterfalls**: Natural falls, monsoon attractions
- **Lakes**: Serene water bodies, birdwatching spots
- **Forests**: Wildlife sanctuaries, nature trails
- **Caves**: Ancient caves, rock formations

### 🛕 Spiritual & Cultural
- **Temples**: Ancient temples, religious sites
- **Mosques**: Islamic heritage, architectural marvels
- **Churches**: Christian heritage, colonial architecture
- **Monasteries**: Buddhist monasteries, meditation centers
- **Ashrams**: Spiritual retreats, yoga centers
- **Heritage Sites**: Historical monuments, cultural landmarks
- **Historical Forts**: Ancient forts, military heritage
- **Ancient Ruins**: Archaeological sites, historical remains
- **Cultural Villages**: Traditional settlements, folk culture
- **Art Galleries**: Contemporary art, cultural exhibitions
- **Museums**: Historical artifacts, cultural collections

### 🏖️ Relaxation & Leisure
- **Beaches**: Coastal destinations, water activities
- **Backwaters**: Serene waterways, boat rides
- **Hot Springs**: Natural thermal springs, wellness spots
- **Hill Stations**: Mountain retreats, cool climate
- **Resorts**: Luxury accommodations, spa retreats
- **Botanical Gardens**: Plant collections, nature walks
- **Sunset/Sunrise Points**: Scenic viewpoints, photography spots
- **Scenic Drives**: Beautiful road routes, driving experiences

### 🛍️ Urban & Fun
- **Shopping Streets**: Retail districts, local markets
- **Flea Markets**: Antique shops, vintage finds
- **Food Streets**: Culinary destinations, street food
- **Amusement Parks**: Entertainment venues, family fun
- **Nightlife Spots**: Bars, clubs, entertainment districts
- **Cafés & Rooftop Lounges**: Dining experiences, city views
- **Street Art Locations**: Murals, public art installations
- **Local Festivals**: Cultural celebrations, seasonal events

### 🧗 Adventure & Activities
- **Adventure Parks**: Thrill rides, outdoor activities
- **Ziplining**: Aerial adventures, canopy tours
- **Rock Climbing Areas**: Climbing spots, bouldering
- **Paragliding Points**: Aerial sports, scenic flights
- **Scuba Diving Spots**: Underwater exploration, marine life
- **Rafting Sites**: River adventures, water sports
- **Camping Sites**: Outdoor camping, stargazing
- **Star-Gazing Spots**: Astronomy sites, night sky viewing

### 👻 Offbeat & Mystery
- **Haunted Places**: Paranormal locations, ghost stories
- **Abandoned Villages**: Deserted settlements, urban exploration
- **Spooky Forest Trails**: Eerie paths, mysterious woods
- **Underground Temples**: Hidden shrines, secret passages
- **Mythical Spots**: Legendary locations, folklore sites
- **UFO Sightings/Legends**: Extraterrestrial stories, mysterious phenomena

### 📸 Instagrammable / Photo Spots
- **Viewpoints**: Scenic overlooks, panoramic vistas
- **Iconic Landmarks**: Famous monuments, recognizable sites
- **Colorful Streets**: Vibrant neighborhoods, artistic areas
- **Unique Architecture**: Modern buildings, design marvels
- **Art Installations**: Public sculptures, creative displays

## 📊 Data Structure

The enhanced app uses `places_extended.csv` with the following columns:
- `id`: Unique identifier
- `name`: Place name
- `category`: Main category (7 broad types)
- `subcategory`: Specific type (40+ detailed types)
- `description`: Detailed description
- `location`: Address/area
- `coordinates`: Latitude and longitude
- `facts`: Interesting facts
- `rules`: Guidelines for visitors
- `spooky`: Whether the place is considered spooky
- `distance_from_pune_km`: Distance from Pune
- `best_time_to_visit`: Recommended visiting time
- `map_link`: Google Maps link

## 🎨 Customization

### Adding New Places
1. Edit `places_extended.csv` to add new destinations
2. Follow the existing data format
3. Use appropriate category and subcategory from the extended list
4. Ensure coordinates are in `[lat, lon]` format
5. Restart the app to see changes

### Modifying Secret Tips
Edit the `SECRET_TIPS` list in `app_enhanced.py` to add your own travel tips!

### Styling
The app uses custom CSS for beautiful styling. You can modify the styles in the `<style>` section of the app.

## 🛠️ Technical Details

- **Framework**: Streamlit
- **Data Processing**: Pandas
- **Mapping**: Streamlit's built-in map component
- **Styling**: Custom CSS with gradients and animations
- **Caching**: Streamlit's `@st.cache_data` for performance
- **Categories**: 7 main categories with 40+ subcategories

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   streamlit run app_enhanced.py --server.port 8502
   ```

2. **Missing dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **CSV file not found**
   - Ensure `places_extended.csv` is in the same directory as `app_enhanced.py`

4. **Map not displaying**
   - Check that coordinates are in correct format `[lat, lon]`
   - Ensure internet connection for map tiles

## 📈 Enhanced Statistics

The enhanced app provides:
- **50+ destinations** with extended categorization
- **7 main categories** for broad filtering
- **40+ subcategories** for detailed filtering
- **Category breakdown** with visual statistics
- **Distance analysis** and spooky place counts
- **Interactive filtering** by multiple criteria

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new destinations to the CSV file
- Suggesting new categories or subcategories
- Improving the UI/UX
- Adding new features
- Fixing bugs
- Adding more secret travel tips

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Thanks to all the local travelers who shared their experiences
- Inspired by the spirit of exploration and adventure
- Enhanced with extended destination types for better discovery
- Built with ❤️ for the travel community

---

**Happy Exploring! 🌍✨**

*Made with ❤️ by Ghumakkad's Enhanced Travel Guide* 