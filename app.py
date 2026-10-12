import streamlit as st

st.set_page_config(page_title="Stars and Moons", page_icon="⭐", layout="centered")

# تخصيص المظهر بألوان ليلية جميلة
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
st.markdown("<p style='text-align: center; color: #94a3b8;'>مشروع لعبة تخمين الأرقام - المرحلة الثانية</p>", unsafe_allow_html=True)

# عرض القائمة الرئيسية كما في الكتاب
st.code("""Welcome to Stars and Moons
1. Instructions
2. Start Game
3. Exit""", language="text")

# إدخال الخيار من المستخدم
option = st.text_input("Please select an option (1, 2, 3):", placeholder="اكتب رقم خيارك هنا...").strip()

if st.button("تأكيد الخيار 🚀", type="primary"):
    # 1. إذا أدخل اللاعب الرقم (1)
    if option == "1":
        st.info("📜 **شرح تعليمات اللعبة:**\n\nيقوم الحاسوب باختيار رقم سري، وعليك تخمين هذا الرقم بناءً على الإرشادات (أكبر أو أصغر / نجوم وأقمار) حتى تصل إلى الحل الصحيح!")
        
    # 2. إذا اختار الرقم (2) أو الرقم (3)
    elif option == "2" or option == "3":
        st.warning("⚠️ لم يتم تنفيذ هذه الخصيصة بعد")
        
    # 3. إذا أدخل أي خيار غير معروف
    else:
        st.error("❌ الخيار المُدخل غير معروف، أدخل 1 أو 2 أو 3")
