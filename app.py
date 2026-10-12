import streamlit as st
import random
import re

st.set_page_config(page_title="Stars & Moons - Game Hub", page_icon="⭐", layout="centered")

def normalize_arabic(text):
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r"[إأآا]", "ا", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"\s+", " ", text)
    return text

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
    .hint-box {
        background: rgba(234, 179, 8, 0.15);
        border: 1px dashed #eab308;
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

WORDS_BANK = {
    "سهل": ["شمس", "قمر", "نجم", "بحر", "طير", "ورد", "شجر", "نهر", "سمك", "جبل"],
    "متوسط": ["كوكب", "صاروخ", "مجرة", "سفينة", "سحاب", "غابة", "تلسكوب", "نيزك", "صحراء", "بركان"],
    "صعب": ["ثقب_اسود", "نيازك_ملتهبه", "مكوك_فضائي", "مجره_اندروميدا", "تلسكوب_جيمس_ويب", "جاذبيه_كونيه", "سديم_كوني", "انفجار_عظيم"]
}

ANIMALS_BANK = {
    "سهل": [
        {"animal": "اسد", "display": "أسد", "clues": ["ملك الغابة", "له زئير قوي"], "hint": "من فصيلة السنوريات المفترسة"},
        {"animal": "قطه", "display": "قطة", "clues": ["حيوان أليف", "صوته مواء"], "hint": "تحب شرب الحليب واللعب بالصوف"},
        {"animal": "فيل", "display": "فيل", "clues": ["أضخم حيوان يابسة", "يمتلك خرطوماً طويلاً"], "hint": "له آذان عريضة جداً وأنياب عاجية"},
        {"animal": "ذئب", "display": "ذئب", "clues": ["يعيش في قطعان", "يعوي ليلاً باتجاه القمر"], "hint": "يشبه الكلب البري وله حاسة شم خارقة"},
        {"animal": "ارنب", "display": "أرنب", "clues": ["حيوان سريع ومرن", "له أذنان طويلتان"], "hint": "طعامه المفضل الجزر والخضار"}
    ],
    "متوسط": [
        {"animal": "زرافه", "display": "زرافة", "clues": ["أطول كائن بري", "جلدها مرقط بالبني والأصفر"], "hint": "تأكل من قمم أشجار السنط بلسانها الطويل"},
        {"animal": "بطريق", "display": "بطريق", "clues": ["طائر لا يستطيع الطيران", "سباح ماهر جداً في الماء"], "hint": "يعيش في الثلوج القطبية ويرتدي بدلة طبيعية سوداء وبيضاء"},
        {"animal": "كنغر", "display": "كنغر", "clues": ["يتحرك بالقفز على رجليه الخلفيتين", "موطنه الأصلي قارة أستراليا"], "hint": "تحمل الأنثى صغيرها في جيب على بطنها"},
        {"animal": "دلفين", "display": "دلفين", "clues": ["حيوان بحري ذكي جداً", "يتنفس الهواء ويتواصل بالصفير"], "hint": "صديق للإنسان ولا يعتبر سمكة بل من الثدييات"},
        {"animal": "نسر", "display": "نسر", "clues": ["طائر جارح حاد البصر", "يبني عشه في قمم الجبال الشاهقة"], "hint": "له مخالب فولاذية وأجنحة ضخمة"}
    ],
    "صعب": [
        {"animal": "خلد الماء", "display": "خلد الماء (بلاتيبوس)", "clues": ["ثديي يبيض ولا يلد", "منقاره عريض يشبه البطة"], "hint": "ذكوره تفرز سماً للدفاع وذيله يشبه القندس"},
        {"animal": "الكسلان", "display": "حيوان الكسلان", "clues": ["أبطأ ثديي في العالم", "يقضي عمره متعلقاً بالأشجار"], "hint": "تنمو الطحالب الخضراء على فرائه لكثرة سكونه"},
        {"animal": "اكل النمل", "display": "آكل النمل الحرشفى (البنغول)", "clues": ["جسمه مصفح بحراشف عريضة قاسية", "يتكور كالكرة عند الخطر"], "hint": "لسانه فائق الطول ومغطى بمادة لزجة لاصطياد النمل"},
        {"animal": "دب الماء", "display": "دب الماء (تارديغرادا)", "clues": ["كائن مجهري خارق للظروف الصعبة", "يعيش في الفراغ الجوي والإشعاع"], "hint": "يتحمل حرارة تقارب الصفر المطلق والجفاف لعقود"},
        {"animal": "الحبار العملاق", "display": "الحبار العملاق", "clues": ["يسكن أعماق المحيط السحيقة", "له أكبر عيون في مملكة الحيوان"], "hint": "يخوض معارك أسطورية ضد حيتان العنبر"}
    ]
}

# تهيئة الجلسة المستقلة
if 'page' not in st.session_state:
    st.session_state.page = "menu"
if 'players' not in st.session_state:
    st.session_state.players = []
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'current_turn' not in st.session_state:
    st.session_state.current_turn = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "سهل"
if 'solved' not in st.session_state:
    st.session_state.solved = False
if 'last_status' not in st.session_state:
    st.session_state.last_status = None
if 'hint_requester' not in st.session_state:
    st.session_state.hint_requester = None
if 'words_queue' not in st.session_state:
    st.session_state.words_queue = []
if 'animals_queue' not in st.session_state:
    st.session_state.animals_queue = []

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
    st.session_state.hint_requester = None
    diff = st.session_state.difficulty

    if st.session_state.game_type == "numbers":
        max_num = 50 if diff == "سهل" else (150 if diff == "متوسط" else 500)
        st.session_state.secret_num = random.randint(0, max_num)
        st.session_state.max_limit = max_num

    elif st.session_state.game_type == "words":
        if not st.session_state.words_queue:
            q = list(WORDS_BANK[diff])
            random.shuffle(q)
            st.session_state.words_queue = q
        chosen = st.session_state.words_queue.pop(0)
        scrambled = list(chosen)
        random.shuffle(scrambled)
        st.session_state.secret_word = chosen
        st.session_state.scrambled_word = " - ".join(scrambled)

    elif st.session_state.game_type == "animals":
        if not st.session_state.animals_queue:
            q = list(ANIMALS_BANK[diff])
            random.shuffle(q)
            st.session_state.animals_queue = q
        chosen = st.session_state.animals_queue.pop(0)
        st.session_state.animal_data = chosen

# ----------------- 1. القائمة الرئيسية -----------------
if st.session_state.page == "menu":
    st.title("⭐ Stars and Moons 🌙")
    st.markdown("<p style='text-align: center; color: #94a3b8;'>منصة ألعاب التخمين والتحدي للجلسات المباشرة</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("1. التعليمات 📜"):
            st.session_state.page = "instructions"
            st.rerun()
    with col2:
        if st.button("2. بدء جلسة جديدة 🚀", type="primary"):
            st.session_state.page = "setup_players"
            st.rerun()
    with col3:
        if st.button("3. خروج 🚪"):
            st.session_state.page = "exit"
            st.rerun()

# ----------------- 2. التعليمات -----------------
elif st.session_state.page == "instructions":
    st.title("📜 تعليمات الجلسة")
    st.markdown("""
    - **جلسة مستقلة:** النقاط خاصة بهذه الجلسة فقط ولا تُخلط بأي جلسات سابقة.
    - **قاعدة المساعدة الفردية:** اللاعب الذي يطلب المساعدة فقط هو من يُخصم نصف نقاطه إذا خمن الحل لاحقاً، بينما يحصل أي لاعب آخر على النقاط كاملة إذا عرف الحل في دوره!
    - **النقاط:** سهل (10) | متوسط (20) | صعب (30).
    """)
    if st.button("⬅ العودة للقائمة"):
        st.session_state.page = "menu"
        st.rerun()

# ----------------- 3. إعداد الجلسة واللاعبين -----------------
elif st.session_state.page == "setup_players":
    st.title("👥 إعداد الجلسة الحالية")
    
    st.subheader("1. اختر مستوى الصعوبة للجلسة:")
    diff_choice = st.radio("المستوى:", ["سهل", "متوسط", "صعب"], horizontal=True, index=0)
    st.session_state.difficulty = diff_choice

    st.subheader("2. حدد عدد اللاعبين:")
    num_players = st.radio("العدد:", [1, 2, 3], horizontal=True)

    names = []
    for i in range(num_players):
        default_name = f"لاعب {i+1}"
        name = st.text_input(f"اسم اللاعب {i+1}:", value=default_name, key=f"p_name_{i}").strip()
        names.append(name if name else default_name)

    col_next, col_back = st.columns(2)
    with col_next:
        if st.button("بدء التحدي 🎮", type="primary"):
            st.session_state.players = names
            st.session_state.scores = {n: 0 for n in names}
            st.session_state.current_turn = 0
            st.session_state.words_queue = []
            st.session_state.animals_queue = []
            st.session_state.page = "choose_game"
            st.rerun()
    with col_back:
        if st.button("⬅ رجوع"):
            st.session_state.page = "menu"
            st.rerun()

# ----------------- 4. اختيار اللعبة ولوحة معلومات الجلسة -----------------
elif st.session_state.page == "choose_game":
    diff = st.session_state.difficulty
    st.title("🕹️ اختر لعبة التخمين")
    st.caption(f"مستوى الجلسة: {diff}")

    st.markdown("### 📊 لوحة معلومات الجلسة الحالية:")
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
        if st.button("🚪 إنهاء الجلسة وعرض النتيجة"):
            st.session_state.page = "exit"
            st.rerun()
    with c_reset:
        if st.button("🔄 تصفير نقاط الجلسة"):
            for p in st.session_state.players:
                st.session_state.scores[p] = 0
            st.success("تم تصفير نقاط الجلسة!")
            st.rerun()

# ----------------- 5. ساحة اللعب والخصم الفردي -----------------
elif st.session_state.page == "play":
    current_player = st.session_state.players[st.session_state.current_turn]
    diff = st.session_state.difficulty
    base_points = 10 if diff == "سهل" else (20 if diff == "متوسط" else 30)

    # حساب نقاط اللاعب الحالي بناءً على ما إذا كان هو من طلب المساعدة شخصياً
    is_penalty_user = (st.session_state.hint_requester == current_player)
    player_points = (base_points // 2) if is_penalty_user else base_points

    st.markdown(f"### 🎯 دور: <span style='color:#38bdf8;'>{current_player}</span> | المستوى: <span style='color:#fbbf24;'>{diff}</span>", unsafe_allow_html=True)
    
    if st.session_state.hint_requester:
        if is_penalty_user:
            st.caption(f"⚠️ لقد طلبت المساعدة: جائزتك لهذا اللغز **{player_points} نقطة** (تم خصم {base_points // 2}).")
        else:
            st.caption(f"ℹ️ تم طلب المساعدة من قبل {st.session_state.hint_requester}. بالنسبة لك، جائزتك كاملة: **{player_points} نقطة**.")

    if st.session_state.last_status:
        st.markdown(st.session_state.last_status, unsafe_allow_html=True)

    # 1. لعبة الأرقام
    if st.session_state.game_type == "numbers":
        max_l = st.session_state.max_limit
        st.subheader(f"🔢 خمّن الرقم السري (0 - {max_l})")
        
        if not st.session_state.solved and not st.session_state.hint_requester:
            if st.button(f"💡 طلب مساعدة (يُخصم {base_points // 2} نقطة من صاحب الطلب فقط)"):
                st.session_state.hint_requester = current_player
                st.rerun()
                
        if st.session_state.hint_requester:
            sec = st.session_state.secret_num
            low = max(0, sec - (max_l // 6))
            high = min(max_l, sec + (max_l // 6))
            st.markdown(f"<div class='hint-box'>💡 <b>مساعدة:</b> الرقم يقع بالتأكيد بين <b>{low}</b> و <b>{high}</b>!</div>", unsafe_allow_html=True)

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
                    st.session_state.last_status = f"<div style='color:#4ade80; font-weight:bold; font-size:20px;'>🎉 إجابة صحيحة يا {current_player}! الرقم هو ({sec}) (+{player_points} نقطة)</div>"
                    st.session_state.scores[current_player] += player_points
                    st.session_state.solved = True
                    trigger_win_effects()
                    st.rerun()

    # 2. لعبة الكلمات
    elif st.session_state.game_type == "words":
        st.subheader("🔤 رتّب الحروف واكتشف الكلمة:")
        st.markdown(f"## ` {st.session_state.scrambled_word} `")
        
        if not st.session_state.solved and not st.session_state.hint_requester:
            if st.button(f"💡 كشف الحرف الأول (يُخصم {base_points // 2} نقطة من صاحب الطلب فقط)"):
                st.session_state.hint_requester = current_player
                st.rerun()
                
        if st.session_state.hint_requester:
            first_letter = st.session_state.secret_word[0]
            st.markdown(f"<div class='hint-box'>💡 <b>مساعدة:</b> الكلمة تبدأ بحرف: <b>'{first_letter}'</b></div>", unsafe_allow_html=True)

        word_guess = st.text_input("اكتب الكلمة الصحيحة:", disabled=st.session_state.solved, key="word_in").strip()
        
        if not st.session_state.solved:
            if st.button("تحقق من الكلمة 🚀"):
                if normalize_arabic(word_guess) == normalize_arabic(st.session_state.secret_word):
                    st.session_state.last_status = f"<div style='color:#4ade80; font-weight:bold; font-size:20px;'>🎉 إجابة صحيحة يا {current_player}! الكلمة هي: {st.session_state.secret_word} (+{player_points} نقطة)</div>"
                    st.session_state.scores[current_player] += player_points
                    st.session_state.solved = True
                    trigger_win_effects()
                    st.rerun()
                else:
                    st.session_state.last_status = f"<div style='color:#f87171; font-weight:bold; font-size:18px;'>❌ إجابة خاطئة! الكلمة ليست '{word_guess}'. ينتقل الدور للاعب التالي!</div>"
                    next_turn()
                    st.rerun()

    # 3. لعبة الحيوانات
    elif st.session_state.game_type == "animals":
        st.subheader("🦁 من أكون؟ اقرأ التلميحات وخمّن الكائن:")
        for idx, clue in enumerate(st.session_state.animal_data["clues"], 1):
            st.write(f"💡 **تلميح {idx}:** {clue}")

        if not st.session_state.solved and not st.session_state.hint_requester:
            if st.button(f"💡 كشف تلميح ذهبي (يُخصم {base_points // 2} نقطة من صاحب الطلب فقط)"):
                st.session_state.hint_requester = current_player
                st.rerun()

        if st.session_state.hint_requester:
            st.markdown(f"<div class='hint-box'>💡 <b>تلميح إضافي خاص:</b> {st.session_state.animal_data['hint']}</div>", unsafe_allow_html=True)

        animal_guess = st.text_input("اسم الحيوان / الكائن:", disabled=st.session_state.solved, key="animal_in").strip()
        
        if not st.session_state.solved:
            if st.button("تحقق من الإجابة 🚀"):
                target = st.session_state.animal_data["animal"]
                if normalize_arabic(animal_guess) == normalize_arabic(target):
                    st.session_state.last_status = f"<div style='color:#4ade80; font-weight:bold; font-size:20px;'>🎉 إجابة صحيحة يا بطل {current_player}! هو بالفعل {st.session_state.animal_data['display']} (+{player_points} نقطة)</div>"
                    st.session_state.scores[current_player] += player_points
                    st.session_state.solved = True
                    trigger_win_effects()
                    st.rerun()
                else:
                    st.session_state.last_status = f"<div style='color:#f87171; font-weight:bold; font-size:18px;'>❌ إجابة خاطئة! ليس '{animal_guess}'. ينتقل الدور للاعب التالي!</div>"
                    next_turn()
                    st.rerun()

    if st.session_state.solved:
        st.write("---")
        if st.button("التخمين التالي ⏭️ (سؤال جديد)", type="primary"):
            next_turn()
            setup_new_challenge()
            st.rerun()

    st.write("---")
    c_back, c_end = st.columns(2)
    with c_back:
        if st.button("⬅ العودة لاختيار الألعاب"):
            st.session_state.last_status = None
            st.session_state.page = "choose_game"
            st.rerun()
    with c_end:
        if st.button("🚪 إنهاء الجلسة"):
            st.session_state.page = "exit"
            st.rerun()

# ----------------- 6. صفحة التتويج الخاصة بالجلسة فقط -----------------
elif st.session_state.page == "exit":
    st.title("🏆 النتائج النهائية للجلسة الحالية")
    
    if st.session_state.scores:
        sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
        st.success("انتهت الجلسة! إليكم ترتيب المتنافسين:")
        for rank, (player, score) in enumerate(sorted_scores, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🎖️"
            st.write(f"### {medal} المركز {rank}: {player} ⟵ {score} نقطة")
    else:
        st.info("لم يتم تسجيل نقاط في هذه الجلسة.")

    st.write("---")
    if st.button("🔄 بدء جلسة جديدة تماماً"):
        st.session_state.page = "menu"
        st.session_state.scores = {}
        st.session_state.players = []
        st.rerun()
