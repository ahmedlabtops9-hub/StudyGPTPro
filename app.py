import streamlit as st
import requests
import json
import time
from datetime import datetime

# ==============================================================================
# 1. إعدادات النظام والتهيئة الأساسية (System Configuration)
# ==============================================================================
st.set_page_config(
    page_title="StudyGPT Enterprise | منصة البكالوريا الذكية",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ضع مفتاح Google AI Studio الخاص بك هنا
API_KEY = st.secrets.get("GEMINI_API_KEY", "my_secret_key")

GEMINI_MODEL = "gemini-2.5-flash"
BASE_URL = "https://googleapis.com"

SUBJECTS = {
    "البرمجة والذكاء الاصطناعي 💻": {
        "code": "CS-201",
        "role": "أستاذ أول في علوم الحاسب والذكاء الاصطناعي وتطوير البرمجيات",
        "color": "#38bdf8"
    },
    "التاريخ والحضارة 🏛️": {
        "code": "HIS-202",
        "role": "خبير ومؤرخ متخصص في مناهج التاريخ للصف الثاني الثانوي",
        "color": "#f59e0b"
    },
    "اللغة العربية والنحو 📖": {
        "code": "ARB-203",
        "role": "كبير معلمي اللغة العربية والنحو والبلاغة والأدب",
        "color": "#10b981"
    },
    "الفيزياء الحديثة ⚡": {
        "code": "PHY-204",
        "role": "أستاذ الفيزياء المتخصص في تبسيط القوانين والمسائل الفيزيائية",
        "color": "#818cf8"
    },
    "الرياضيات البحتة والتطبيقية 📐": {
        "code": "MTH-205",
        "role": "أستاذ الرياضيات المتخصص في التفاضل وحساب المثلثات والجبر",
        "color": "#f43f5e"
    },
    "الكيمياء 🧪": {
        "code": "CHM-206",
        "role": "أستاذ الكيمياء المتخصص في المعادلات والتفاعلات الكيميائية",
        "color": "#a855f7"
    },
    "اللغة الإنجليزية 🌍": {
        "code": "ENG-207",
        "role": "خبير تدريس اللغة الإنجليزية والقواعد والترجمة",
        "color": "#06b6d4"
    },
    "الأحياء 🧬": {
        "code": "BIO-208",
        "role": "أستاذ الأحياء والعلوم البيولوجية للصف الثاني الثانوي",
        "color": "#22c55e"
    }
}

# ==============================================================================
# 2. محرك التصميم الفاخر (Luxury Dark Glassmorphism CSS Engine)
# ==============================================================================
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://googleapis.com');

        html, body, [class*="css"] {
            font-family: 'Cairo', sans-serif !important;
            direction: rtl;
            text-align: right;
        }

        .stApp {
            background: radial-gradient(circle at 10% 10%, #13182e 0%, #080a10 50%, #040508 100%);
            color: #f8fafc;
        }

        #MainMenu, footer, header {visibility: hidden;}

        /* الشريط الجانبي الزجاجي */
        [data-testid="stSidebar"] {
            background: rgba(12, 16, 28, 0.92) !important;
            backdrop-filter: blur(20px);
            border-left: 1px solid rgba(99, 102, 241, 0.25);
        }

        /* بانر الهيدر الرئيسي */
        .enterprise-header {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(129, 140, 248, 0.35);
            border-radius: 22px;
            padding: 26px 32px;
            margin-bottom: 22px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.14);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
            padding: 5px 16px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .main-heading {
            font-size: 38px;
            font-weight: 900;
            background: linear-gradient(90deg, #ffffff 0%, #a5b4fc 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            line-height: 1.25;
        }

        .sub-heading {
            color: #94a3b8;
            font-size: 16px;
            margin-top: 8px;
        }

        /* بطاقات الإحصائيات */
        .kpi-card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 16px;
            padding: 18px 20px;
            text-align: center;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        .kpi-value {
            font-size: 30px;
            font-weight: 900;
            color: #818cf8;
        }
        .kpi-label {
            font-size: 13px;
            color: #94a3b8;
            font-weight: 600;
        }

        /* بطاقة الفلاش كارد التفاعلية */
        .flashcard-box {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 2px solid rgba(99, 102, 241, 0.45);
            border-radius: 24px;
            padding: 45px 35px;
            text-align: center;
            min-height: 240px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
            margin: 20px 0;
        }
        .flashcard-tag {
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1px;
            padding: 4px 14px;
            border-radius: 20px;
            margin-bottom: 18px;
        }
        .flashcard-text {
            font-size: 24px;
            font-weight: 800;
            color: #f8fafc;
            line-height: 1.6;
        }

        /* الأزرار الاحترافية */
        .stButton > button {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)) !important;
            color: #f1f5f9 !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
            border-radius: 14px !important;
            padding: 12px 18px !important;
            font-weight: 700 !important;
            transition: all 0.25s ease !important;
            width: 100%;
        }

        .stButton > button:hover {
            border-color: #818cf8 !important;
            background: linear-gradient(145deg, rgba(67, 56, 202, 0.75), rgba(30, 27, 75, 0.95)) !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.35) !important;
        }

        /* فقاعات المحادثة */
        [data-testid="stChatMessage"] {
            background: rgba(17, 24, 39, 0.82) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 18px !important;
            padding: 16px 22px !important;
            margin-bottom: 14px !important;
        }

        /* التبويبات */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background: rgba(15, 23, 42, 0.6);
            padding: 8px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 10px 20px;
            font-weight: 700;
            color: #94a3b8;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(79, 70, 229, 0.3) !important;
            color: #ffffff !important;
            border: 1px solid rgba(129, 140, 248, 0.5) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. إدارة حالة الجلسة والبيانات (State & Analytics Manager)
# ==============================================================================
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

# ==============================================================================
# 4. محرك الذكاء الاصطناعي (Gemini AI Core Engine)
# ==============================================================================
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
                                text_chunk = data_obj["candidates"]["content"]["parts"]["text"]
                                yield text_chunk
                            except Exception:
                                continue
        except Exception as e:
            yield f"⚠️ حدث خطأ في الاتصال بالخادم الذكي: {str(e)}"

    @staticmethod
    def generate_structured_json(prompt):
