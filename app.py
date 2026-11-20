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
    "Arabic": "معلم لغة عربية ونحو وبلاغة",
    "English": "معلم لغة إنجليزية",
    "Mathematics": "معلم رياضيات",
    "Physics": "معلم فيزياء",
    "Chemistry": "معلم كيمياء",
    "Biology": "معلم أحياء",
    "History": "معلم تاريخ",
    "Geography": "معلم جغرافيا",
    "Programming & AI": "معلم برمجة وعلوم حاسب",
}

st.session_state.setdefault("theme_mode", "Light")
theme_mode = st.sidebar.radio("Appearance", ["Light", "Dark"], horizontal=True, key="theme_mode")
if theme_mode == "Dark":
    theme = {
        "bg": "#212121", "sidebar": "#171717", "panel": "#2f2f2f",
        "text": "#ececec", "muted": "#a3a3a3", "border": "#3f3f3f",
        "input": "#303030", "hover": "#383838", "scheme": "dark"
    }
else:
    theme = {
        "bg": "#ffffff", "sidebar": "#f7f7f8", "panel": "#f7f7f8",
        "text": "#171717", "muted": "#6b7280", "border": "#e5e5e5",
        "input": "#ffffff", "hover": "#eeeeee", "scheme": "light"
    }

st.markdown("""
<style>
:root { color-scheme: __SCHEME__; }
html, body, [class*="css"] { color: __TEXT__; }
.stApp, [data-testid="stAppViewContainer"] { background: __BG__; color: __TEXT__; }
[data-testid="stHeader"] { background: __BG__; }
.block-container { max-width: 1040px; padding-top: 1.4rem; padding-bottom: 4rem; }
[data-testid="stSidebar"] { background: __SIDEBAR__; border-right: 1px solid __BORDER__; }
[data-testid="stSidebar"] * { color: __TEXT__; }
[data-testid="stMarkdownContainer"], [data-testid="stChatMessageContent"] {
  color: __TEXT__; unicode-bidi: plaintext; text-align: start;
}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {
  color: __TEXT__; line-height: 1.75;
}
.app-topbar {
  display:flex; align-items:center; justify-content:space-between;
  padding: 8px 2px 18px; border-bottom:1px solid __BORDER__;
  margin-bottom:24px; color:__TEXT__; font-size:14px;
}
.app-topbar strong { font-size:19px; letter-spacing:-.5px; }
.app-topbar span:last-child { color:__MUTED__; }
.stButton > button, .stDownloadButton > button,
[data-testid="stFormSubmitButton"] button {
  border-radius: 12px; min-height: 42px; border:1px solid __BORDER__ !important;
  background: __PANEL__ !important; color: __TEXT__ !important;
  font-weight:600; transition: background .15s ease, border-color .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
  background: __HOVER__ !important; border-color: __MUTED__ !important;
}
.stButton > button *, .stDownloadButton > button *,
[data-testid="stFormSubmitButton"] button * {
  color: __TEXT__ !important; -webkit-text-fill-color: __TEXT__ !important;
}
[data-testid="stChatMessage"] {
  background: transparent; border:0; border-radius:14px;
  padding: 12px 14px; margin: 8px 0;
}
[data-testid="stChatInput"] {
  background: __INPUT__; border:1px solid __BORDER__;
  border-radius:18px; box-shadow:0 4px 18px rgba(0,0,0,.06);
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
  background: __INPUT__ !important; color: __TEXT__ !important;
  -webkit-text-fill-color: __TEXT__ !important; caret-color: __TEXT__ !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: __MUTED__ !important; -webkit-text-fill-color: __MUTED__ !important;
}
.stTextInput input, .stTextArea textarea, .stNumberInput input {
  background: __INPUT__ !important; color: __TEXT__ !important;
  -webkit-text-fill-color: __TEXT__ !important; border:1px solid __BORDER__ !important;
  border-radius:10px !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
  color: __MUTED__ !important; -webkit-text-fill-color: __MUTED__ !important;
}
.stSelectbox [data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
  background: __INPUT__ !important; color: __TEXT__ !important;
  border:1px solid __BORDER__ !important; border-radius:10px;
}
.stSelectbox [data-baseweb="select"] *, [data-testid="stSelectbox"] [data-baseweb="select"] * {
  color: __TEXT__ !important; -webkit-text-fill-color: __TEXT__ !important;
}
[data-baseweb="popover"] [role="listbox"], [data-baseweb="popover"] [role="option"],
[data-baseweb="menu"], [data-baseweb="menu"] * {
  background: __PANEL__ !important; color: __TEXT__ !important;
  -webkit-text-fill-color: __TEXT__ !important;
}
[data-baseweb="popover"] [role="option"]:hover, [aria-selected="true"] {
  background: __HOVER__ !important;
}
[data-testid="stMetric"] {
  background: __PANEL__; border:1px solid __BORDER__;
  padding:14px; border-radius:14px;
}
[data-testid="stMetric"] * { color:__TEXT__ !important; }
[data-testid="stTabs"] button { color:__TEXT__ !important; }
[data-testid="stFileUploader"] {
  background:__PANEL__; border:1px dashed __BORDER__; border-radius:12px; padding:10px;
}
[data-testid="stFileUploader"] * { color:__TEXT__ !important; }
[data-testid="stForm"] {
  background:__PANEL__; border:1px solid __BORDER__; border-radius:14px; padding:16px;
}
[data-testid="stCaptionContainer"], small { color:__MUTED__ !important; }
[data-testid="stAlert"] { border-radius:12px; }
hr { border-color:__BORDER__; }
@media(max-width:700px) {
  .block-container { padding:1rem .8rem 2rem; }
  .app-topbar { margin-bottom:16px; }
}
</style>
""".replace("__SCHEME__", theme["scheme"])
  .replace("__TEXT__", theme["text"])
  .replace("__BG__", theme["bg"])
  .replace("__SIDEBAR__", theme["sidebar"])
  .replace("__PANEL__", theme["panel"])
  .replace("__MUTED__", theme["muted"])
  .replace("__BORDER__", theme["border"])
  .replace("__INPUT__", theme["input"])
  .replace("__HOVER__", theme["hover"]), unsafe_allow_html=True)

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
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "contents": contents,
        "generationConfig": config,
    }
    headers = {"x-goog-api-key": key, "Content-Type": "application/json"}

    # Try the preferred model first, then other current Flash/Lite models.
    # Model-specific quota exhaustion (429) moves immediately to the next model.
    model_candidates = list(dict.fromkeys([
        MODEL,
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.6-flash",
    ]))
    failures = []

    for model_name in model_candidates:
        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/"
            f"models/{model_name}:generateContent"
        )
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=payload,
                    timeout=(5, 45),
                )
            except requests.RequestException as error:
                failures.append(f"{model_name}: network error ({type(error).__name__})")
                if attempt < max_attempts - 1:
                    time.sleep(2 ** attempt)
                    continue
                break

            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    raise RuntimeError("وصل رد فارغ من Gemini. جرّب صياغة السؤال مرة أخرى.")
                parts = candidates[0].get("content", {}).get("parts", [])
                answer = "\\n".join(
                    part.get("text", "") for part in parts if part.get("text")
                )
                if not answer.strip():
                    raise RuntimeError("النموذج لم يُرجع نصًا. جرّب سؤالًا أوضح.")
                return answer.strip()

            try:
                error_data = response.json().get("error", {})
                message = error_data.get("message", response.text[:250])
                status_name = error_data.get("status", "")
            except ValueError:
                message = response.text[:250]
                status_name = ""

            status = response.status_code
            failures.append(
                f"{model_name}: HTTP {status} {status_name} {message[:180]}"
            )

            # A model-specific quota is exhausted: continue to the next model.
            if status == 429 or status == 404:
                break

            # Temporary upstream errors get a short exponential-backoff retry.
            if status in (408, 500, 502, 503, 504) and attempt < max_attempts - 1:
                retry_after = response.headers.get("Retry-After", "")
                try:
                    delay = min(max(float(retry_after), 1), 15) if retry_after else 2 ** attempt
                except ValueError:
                    delay = 2 ** attempt
                time.sleep(delay)
                continue

            # Invalid key, permission, or request errors won't improve with another model.
            raise RuntimeError(f"Gemini API ({status}): {message}")

    details = "\\n".join(failures[-8:])
    raise RuntimeError(
        "الحصة المجانية أو الخدمة غير متاحة حاليًا في نماذج Gemini التي جُرّبت. "
        "جرّب لاحقًا؛ لا توجد طريقة مضمونة لتجاوز حدود Google المجانية. "
        "تفاصيل المحاولات:\\n" + details
    )


