import streamlit as st
import random
import json
import os

st.set_page_config(page_title="Stars & Moons - Game Hub", page_icon="⭐", layout="centered")

SCORES_FILE = "scores.json"

# إدارة حفظ النتائج محلياً
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

# تصميم الألوان والواجهة
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

# بنوك البيانات مقسمة حسب مستويات الصعوبة
WORDS_DATA = {
    "سهل": ["شمس", "قمر", "نجم", "بحر", "طير", "ورد"],
    "متوسط": ["كوكب", "صاروخ", "مجرة", "سفينة", "سحاب", "غابة"],
    "صعب": ["تلسكوب", "مذنبات", "رائد_فضاء", "جاذبية", "نيازك", "أندروميدا"]
}

ANIMALS_DATA = {
    "سهل": [
        {"animal": "أسد", "clues": ["ملك الغابة", "له زئير قوي", "يعيش في جماعات"]},
        {"animal": "قطة", "clues": ["حيوان أليف", "صوتها مواء", "تحب شرب الحليب"]},
        {"animal": "فيل", "clues": ["أضخم حيوان بري", "يمتلك خرطوماً طويلاً", "له أنياب عاجية"]}
    ],
    "متوسط": [
        {"animal": "زرافة", "clues": ["أطول حيوان في العالم", "رقبتها طويلة جداً", "جلدها مرقط بالبني"]},
        {"animal": "بطريق", "clues": ["طائر لا يطير", "سباح ماهر في الماء", "يعيش في القطب الجليدي"]},
        {"animal": "كنغر", "clues": ["يتحرك بالقفز السريع", "يحمل صغيره في جيب أمامي", "مشهور في أستراليا"]}
    ],
    "صعب": [
        {"animal": "حوت_أزرق", "clues": ["أضخم كائن على كوكب الأرض", "يعيش في المحيطات", "يتنفس من فتحة برأسه"]},
        {"animal": "أخطبوط", "clues": ["كائن بحري رخوي", "له 3 قلوب و8 أذرع", "يفرز حبراً عند الخطر"]},
        {"animal": "حرباء", "clues": ["تغير لون جلدها للتمويه", "عيناها تتحركان في اتجاهين مختلفين", "لسانها طويل لاصطياد الحشرات"]}
    ]
}

# تهيئة الجلسة
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'players' not in st.session_state:
    st.session_state.players = []
if 'scores' not in st.session_state:
    st.session_state.scores = load_saved_scores()
if 'current_turn' not in st.session_state:
    st.session_state.current_turn = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "سهل"
if 'solved' not in st.session_state:
    st.session_state.solved = False

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

def setup_new_challenge():
    st.session_state.solved = False
    diff = st.session_state.difficulty

    if st.session_state.game_type == "numbers":
        max_num = 50 if diff == "سهل" else (150 if diff == "متوسط" else 300)
        st.session_state.secret_num = random.randint(0, max_num)
        st.session_state.max_limit = max_num

    elif st.session_state.game_type == "words":
        word_list = WORDS_DATA[diff]
        chosen = random.choice(word_list)
        scrambled = list(chosen)
        random.shuffle(scrambled)
        st.session_state.secret_word = chosen
        st.session_state.scrambled_word = " - ".join(scrambled)

    elif st.session_state.game_type == "animals":
        st.session_state.animal_data = random.choice(ANIMALS_DATA[diff])

# ----------------- 1. القائمة الرئيسية -----------------
if st.session_state.page == "menu":
    st.title("⭐ Stars and Moons 🌙")
    st.markdown("<p style='text-align: center; color: #94a3b8;'>منصة ألعاب التخمين والتحديات المتعددة</p>", unsafe_allow_html=True)

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

    saved = load_saved_scores()
    if saved:
        st.write("---")
        st.markdown("### 🏆 لوحة الشرف السابقة:")
        sorted_saved = sorted(saved.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_saved, 1):
            st.write(f"**المركز {rank}:** {player} ⟵ **{score} نقطة**")

