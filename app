import streamlit as st
import random

st.set_page_config(page_title="Stars and Moons", page_icon="⭐", layout="centered")

st.markdown("""
    <style>
    .main {
        background: radial-gradient(circle at top, #1e293b, #0f172a, #020617);
        color: #f8fafc;
    }
    h1 {
        color: #fbbf24 !important;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⭐ Stars and Moons 🌙")
st.markdown("<p style='text-align: center; color: #94a3b8;'>خمّن الرقم السري بين 0 و 300</p>", unsafe_allow_html=True)

if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(0, 300)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []

def restart_game():
    st.session_state.secret_number = random.randint(0, 300)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []

guess = st.number_input("أدخل تخمينك:", min_value=0, max_value=300, step=1, disabled=st.session_state.game_over)

col1, col2 = st.columns(2)
with col1:
    submit = st.button("تحقق 🚀", type="primary", disabled=st.session_state.game_over)
with col2:
    reset = st.button("إعادة اللعب 🔄", on_click=restart_game)

if submit and not st.session_state.game_over:
    st.session_state.attempts += 1
    secret = st.session_state.secret_number

    if guess < secret:
        msg = f"محاولة {st.session_state.attempts}: الرقم [{guess}] ⬅ الرقم السري أكبر من ذلك ⬆️"
        st.info("الرقم السري أكبر من ذلك ⬆️")
        st.session_state.history.insert(0, msg)
    elif guess > secret:
        msg = f"محاولة {st.session_state.attempts}: الرقم [{guess}] ⬅ الرقم السري أصغر من ذلك ⬇️"
        st.warning("الرقم السري أصغر من ذلك ⬇️")
        st.session_state.history.insert(0, msg)
    else:
        st.session_state.game_over = True
        msg = f"🎉 تم الحل في المحاولة {st.session_state.attempts}! الرقم هو {guess}"
        st.session_state.history.insert(0, msg)
        st.success(f"🎉 مبروك! فزت باللعبة بعد {st.session_state.attempts} محاولات!")
        st.balloons()
        st.markdown("""
            <audio autoplay>
                <source src="https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3" type="audio/mpeg">
            </audio>
        """, unsafe_allow_html=True)

if st.session_state.history:
    st.write("---")
    st.subheader("📜 سجل المحاولات:")
    for item in st.session_state.history:
        st.write(item)