@st.cache_data(ttl=604800, max_entries=500, show_spinner=False)
def parse_json(prompt):
    # Cache identical exam, flashcard, and curriculum-bank generation requests
    # for seven days so students can reuse the same generated material.
    raw = gemini(
        [{"role": "user", "parts": prompt if isinstance(prompt, list) else [{"text": prompt}]}],
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
                         "exam_result", "bank_questions", "bank_result", "cards", "card_index", "card_flipped", "activity"):
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
        "bank_questions", "bank_result", "cards", "card_index", "card_flipped", "activity"
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
        "exam_data": None, "exam_result": None, "bank_questions": None, "bank_result": None, "cards": [],
        "card_index": 0, "card_flipped": False,
        "activity": {name: 0 for name in SUBJECTS},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

for subject_name in SUBJECTS:
    st.session_state.activity.setdefault(subject_name, 0)

if get_user_email() and not st.session_state.get("_cloud_loaded", False):
    restore_cloud_progress()
    st.session_state["_cloud_loaded"] = True

with st.sidebar:
    st.markdown("## StudyGPT Pro")
    st.caption("AI learning workspace")
    st.caption("A flexible platform — more study stages can be added over time.")

    signed_email = get_user_email()
    if signed_email:
        st.success("Signed in")
        st.caption(signed_email)
        if st.button("Sign out", use_container_width=True):
            st.logout()
    else:
        if st.button("Continue with Google", use_container_width=True):
            try:
                st.login()
            except Exception:
                st.error("Google sign-in is not configured in Streamlit Secrets yet.")

    grade = st.selectbox("Study level", [
        "Egyptian Baccalaureate — Year 1", "Egyptian Baccalaureate — Year 2",
        "Secondary Year 1", "Secondary Year 2", "Secondary Year 3",
        "Preparatory Year 1", "Preparatory Year 2", "Preparatory Year 3",
        "Primary — Coming later"
    ])
    subject = st.selectbox("Subject", list(SUBJECTS))
    language = st.selectbox("Reply language", [
        "Auto-detect", "Arabic (Egyptian)", "Arabic (Modern Standard)", "English",
        "German", "French", "Italian", "Japanese", "Spanish", "Chinese", "Turkish", "Portuguese"
    ])
    style = st.selectbox("Teaching style", [
        "Simple step-by-step", "Detailed explanation", "Bullet-point summary", "Examples and practice"
    ])
    st.divider()
    left, right = st.columns(2)
    left.metric("Questions", st.session_state.question_count)
    right.metric("Exams", len(st.session_state.exam_history))
    if st.button("New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.session_state.messages:
        transcript = "\n\n".join(
            ("You: " if m["role"] == "user" else "StudyGPT: ") + m["content"]
            for m in st.session_state.messages
        )
        st.download_button("Export conversation", transcript, "StudyGPT.txt", use_container_width=True)
    st.divider()
    st.caption("AI-generated answers can be wrong. Verify important information with trusted study materials.")

st.markdown("""
<div class="hero">
<div style="color:var(--muted);font-weight:700;letter-spacing:.08em">YOUR PERSONAL AI LEARNING SPACE</div>
<h1>StudyGPT Pro</h1>
<p>Learn, practice, and track your progress in one workspace.</p>
</div>
""", unsafe_allow_html=True)

tutor, exams, bank, flashcards, analytics = st.tabs([
    "💬 AI Tutor", "📝 Practice Exams", "📚 Question Bank", "🧠 Flashcards", "📊 Progress"
])

if tutor:
    st.subheader("Ask your AI tutor")
    st.caption(f"{grade} • {subject} • Reply: {language}")
    uploaded_file = st.file_uploader(
        "Attach a page or question image",
        type=["pdf", "png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        help="Upload a PDF page or a clear image, then ask your question. Maximum file size: 15 MB."
    )
    if uploaded_file:
        st.caption(f"Attached: {uploaded_file.name}")
    q1, q2, q3 = st.columns(3)
    quick = None
    if q1.button("Test my understanding", use_container_width=True):
        quick = f"اختبر فهمي في {subject} بسؤال واحد، وانتظر إجابتي قبل كشف الحل."
    if q2.button("Summarize lesson", use_container_width=True):
        quick = f"لخص أهم موضوعات {subject} لطلاب {grade}."
    if q3.button("7-day revision plan", use_container_width=True):
        quick = f"ضع خطة مراجعة لمدة 7 أيام لمادة {subject}."
    for item in st.session_state.messages:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])
    typed = st.chat_input(f"Message your tutor about {subject}...")
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
            ("Automatically detect the language of the latest student message and reply in that same language. " if language == "Auto-detect" else f"Reply in {language}. ")
            "أجب بشكل مباشر ومنظم، واستخدم أمثلة عند الحاجة. "
            "إذا أرفق الطالب ملفًا أو صورة فاعتمد على محتواها أولًا، واذكر بوضوح إذا كانت معلومة غير ظاهرة أو غير مقروءة. "
            "لا تخترع معلومات أو تنسب المحتوى لكتاب الوزارة دون تحقق."
        )
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
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
                            "inlineData": {
                                "mimeType": uploaded_file.type or "application/octet-stream",
                                "data": base64.b64encode(file_bytes).decode("utf-8")
                            }
                        })
                    contents.append({"role": "user", "parts": user_parts})
                    answer = gemini(contents, instructions)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as error:
                    st.error(str(error))