# ----------------- 2. التعليمات -----------------
elif st.session_state.page == "instructions":
    st.title("📜 تعليمات اللعبة والمستويات")
    st.markdown("""
    - **مستويات الصعوبة:**
      - 🟢 **سهل:** الأرقام من (0 إلى 50) | كلمات من 3 أحرف | تلميحات حيوانات مباشرة وسهلة.
      - 🟡 **متوسط:** الأرقام من (0 إلى 150) | كلمات من 4-5 أحرف | تلميحات متوسطة.
      - 🔴 **صعب:** الأرقام من (0 إلى 300) | كلمات طويلة وذكية | تلميحات غامضة تتطلب دقة.
    - **التخمين التالي:** بعد كل إجابة صحيحة، يظهر زر **التخمين التالي ⏭️** لبدء لغز جديد فوراً.
    - **النقاط:** اللعب السهل يمنح 10 نقاط، المتوسط 20 نقطة، والصعب 30 نقطة!
    """)
    if st.button("⬅ العودة للقائمة"):
        st.session_state.page = "menu"
        st.rerun()

# ----------------- 3. إعداد اللاعبين والصعوبة -----------------
elif st.session_state.page == "setup_players":
    st.title("👥 إعداد اللاعبين ومستوى الصعوبة")
    
    diff_choice = st.select_slider(
        "🎚️ حدد مستوى الصعوبة:",
        options=["سهل", "متوسط", "صعب"],
        value="سهل"
    )
    st.session_state.difficulty = diff_choice

    num_players = st.radio("عدد اللاعبين:", [1, 2, 3], horizontal=True)

    names = []
    saved_scores = load_saved_scores()
    for i in range(num_players):
        default_name = f"لاعب {i+1}"
        name = st.text_input(f"اسم اللاعب {i+1}:", value=default_name, key=f"p_name_{i}").strip()
        names.append(name if name else default_name)

    col_next, col_back = st.columns(2)
    with col_next:
        if st.button("متابعة لاختيار اللعبة 🎮", type="primary"):
            st.session_state.players = names
            st.session_state.scores = {n: saved_scores.get(n, 0) for n in names}
            st.session_state.current_turn = 0
            st.session_state.page = "choose_game"
            st.rerun()
    with col_back:
        if st.button("⬅ رجوع"):
            st.session_state.page = "menu"
            st.rerun()

# ----------------- 4. اختيار لعبة التخمين -----------------
elif st.session_state.page == "choose_game":
    diff = st.session_state.difficulty
    st.title("🕹️ اختر لعبة التخمين")
    st.caption(f"مستوى الصعوبة الحالي: {diff}")

    st.markdown("### 🏆 النتائج الحالية:")
    cols = st.columns(len(st.session_state.players))
    for idx, p in enumerate(st.session_state.players):
        cols[idx].metric(label=p, value=f"{st.session_state.scores.get(p, 0)} نقطة")
    st.write("---")

    g1, g2, g3 = st.columns(3)
    with g1:
        max_preview = 50 if diff == "سهل" else (150 if diff == "متوسط" else 300)
        if st.button(f"🔢 تخمين الأرقام\n(0 - {max_preview})"):
            st.session_state.game_type = "numbers"
            setup_new_challenge()
            st.session_state.page = "play"
            st.rerun()
    with g2:
        if st.button("🔤 تخمين الكلمة\n(حروف مبعثرة)"):
            st.session_state.game_type = "words"
            setup_new_challenge()
            st.session_state.page = "play"
            st.rerun()
    with g3:
        if st.button("🦁 خمن الحيوان\n(بالتلميحات)"):
            st.session_state.game_type = "animals"
            setup_new_challenge()
            st.session_state.page = "play"
            st.rerun()

    st.write("---")
    if st.button("💾 حفظ وخروج نهائي 🚪"):
        all_s = load_saved_scores()
        all_s.update(st.session_state.scores)
        save_scores(all_s)
        st.session_state.page = "exit"
        st.rerun()

