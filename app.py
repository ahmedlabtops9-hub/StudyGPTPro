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
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');
:root{color-scheme:light}
html,body,[class*="css"]{font-family:'Cairo',sans-serif}
.stApp,[data-testid="stAppViewContainer"]{background:#f4f7fb;color:#17263d}
[data-testid="stHeader"]{background:rgba(244,247,251,.92)}
.block-container{max-width:1180px;padding-top:2rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#101f35;border-left:1px solid #263b57}
[data-testid="stSidebar"] *{color:#edf4ff}
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:#1b304c;border-color:#38516f}
[data-testid="stMarkdownContainer"],[data-testid="stChatMessageContent"]{direction:rtl;text-align:right;color:#17263d}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{line-height:1.9}
.hero{padding:30px 34px;border-radius:22px;margin:4px 0 24px;background:linear-gradient(115deg,#12243c 0%,#1d4266 62%,#167d83 100%);border:1px solid #294b68;box-shadow:0 14px 36px rgba(18,36,60,.12);color:#fff}
.hero h1{font-size:clamp(30px,4vw,42px);font-weight:900;margin:5px 0;color:#fff;letter-spacing:-.6px}
.hero p{color:#dce9f4;font-size:16px;margin-bottom:0}
.stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"] button{border-radius:12px;background:#173d5d;color:#fff;border:1px solid #244f70;font-weight:700;min-height:44px;transition:all .18s ease}
.stButton>button:hover,.stDownloadButton>button:hover{background:#0f766e;border-color:#0f766e;color:#fff}
[data-testid="stMetric"]{background:#fff;border:1px solid #e1e8f0;padding:15px;border-radius:15px;box-shadow:0 5px 18px rgba(26,45,70,.045)}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"]{color:#17263d}
[data-testid="stTabs"] button{font-family:'Cairo',sans-serif;font-weight:700;color:#52647a}
[data-testid="stTabs"] button[aria-selected="true"]{color:#0f766e;border-bottom-color:#0f766e}
[data-testid="stChatMessage"]{background:#fff;border:1px solid #e5ebf2;border-radius:16px;padding:14px 18px;margin:10px 0;box-shadow:0 4px 14px rgba(20,40,65,.035)}
[data-testid="stChatInput"]{background:#fff;border:1px solid #cbd7e4;border-radius:16px;box-shadow:0 8px 24px rgba(25,45,70,.08)}
[data-testid="stChatInput"] textarea,[data-testid="stChatInput"] textarea:focus{background:#fff!important;color:#17263d!important;-webkit-text-fill-color:#17263d!important;caret-color:#0f766e!important;opacity:1!important}
[data-testid="stChatInput"] textarea::placeholder{color:#8291a4!important;-webkit-text-fill-color:#8291a4!important;opacity:1!important}
[data-testid="stChatInput"] button{color:#0f766e!important}
.stTextInput input,.stTextArea textarea{background:#fff!important;color:#17263d!important;-webkit-text-fill-color:#17263d!important;border-color:#cbd7e4!important;border-radius:11px!important}
.stSelectbox [data-baseweb="select"]>div{background:#fff;color:#17263d;border-color:#cbd7e4;border-radius:11px}
.stRadio label,.stCheckbox label{color:#263a52}
hr{border-color:#e2e9f1}
@media(max-width:700px){.block-container{padding:1rem 1rem 2rem}.hero{padding:22px}.hero h1{font-size:30px}}
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
    config = {"temperature": 0.45, "maxOutputTokens": 2048}
    if json_mode:
        config["responseMimeType"] = "application/json"
    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": contents,
        "generationConfig": config,
    }
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}
    response = None
    active_model = MODEL
    model_candidates = [MODEL, "gemini-3.5-flash-lite"]
    last_error = None

    for model_index, model_name in enumerate(model_candidates):
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        for attempt in range(2):
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=75,
                )
            except requests.RequestException as error:
                last_error = error
                if attempt == 0:
                    time.sleep(2)
                    continue
                break

            if response.status_code == 200:
                active_model = model_name
                break

            if response.status_code == 503 and attempt == 0:
                time.sleep(3)
                continue

            last_error = response
            break

        if response is not None and response.status_code == 200:
            break

        if model_index == 0 and response is not None and response.status_code == 503:
            response = None
            continue
        break

    if response is None:
        raise RuntimeError(
            "تعذر الاتصال بخدمة Gemini. تحقق من الإنترنت ومفتاح API ثم حاول لاحقًا."
        ) from (last_error if isinstance(last_error, Exception) else None)

    if response.status_code != 200:
        try:
            message = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            message = response.text
        if response.status_code == 503:
            raise RuntimeError(
                "Gemini 3.8 والنموذج البديل مشغولان حاليًا. أعد المحاولة بعد قليل؛ "
                "المشكلة من توفر الخدمة وليست من صياغة سؤالك."
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
        history = list(st.session_state.messages[-6:])
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.question_count += 1
        st.session_state.activity[subject] += 1
        with st.chat_message("user"):
            st.markdown(prompt)
        instructions = (
            f"أنت {SUBJECTS[subject]} لطلاب {grade}. أسلوب الشرح: {style}. "
            "أجب بالعربية الواضحة وبشكل مباشر ومنظم. ابدأ بالإجابة، واستخدم أمثلة عند الحاجة. "
            "لا تطل بلا داعٍ، ولا تخترع معلومات أو تنسب المحتوى لكتاب الوزارة دون تحقق."
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
