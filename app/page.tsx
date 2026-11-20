"use client";

import { useState } from "react";
import {
  Activity, ArrowLeft, ArrowUpLeft, BookOpen, BrainCircuit, CalendarDays,
  Check, ChevronLeft, CircleHelp, Clock3, GraduationCap, Home, Layers3,
  Menu, MessageCircle, Plus, Search, Send, Settings2, Sparkles, Target,
  TrendingUp, Trophy, X, Zap
} from "lucide-react";

const subjects = [
  { name: "اللغة العربية", short: "ع", color: "coral", progress: 72 },
  { name: "اللغة الإنجليزية", short: "EN", color: "blue", progress: 58 },
  { name: "الرياضيات", short: "∑", color: "violet", progress: 84 },
  { name: "التاريخ", short: "ت", color: "amber", progress: 46 }
];

const features = [
  { icon: MessageCircle, title: "المعلم الذكي", desc: "اسأل عن أي نقطة وخد شرحًا خطوة بخطوة.", tone: "blue", tag: "متاح الآن" },
  { icon: Target, title: "تدريب مخصص", desc: "أسئلة على مستواك مع تصحيح وشرح الإجابات.", tone: "violet", tag: "تدرب بذكاء" },
  { icon: BookOpen, title: "مكتبة المذاكرة", desc: "نظّم دروسك وملاحظاتك ومصادرك في مكان واحد.", tone: "amber", tag: "قريبًا" },
  { icon: Activity, title: "تحليل تقدمك", desc: "اعرف نقاط قوتك والموضوعات التي تحتاج مراجعة.", tone: "green", tag: "متابعة مستمرة" }
];

