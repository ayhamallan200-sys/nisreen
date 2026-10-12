import streamlit as st
import random

st.set_page_config(page_title="Stars & Moons - Game Hub", page_icon="🎮", layout="centered")

# تصميم الألوان والخلفية
st.markdown("""
    <style>
    .main {
        background: radial-gradient(circle at top, #1e293b, #0f172a, #020617);
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #fbbf24 !important;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
    }
    .score-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# بنك الكلمات والحيوانات
WORDS_BANK = ["كوكب", "مجرة", "صاروخ", "سفينة", "فضاء", "تلسكوب", "نيزك", "شمس"]
ANIMALS_BANK = [
    {"animal": "أسد", "clues": ["ملك الغابة", "له شعر كثيف حول رقبته (لبدة)", "يعيش في جماعات"]},
    {"animal": "فيل", "clues": ["أضخم حيوان يعيش على اليابسة", "له خرطوم طويل", "يمتلك أنياباً عاجية"]},
    {"animal": "زرافة", "clues": ["أطول حيوان في العالم", "رقبتها طويلة جداً", "جلدها مرقط"]},
    {"animal": "بطريق", "clues": ["طائر لا يطير", "سباح ماهر جداً", "يعيش في المناطق الجليدية"]}
]

# تهيئة الذاكرة
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'players' not in st.session_state:
    st.session_state.players = []
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'current_turn' not in st.session_state:
    st.session_state.current_turn = 0

# دوال مساعدة
def trigger_win_effects():
    st.balloons()
    st.components.v1.html("""
    <script>
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const notes = [
        { f: 330, d: 0.12 }, { f: 392, d: 0.12 }, { f: 659, d: 0.15 },
        { f: 523, d: 0.15 }, { f: 587, d: 0.15 }, { f: 784, d: 0.35 }
      ];
      let now = ctx.currentTime;
      notes.forEach(n => {
        let osc = ctx.createOscillator();
        let gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(n.f, now);
        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + n.d);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + n.d);
        now += n.d;
      });
    </script>
    """, height=0)

def next_turn():
    if st.session_state.players:
        st.session_state.current_turn = (st.session_state.current_turn + 1) % len(st.session_state.players)

# ----------------- 1. القائمة الرئيسية -----------------
if st.session_state.page == "menu":
    st.title("⭐ Stars and Moons 🌙")
    st.markdown("<p style='text-align: center; color: #94a3b8;'>منصة ألعاب التخمين والتحدي</p>", unsafe_allow_html=True)
    
    st.code("""1. Instructions (التعليمات)
