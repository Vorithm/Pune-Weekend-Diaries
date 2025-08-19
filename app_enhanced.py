import streamlit as st
import pandas as pd
import ast
import random
from datetime import datetime
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Pune Weekend Diaries",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HELPER FUNCTION TO ENCODE IMAGE ---
def img_to_base64(img_path):
    try:
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded
    except FileNotFoundError:
        return None

# --- DATA LOADER WITH TYPE SANITIZATION ---
@st.cache_data
def load_data():
    # Try reading main CSV, fallback to alternate
    try:
        df = pd.read_csv('places_expand.csv')
    except FileNotFoundError:
        df = pd.read_csv('places.csv', encoding='ISO-8859-1')
        if 'subcategory' not in df.columns and 'category' in df.columns:
            df['subcategory'] = df['category']

    # Standardize column names (strip spaces)
    df.columns = [c.strip() for c in df.columns]

    # Ensure required columns exist
    required_cols = [
        'place_name', 'category', 'subcategory', 'description', 'location',
        'best_time_to_visit', 'facts', 'rules', 'spooky',
        'distance_from_pune_km', 'id', 'map_link'
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = pd.NA

    # Coerce distance to numeric (extract numeric part if values like '25 km')
    df['distance_from_pune_km'] = (
        pd.to_numeric(
            df['distance_from_pune_km']
            .astype(str)
            .str.extract(r'([0-9]*\.?[0-9]+)', expand=False),
            errors='coerce'
        )
        .astype(float)
    )

    # Normalize spooky to boolean
    df['spooky'] = (
        df['spooky']
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(['true', '1', 'yes', 'y'])
    )

    # Fill text columns to avoid NaN issues in .str.contains
    text_cols = [
        'best_time_to_visit', 'category', 'subcategory', 'description',
        'location', 'facts', 'rules', 'place_name', 'map_link'
    ]
    for c in text_cols:
        df[c] = df[c].fillna('')

    # Ensure id is present and usable
    if 'id' in df.columns and df['id'].notna().any():
        df['id'] = df['id'].astype(str).fillna('')
    else:
        df['id'] = (df['place_name'].fillna('').str[:20] + '_' + df.index.astype(str))

    return df

# Category Icons
CATEGORY_ICONS = {
    "Nature & Outdoors": "🏞️",
    "Spiritual & Cultural": "🛕",
    "Relaxation & Leisure": "🏖️",
    "Urban & Fun": "🛍️",
    "Adventure & Activities": "🧗",
    "Offbeat & Mystery": "👻",
    "Instagrammable / Photo Spots": "📸"
}

# Secret Tips
SECRET_TIPS = [
    "🔐 Secret Tip of the Week: If you're visiting a temple early morning, carry a small packet of sweets—some locals say it brings you unexpected blessings! 😉🍬",
    "🔐 Secret Tip of the Week: Always carry a small mirror when visiting forts—locals believe it helps ward off negative energy! ✨🪞",
    "🔐 Secret Tip of the Week: Visit lakes during sunrise with a cup of chai—the combination of mist and morning light creates magical moments! ☕🌅",
    "🔐 Secret Tip of the Week: For scary roads, play local folk music in your car—it's said to keep spirits at bay! 🎵👻",
    "🔐 Secret Tip of the Week: Carry a small bell when trekking—the sound helps you stay connected with your group in dense forests! 🔔🌲",
    "🔐 Secret Tip of the Week: Visit gardens on weekdays for the most peaceful experience—weekends can get crowded! 🌸📅",
    "🔐 Secret Tip of the Week: For mysterious places, visit during full moon—the atmosphere becomes even more enchanting! 🌕✨",
    "🔐 Secret Tip of the Week: Always greet the local deity before starting your journey—it's considered auspicious! 🙏🕉️",
    "🔐 Secret Tip of the Week: For adventure spots, visit during monsoon for the most thrilling experience! 🌧️🏔️",
    "🔐 Secret Tip of the Week: For urban spots, visit during festivals for the most vibrant atmosphere! 🎉🏙️"
]

# Weekend Picks
def get_weekend_picks(df, num_picks=3):
    # NaN-safe contains and distance handling
    weekend_places = df[
        (df['best_time_to_visit'].str.contains('Anytime', case=False, na=False)) |
        (df['best_time_to_visit'].str.contains('Evening', case=False, na=False)) |
        (df['best_time_to_visit'].str.contains('Sunset', case=False, na=False)) |
        (df['distance_from_pune_km'].fillna(float('inf')) <= 30)
    ]
    if len(weekend_places) >= num_picks:
        return weekend_places.sample(n=num_picks, random_state=random.randint(0, 10_000))
    # Fallback to any places with valid numeric distance first, else any
    fallback = df.dropna(subset=['distance_from_pune_km'])
    if len(fallback) >= num_picks:
        return fallback.sample(n=num_picks, random_state=random.randint(0, 10_000))
    return df.sample(n=min(num_picks, len(df)), random_state=random.randint(0, 10_000))

# Display Card
def display_place_card(place, card_id):
    with st.container():
        st.markdown(f"### 📍 {place['place_name']}")
        icon = CATEGORY_ICONS.get(place['category'], '🏷️')
        st.markdown(f"**{icon} {place['category']}** • **{place['subcategory']}**")

        col1, col2 = st.columns([2, 1])
        with col1:
            if str(place.get('description', '')).strip():
                st.markdown(f"**📖 Description:** {place['description']}")
            if str(place.get('location', '')).strip():
                st.markdown(f"**🌐 Location:** {place['location']}")
            if str(place.get('best_time_to_visit', '')).strip():
                st.markdown(f"**📅 Best time to visit:** {place['best_time_to_visit']}")
            if str(place.get('facts', '')).strip():
                st.markdown(f"**🧠 Interesting Fact:** {place['facts']}")
            if str(place.get('rules', '')).strip():
                st.markdown(f"**⚠️ Rules:** {place['rules']}")
        with col2:
            spooky_status = "Yes 👻" if bool(place['spooky']) else "No 😊"
            st.markdown(f"**👻 Spooky?** {spooky_status}")
            dist_val = place.get('distance_from_pune_km')
            if pd.notna(dist_val):
                st.markdown(f"**📏 Distance:** {float(dist_val):.1f} km")
            else:
                st.markdown(f"**📏 Distance:** —")
            st.markdown(f"**🆔 ID:** {place['id']}")

            map_link = place.get('map_link')
            if isinstance(map_link, str) and map_link.strip():
                st.markdown(
                    f'<a href="{map_link}" target="_blank" style="text-decoration:none;">'
                    f'<button style="padding: 0.5em 1em;">🗺️ View on Map</button></a>',
                    unsafe_allow_html=True
                )
        st.markdown("---")

# Main App
def main():
    st.title("🗓️ Pune Weekend Diaries✨")
    st.markdown("### Hey Weekend Warrior! 🌍✨")
    st.markdown("Ready to discover amazing places around Pune for your next adventure?")

    df = load_data()

    # --- Sidebar ---
    # Image at top
    img_base64 = img_to_base64("Img.jpg")
    if img_base64:
        st.sidebar.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/jpg;base64,{img_base64}" alt="Pune Hidden Gem" style="width: 100%; object-fit: cover; border-radius: 10px;">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.sidebar.warning("Image 'Img.jpg' not found.")

    st.sidebar.markdown("## 🧭 Pick Your Vibe")

    categories = sorted([c for c in df['category'].dropna().unique()])
    st.sidebar.markdown("### 🏷️ Main Categories")
    selected_categories = st.sidebar.multiselect(
        "Select destination categories:",
        categories,
        help="Choose one or more main categories you're interested in!"
    )

    if selected_categories:
        filtered_df_for_sub = df[df['category'].isin(selected_categories)]
        subcategories = sorted([s for s in filtered_df_for_sub['subcategory'].dropna().unique()])
        st.sidebar.markdown("### 🎪 Specific Types")
        selected_subcategories = st.sidebar.multiselect(
            "Select specific types (optional):",
            subcategories,
            help="Filter by specific types within selected categories"
        )
    else:
        selected_subcategories = []

    # Distance slider guard
    max_distance_available = df['distance_from_pune_km'].dropna()
    if not max_distance_available.empty:
        max_dist_val = int(max_distance_available.max())
        default_max = max_dist_val
    else:
        max_dist_val = 100
        default_max = 100

    st.sidebar.markdown("## 📏 Distance from Pune")
    max_distance = st.sidebar.slider(
        "Maximum distance (km):",
        min_value=0,
        max_value=max_dist_val if max_dist_val > 0 else 100,
        value=default_max if default_max > 0 else 100,
        step=5
    )

    spooky_preference = st.sidebar.selectbox(
        "👻 Spooky preference:",
        ["All places", "Only spooky places", "Only non-spooky places"]
    )

    # --- Main Filtering Logic ---
    if selected_categories:
        filtered_df = df[df['category'].isin(selected_categories)]
        if selected_subcategories:
            filtered_df = filtered_df[filtered_df['subcategory'].isin(selected_subcategories)]
        # Distance filter (NaN-safe by filling NaN with inf so they get excluded)
        filtered_df = filtered_df[filtered_df['distance_from_pune_km'].fillna(float('inf')) <= float(max_distance)]

        if spooky_preference == "Only spooky places":
            filtered_df = filtered_df[filtered_df['spooky'] == True]
        elif spooky_preference == "Only non-spooky places":
            filtered_df = filtered_df[filtered_df['spooky'] == False]

        if len(filtered_df) > 0:
            st.markdown(f"## 🎉 Found {len(filtered_df)} amazing places for you!")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Places", len(filtered_df))
            with col2:
                spooky_count = int(filtered_df['spooky'].sum())
                st.metric("Spooky Places", spooky_count)
            with col3:
                if filtered_df['distance_from_pune_km'].notna().any():
                    avg_distance = filtered_df['distance_from_pune_km'].mean()
                    st.metric("Avg Distance", f"{avg_distance:.1f} km")
                else:
                    st.metric("Avg Distance", "—")
            with col4:
                if filtered_df['distance_from_pune_km'].notna().any():
                    max_dist = filtered_df['distance_from_pune_km'].max()
                    st.metric("Max Distance", f"{max_dist:.1f} km")
                else:
                    st.metric("Max Distance", "—")

            st.markdown("## 📊 Category Breakdown")
            category_counts = filtered_df['category'].value_counts()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Main Categories:**")
                for category, count in category_counts.items():
                    icon = CATEGORY_ICONS.get(category, '🏷️')
                    st.markdown(f"• {icon} {category}: {count} places")
            with col2:
                st.markdown("**Top Subcategories:**")
                subcategory_counts = filtered_df['subcategory'].value_counts().head(10)
                for subcategory, count in subcategory_counts.items():
                    st.markdown(f"• {subcategory}: {count} places")

            st.markdown("---")
            for idx, place in filtered_df.iterrows():
                display_place_card(place, f"filtered_{idx}")

        else:
            st.warning("🤔 No places found with your current filters. Try adjusting your preferences in the sidebar!")
    else:
        st.info("📌 Please select at least one category to begin exploring!")

    # --- Weekend Picks ---
    st.markdown("## 🗓️ This Weekend's Picks")
    with st.container():
        st.info("🎯 **Curated Just For You** - Here are perfect destinations for your weekend adventure!")
    weekend_picks = get_weekend_picks(df)
    for idx, place in weekend_picks.iterrows():
        display_place_card(place, f"weekend_{idx}")

    # --- Surprise Me Button ---
    st.markdown("## 🎁 Feeling Lucky?")
    st.markdown("Click below and discover a hidden gem you didn’t expect!")
    if st.button("🎉 Surprise Me!"):
        if len(df) > 0:
            surprise = df.sample(1, random_state=random.randint(0, 10_000)).iloc[0]
            display_place_card(surprise, "surprise_card")
        else:
            st.warning("No data available to surprise! Please check your CSV.")

    # --- Diary Entries (placeholder) ---
    st.markdown("## 📓 Your Diary Entries")
    with st.container():
        st.info("📝 **Coming Soon!** Save your favorite places, add personal notes, and track your adventures!")

    # --- Secret Tips ---
    st.markdown("## 🔐 Secret Tip of the Week")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Get This Week's Secret Tip!", key="secret_tip"):
            st.success(random.choice(SECRET_TIPS))
    with col2:
        if st.button("🎲 Get Another Secret Tip!", key="another_tip"):
            st.success(random.choice(SECRET_TIPS))

    st.markdown("---")
    st.markdown("🗓️ Made with ❤️ by Pune Weekend Diaries | Happy Exploring! ✨")
    st.markdown(f"Last updated: {datetime.now().strftime('%B %d, %Y')}")

if __name__ == "__main__":
    main()
