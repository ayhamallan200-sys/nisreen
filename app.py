import streamlit as st
import random
import json
import os
import re

st.set_page_config(page_title="Stars & Moons - Game Hub", page_icon="⭐", layout="centered")

SCORES_FILE = "scores.json"

# دالة لتسوية وتوحيد الكلمات (الهمزات والتاء المربوطة)
def normalize_arabic(text):
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r"[إأآا]", "ا", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"\s+", " ", text)
    return text

# إدارة حفظ واسترجاع النتائج
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

# بنك الكلمات المطور
WORDS_DATA = {
    "سهل": ["شمس", "قمر", "نجم", "بحر", "طير", "ورد"],
    "متوسط": ["كوكب", "صاروخ", "مجرة", "سفينة", "سحاب", "غابة"],
    "صعب": ["ثقب_اسود", "نيازك_ملتهبه", "مكوك_فضائي", "مجره_اندروميدا", "تلسكوب_جيمس_ويب", "جاذبيه_كونيه"]
}

# بنك الحيوانات مع مرونة الهمزات وتحدي الصعب
ANIMALS_DATA = {
    "سهل": [
        {"animal": "اسد", "display": "أسد", "clues": ["ملك الغابة", "له زئير قوي", "يعيش في جماعات"]},
        {"animal": "قطه", "display": "قطة", "clues": ["حيوان أليف", "صوته مواء", "يحب اللعب بالخيوط"]},
        {"animal": "فيل", "display": "فيل", "clues": ["أضخم حيوان بري", "يمتلك خرطوماً طويلاً", "له أنياب عاجية"]}
    ],
    "متوسط": [
        {"animal": "زرافه", "display": "زرافة", "clues": ["أطول حيوان في العالم", "رقبتها طويلة جداً", "جلدها مرقط"]},
        {"animal": "بطريق", "display": "بطريق", "clues": ["طائر لا يطير", "سباح ماهر جداً", "يعيش في الجليد"]},
        {"animal": "كنغر", "display": "كنغر", "clues": ["يتحرك بالقفز العالي", "يحمل صغيره في جراب أمامي", "موطنه أستراليا"]}
    ],
    "صعب": [
        {"animal": "خلد الماء", "display": "خلد الماء (بلاتيبوس)", "clues": ["ثديي يبيض ولا يلد", "له منقار كالبط وذيل كالقندس", "ذكوره تفرز سماً من أرجلها"]},
        {"animal": "الكسلان", "display": "حيوان الكسلان", "clues": ["أبطأ حيوان ثديي في العالم", "يقضي أغلب حياته معلقاً رأساً على عقب", "تنمو الطحالب الخضراء على فرائه"]},
        {"animal": "اكل النمل", "display": "آكل النمل الحرشفى (البنغول)", "clues": ["جسمه مغطى بحراشف صلبة كالدروع", "يتكور كالكرة تماماً عند الإحساس بالخطر", "لسانه أطول من جسمه لالتقاط الحشرات"]},
        {"animal": "دب الماء", "display": "دب الماء (تارديغرادا)", "clues": ["كائن مجهري خارق", "يستطيع العيش في الفضاء الخارجي وبدون ماء لسنوات", "يتحمل درجات حرارة متجمدة وإشعاعات نووية"]}
    ]
}

# تهيئة المتغيرات في الجلسة
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
if 'last_status' not in st.session_state:
    st.session_state.last_status = None

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
    st.session_state.last_status = None
    diff = st.session_state.difficulty

    if st.session_state.game_type == "numbers":
        max_num = 50 if diff == "سهل" else (150 if diff == "متوسط" else 500)
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
    st.markdown("<p style='text-align: center; color: #94a3b8;'>منصة ألعاب التخمين والتحدي الذكي</p>", unsafe_allow_html=True)

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
        st.markdown("### 🏆 لوحة الشرف المحفوظة:")
        sorted_saved = sorted(saved.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_saved, 1):
            st.write(f"**المركز {rank}:** {player} ⟵ **{score} نقطة**")

