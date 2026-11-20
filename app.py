import json
import os
import streamlit as st
import requests
import time

st.set_page_config(page_title="StudyGPT Pro", page_icon="🎓", layout="wide")

MODEL = "gemini-3.8-flash"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
SUBJECTS = {
    "اللغة العربية": "معلم لغة عربية ونحو وبلاغة",
    "اللغة الإنجليزية": "معلم لغة إنجليزية",
    "الرياضيات": "معلم رياضيات",
    "الفيزياء": "معلم فيزياء",
    "الكيمياء": "معلم كيمياء",
    "الأحياء": "معلم أحياء",
    "التاريخ": "معلم تاريخ",
    "الجغرافيا": "معلم جغرافيا",
    "البرمجة والذكاء الاصطناعي": "معلم برمجة وعلوم حاسب",
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
html,body,[class*="css"]{font-family:'Cairo',sans-serif}
.stApp{background:radial-gradient(ellipse at 12% 0%,#172b4b 0%,#091321 42%,#07101c 100%);color:#f8fafc}
[data-testid="stSidebar"]{background:#0b1728}
[data-testid="stMarkdownContainer"],[data-testid="stChatMessageContent"]{direction:rtl;text-align:right}
.hero{padding:26px 30px;border-radius:20px;margin:4px 0 22px;background:linear-gradient(120deg,#173766,#101c30);border:1px solid #315887}
.hero h1{font-size:38px;font-weight:900;margin:4px 0}
.hero p{color:#c5d5e9}
.stButton>button,.stDownloadButton>button{border-radius:11px;background:#172d49;color:white;border:1px solid #365b83;font-weight:700;min-height:42px}
[data-testid="stMetric"]{background:#14243a;border:1px solid #2b4564;padding:12px;border-radius:14px}
</style>
""", unsafe_allow_html=True)

def api_key():
    try:
        value = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        value = ""
    return (value or os.getenv("GEMINI_API_KEY", "")).strip()

def gemini(contents, system_instruction, json_mode=False):
    key = api_key()
    if not key:
        raise RuntimeError("مفتاح Gemini غير مضبوط. أضف GEMINI_API_KEY في Streamlit Secrets.")
    config = {"temperature": 0.6, "maxOutputTokens": 4096}
    if json_mode:
        config["responseMimeType"] = "application/json"
    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": contents,
        "generationConfig": config,
    }
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}
    response = None
    for attempt in range(3):
        try:
            response = requests.post(
                ENDPOINT,
                headers=headers,
                json=payload,
                timeout=75,
            )
        except requests.RequestException as error:
            if attempt < 2:
                time.sleep(2 ** attempt * 2)
                continue
            raise RuntimeError("تعذر الاتصال بخدمة Gemini بعد 3 محاولات. تحقق من الاتصال وحاول لاحقًا.") from error

        if response.status_code == 503 and attempt < 2:
            time.sleep(2 ** attempt * 3)
            continue
        break

    if response is None:
        raise RuntimeError("تعذر الوصول إلى خدمة Gemini. حاول مرة أخرى لاحقًا.")

    if response.status_code != 200:
        try:
            message = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            message = response.text
        if response.status_code == 503:
            raise RuntimeError(
                "خدمة Gemini عليها ضغط مرتفع حاليًا. حاولنا تلقائيًا 3 مرات ولم تتوفر الخدمة. "
                "المشكلة من جهة خوادم Gemini وليست من إجابتك. انتظر قليلًا ثم أعد المحاولة."
            )
        raise RuntimeError(f"Gemini API ({response.status_code}): {message}")
    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini لم يرجع إجابة. حاول مرة أخرى.")
    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(part.get("text", "") for part in parts).strip()
    if not text:
        raise RuntimeError("وصل رد فارغ من Gemini.")
    return text

def parse_json(prompt):
    raw = gemini(
        [{"role": "user", "parts": [{"text": prompt}]}],
        "أعد JSON صالحًا فقط دون Markdown أو شرح خارجي.",
        True,
    )
    return json.loads(raw)

def init_state():
    defaults = {
        "messages": [], "question_count": 0, "exam_history": [],
        "exam_data": None, "exam_result": None, "cards": [],
        "card_index": 0, "card_flipped": False,
        "activity": {name: 0 for name in SUBJECTS},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

with st.sidebar:
    st.markdown("## 🎓 StudyGPT Pro")
    st.caption("المساعد التعليمي الذكي لطلاب مصر")
    grade = st.selectbox("المرحلة الدراسية", [
        "المرحلة الإعدادية", "الصف الأول الثانوي", "الصف الثاني الثانوي",
        "الصف الثالث الثانوي", "البكالوريا"
    ])
    subject = st.selectbox("المادة", list(SUBJECTS))
    style = st.selectbox("أسلوب الشرح", [
        "شرح مبسط خطوة بخطوة", "شرح تفصيلي", "ملخص في نقاط", "أمثلة وتطبيقات"
    ])
    st.divider()
    left, right = st.columns(2)
    left.metric("الأسئلة", st.session_state.question_count)
    right.metric("الامتحانات", len(st.session_state.exam_history))
    if st.button("محادثة جديدة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.session_state.messages:
        transcript = "\n\n".join(
            ("الطالب: " if m["role"] == "user" else "StudyGPT: ") + m["content"]
            for m in st.session_state.messages
        )
        st.download_button("تحميل المحادثة", transcript, "StudyGPT.txt", use_container_width=True)
    st.divider()
    st.caption("نسخة تجريبية. راجع المعلومات المهمة مع كتابك ومعلمك.")

st.markdown("""
<div class="hero">
<div style="color:#7dd3fc;font-weight:800">YOUR AI LEARNING COMPANION</div>
<h1>StudyGPT Pro</h1>
<p>افهم دروسك، تدرب على الامتحانات، وتابع تقدمك في مكان واحد.</p>
</div>
""", unsafe_allow_html=True)

tutor, exams, flashcards, analytics = st.tabs([
    "💬 المعلم الذكي", "📝 محاكي الامتحانات", "🧠 البطاقات الذكية", "📊 تحليل الأداء"
])

with tutor:
    st.subheader("اسأل المعلم الذكي")
    st.caption(f"{grade} • {subject}")
    q1, q2, q3 = st.columns(3)
    quick = None
    if q1.button("اختبر فهمي", use_container_width=True):
        quick = f"اختبر فهمي في {subject} بسؤال واحد، وانتظر إجابتي قبل كشف الحل."
    if q2.button("لخص الدرس", use_container_width=True):
        quick = f"لخص أهم موضوعات {subject} لطلاب {grade}."
    if q3.button("خطة مراجعة", use_container_width=True):
        quick = f"ضع خطة مراجعة لمدة 7 أيام لمادة {subject}."
    for item in st.session_state.messages:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])
    typed = st.chat_input(f"اكتب سؤالك في {subject}...")
    prompt = quick or typed
    if prompt:
        history = list(st.session_state.messages)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.question_count += 1
        st.session_state.activity[subject] += 1
        with st.chat_message("user"):
            st.markdown(prompt)
        instructions = (
            f"أنت {SUBJECTS[subject]} لطلاب {grade}. أسلوب الشرح: {style}. "
            "أجب بالعربية الواضحة، ونظم الشرح بعناوين وأمثلة. لا تخترع معلومات "
            "أو تدّع أن المحتوى من كتاب الوزارة دون تحقق. ساعد الطالب على الفهم."
        )
        with st.chat_message("assistant"):
            with st.spinner("StudyGPT يفكر..."):
                try:
                    contents = []
                    for message in history:
                        role = "model" if message["role"] == "assistant" else "user"
                        contents.append({"role": role, "parts": [{"text": message["content"]}]})
                    contents.append({"role": "user", "parts": [{"text": prompt}]})
                    answer = gemini(contents, instructions)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as error:
                    st.error(str(error))

with exams:
    st.subheader("أنشئ امتحانًا تدريبيًا")
    with st.form("exam_setup"):
        topic = st.text_input("اسم الدرس أو الوحدة", placeholder="مثال: قوانين نيوتن أو النحو")
        level = st.selectbox("مستوى الصعوبة", ["سهل", "متوسط", "متقدم"])
        count = st.selectbox("عدد الأسئلة", [5, 10, 15])
        create = st.form_submit_button("إنشاء الامتحان", use_container_width=True)
    if create:
        if not topic.strip():
            st.warning("اكتب اسم الدرس أولًا.")
        else:
            prompt = (
                f"أنشئ {count} أسئلة اختيار من متعدد باللغة العربية في {subject} "
                f"لمرحلة {grade} عن {topic} بمستوى {level}. أعد JSON فقط بالشكل "
                '{"questions":[{"question":"السؤال","options":["أ","ب","ج","د"],'
                '"answer_index":0,"explanation":"التفسير"}]}. '
                "answer_index رقم من صفر إلى ثلاثة."
            )
            with st.spinner("يتم إنشاء الامتحان..."):
                try:
                    data = parse_json(prompt)
                    questions = data.get("questions", [])
                    if not questions:
                        raise ValueError("لم يتم إنشاء أسئلة.")
                    for item in questions:
                        if len(item["options"]) != 4 or item["answer_index"] not in [0, 1, 2, 3]:
                            raise ValueError("صيغة أحد الأسئلة غير صحيحة.")
                    st.session_state.exam_data = {
                        "topic": topic, "subject": subject, "questions": questions
                    }
                    st.session_state.exam_result = None
                    st.rerun()
                except Exception as error:
                    st.error(f"تعذر إنشاء الامتحان: {error}")
    if st.session_state.exam_data:
        exam = st.session_state.exam_data
        st.divider()
        st.markdown(f"### امتحان: {exam['topic']}")
        with st.form("exam_answers"):
            chosen = []
            for i, question in enumerate(exam["questions"]):
                st.markdown(f"**س{i + 1}: {question['question']}**")
                chosen.append(st.radio(
                    "اختر الإجابة", question["options"], index=None,
                    key=f"answer_{i}_{exam['topic']}", label_visibility="collapsed"
                ))
            submitted = st.form_submit_button("تصحيح الامتحان", use_container_width=True)
        if submitted:
            if any(answer is None for answer in chosen):
                st.warning("أجب عن جميع الأسئلة قبل التصحيح.")
            else:
                correct = sum(
                    chosen[i] == question["options"][question["answer_index"]]
                    for i, question in enumerate(exam["questions"])
                )
                score = round(correct / len(exam["questions"]) * 100)
                st.session_state.exam_result = {"chosen": chosen, "correct": correct, "score": score}
                st.session_state.exam_history.append({
                    "subject": exam["subject"], "topic": exam["topic"],
                    "score": score, "total": len(exam["questions"])
                })
                st.rerun()
        if st.session_state.exam_result:
            result = st.session_state.exam_result
            st.success(f"نتيجتك: {result['correct']} من {len(exam['questions'])} — {result['score']}%")
            for i, question in enumerate(exam["questions"]):
                answer = question["options"][question["answer_index"]]
                if result["chosen"][i] == answer:
                    st.success(f"السؤال {i + 1}: صحيح")
                else:
                    st.error(f"السؤال {i + 1}: الصحيح هو {answer}")
                st.write(question.get("explanation", ""))
            if st.button("امتحان جديد"):
                st.session_state.exam_data = None
                st.session_state.exam_result = None
                st.rerun()

with flashcards:
    st.subheader("البطاقات الذكية")
    with st.form("cards_setup"):
        card_topic = st.text_input("موضوع البطاقات", placeholder="مصطلحات البرمجة أو مفاهيم التاريخ...")
        card_count = st.selectbox("عدد البطاقات", [5, 8, 10])
        make_cards = st.form_submit_button("إنشاء البطاقات", use_container_width=True)
    if make_cards:
        if not card_topic.strip():
            st.warning("اكتب موضوع البطاقات.")
        else:
            prompt = (
                f"أنشئ {card_count} بطاقات مراجعة بالعربية في {subject} لطلاب {grade} "
                f"عن {card_topic}. أعد JSON بالشكل "
                '{"cards":[{"front":"سؤال أو مصطلح","back":"إجابة مختصرة دقيقة"}]}.'
            )
            with st.spinner("يتم إنشاء البطاقات..."):
                try:
                    data = parse_json(prompt)
                    st.session_state.cards = data.get("cards", [])
                    if not st.session_state.cards:
                        raise ValueError("لم تصل بطاقات صالحة.")
                    st.session_state.card_index = 0
                    st.session_state.card_flipped = False
                    st.rerun()
                except Exception as error:
                    st.error(f"تعذر إنشاء البطاقات: {error}")
    if st.session_state.cards:
        cards = st.session_state.cards
        index = st.session_state.card_index
        card = cards[index]
        st.progress((index + 1) / len(cards), text=f"بطاقة {index + 1} من {len(cards)}")
        label = "الإجابة" if st.session_state.card_flipped else "السؤال"
        visible = card["back"] if st.session_state.card_flipped else card["front"]
        st.markdown(
            f'<div class="hero" style="text-align:center;min-height:170px">'
            f'<div style="color:#7dd3fc">{label}</div><h2>{visible}</h2></div>',
            unsafe_allow_html=True,
        )
        flip, previous, following = st.columns(3)
        if flip.button("اقلب البطاقة", use_container_width=True):
            st.session_state.card_flipped = not st.session_state.card_flipped
            st.rerun()
        if previous.button("السابقة", disabled=index == 0, use_container_width=True):
            st.session_state.card_index -= 1
            st.session_state.card_flipped = False
            st.rerun()
        if following.button("التالية", disabled=index == len(cards) - 1, use_container_width=True):
            st.session_state.card_index += 1
            st.session_state.card_flipped = False
            st.rerun()

with analytics:
    st.subheader("تحليل الأداء")
    history = st.session_state.exam_history
    average = round(sum(x["score"] for x in history) / len(history)) if history else 0
    best = max((x["score"] for x in history), default=0)
    a, b, c = st.columns(3)
    a.metric("الأسئلة", st.session_state.question_count)
    b.metric("الامتحانات", len(history))
    c.metric("متوسط الدرجات", f"{average}%")
    st.divider()
    st.markdown("#### نشاط المذاكرة حسب المادة")
    st.bar_chart(st.session_state.activity)
    st.markdown("#### سجل الامتحانات")
    if history:
        st.dataframe(
            [{"المادة": x["subject"], "الموضوع": x["topic"],
              "الدرجة": f"{x['score']}%", "عدد الأسئلة": x["total"]} for x in reversed(history)],
            use_container_width=True, hide_index=True
        )
        st.metric("أعلى نتيجة", f"{best}%")
    else:
        st.info("ستظهر نتائجك هنا بعد حل أول امتحان.")

st.divider()
st.caption("StudyGPT Pro • منصة تعليمية تجريبية • Gemini AI")
