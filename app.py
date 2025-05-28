import pandas as pd
import streamlit as st
import os

image_folder = r"C:\zoya_profiles\static\images"

def get_local_image_path(image_code):
    filename = image_code + ".png" if not image_code.lower().endswith(".png") else image_code
    full_path = os.path.join(image_folder, filename)
    return full_path

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_excel("cleaned_data.xlsx")
image_df = pd.read_excel("image_links.xlsx")

df_limited = df.copy()

# ----------------------------
# STREAMLIT STYLING
# ----------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&display=swap');
        html, body, .main, .stApp {
            background-color: #fdf6ef !important;
            font-family: 'Cormorant Garamond', serif !important;
            color: #6B4226 !important;
        }
        .homepage-title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: #6B4226;
            margin-top: 50px;
        }
        .stButton > button {
            background-color: #6B4226;
            color: white;
            border-radius: 8px;
            font-family: 'Cormorant Garamond', serif;
        }
        .stButton > button:hover {
            background-color: #a97142;
            color: white;
        }
        .stSelectbox > div {
            background-color: #fff6e9;
            border: 1px solid #6B4226;
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# SESSION STATE
# ----------------------------
if "profile_loaded" not in st.session_state:
    st.session_state.profile_loaded = False

# ----------------------------
# UI - CUSTOMER SELECTION
# ----------------------------
if not st.session_state.profile_loaded:
    st.markdown("<div class='homepage-title'>Select a Customer ID to view their personalized one-pager</div>", unsafe_allow_html=True)
    customer_ids = df_limited['Customer ID'].astype(str).tolist()
    customer_id = st.selectbox("Select Customer ID:", customer_ids)

    if st.button("Load Profile"):
        st.session_state.profile_loaded = True
        st.session_state.customer_id = customer_id
        st.rerun()

# ----------------------------
# DISPLAY PROFILE
# ----------------------------
else:
    customer_id = st.session_state.customer_id
    customer_data = df_limited[df_limited['Customer ID'] == int(customer_id)].iloc[0]

    st.markdown(f"<h2 style='text-align:center;'><strong>Customer Profile</strong></h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align:center;'><strong>Customer ID: {customer_id}</strong></h4>", unsafe_allow_html=True)

    # Demographics
    st.markdown("### 👤 Demographics")
    st.markdown(f"""
    **Customer Name:** {customer_data['Customer Name']}  
    **Age:** {int(customer_data['Age'])}  
    **Gender:** {customer_data['Gender']}  
    **Tier:** {customer_data['Tier']}  
    **Last purchase date:** {customer_data['Last purchase date'].date()}  
    **Average spend:** ₹{customer_data['Average spend']:,}
    """)

    # Purchase history
    st.markdown("### 🛍️ Purchase History")
    st.markdown(f"""
        **Preference:** {customer_data['Preference']}  
        **Favourite Product Categories:** {customer_data['Favourite Product Categories']}  
        **Favourite collections:** {customer_data['Favourite collections']}
    """)

    # Pitch timing
    st.markdown("### 🗓️ When to Pitch?")
    st.markdown(f"""
        **Birthday:** {customer_data['Birthday']}  
        **Anniversary:** {customer_data['Anniversary']}  
        **Spouse birthday:** {customer_data['Spouse Birthday']}  
        **Preferred Quarter of Purchase:** {customer_data['Preferred Quarter of Purchase']}
    """)

    # Persona
    st.markdown("### 🧠 Persona")
    # Note: removed trailing space in key
    if 'Customer description' in customer_data.index and pd.notna(customer_data['Customer description']):
        st.markdown(customer_data['Customer description'])
    else:
        st.markdown("*No customer description available.*")

    # ----------------------------
    # STYLE INSPIRATION IMAGES
    # ----------------------------
    st.markdown("### 🎨 Style Inspirations")

    image_codes = [
        customer_data.get('itemcode_1'),
        customer_data.get('itemcode_2'),
        customer_data.get('itemcode_3'),
    ]

    # Filter and clean codes
    valid_image_codes = [code.strip() for code in image_codes if pd.notna(code)]

    if valid_image_codes:
        cols = st.columns(len(valid_image_codes))
        for col, code in zip(cols, valid_image_codes):
            with col:
                local_path = get_local_image_path(code)
                if os.path.exists(local_path):
                    st.image(local_path, use_container_width=True, caption=code)
                else:
                    st.warning(f"Image not found for: {code}")
    else:
        st.warning("No style inspiration images available for this customer.")