if exams:
    st.subheader("Create a practice exam")
    with st.form("exam_setup"):
        topic = st.text_input("Lesson or unit", placeholder="e.g. Newton’s laws or grammar")
        level = st.selectbox("Difficulty", ["Easy", "Intermediate", "Advanced"])
        count = st.selectbox("Number of questions", [5, 10, 15])
        create = st.form_submit_button("Generate exam", use_container_width=True)
    if create:
        if not topic.strip():
            st.warning("Enter a lesson or unit first.")
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
            submitted = st.form_submit_button("Submit exam", use_container_width=True)
        if submitted:
            if any(answer is None for answer in chosen):
                st.warning("Answer every question before submitting.")
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


if bank:
    st.subheader("Curriculum question bank")
    st.caption(f"{grade} • {subject} — Build practice around a unit and lesson")
    st.info("Questions are AI-generated practice, not official ministry questions. Upload your lesson pages or PDF when you need practice grounded in a specific source.")
    with st.form("curriculum_bank_setup"):
        unit_name = st.text_input("Unit", placeholder="e.g. Unit 1")
        lesson_name = st.text_input("Lesson", placeholder="Enter lesson name")
        bank_level = st.selectbox("Question difficulty", ["Easy", "Intermediate", "Advanced"])
        bank_count = st.selectbox("Number of questions", [5, 10, 15])
        source_file = st.file_uploader(
            "Upload lesson pages or textbook (optional)",
            type=["pdf", "png", "jpg", "jpeg", "webp"],
            accept_multiple_files=False,
            key="bank_source_file",
        )
        build_bank = st.form_submit_button("Generate lesson questions", use_container_width=True)
    if build_bank:
        if not unit_name.strip() or not lesson_name.strip():
            st.warning("Enter the unit and lesson first.")
        else:
            bank_prompt = (
                f"أنشئ {bank_count} سؤال اختيار من متعدد باللغة العربية لطلاب {grade} "
                f"في مادة {subject}، الوحدة: {unit_name}، الدرس: {lesson_name}، "
                f"بمستوى {bank_level}. "
                "إذا أرفق الطالب مصدرًا، التزم بالمعلومات الواردة فيه فقط ولا تضف معلومات من خارجه. "
                "إذا لم يرفق مصدرًا، أنشئ تدريبًا عامًا مناسبًا للموضوع ولا تدّعِ أنه من كتاب الوزارة. "
                "نوّع بين الفهم والتطبيق والتذكر، وتجنب تكرار الأسئلة. "
                "أعد JSON فقط بالشكل "
                '{"questions":[{"question":"نص السؤال","options":["أ","ب","ج","د"],'
                '"answer_index":0,"explanation":"سبب صحة الإجابة"}]}. '
                "answer_index عدد صحيح من صفر إلى ثلاثة."
            )
            try:
                user_parts = [{"text": bank_prompt}]
                if source_file is not None:
                    source_bytes = source_file.getvalue()
                    if len(source_bytes) > 15 * 1024 * 1024:
                        raise ValueError("حجم الملف أكبر من 15 ميجابايت.")
                    user_parts.append({
                        "inlineData": {
                            "mimeType": source_file.type or "application/octet-stream",
                            "data": base64.b64encode(source_bytes).decode("utf-8"),
                        }
                    })
                with st.spinner("يتم إعداد أسئلة الوحدة والدرس..."):
                    bank_data = parse_json(user_parts)
                questions = bank_data.get("questions", [])
                if not questions:
                    raise ValueError("لم يتم إنشاء أسئلة صالحة.")
                for question in questions:
                    if (not isinstance(question.get("question"), str)
                        or len(question.get("options", [])) != 4
                        or question.get("answer_index") not in [0, 1, 2, 3]):
                        raise ValueError("وصل سؤال بتنسيق غير صحيح. حاول مرة أخرى.")
                st.session_state.bank_questions = {
                    "grade": grade, "subject": subject, "unit": unit_name,
                    "lesson": lesson_name, "questions": questions,
                }
                st.session_state.bank_result = None
                st.rerun()
            except Exception as error:
                st.error(f"تعذر إنشاء بنك الأسئلة: {error}")
    if st.session_state.bank_questions:
        bank_data = st.session_state.bank_questions
        st.divider()
        st.markdown(f"### {bank_data['unit']} — {bank_data['lesson']}")
        st.caption(f"{bank_data['grade']} • {bank_data['subject']} • {len(bank_data['questions'])} أسئلة")
        with st.form("curriculum_bank_answers"):
            bank_answers = []
            for idx, question in enumerate(bank_data["questions"]):
                st.markdown(f"**س{idx + 1}: {question['question']}**")
                bank_answers.append(st.radio(
                    "اختر الإجابة", question["options"], index=None,
                    key=f"bank_answer_{idx}_{bank_data['lesson']}",
                    label_visibility="collapsed",
                ))
            bank_submit = st.form_submit_button("Submit answers", use_container_width=True)
        if bank_submit:
            if any(answer is None for answer in bank_answers):
                st.warning("أجب عن جميع الأسئلة قبل التصحيح.")
            else:
                correct_count = sum(
                    bank_answers[idx] == question["options"][question["answer_index"]]
                    for idx, question in enumerate(bank_data["questions"])
                )
                bank_score = round(correct_count / len(bank_data["questions"]) * 100)
                st.session_state.bank_result = {
                    "answers": bank_answers, "correct": correct_count, "score": bank_score,
                }
                st.session_state.exam_history.append({
                    "subject": bank_data["subject"],
                    "topic": f"{bank_data['unit']} - {bank_data['lesson']}",
                    "score": bank_score, "total": len(bank_data["questions"]),
                })
                st.rerun()
        if st.session_state.bank_result:
            result = st.session_state.bank_result
            st.success(f"نتيجتك: {result['correct']} من {len(bank_data['questions'])} — {result['score']}%")
            for idx, question in enumerate(bank_data["questions"]):
                correct_answer = question["options"][question["answer_index"]]
                if result["answers"][idx] == correct_answer:
                    st.success(f"السؤال {idx + 1}: إجابة صحيحة")
                else:
                    st.error(f"السؤال {idx + 1}: الإجابة الصحيحة هي {correct_answer}")
                st.write(question.get("explanation", ""))
        if st.button("Create a new question set", key="new_bank_questions"):
            st.session_state.bank_questions = None
            st.session_state.bank_result = None
            st.rerun()


