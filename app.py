import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="StudyGPT Enterprise | منصة البكالوريا الذكية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_KEY = st.secrets.get("GEMINI_API_KEY", "local_key")
GEMINI_MODEL = "gemini-2.5-flash"
BASE_URL = "https://googleapis.com"

SUBJECTS = {
    "البرمجة والذكاء الاصطناعي 💻": {
        "code": "CS-201",
        "role": "أستاذ أول في علوم الحاسب والذكاء الاصطناعي وتطوير البرمجيات"
    },
    "التاريخ والحضارة 🏛️": {
        "code": "HIS-202",
        "role": "خبير ومؤرخ متخصص في مناهج التاريخ للصف الثاني الثانوي"
    },
    "اللغة العربية والنحو 📖": {
        "code": "ARB-203",
        "role": "كبير معلمي اللغة العربية والنحو والبلاغة والأدب"
    },
    "الفيزياء الحديثة ⚡": {
        "code": "PHY-204",
        "role": "أستاذ الفيزياء المتخصص في تبسيط القوانين والمسائل الفيزيائية"
    },
    "الرياضيات البحتة والتطبيقية 📐": {
        "code": "MTH-205",
        "role": "أستاذ الرياضيات المتخصص في التفاضل وحساب المثلثات والجبر"
    },
    "الكيمياء 🧪": {
        "code": "CHM-206",
        "role": "أستاذ الكيمياء المتخصص في المعادلات والتفاعلات الكيميائية"
    },
    "اللغة الإنجليزية 🌍": {
        "code": "ENG-207",
        "role": "خبير تدريس اللغة الإنجليزية والقواعد والترجمة"
    },
    "الأحياء 🧬": {
        "code": "BIO-208",
        "role": "أستاذ الأحياء والعلوم البيولوجية للصف الثاني الثانوي"
    }
}

