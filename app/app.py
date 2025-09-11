import streamlit as st
import joblib
import pandas as pd

# ---- Page Config ----
st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="wide")

# ---- Custom CSS ----
st.markdown(
    """
    <style>
    body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* Hero Image */
    .hero {
        width: 100%;
        border-radius: 18px;
        margin-bottom: 25px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
    }

    /* Title */
    h1 {
        font-weight: 700;
        text-align: center;
        font-size: 2.6rem;
        background: -webkit-linear-gradient(45deg, #ff9a9e, #fad0c4, #fad0c4, #fbc2eb, #a6c1ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 10px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #374151;
        margin-bottom: 30px;
    }

    /* Glass card for form */
    .stForm {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(10px);
        padding: 28px 32px;
        border-radius: 22px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    /* Buttons */
    .stForm button {
        background: linear-gradient(90deg, #36d1dc, #5b86e5);
        color: white;
        font-weight: 600;
        padding: 12px 22px;
        border-radius: 14px;
        border: none;
        transition: 0.3s ease-in-out;
    }
    .stForm button:hover {
        background: linear-gradient(90deg, #5b86e5, #36d1dc);
        transform: scale(1.04);
    }

    /* Success Card */
    .stSuccess {
        background: #f0fdf4 !important;
        border: 2px solid #34d399;
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        color: #065f46;
        margin-top: 20px;
    }

    /* Responsive */
    @media (max-width: 768px) {
        h1 { font-size: 2rem; }
        .subtitle { font-size: 1rem; }
        .stForm { padding: 18px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Hero Banner ----
st.image(
    "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=1600&q=80",
    use_container_width=True,
    caption="Smart Living, Smarter Pricing"
)

# ---- Title ----
st.markdown("<h1>🏠 House Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-powered insights to help you estimate your home's value instantly.</p>", unsafe_allow_html=True)

# ---- Load Model ----
model = joblib.load("../model.pkl")

# ---- Input Form ----
with st.form("predict"):
    col1, col2 = st.columns(2)
    with col1:
        rent = st.number_input("💰 Monthly Rent", value=15000, step=500)
        area = st.number_input("📏 Area (sqft)", value=1000, step=50)
        bedrooms = st.number_input("🛏 Bedrooms", value=2, min_value=0, max_value=10, step=1)
        bathrooms = st.number_input("🚿 Bathrooms", value=2, min_value=0, max_value=10, step=1)

    with col2:
        locality_list = [
            "BTM Layout", "Attibele", "K R Puram", "Marathahalli", "Indiranagar",
            "Electronic City", "Yalahanka", "Malleshwaram", "Jayanagar", "Missing"
        ]
        locality = st.selectbox("📍 Locality", locality_list, index=0)

        parking = st.selectbox("🚗 Parking", ["Bike", "Bike and Car", "Car", "Missing"], index=0)

        facinn = ["North", "South", "East", "West", "Missing"]
        facing = st.selectbox("🧭 Facing Direction", facinn, index=0)

    submitted = st.form_submit_button("🔮 Predict Price")

# ---- Prediction ----
if submitted:
    X = pd.DataFrame([{
        "rent": rent,
        "area": area,
        "locality": locality if locality else "Missing",
        "BHK": bedrooms,
        "parking": parking if parking else "Missing",
        "bathrooms": bathrooms,
        "facing": facing if facing else "Missing"
    }])

    pred = model.predict(X)[0]

    st.markdown("---")
    st.success(f"🎯 Predicted Price: ₹ {pred:,.2f}")