if flashcards:
    st.subheader("Flashcards")
    with st.form("cards_setup"):
        card_topic = st.text_input("Flashcard topic", placeholder="مصطلحات البرمجة أو مفاهيم التاريخ...")
        card_count = st.selectbox("Number of cards", [5, 8, 10])
        make_cards = st.form_submit_button("Generate flashcards", use_container_width=True)
    if make_cards:
        if not card_topic.strip():
            st.warning("Enter a flashcard topic.")
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
        label = "Answer" if st.session_state.card_flipped else "Question"
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
        if previous.button("Previous", disabled=index == 0, use_container_width=True):
            st.session_state.card_index -= 1
            st.session_state.card_flipped = False
            st.rerun()
        if following.button("Next", disabled=index == len(cards) - 1, use_container_width=True):
            st.session_state.card_index += 1
            st.session_state.card_flipped = False
            st.rerun()

if analytics:
    st.subheader("Learning progress")
    history = st.session_state.exam_history
    average = round(sum(x["score"] for x in history) / len(history)) if history else 0
    best = max((x["score"] for x in history), default=0)
    a, b, c = st.columns(3)
    a.metric("Questions", st.session_state.question_count)
    b.metric("Exams", len(history))
    c.metric("Average score", f"{average}%")
    st.divider()
    st.markdown("#### Study activity by subject")
    st.bar_chart(st.session_state.activity)
    st.markdown("#### Exam history")
    if history:
        st.dataframe(
            [{"Subject": x["subject"], "Topic": x["topic"],
              "Score": f"{x['score']}%", "Questions": x["total"]} for x in reversed(history)],
            use_container_width=True, hide_index=True
        )
        st.metric("Best score", f"{best}%")
    else:
        st.info("Your results will appear here after your first exam.")

st.divider()
if get_user_email():
    if persist_cloud_progress():
        st.caption("Your progress has been saved to your account.")
    else:
        st.warning("Cloud saving is not configured. Check the Supabase settings.")
else:
    st.caption("Sign in with Google to enable cloud progress after setup.")
st.caption("StudyGPT Pro • AI-powered learning workspace")