# ----------------- 2. التعليمات -----------------
elif st.session_state.page == "instructions":
    st.title("📜 تعليمات الألعاب والمستويات")
    st.markdown("""
    - **خيارات الصعوبة:**
      - 🟢 **سهل:** أرقام (0 إلى 50) | كلمات بسيطة | تلميحات واضحة.
      - 🟡 **متوسط:** أرقام (0 إلى 150) | كلمات متوسطة | تلميحات معتدلة.
      - 🔴 **صعب:** أرقام (0 إلى 500) | كلمات فضائية مركبة | حيوانات وكائنات خارقة بتلميحات ذكية.
    - **كتابة الإجابة:** النظام يقبل الإجابة سواء كتبتها بهمزة أو بدون همزة (أ/ا) وبالتاء أو الهاء (ة/ه).
    - **التخمين التالي:** بعد حل أي لغز، اضغط على زر **التخمين التالي ⏭️** لبدء لغز جديد مع احتساب النقاط وتناوب الأدوار.
    - **تصفير النتائج:** يمكنك تصفير كافة النقاط في أي وقت من شاشة الألعاب.
    """)
    if st.button("⬅ العودة للقائمة"):
        st.session_state.page = "menu"
        st.rerun()

# ----------------- 3. إعداد اللاعبين والمستوى -----------------
elif st.session_state.page == "setup_players":
    st.title("👥 إعداد اللعبة")
    
    st.subheader("1. اختر مستوى الصعوبة:")
    diff_choice = st.radio(
        "المستوى:",
        options=["سهل", "متوسط", "صعب"],
        horizontal=True,
        index=0
    )
    st.session_state.difficulty = diff_choice

    st.subheader("2. حدد عدد اللاعبين:")
    num_players = st.radio("العدد:", [1, 2, 3], horizontal=True)

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

# ----------------- 4. اختيار اللعبة وإدارة النتائج -----------------
elif st.session_state.page == "choose_game":
    diff = st.session_state.difficulty
    st.title("🕹️ اختر لعبة التخمين")
    st.caption(f"المستوى الحالي: {diff}")

    st.markdown("### 🏆 النتائج الحالية:")
    cols = st.columns(len(st.session_state.players))
    for idx, p in enumerate(st.session_state.players):
        cols[idx].metric(label=p, value=f"{st.session_state.scores.get(p, 0)} نقطة")
    st.write("---")

    g1, g2, g3 = st.columns(3)
    with g1:
        max_preview = 50 if diff == "سهل" else (150 if diff == "متوسط" else 500)
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
        if st.button("🦁 خمن الكائن / الحيوان\n(بالتلميحات)"):
            st.session_state.game_type = "animals"
            setup_new_challenge()
            st.session_state.page = "play"
            st.rerun()

    st.write("---")
    c_exit, c_reset = st.columns(2)
    with c_exit:
        if st.button("💾 حفظ وخروج نهائي 🚪"):
            all_s = load_saved_scores()
            all_s.update(st.session_state.scores)
            save_scores(all_s)
            st.session_state.page = "exit"
            st.rerun()
    with c_reset:
        if st.button("🔄 تصفير النتائج"):
            for p in st.session_state.players:
                st.session_state.scores[p] = 0
            all_s = load_saved_scores()
            for p in st.session_state.players:
                all_s[p] = 0
            save_scores(all_s)
            st.success("تم تصفير جميع النتائج بنجاح!")
            st.rerun()

