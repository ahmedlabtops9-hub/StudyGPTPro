import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="StudyGPT Enterprise", page_icon="🎓", layout="wide")

API_KEY = st.secrets.get("GEMINI_API_KEY", "local_key")
GEMINI_MODEL = "gemini-2.5-flash"
BASE_URL = "https://googleapis.com"

SUBJECTS = {
    "البرمجة والذكاء الاصطناعي 💻": "أستاذ أول في علوم الحاسب والذكاء الاصطناعي وتطوير البرمجيات",
    "التاريخ والحضارة 🏛️": "خبير ومؤرخ متخصص في مناهج التاريخ للصف الثاني الثانوي",
    "اللغة العربية والنحو 📖": "كبير معلمي اللغة العربية والنحو والبلاغة والأدب",
    "الفيزياء الحديثة ⚡": "أستاذ الفيزياء المتخصص في تبسيط القوانين والمسائل الفيزيائية",
    "الرياضيات البحتة والتطبيقية 📐": "أستاذ الرياضيات المتخصص في التفاضل وحساب المثلثات والجبر",
    "الكيمياء 🧪": "أستاذ الكيمياء المتخصص في المعادلات والتفاعلات الكيميائية",
    "اللغة الإنجليزية 🌍": "خبير تدريس اللغة الإنجليزية والقواعد والترجمة",
    "الأحياء 🧬": "أستاذ الأحياء والعلوم البيولوجية للصف الثاني الثانوي"
}

st.markdown("""
<style>
@import url('https://googleapis.com');
.stApp {
    background: radial-gradient(circle at 10% 10%, #13182e 0%, #080a10 50%, #040508 100%);
    color: #f8fafc;
    font-family: 'Cairo', sans-serif;
}
[data-testid="stMarkdownContainer"], [data-testid="stChatMessageContent"], .hero-card, .fc-card, .kpi-box {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
    text-align: right;
}
[data-testid="stSidebar"] {
    background: rgba(12, 16, 28, 0.96) !important;
}
.hero-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.75), rgba(15, 23, 42, 0.95));
    border: 1px solid rgba(129, 140, 248, 0.4);
    border-radius: 20px;
    padding: 24px 30px;
    margin-bottom: 20px;
}
.badge {
    display: inline-block;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.45);
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 10px;
}
.title-grad {
    font-size: 34px;
    font-weight: 900;
    background: linear-gradient(90deg, #ffffff, #a5b4fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.kpi-box {
    background: rgba(17, 24, 39, 0.85);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 16px;
    padding: 16px;
    text-align: center;
}
.fc-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 2px solid rgba(99, 102, 241, 0.5);
    border-radius: 22px;
    padding: 40px 30px;
    text-align: center;
    margin: 18px 0;
}
.stButton > button {
    background: linear-gradient(145deg, #1e293b, #0f172a) !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(99, 102, 241, 0.45) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    width: 100%;
}
[data-testid="stChatMessage"] {
    background: rgba(17, 24, 39, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
}
</style>
""", unsafe_allow_html=True)

for k, v in {
    "messages": [],
    "q_count": 0,
    "exams": [],
    "exam_data": None,
    "exam_done": False,
    "cards": [],
    "c_idx": 0,
    "c_flip": False,
    "activity": {s: 10 for s in SUBJECTS}
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def stream_gemini(history, sys_prompt):
    url = f"{BASE_URL}/{GEMINI_MODEL}:streamGenerateContent?alt=sse&key={API_KEY}"
    contents = [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]} for m in history]
    payload = {"system_instruction": {"parts": [{"text": sys_prompt}]}, "contents": contents}
    try:
        with requests.post(url, json=payload, stream=True, timeout=35) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line and line.startswith(b"data: "):
                    try:
                        chunk = json.loads(line[6:].decode("utf-8"))
                        yield chunk["candidates"]["content"]["parts"]["text"]
                    except Exception:
                        continue
    except Exception as e:
        yield f"⚠️ خطأ في الاتصال: {e}"

def get_json_gemini(prompt):
    url = f"{BASE_URL}/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
    r = requests.post(url, json=payload, timeout=40)
    r.raise_for_status()
    return json.loads(r.json()["candidates"]["content"]["parts"]["text"])

