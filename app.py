import streamlit as st
import random
import json
import os

st.set_page_config(page_title="Stars & Moons - Game Hub", page_icon="🎮", layout="centered")

SCORES_FILE = "scores.json"

# دوال إدارة الحفظ والاسترجاع
def load_saved_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_scores(scores_dict):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores_dict, f, ensure_ascii=False, indent=2)

# تصميم الواجهة
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
    </style>
""", unsafe_allow_html=True)

WORDS_BANK = ["كوكب", "مجرة", "صاروخ", "سفينة", "فضاء", "تلسكوب", "نيزك", "شمس"]
ANIMALS_BANK = [
    {"animal": "أسد", "clues": ["ملك الغابة", "له شعر كثيف حول رقبته (لبدة)", "يعيش في جماعات"]},
    {"animal": "فيل", "clues": ["أضخم حيوان يعيش على اليابسة", "له خرطوم طويل", "يمتلك أنياباً عاجية"]},
    {"animal": "زرافة", "clues": ["أطول حيوان في العالم", "رقبتها طويلة جداً", "جلدها مرقط"]},
    {"animal": "بطريق", "clues": ["طائر لا يطير", "سباح ماهر جداً", "يعيش في المناطق الجليدية"]}
]

# تهيئة الجلسة
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'players' not in st.session_state:
    st.session_state.players = []
if 'scores' not in st.session_state:
    st.session_state.scores = load_saved_scores()
if 'current_turn' not in st.session_state:
    st.session_state.current_turn = 0

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
    st.markdown("<p style='text-align: center; color: #94a3b8;'>منصة ألعاب التخمين والتحدي الجماعي</p>", unsafe_allow_html=True)
    
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

    # استعراض النتائج المحفوظة مسبقاً إن وجدت
    saved = load_saved_scores()
    if saved:
        st.write("---")
        st.markdown("### 🏆 لوحة الشرف المحفوظة:")
        sorted_saved = sorted(saved.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_saved, 1):
            st.write(f"**المركز {rank}:** {player} ⟵ **{score} نقطة**")

# ----------------- 2. صفحة التعليمات -----------------
elif st.session_state.page == "instructions":
    st.title("📜 تعليمات الألعاب")
    st.markdown("""
    - **تخمين الأرقام:** خمن الرقم بين 0 و 300 مع توجيهات (أكبر / أصغر).
    - **تخمين الكلمة:** أعد ترتيب الحروف المبعثرة لمعرفة الكلمة الصحيحة.
    - **تخمين الحيوان:** استنتج اسم الحيوان من 3 تلميحات ذكية.
    - **الحفظ التلقائي:** يتم حفظ النقاط تلقائياً ويمكنك الخروج في أي وقت وحفظ الترتيب النهائي!
    """)
    if st.button("⬅ العودة للقائمة"):
        st.session_state.page = "menu"
        st.rerun()

# ----------------- 3. إعداد اللاعبين -----------------
elif st.session_state.page == "setup_players":
    st.title("👥 تسجيل اللاعبين")
    num_players = st.radio("اختر عدد اللاعبين:", [1, 2, 3], horizontal=True)

    names = []
    saved_scores = load_saved_scores()
    for i in range(num_players):
        default_name = f"لاعب {i+1}"
        name = st.text_input(f"اسم اللاعب {i+1}:", value=default_name, key=f"player_input_{i}").strip()
        names.append(name if name else default_name)

    col_start, col_back = st.columns(2)
    with col_start:
        if st.button("متابعة لاختيار اللعبة 🎮", type="primary"):
            st.session_state.players = names
            # استعادة النقاط السابقة لنفس اللاعب أو البدء من الصفر
            st.session_state.scores = {n: saved_scores.get(n, 0) for n in names}
            st.session_state.current_turn = 0
            st.session_state.page = "choose_game"
            st.rerun()
    with col_back:
        if st.button("⬅ رجوع"):
            st.session_state.page = "menu"
            st.rerun()

# ----------------- 4. اختيار اللعبة -----------------
elif st.session_state.page == "choose_game":
    st.title("🕹️ اختر لعبة التخمين")
    
    st.markdown("### 🏆 النتائج الحالية:")
    cols = st.columns(len(st.session_state.players))
    for idx, p in enumerate(st.session_state.players):
        cols[idx].metric(label=p, value=f"{st.session_state.scores.get(p, 0)} نقطة")
    st.write("---")

    g1, g2, g3 = st.columns(3)
    with g1:
        if st.button("🔢 تخمين الأرقام\n(0 - 300)"):
            st.session_state.secret_num = random.randint(0, 300)
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
            st.session_state.animal_data = random.choice(ANIMALS_BANK)
            st.session_state.game_type = "animals"
            st.session_state.page = "play"
            st.rerun()

    st.write("---")
    c_exit, c_reset = st.columns(2)
    with c_exit:
        if st.button("💾 حفظ النتائج والخروج 🚪", type="secondary"):
            # دمج النتائج مع المحفوظات وحفظها
            current_all = load_saved_scores()
            current_all.update(st.session_state.scores)
            save_scores(current_all)
            st.session_state.page = "exit"
            st.rerun()
    with c_reset:
        if st.button("🔄 تصفير النقاط"):
            for p in st.session_state.players:
                st.session_state.scores[p] = 0
            current_all = load_saved_scores()
            for p in st.session_state.players:
                current_all[p] = 0
            save_scores(current_all)
            st.success("تم تصفير النقاط بنجاح!")
            st.rerun()

# ----------------- 5. ساحة اللعب -----------------
elif st.session_state.page == "play":
    current_player = st.session_state.players[st.session_state.current_turn]
    st.markdown(f"### 🎯 دور اللاعب: <span style='color:#38bdf8;'>{current_player}</span>", unsafe_allow_html=True)

    # 1. الأرقام
    if st.session_state.game_type == "numbers":
        st.subheader("🔢 خمّن الرقم السري (0 - 300)")
        guess = st.number_input("أدخل تخمينك:", min_value=0, max_value=300, step=1, key="num_in")
        if st.button("تحقق 🚀"):
            sec = st.session_state.secret_num
            if guess < sec:
                st.info("الرقم السري أكبر من ذلك ⬆️")
                next_turn()
            elif guess > sec:
                st.warning("الرقم السري أصغر من ذلك ⬇️")
                next_turn()
            else:
                st.success(f"🎉 أحسنت يا {current_player}! الرقم هو {sec} (+10 نقاط)")
                st.session_state.scores[current_player] += 10
                # حفظ فوري
                all_s = load_saved_scores()
                all_s.update(st.session_state.scores)
                save_scores(all_s)
                trigger_win_effects()
                if st.button("العودة لاختيار لعبة 🔄"):
                    st.session_state.page = "choose_game"
                    st.rerun()

    # 2. الكلمات
    elif st.session_state.game_type == "words":
        st.subheader("🔤 رتّب الحروف واكتشف الكلمة:")
        st.markdown(f"## ` {st.session_state.scrambled_word} `")
        word_guess = st.text_input("اكتب الكلمة الصحيحة:", key="word_in").strip()
        if st.button("إرسال الإجابة 🚀"):
            if word_guess == st.session_state.secret_word:
                st.success(f"🎉 ممتاز يا {current_player}! الكلمة صحيحة (+10 نقاط)")
                st.session_state.scores[current_player] += 10
                all_s = load_saved_scores()
                all_s.update(st.session_state.scores)
                save_scores(all_s)
                trigger_win_effects()
                if st.button("العودة لاختيار لعبة 🔄"):
                    st.session_state.page = "choose_game"
                    st.rerun()
            else:
                st.error("إجابة غير صحيحة! الدور ينتقل للاعب التالي...")
                next_turn()

    # 3. الحيوانات
    elif st.session_state.game_type == "animals":
        st.subheader("🦁 من أكون؟ اقرأ التلميحات وخمّن الحيوان:")
        for idx, clue in enumerate(st.session_state.animal_data["clues"], 1):
            st.write(f"💡 **تلميح {idx}:** {clue}")
        animal_guess = st.text_input("اسم الحيوان:", key="animal_in").strip()
        if st.button("تحقق من الحيوان 🚀"):
            if animal_guess == st.session_state.animal_data["animal"]:
                st.success(f"🎉 رائع يا {current_player}! الحيوان هو {animal_guess} (+10 نقاط)")
                st.session_state.scores[current_player] += 10
                all_s = load_saved_scores()
                all_s.update(st.session_state.scores)
                save_scores(all_s)
                trigger_win_effects()
                if st.button("العودة لاختيار لعبة 🔄"):
                    st.session_state.page = "choose_game"
                    st.rerun()
            else:
                st.error("إجابة خاطئة! الدور ينتقل للاعب التالي...")
                next_turn()

    st.write("---")
    col_back, col_exit = st.columns(2)
    with col_back:
        if st.button("⬅ التوقف والعودة للقائمة"):
            st.session_state.page = "choose_game"
            st.rerun()
    with col_exit:
        if st.button("💾 حفظ وخروج نهائي 🚪"):
            all_s = load_saved_scores()
            all_s.update(st.session_state.scores)
            save_scores(all_s)
            st.session_state.page = "exit"
            st.rerun()

# ----------------- 6. صفحة الخروج وشاشة التكريم -----------------
elif st.session_state.page == "exit":
    st.title("🏆 النتائج النهائية والمحفوظة")
    all_scores = load_saved_scores()
    
    if all_scores:
        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        st.success("✅ تم حفظ كافة النتائج بأمان في ملف البيانات!")
        st.markdown("### 🥇 ترتيب الأبطال:")
        for rank, (player, score) in enumerate(sorted_scores, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🎖️"
            st.write(f"### {medal} المركز {rank}: {player} ⟵ {score} نقطة")
    else:
        st.info("شكراً لتجربتك اللعبة!")

    st.write("---")
    if st.button("🔄 العودة إلى الشاشة الرئيسية"):
        st.session_state.page = "menu"
        st.rerun()