# ----------------- 5. ساحة اللعب وخيار التخمين التالي -----------------
elif st.session_state.page == "play":
    current_player = st.session_state.players[st.session_state.current_turn]
    diff = st.session_state.difficulty
    points_reward = 10 if diff == "سهل" else (20 if diff == "متوسط" else 30)

    st.markdown(f"### 🎯 دور: <span style='color:#38bdf8;'>{current_player}</span> | المستوى: <span style='color:#fbbf24;'>{diff}</span>", unsafe_allow_html=True)

    # 1. لعبة الأرقام
    if st.session_state.game_type == "numbers":
        max_l = st.session_state.max_limit
        st.subheader(f"🔢 خمّن الرقم السري (0 - {max_l})")
        
        guess = st.number_input("أدخل تخمينك:", min_value=0, max_value=max_l, step=1, disabled=st.session_state.solved, key="num_in")
        
        if not st.session_state.solved:
            if st.button("تحقق من الرقم 🚀"):
                sec = st.session_state.secret_num
                if guess < sec:
                    st.info("الرقم السري أكبر من ذلك ⬆️")
                    next_turn()
                    st.rerun()
                elif guess > sec:
                    st.warning("الرقم السري أصغر من ذلك ⬇️")
                    next_turn()
                    st.rerun()
                else:
                    st.success(f"🎉 أحسنت يا {current_player}! الرقم الصحيح هو ({sec})! (+{points_reward} نقطة)")
                    st.session_state.scores[current_player] += points_reward
                    st.session_state.solved = True
                    trigger_win_effects()
                    st.rerun()

    # 2. لعبة الكلمات
    elif st.session_state.game_type == "words":
        st.subheader("🔤 رتّب الحروف واكتشف الكلمة:")
        st.markdown(f"## ` {st.session_state.scrambled_word} `")
        word_guess = st.text_input("اكتب الكلمة الصحيحة:", disabled=st.session_state.solved, key="word_in").strip()
        
        if not st.session_state.solved:
            if st.button("تحقق من الكلمة 🚀"):
                if word_guess == st.session_state.secret_word:
                    st.success(f"🎉 إجابة صحيحة يا {current_player}! (+{points_reward} نقطة)")
                    st.session_state.scores[current_player] += points_reward
                    st.session_state.solved = True
                    trigger_win_effects()
                    st.rerun()
                else:
                    st.error("إجابة خاطئة! ينتقل الدور للاعب التالي...")
                    next_turn()
                    st.rerun()

    # 3. لعبة الحيوانات
    elif st.session_state.game_type == "animals":
        st.subheader("🦁 من أكون؟ اقرأ التلميحات وخمّن الحيوان:")
        for idx, clue in enumerate(st.session_state.animal_data["clues"], 1):
            st.write(f"💡 **تلميح {idx}:** {clue}")

        animal_guess = st.text_input("اسم الحيوان:", disabled=st.session_state.solved, key="animal_in").strip()
        
        if not st.session_state.solved:
            if st.button("تحقق من الحيوان 🚀"):
                if animal_guess == st.session_state.animal_data["animal"]:
                    st.success(f"🎉 ذكي جداً يا {current_player}! الحيوان هو {animal_guess} (+{points_reward} نقطة)")
                    st.session_state.scores[current_player] += points_reward
                    st.session_state.solved = True
                    trigger_win_effects()
                    st.rerun()
                else:
                    st.error("خطأ! ينتقل الدور للاعب التالي...")
                    next_turn()
                    st.rerun()

    # زر "التخمين التالي" عند حل اللغز
    if st.session_state.solved:
        st.write("---")
        if st.button("التخمين التالي ⏭️ (لغز جديد)", type="primary"):
            next_turn()
            setup_new_challenge()
            st.rerun()

    st.write("---")
    c_back, c_save = st.columns(2)
    with c_back:
        if st.button("⬅ العودة لاختيار الألعاب"):
            st.session_state.page = "choose_game"
            st.rerun()
    with c_save:
        if st.button("💾 حفظ وخروج نهائي 🚪"):
            all_s = load_saved_scores()
            all_s.update(st.session_state.scores)
            save_scores(all_s)
            st.session_state.page = "exit"
            st.rerun()

# ----------------- 6. صفحة الخروج ولوحة الشرف -----------------
elif st.session_state.page == "exit":
    st.title("🏆 لوحة الأبطال النهائية")
    all_scores = load_saved_scores()

    if all_scores:
        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        st.success("✅ تم حفظ النقاط بنجاح!")
        for rank, (player, score) in enumerate(sorted_scores, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🎖️"
            st.write(f"### {medal} المركز {rank}: {player} ⟵ {score} نقطة")

    if st.button("🔄 العودة إلى القائمة الرئيسية"):
        st.session_state.page = "menu"
        st.rerun()