2. Start Game (بدء اللعب)
3. Exit (خروج)""", language="text")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("1. التعليمات 📜"):
            st.session_state.page = "instructions"
            st.rerun()
    with col2:
        if st.button("2. بدء اللعب 🚀", type="primary"):
            st.session_state.page = "setup_players"
            st.rerun()
    with col3:
        if st.button("3. خروج 🚪"):
            st.session_state.page = "exit"
            st.rerun()

# ----------------- صفحة التعليمات -----------------
elif st.session_state.page == "instructions":
    st.title("📜 تعليمات الألعاب")
    st.markdown("""
    - **تخمين الأرقام:** يخمن اللاعب رقماً بين 0 و 300 مع إرشادات (أكبر / أصغر).
    - **تخمين الكلمة:** تظهر أحرف الكلمة مبعثرة والمطلوب معرفة الكلمة الصحيحة.
    - **تخمين الحيوان:** يُعطى اللاعب 3 تلميحات ذكية لمعرفة اسم الحيوان.
    - يدعم النظام اللعب الفردي أو الجماعي (حتى 3 لاعبين) مع لوحة نتائج تفاعلية!
    """)
    if st.button("⬅ العودة للقائمة"):
        st.session_state.page = "menu"
        st.rerun()

# ----------------- صفحة الخروج -----------------
elif st.session_state.page == "exit":
    st.title("👋 مع السلامة!")
    st.info("شكراً لتجربتك اللعبة. يمكنك العودة في أي وقت بالضغط بالأسفل.")
    if st.button("🔄 إعادة تشغيل القائمة"):
        st.session_state.page = "menu"
        st.rerun()

# ----------------- إعداد اللاعبين -----------------
elif st.session_state.page == "setup_players":
    st.title("👥 إعداد اللاعبين")
    num_players = st.radio("كم شخص سيلعب؟", [1, 2, 3], horizontal=True)

    names = []
    for i in range(num_players):
        name = st.text_input(f"اسم اللاعب {i+1}:", value=f"لاعب {i+1}", key=f"p_{i}")
        names.append(name.strip())

    if st.button("متابعة لاختيار اللعبة 🎮", type="primary"):
        st.session_state.players = names
        st.session_state.scores = {n: 0 for n in names}
        st.session_state.current_turn = 0
        st.session_state.page = "choose_game"
        st.rerun()

# ----------------- اختيار نوع اللعبة -----------------
elif st.session_state.page == "choose_game":
    st.title("🕹️ اختر لعبة التخمين")
    
    # عرض لوحة النتائج
    st.markdown("### 🏆 لوحة النتائج الحالية")
    cols = st.columns(len(st.session_state.players))
    for idx, (p, s) in enumerate(st.session_state.scores.items()):
        cols[idx].metric(label=p, value=f"{s} نقطة")
    st.write("---")

    g1, g2, g3 = st.columns(3)
    with g1:
        if st.button("🔢 تخمين الأرقام\n(0 - 300)"):
            st.session_state.secret_num = random.randint(0, 300)
            st.session_state.num_attempts = 0
            st.session_state.game_type = "numbers"
            st.session_state.page = "play"
            st.rerun()
    with g2:
        if st.button("🔤 تخمين الكلمة\n(المبعثرة)"):
            chosen = random.choice(WORDS_BANK)
            scrambled = list(chosen)
            random.shuffle(scrambled)
            st.session_state.secret_word = chosen
            st.session_state.scrambled_word = " - ".join(scrambled)
            st.session_state.game_type = "words"
            st.session_state.page = "play"
            st.rerun()
    with g3:
        if st.button("🦁 خمن الحيوان\n(بالتلميحات)"):
            chosen_animal = random.choice(ANIMALS_BANK)
            st.session_state.animal_data = chosen_animal
            st.session_state.game_type = "animals"
            st.session_state.page = "play"
            st.rerun()

# ----------------- ساحة اللعب -----------------
elif st.session_state.page == "play":
    current_player = st.session_state.players[st.session_state.current_turn]
    st.markdown(f"### 🎯 دور اللاعب: <span style='color:#38bdf8;'>{current_player}</span>", unsafe_allow_html=True)

    # 1. لعبة الأرقام
    if st.session_state.game_type == "numbers":
        st.subheader("🔢 خمّن الرقم السري (0 - 300)")
        guess = st.number_input("أدخل تخمينك:", min_value=0, max_value=300, step=1)
        if st.button("تحقق 🚀"):
            st.session_state.num_attempts += 1
            sec = st.session_state.secret_num
            if guess < sec:
                st.info("الرقم السري أكبر من ذلك ⬆️")
                next_turn()
            elif guess > sec:
                st.warning("الرقم السري أصغر من ذلك ⬇️")
                next_turn()
            else:
                st.success(f"🎉 أحسنت يا {current_player}! خمنت الرقم الصحيح ({sec})!")
                st.session_state.scores[current_player] += 10
                trigger_win_effects()
                st.balloons()
                if st.button("العودة لاختيار لعبة 🔄"):
                    st.session_state.page = "choose_game"
                    st.rerun()

    # 2. لعبة الكلمات
    elif st.session_state.game_type == "words":
        st.subheader("🔤 رتّب الحروف واكتشف الكلمة:")
        st.markdown(f"## ` {st.session_state.scrambled_word} `")
        word_guess = st.text_input("اكتب الكلمة الصحيحة:").strip()
        if st.button("إرسال الإجابة 🚀"):
            if word_guess == st.session_state.secret_word:
                st.success(f"🎉 بطل يا {current_player}! الكلمة صحيحة: {st.session_state.secret_word}")
                st.session_state.scores[current_player] += 10
                trigger_win_effects()
                if st.button("العودة لاختيار لعبة 🔄"):
                    st.session_state.page = "choose_game"
                    st.rerun()
            else:
                st.error("إجابة غير صحيحة، حاول مجدداً في دورك القادم!")
                next_turn()

    # 3. لعبة الحيوانات
    elif st.session_state.game_type == "animals":
        st.subheader("🦁 من أكون؟ اقرأ التلميحات وخمّن الحيوان:")
        for idx, clue in enumerate(st.session_state.animal_data["clues"], 1):
            st.write(f"💡 **تلميح {idx}:** {clue}")
        animal_guess = st.text_input("اسم الحيوان:").strip()
        if st.button("تحقق من الحيوان 🚀"):
            if animal_guess == st.session_state.animal_data["animal"]:
                st.success(f"🎉 ممتاز يا {current_player}! الحيوان هو بالفعل {animal_guess}")
                st.session_state.scores[current_player] += 10
                trigger_win_effects()
                if st.button("العودة لاختيار لعبة 🔄"):
                    st.session_state.page = "choose_game"
                    st.rerun()
            else:
                st.error("خطأ! الدور ينتقل للاعب التالي...")
                next_turn()

    st.write("---")
    if st.button("🚪 إنهاء الجولة والعودة لاختيار الألعاب"):
        st.session_state.page = "choose_game"
        st.rerun()