export default function HomePage() {
  const [active, setActive] = useState("الرئيسية");
  const [prompt, setPrompt] = useState("");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [notice, setNotice] = useState("");

  const nav = [
    { label: "الرئيسية", icon: Home },
    { label: "المعلم الذكي", icon: MessageCircle },
    { label: "المواد الدراسية", icon: Layers3 },
    { label: "الامتحانات", icon: Target },
    { label: "البطاقات الذكية", icon: BrainCircuit },
    { label: "تحليل الأداء", icon: TrendingUp }
  ];

  function submitPrompt() {
    if (!prompt.trim()) return;
    setNotice("واجهة تجريبية: سيتم ربط المحادثة بمحرك الذكاء الاصطناعي في المرحلة التالية.");
    setPrompt("");
  }

  return (
    <main className="app-shell">
      <aside className={`sidebar ${mobileOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-mark"><GraduationCap size={24} strokeWidth={2.2} /></div>
          <div><strong>StudyGPT <span>Pro</span></strong><small>مساحتك للتعلّم الذكي</small></div>
          <button className="mobile-close" onClick={() => setMobileOpen(false)} aria-label="إغلاق القائمة"><X size={19}/></button>
        </div>
        <div className="workspace-label">مساحة الطالب</div>
        <nav className="side-nav">
          {nav.map(({label, icon: Icon}) => (
            <button key={label} className={`nav-item ${active === label ? "active" : ""}`} onClick={() => {setActive(label);setMobileOpen(false);}}>
              <Icon size={19}/><span>{label}</span>{label === "المعلم الذكي" && <i className="nav-dot"/>}
            </button>
          ))}
        </nav>
        <div className="sidebar-spacer"/>
        <div className="sidebar-tip">
          <div className="tip-icon"><Sparkles size={17}/></div>
          <strong>خطوة صغيرة كل يوم</strong>
          <p>الاستمرار أهم من عدد ساعات المذاكرة.</p>
          <div className="tip-progress"><span/></div>
          <small>هدفك اليومي · 3 من 5 جلسات</small>
        </div>
        <button className="nav-item settings"><Settings2 size={19}/><span>الإعدادات</span></button>
        <div className="profile">
          <div className="avatar">ط</div>
          <div className="profile-text"><strong>حساب الطالب</strong><small>البكالوريا المصرية</small></div>
          <button className="profile-more" aria-label="خيارات الحساب">···</button>
        </div>
      </aside>

      {mobileOpen && <button className="scrim" onClick={() => setMobileOpen(false)} aria-label="إغلاق القائمة"/>}

      <section className="main-area">
        <header className="topbar">
          <div className="topbar-right">
            <button className="menu-toggle" onClick={() => setMobileOpen(true)} aria-label="فتح القائمة"><Menu size={21}/></button>
            <div className="breadcrumb">مساحة الطالب <ChevronLeft size={15}/> <b>{active}</b></div>
          </div>
          <div className="topbar-left">
            <div className="today"><CalendarDays size={16}/> الجمعة، 20 نوفمبر</div>
            <button className="icon-button" aria-label="البحث"><Search size={19}/></button>
            <div className="top-avatar">ط</div>
          </div>
        </header>

        <div className="content">
          <section className="welcome-row">
            <div>
              <div className="eyebrow"><span className="eyebrow-line"/> منصتك التعليمية في مكان واحد</div>
              <h1>أهلاً بك في <span>StudyGPT Pro</span></h1>
              <p className="welcome-sub">خلّي مذاكرتك أذكى. افهم، اتدرّب، وشوف تقدمك خطوة بخطوة.</p>
            </div>
            <div className="welcome-badge"><div className="badge-orbit"><GraduationCap size={28}/></div><span>تعلّم<br/>بثقة</span></div>
          </section>

          <section className="hero-panel">
            <div className="hero-copy">
              <div className="hero-kicker"><Sparkles size={15}/> مساعدك الدراسي الذكي</div>
              <h2>سؤالك هو أول<br/><em>خطوة للفهم.</em></h2>
              <p>اسأل، ارفع سؤالًا من كتابك، أو اطلب شرح فكرة صعبة — وابدأ من حيث أنت.</p>
              <div className="hero-actions">
                <button className="primary-btn" onClick={() => setActive("المعلم الذكي")}>ابدأ جلسة مذاكرة <ArrowLeft size={17}/></button>
                <span className="secure-note"><Check size={14}/> شرح منظم يناسب مستواك</span>
              </div>
            </div>
            <div className="hero-art" aria-hidden="true">
              <div className="art-glow"/>
              <div className="art-orbit orbit-one"/>
              <div className="art-orbit orbit-two"/>
              <div className="book-stack"><div className="book book-back"/><div className="book book-mid"/><div className="book book-front"><span>STUDY<br/>SMART</span><GraduationCap size={30}/></div></div>
              <div className="floating-note note-one"><BrainCircuit size={17}/><span>فهم أعمق</span></div>
              <div className="floating-note note-two"><Zap size={17}/><span>تقدّم مستمر</span></div>
              <div className="spark spark-a">✦</div><div className="spark spark-b">✧</div>
            </div>
            <div className="hero-bottom"><span>01</span><div/><span>تعلّم بطريقتك، وبالسرعة المناسبة لك</span></div>
          </section>

          <section className="section-block">
            <div className="section-heading"><div><span className="section-kicker">YOUR LEARNING SPACE</span><h3>ابدأ من هنا</h3><p>كل أدواتك الأساسية علشان تذاكر بتركيز.</p></div><button className="text-link" onClick={() => setActive("المواد الدراسية")}>عرض الكل <ArrowLeft size={15}/></button></div>
            <div className="feature-grid">
              {features.map(({icon: Icon,title,desc,tone,tag}) => (
                <button className="feature-card" key={title} onClick={() => {setActive(title === "المعلم الذكي" ? title : title === "تحليل تقدمك" ? "تحليل الأداء" : title);setNotice(`قسم ${title} ضمن نموذج التصميم الأولي.`);}}>
                  <div className={`feature-icon ${tone}`}><Icon size={21}/></div>
                  <span className="feature-tag">{tag}</span>
                  <strong>{title}</strong><p>{desc}</p>
                  <span className="card-arrow"><ArrowUpLeft size={17}/></span>
                </button>
              ))}
            </div>
          </section>

          <section className="lower-grid">
            <div className="panel subjects-panel">
              <div className="panel-heading"><div><span className="section-kicker">YOUR SUBJECTS</span><h3>موادك الدراسية</h3></div><button className="round-link" onClick={() => setActive("المواد الدراسية")}><ArrowLeft size={16}/></button></div>
              <div className="subject-list">
                {subjects.map(s => <div className="subject-row" key={s.name}><div className={`subject-symbol ${s.color}`}>{s.short}</div><div className="subject-info"><strong>{s.name}</strong><div className="progress-track"><span style={{width:s.progress+"%"}}/></div></div><b>{s.progress}%</b></div>)}
              </div>
              <div className="panel-footnote"><CircleHelp size={14}/> المواد المعروضة نموذج أولي قابل للتعديل حسب المسار الدراسي.</div>
            </div>
            <div className="panel progress-panel">
              <div className="panel-heading"><div><span className="section-kicker">WEEKLY OVERVIEW</span><h3>نظرة على أسبوعك</h3></div><span className="week-pill">هذا الأسبوع</span></div>
              <div className="stats-row"><div><span className="stat-label">وقت المذاكرة</span><strong>— <small>ساعة</small></strong></div><div><span className="stat-label">جلسات مكتملة</span><strong>— <small>جلسة</small></strong></div></div>
              <div className="empty-chart"><div className="chart-lines"><i/><i/><i/><i/></div><div className="chart-bars">{[34,52,43,76,58,88,28].map((v,i)=><div key={i} className="bar-col"><span style={{height:v+"%"}}/><small>{["س","ح","ن","ث","ر","خ","ج"][i]}</small></div>)}</div></div>
              <p className="chart-caption"><Trophy size={14}/> بيانات الأداء الحقيقية هتظهر بعد ربط حسابك.</p>
            </div>
          </section>

          <section className="ask-panel">
            <div className="ask-icon"><MessageCircle size={20}/></div>
            <div className="ask-copy"><strong>في نقطة واقفة معاك؟</strong><span>اكتب سؤالك وابدأ مع المعلم الذكي.</span></div>
            <div className="ask-input"><input value={prompt} onChange={e=>setPrompt(e.target.value)} onKeyDown={e=>e.key==="Enter"&&submitPrompt()} placeholder="مثلاً: اشرح لي الفكرة دي ببساطة..." /><button onClick={submitPrompt} aria-label="إرسال السؤال"><Send size={17}/></button></div>
          </section>
          {notice && <div className="notice" role="status"><Check size={16}/>{notice}<button onClick={()=>setNotice("")} aria-label="إغلاق"><X size={15}/></button></div>}
          <footer><span>© 2026 StudyGPT Pro</span><span>صُممت لتجعل التعلّم أوضح وأسهل.</span><span className="footer-status"><i/> نسخة تصميم تجريبية</span></footer>
        </div>
      </section>
    </main>
  );
}
