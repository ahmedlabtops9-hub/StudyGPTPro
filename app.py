import base64
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
:root{color-scheme:dark}
html,body,[class*="css"]{font-family:'Cairo',sans-serif;color:#f4f7fc}
.stApp,[data-testid="stAppViewContainer"]{background:radial-gradient(ellipse at 82% 4%,rgba(36,105,190,.34),transparent 34%),linear-gradient(135deg,#07101e 0%,#0b1729 54%,#102747 100%);color:#f4f7fc}
[data-testid="stHeader"]{background:rgba(7,16,30,.82)}
.block-container{max-width:1280px;padding-top:1.7rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#101e35 0%,#0a1425 100%);border-right:1px solid #294366}
[data-testid="stSidebar"] *{color:#f4f7fc}
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:#172943;border:1px solid #3b567b;color:#fff}
[data-testid="stSidebar"] [data-baseweb="select"] *{color:#fff!important}
[data-testid="stMarkdownContainer"],[data-testid="stChatMessageContent"]{direction:rtl;text-align:right;color:#f4f7fc}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{line-height:1.9;color:#f4f7fc}
.hero{padding:30px 34px;border-radius:20px;margin:4px 0 24px;background:linear-gradient(115deg,#102847 0%,#173d69 58%,#087fae 100%);border:1px solid #315b87;box-shadow:0 14px 38px rgba(0,0,0,.24);color:#fff}
.hero h1,.hero p{color:#fff}
.hero h1{font-size:clamp(30px,4vw,42px);font-weight:900;margin:5px 0;letter-spacing:-.6px}
.hero p{font-size:16px;margin-bottom:0}
.stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"] button{border-radius:11px;background:linear-gradient(105deg,#287cf0,#12a5ce)!important;color:#fff!important;border:1px solid #398edc!important;font-weight:700;min-height:44px;transition:all .18s ease}
.stButton>button *, .stDownloadButton>button *, [data-testid="stFormSubmitButton"] button *{color:#fff!important;-webkit-text-fill-color:#fff!important}
.stButton>button:hover,.stDownloadButton>button:hover,[data-testid="stFormSubmitButton"] button:hover{filter:brightness(1.12);border-color:#75c8f5!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,#142b49,#1b3557);border:1px solid #36577e;padding:15px;border-radius:14px;box-shadow:0 7px 20px rgba(0,0,0,.18)}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"],[data-testid="stMetric"] *{color:#fff!important}
[data-testid="stTabs"]{background:transparent}
[data-testid="stTabs"] button{font-family:'Cairo',sans-serif;font-weight:700;color:#dce8f7!important}
[data-testid="stTabs"] button[aria-selected="true"]{color:#fff!important;border-bottom-color:#35a9f0}
[data-testid="stChatMessage"]{background:linear-gradient(145deg,#142944,#1b3554);border:1px solid #36577e;border-radius:15px;padding:14px 18px;margin:10px 0;box-shadow:0 5px 16px rgba(0,0,0,.16)}
[data-testid="stChatMessage"] *{color:#f4f7fc!important}
[data-testid="stChatInput"]{background:#172943;border:1px solid #45658d;border-radius:14px;box-shadow:0 7px 22px rgba(0,0,0,.18)}
[data-testid="stChatInput"] textarea,[data-testid="stChatInput"] textarea:focus{background:#172943!important;color:#fff!important;-webkit-text-fill-color:#fff!important;caret-color:#fff!important;opacity:1!important}
[data-testid="stChatInput"] textarea::placeholder{color:#b9c9df!important;-webkit-text-fill-color:#b9c9df!important;opacity:1!important}
[data-testid="stChatInput"] button{color:#fff!important}
.stTextInput input,.stTextArea textarea{background:#172943!important;color:#fff!important;-webkit-text-fill-color:#fff!important;border-color:#45658d!important;border-radius:10px!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#b9c9df!important;-webkit-text-fill-color:#b9c9df!important}
.stSelectbox [data-baseweb="select"]>div{background:#172943;color:#fff;border:1px solid #45658d;border-radius:10px}
.stSelectbox [data-baseweb="select"] *{color:#fff!important}
.stRadio label,.stCheckbox label{color:#f4f7fc!important}
[data-testid="stFileUploader"]{background:#142944;border:1px dashed #52749c;border-radius:12px;padding:10px}
[data-testid="stFileUploader"] *{color:#f4f7fc!important}
[data-testid="stDataFrame"],[data-testid="stTable"]{background:#142944}
[data-testid="stAlert"]{border-radius:12px}
hr{border-color:#294362}
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

    config = {"temperature": 0.4, "maxOutputTokens": 900}
    if json_mode:
        config["responseMimeType"] = "application/json"

    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": contents,
        "generationConfig": config,
    }
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}

    # Start with the low-latency model; use the stronger Flash model only as fallback.
    model_candidates = ["gemini-3.8-flash"]
    last_error = None

    for model_name in model_candidates:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=20,
            )
        except requests.RequestException as error:
            last_error = error
            continue

        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if not candidates:
                raise RuntimeError("وصل رد فارغ من Gemini. جرّب صياغة السؤال مرة أخرى.")
            parts = candidates[0].get("content", {}).get("parts", [])
            answer = "\n".join(part.get("text", "") for part in parts if part.get("text"))
            if not answer.strip():
                raise RuntimeError("النموذج لم يُرجع نصًا. جرّب سؤالًا أوضح.")
            return answer.strip()

        last_error = response
        # Move to the fallback immediately on temporary overload; do not wait through
        # multiple long retries that make the student wait.
        if response.status_code in (429, 500, 502, 503, 504):
            continue

        try:
            message = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            message = response.text
        raise RuntimeError(f"Gemini API ({response.status_code}): {message}")

    if isinstance(last_error, requests.Response):
        if last_error.status_code in (429, 500, 502, 503, 504):
            raise RuntimeError(
                "خدمة Gemini مشغولة حاليًا. جرّب بعد دقيقة؛ قلّلنا وقت الانتظار لكن توفر الخدمة خارج تحكم التطبيق."
            )
        raise RuntimeError(f"تعذر الاتصال بـ Gemini: {last_error.text[:300]}")
    raise RuntimeError(
        "الاتصال بـ Gemini استغرق وقتًا أطول من المتوقع. تحقق من الاتصال وحاول مرة أخرى."
    )

def parse_json(prompt):
    raw = gemini(
        [{"role": "user", "parts": [{"text": prompt}]}],
        "أعد JSON صالحًا فقط دون Markdown أو شرح خارجي.",
        True,
    )
    return json.loads(raw)

def get_cloud_settings():
    try:
        url = st.secrets.get("SUPABASE_URL", "").rstrip("/")
        key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY", "")
        return url, key
    except Exception:
        return "", ""

def get_user_email():
    try:
        if st.user.is_logged_in:
            return str(st.user.email).strip().lower()
    except Exception:
        pass
    return ""

def restore_cloud_progress():
    url, key, email = *get_cloud_settings(), get_user_email()
    if not (url and key and email):
        return False
    headers = {"apikey": key, "Authorization": f"Bearer {key}"}
    try:
        response = requests.get(
            f"{url}/rest/v1/study_progress",
            headers=headers,
            params={"user_email": f"eq.{email}", "select": "data", "limit": "1"},
            timeout=12,
        )
        if response.status_code == 200 and response.json():
            saved = response.json()[0].get("data", {})
            for name in ("messages", "question_count", "exam_history", "exam_data",
                         "exam_result", "cards", "card_index", "card_flipped", "activity"):
                if name in saved:
                    st.session_state[name] = saved[name]
            return True
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return False
    return False

def persist_cloud_progress():
    url, key = get_cloud_settings()
    email = get_user_email()
    if not (url and key and email):
        return False
    data = {name: st.session_state.get(name) for name in (
        "messages", "question_count", "exam_history", "exam_data", "exam_result",
        "cards", "card_index", "card_flipped", "activity"
    )}
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }
    try:
        response = requests.post(
            f"{url}/rest/v1/study_progress",
            headers=headers,
            json={"user_email": email, "data": data},
            timeout=12,
        )
        return response.status_code in (200, 201, 204)
    except requests.RequestException:
        return False

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

if get_user_email() and not st.session_state.get("_cloud_loaded", False):
    restore_cloud_progress()
    st.session_state["_cloud_loaded"] = True

with st.sidebar:
    st.markdown("## 🎓 StudyGPT Pro")
    st.caption("المساعد التعليمي الذكي لطلاب مصر")

    signed_email = get_user_email()
    if signed_email:
        st.success("تم تسجيل الدخول")
        st.caption(signed_email)
        if st.button("تسجيل الخروج", use_container_width=True):
            st.logout()
    else:
        if st.button("تسجيل الدخول بحساب Google", use_container_width=True):
            try:
                st.login()
            except Exception:
                st.error("إعداد Google OAuth غير مكتمل في Streamlit Secrets.")

    grade = st.selectbox("المرحلة الدراسية", [
        "الصف الأول الإعدادي", "الصف الثاني الإعدادي", "الصف الثالث الإعدادي",
        "الصف الأول الثانوي", "الصف الثاني الثانوي", "الصف الثالث الثانوي",
        "البكالوريا المصرية"
    ])
    subject = st.selectbox("المادة", list(SUBJECTS))
    language = st.selectbox("لغة الشرح", [
        "العربية المصرية", "العربية الفصحى", "English"
    ])
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
<div style="color:#ffffff;font-weight:800">SMART LEARNING • MADE FOR STUDENTS</div>
<h1>StudyGPT Pro</h1>
<p>افهم دروسك، تدرب على الامتحانات، وتابع تقدمك في مكان واحد.</p>
</div>
""", unsafe_allow_html=True)

tutor, exams, flashcards, analytics = st.tabs([
    "💬 المعلم الذكي", "📝 محاكي الامتحانات", "🧠 البطاقات الذكية", "📊 تحليل الأداء"
])

with tutor:
    st.subheader("اسأل المعلم الذكي")
    st.caption(f"{grade} • {subject} • {language}")
    uploaded_file = st.file_uploader(
        "اسأل كتابك أو صورة السؤال",
        type=["pdf", "png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        help="ارفع صفحة PDF أو صورة واضحة، ثم اكتب سؤالك في مربع المحادثة. الحد الأقصى 15 ميجابايت."
    )
    if uploaded_file:
        st.caption(f"الملف المرفق: {uploaded_file.name}")
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
        history = list(st.session_state.messages[-4:])
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.question_count += 1
        st.session_state.activity[subject] += 1
        with st.chat_message("user"):
            st.markdown(prompt)
        instructions = (
            f"أنت {SUBJECTS[subject]} لطلاب {grade}. أسلوب الشرح: {style}. "
            f"لغة الإجابة المطلوبة: {language}. إذا اختار الطالب العربية المصرية فاستخدم تعبيرات مصرية تعليمية واضحة دون مبالغة. "
            "أجب بشكل مباشر ومنظم، واستخدم أمثلة عند الحاجة. "
            "إذا أرفق الطالب ملفًا أو صورة فاعتمد على محتواها أولًا، واذكر بوضوح إذا كانت معلومة غير ظاهرة أو غير مقروءة. "
            "لا تخترع معلومات أو تنسب المحتوى لكتاب الوزارة دون تحقق."
        )
        with st.chat_message("assistant"):
            with st.spinner("StudyGPT يفكر..."):
                try:
                    contents = []
                    for message in history:
                        role = "model" if message["role"] == "assistant" else "user"
                        contents.append({"role": role, "parts": [{"text": message["content"]}]})
                    user_parts = [{"text": prompt}]
                    if uploaded_file is not None:
                        file_bytes = uploaded_file.getvalue()
                        if len(file_bytes) > 15 * 1024 * 1024:
                            raise ValueError("حجم الملف أكبر من 15 ميجابايت. ارفع ملفًا أصغر.")
                        user_parts.append({
                            "inline_data": {
                                "mime_type": uploaded_file.type or "application/octet-stream",
                                "data": base64.b64encode(file_bytes).decode("utf-8")
                            }
                        })
                    contents.append({"role": "user", "parts": user_parts})
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
if get_user_email():
    if persist_cloud_progress():
        st.caption("تم حفظ تقدمك على حسابك.")
    else:
        st.warning("الحفظ السحابي غير جاهز. راجع إعدادات Supabase.")
else:
    st.caption("سجّل الدخول بحساب Google لتفعيل حفظ تقدمك بعد إعداد الخدمة.")
st.caption("StudyGPT Pro • منصة تعليمية تجريبية • Gemini AI")