def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://googleapis.com');

        .stApp {
            background: radial-gradient(circle at 10% 10%, #13182e 0%, #080a10 50%, #040508 100%);
            color: #f8fafc;
            font-family: 'Cairo', sans-serif;
        }

        [data-testid="stMarkdownContainer"], [data-testid="stChatMessageContent"], .enterprise-header, .flashcard-box, .kpi-card {
            font-family: 'Cairo', sans-serif !important;
            direction: rtl;
            text-align: right;
        }

        [data-testid="stSidebar"] {
            background: rgba(12, 16, 28, 0.95) !important;
            border-right: 1px solid rgba(99, 102, 241, 0.25);
        }

        .enterprise-header {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(129, 140, 248, 0.4);
            border-radius: 22px;
            padding: 26px 32px;
            margin-bottom: 22px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.55);
        }

        .status-pill {
            display: inline-block;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.45);
            padding: 5px 16px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .main-heading {
            font-size: 36px;
            font-weight: 900;
            background: linear-gradient(90deg, #ffffff 0%, #a5b4fc 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        .sub-heading {
            color: #94a3b8;
            font-size: 16px;
            margin-top: 8px;
        }

        .kpi-card {
            background: rgba(17, 24, 39, 0.85);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 18px 20px;
            text-align: center;
        }
        .kpi-value {
            font-size: 30px;
            font-weight: 900;
            color: #818cf8;
            text-align: center;
        }
        .kpi-label {
            font-size: 13px;
            color: #94a3b8;
            font-weight: 600;
            text-align: center;
        }

        .flashcard-box {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 2px solid rgba(99, 102, 241, 0.5);
            border-radius: 24px;
            padding: 45px 35px;
            text-align: center;
            min-height: 220px;
            margin: 20px 0;
        }
        .flashcard-tag {
            display: inline-block;
            font-size: 12px;
            font-weight: 800;
            padding: 4px 14px;
            border-radius: 20px;
            margin-bottom: 18px;
        }
        .flashcard-text {
            font-size: 24px;
            font-weight: 800;
            color: #f8fafc;
            text-align: center;
        }

        .stButton > button {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.98)) !important;
            color: #f1f5f9 !important;
            border: 1px solid rgba(99, 102, 241, 0.45) !important;
            border-radius: 14px !important;
            padding: 12px 18px !important;
            font-weight: 700 !important;
            width: 100%;
        }

        .stButton > button:hover {
            border-color: #818cf8 !important;
            background: linear-gradient(145deg, rgba(67, 56, 202, 0.8), rgba(30, 27, 75, 0.98)) !important;
        }

        [data-testid="stChatMessage"] {
            background: rgba(17, 24, 39, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 18px !important;
            padding: 16px 22px !important;
            margin-bottom: 14px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    defaults = {
        "messages": [],
        "questions_asked": 0,
        "exams_history": [],
        "current_exam": None,
        "exam_submitted": False,
        "flashcards": [],
        "card_index": 0,
        "card_flipped": False,
        "subject_activity": {sub: 10 for sub in SUBJECTS.keys()}
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

class AIEngine:
    @staticmethod
    def stream_chat(messages_history, system_prompt):
        url = f"{BASE_URL}/{GEMINI_MODEL}:streamGenerateContent?alt=sse&key={API_KEY}"
        formatted_contents = [
            {
                "role": "user" if m["role"] == "user" else "model",
                "parts": [{"text": m["content"]}]
            }
            for m in messages_history
        ]
        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": formatted_contents,
            "generationConfig": {"temperature": 0.65}
        }
        try:
            with requests.post(url, json=payload, stream=True, timeout=35) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        decoded = line.decode("utf-8")
                        if decoded.startswith("data: "):
                            try:
                                data_obj = json.loads(decoded[6:])
                                text_chunk = data_obj["candidates"][0]["content"]["parts"][0]["text"]
                                yield text_chunk
                            except Exception:
                                continue
        except Exception as e:
            yield f"⚠️ تعذر الاتصال بالخادم الذكي: {str(e)}"

    @staticmethod
    def generate_structured_json(prompt):
        url = f"{BASE_URL}/{GEMINI_MODEL}:generateContent?key={API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.4,
                "responseMimeType": "application/json"
            }
        }
        response = requests.post(url, json=payload, timeout=40)
        response.raise_for_status()
        raw_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(raw_text)

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🎓 StudyGPT **Enterprise**")
        st.caption("منصة التعلم الذكي المتكاملة - نظام البكالوريا")
        st.divider()

        selected_subject = st.selectbox(
            "📚 اختر المادة الدراسية النشطة:",
            list(SUBJECTS.keys())
        )

        explanation_style = st.selectbox(
            "🧠 استراتيجية الشرح:",
            [
                "شرح أكاديمي مبسط مع أمثلة تطبيقية",
                "تلخيص مركز في نقاط ذهنية سريعة",
                "تحليل عميق للمفاهيم والقوانين",
                "تبسيط فائق للمبتدئين"
            ]
        )

        st.divider()
        st.markdown("### 📊 ملخص جلستك الحية")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("الأسئلة", st.session_state.questions_asked)
        with c2:
            st.metric("الامتحانات", len(st.session_state.exams_history))

        if st.session_state.messages:
            chat_export = "\n\n".join(
                [f"{'الطالب' if m['role']=='user' else 'المعلم الذكي'}:\n{m['content']}" for m in st.session_state.messages]
            )
            st.download_button(
                label="📥 تحميل ملخص الجلسة (TXT)",
                data=chat_export.encode("utf-8"),
                file_name=f"StudyGPT_Notes_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

        if st.button("🗑️ تصفير المحادثة الحالية"):
            st.session_state.messages = []
            st.rerun()

        st.divider()
        st.markdown("""
        <div style="background: rgba(79, 70, 229, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); border-radius: 14px; padding: 14px; direction: rtl; text-align: right;">
            <div style="font-weight: 800; color: #a5b4fc; font-size: 14px;">🏆 مشروع البرمجة والذكاء الاصطناعي</div>
            <div style="font-size: 12px; color: #cbd5e1; margin-top: 6px; line-height: 1.6;">