# ----------------- 5. ساحة اللعب وعرض النتيجة -----------------
elif st.session_state.page == "play":
    current_player = st.session_state.players[st.session_state.current_turn]
    diff = st.session_state.difficulty
    points_reward = 10 if diff == "سهل" else (20 if diff == "متوسط" else 30)

    st.markdown(f"### 🎯 دور: <span style='color:#38bdf8;'>{current_player}</span> | المستوى: <span style='color:#fbbf24;'>{diff}</span>", unsafe_allow_html=True)

    # عرض الرسالة الأخيرة للإجابة (صحيحة / خاطئة)
    if st.session_state.last_status:
        st.markdown(st.session_state.last_status, unsafe_allow_html=True)

    # 1. لعبة الأرقام
    if st.session_state.game_type == "numbers":
        max_l = st.session_state.max_limit
        st.subheader(f"🔢 خمّن الرقم السري (0 - {max_l})")
        
        guess = st.number_input("أدخل تخمينك:", min_value=0, max_value=max_l, step=1, disabled=st.session_state.solved, key="num_in")
        
        if not st.session_state.solved:
            if st.button("تحقق من الرقم 🚀"):
                sec = st.session_state.secret_num
                if guess < sec:
                    st.session_state.last_status = f"<div style='color:#f87171; font-weight:bold; font-size:18px;'>❌ إجابة خاطئة! الرقم السري أكبر من {guess} ⬆️</div>"
                    next_turn()
                    st.rerun()
                elif guess > sec:
                    st.session_state.last_status = f"<div style='color:#f87171; font-weight:bold; font-size:18px;'>❌ إجابة خاطئة! الرقم السري أصغر من {guess} ⬇️</div>"
                    next_turn()
                    st.rerun()
                else:
                    st.session_state.last_status = f"<div style='color:#4ade80; font-weight:bold; font-size:20px;'>🎉 إجابة صحيحة وممتازة يا {current_player}! الرقم هو ({sec}) (+{points_reward} نقطة)</div>"
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
                # مقارنة متساهلة مع الهمزات
                if normalize_arabic(word_guess) == normalize_arabic(st.session_state.secret_word):
                    st.session_state.last_status = f"<div style='color:#4ade80; font-weight:bold; font-size:20px;'>🎉 إجابة صحيحة يا {current_player}! الكلمة هي: {st.session_state.secret_word} (+{points_reward} نقطة)</div>"
                    st.session_state.scores[current_player] += points_reward
                    st.session_state.solved = True
                    trigger_win_effects()
                    st.rerun()
                else:
                    st.session_state.last_status = f"<div style='color:#f87171; font-weight:bold; font-size:18px;'>❌ إجابة خاطئة! الكلمة ليست '{word_guess}'. ينتقل الدور للاعب التالي!</div>"
                    next_turn()
                    st.rerun()

    # 3. لعبة الحيوانات والكائنات
    elif st.session_state.game_type == "animals":
        st.subheader("🦁 من أكون؟ اقرأ التلميحات وخمّن الكائن:")
        for idx, clue in enumerate(st.session_state.animal_data["clues"], 1):
            st.write(f"💡 **تلميح {idx}:** {clue}")

        animal_guess = st.text_input("اسم الحيوان / الكائن:", disabled=st.session_state.solved, key="animal_in").strip()
        
        if not st.session_state.solved:
            if st.button("تحقق من الإجابة 🚀"):
                target = st.session_state.animal_data["animal"]
                if normalize_arabic(animal_guess) == normalize_arabic(target):
                    st.session_state.last_status = f"<div style='color:#4ade80; font-weight:bold; font-size:20px;'>🎉 إجابة صحيحة يا بطل {current_player}! هو بالفعل {st.session_state.animal_data['display']} (+{points_reward} نقطة)</div>"
                    st.session_state.scores[current_player] += points_reward
                    st.session_state.solved = True
                    trigger_win_effects()
                    st.rerun()
                else:
                    st.session_state.last_status = f"<div style='color:#f87171; font-weight:bold; font-size:18px;'>❌ إجابة خاطئة! ليس '{animal_guess}'. ينتقل الدور للاعب التالي!</div>"
                    next_turn()
                    st.rerun()

    # زر "التخمين التالي" عند الحل الصحيح
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
            st.session_state.last_status = None
            st.session_state.page = "choose_game"
            st.rerun()
    with c_save:
        if st.button("💾 حفظ وخروج نهائي 🚪"):
            all_s = load_saved_scores()
            all_s.update(st.session_state.scores)
            save_scores(all_s)
            st.session_state.page = "exit"
            st.rerun()

# ----------------- 6. صفحة الخروج والنتائج -----------------
elif st.session_state.page == "exit":
    st.title("🏆 لوحة الشرف والنتائج")
    all_scores = load_saved_scores()

    if all_scores:
        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        st.success("✅ تم حفظ كافة البيانات بنجاح!")
        for rank, (player, score) in enumerate(sorted_scores, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🎖️"
            st.write(f"### {medal} المركز {rank}: {player} ⟵ {score} نقطة")

    if st.button("🔄 العودة إلى القائمة الرئيسية"):
        st.session_state.page = "menu"
        st.rerun()