with st.sidebar:
    st.markdown("## 🎓 StudyGPT **Enterprise**")
    st.caption("منصة البكالوريا الذكية المتكاملة")
    st.divider()
    subject = st.selectbox("📚 المادة الدراسية:", list(SUBJECTS.keys()))
    style = st.selectbox("🧠 أسلوب الشرح:", ["شرح مبسط وأمثلة", "تلخيص في نقاط", "تحليل عميق"])
    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("الأسئلة", st.session_state.q_count)
    c2.metric("الامتحانات", len(st.session_state.exams))
    if st.session_state.messages:
        txt = "\n\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        st.download_button("📥 تحميل ملخص الجلسة", txt.encode("utf-8"), "StudyGPT_Notes.txt")
    if st.button("🗑️ محادثة جديدة"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info("🏆 مشروع البرمجة والذكاء الاصطناعي\nالصف الثاني الثانوي (بكالوريا)")

st.markdown(f"""
<div class="hero-card">
    <div class="badge">🟢 النظام نشط • {subject}</div>
    <h1 class="title-grad">StudyGPT Enterprise Platform</h1>
    <p style="color:#94a3b8; margin-top:6px;">منصة ذكاء اصطناعي للشرح المباشر، محاكاة الامتحانات بالتصحيح الفوري، والبطاقات الذكية.</p>
</div>
""", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["💬 المعلم الذكي", "🎯 محاكي الامتحانات", "🗂️ البطاقات الذكية", "📊 تحليل الأداء"])

with t1:
    b1, b2, b3, b4 = st.columns(4)
    qp = None
    if b1.button("🗺️ خريطة ذهنية"):
        qp = f"اعمل خريطة ذهنية لأهم أفكار مادة {subject} للصف الثاني الثانوي."
    if b2.button("⚡ أهم القوانين والمفاهيم"):
        qp = f"لخص أهم قوانين ومفاهيم مادة {subject} في نقاط سريعة."
    if b3.button("🧩 سؤال تفكير عليا"):
        qp = f"اعطني سؤال تفكير عليا في مادة {subject} واشرح حله."
    if b4.button("📅 خطة مراجعة"):
        qp = f"ضع خطة مراجعة سريعة لمادة {subject} في 7 أيام."

    for m in st.session_state.messages:
        with st.chat_message(m["role"], avatar="🧑‍🎓" if m["role"] == "user" else "🤖"):
            st.markdown(m["content"])

    inp = st.chat_input(f"اسأل أي سؤال في {subject}...")
    prompt = qp if qp else inp
    if prompt:
        st.session_state.q_count += 1
        st.session_state.activity[subject] += 15
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)
        sys_p = f"أنت {SUBJECTS[subject]} لطلاب الصف الثاني الثانوي. الأسلوب: {style}. أجب بالعربية بوضوح وتنظيم."
        with st.chat_message("assistant", avatar="🤖"):
            reply = st.write_stream(stream_gemini(st.session_state.messages, sys_p))
        st.session_state.messages.append({"role": "assistant", "content": reply})

with t2:
    col_a, col_b = st.columns()
    topic = col_a.text_input("اسم الدرس للامتحان:", placeholder="مثال: الخوارزميات، الدولة العباسية، النحو...")
    num_q = col_b.selectbox("عدد الأسئلة:",)
    if st.button("🚀 ابدأ الامتحان الآن") and topic.strip():
        with st.spinner("جاري إعداد الامتحان..."):
            p = f'أنشئ {num_q} أسئلة اختيار من متعدد بالعربية في مادة {subject} عن "{topic}". أعد JSON فقط كقائمة كائنات بها: "question", "options" (4 اختيارات), "answer_index" (0-3), "explanation".'
            try:
                st.session_state.exam_data = {"topic": topic, "qs": get_json_gemini(p)}
                st.session_state.exam_done = False
                st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

    if st.session_state.exam_data:
        ed = st.session_state.exam_data
        ans = {}
        for i, q in enumerate(ed["qs"]):
            st.markdown(f"**س{i+1}: {q['question']}**")
            ch = st.radio("اختر:", q["options"], key=f"q_{i}", label_visibility="collapsed")
            ans[i] = q["options"].index(ch)
        if st.button("✅ تصحيح الامتحان"):
            st.session_state.exam_done = True
            sc = round(sum(1 for i, q in enumerate(ed["qs"]) if ans[i] == q["answer_index"]) / len(ed["qs"]) * 100)
            st.session_state.exams.append({"sub": subject, "topic": ed["topic"], "score": sc})
            st.session_state.activity[subject] += sc // 2
        if st.session_state.exam_done:
            sc = round(sum(1 for i, q in enumerate(ed["qs"]) if ans[i] == q["answer_index"]) / len(ed["qs"]) * 100)
            st.success(f"🏆 نتيجتك: {sc}%")
            for i, q in enumerate(ed["qs"]):
                if ans[i] == q["answer_index"]:
                    st.info(f"✅ س{i+1} صحيح: {q['explanation']}")
                else:
                    st.error(f"❌ س{i+1} خطأ | الصحيح: {q['options'][q['answer_index']]} — {q['explanation']}")

with t3:
    fc_t = st.text_input("موضوع البطاقات الذكية:", placeholder="مثال: مصطلحات البرمجة، قوانين الفيزياء...")
    if st.button("✨ توليد 5 بطاقات") and fc_t.strip():
        with st.spinner("جاري التصميم..."):
            p = f'أنشئ 5 بطاقات تعليمية بالعربية في مادة {subject} عن "{fc_t}". أعد JSON فقط كقائمة كائنات بها: "front" (سؤال/مصطلح), "back" (الإجابة).'
            try:
                st.session_state.cards = get_json_gemini(p)
                st.session_state.c_idx = 0
                st.session_state.c_flip = False
                st.rerun()
            except Exception as e:
                st.error(f"خطأ: {e}")

    if st.session_state.cards:
