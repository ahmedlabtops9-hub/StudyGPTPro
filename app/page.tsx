"use client";

import { useMemo, useState } from "react";
import {
  Activity, ArrowLeft, ArrowUpLeft, BookOpen, BrainCircuit, CalendarDays,
  CheckCircle2, ChevronDown, ChevronLeft, CircleHelp, Clock3, FileText,
  GraduationCap, Home, Layers3, Library, Menu, MessageCircle, Plus, Search,
  Send, Settings2, Sparkles, Target, TrendingUp, Trophy, X, Zap, Bookmark,
  ClipboardList, Bell, Play, ShieldCheck, Video, CalendarCheck, ListChecks
} from "lucide-react";

type Section = "الرئيسية" | "المعلم الذكي" | "المواد الدراسية" | "الامتحانات" | "البطاقات الذكية" | "مكتبة المذاكرة" | "جدولي" | "تحليل الأداء" | "مجموعات المدرسين" | "الإعدادات";

const subjects = [
  { name: "اللغة العربية", short: "ع", color: "coral" },
  { name: "اللغة الإنجليزية", short: "EN", color: "blue" },
  { name: "الرياضيات", short: "∑", color: "violet" },
  { name: "التاريخ", short: "ت", color: "amber" },
  { name: "البرمجة", short: "</>", color: "green" }
];

const navigation: { label: Section; icon: any }[] = [
  { label: "الرئيسية", icon: Home },
  { label: "المعلم الذكي", icon: MessageCircle },
  { label: "المواد الدراسية", icon: Layers3 },
  { label: "الامتحانات", icon: Target },
  { label: "البطاقات الذكية", icon: BrainCircuit },
  { label: "مكتبة المذاكرة", icon: Library },
  { label: "جدولي", icon: CalendarDays },
  { label: "تحليل الأداء", icon: TrendingUp },
  { label: "مجموعات المدرسين", icon: GraduationCap }
];

const sampleSchedule = [
  { day: "الأحد", time: "04:00 م", title: "حصة اللغة العربية", duration: "90 دقيقة", kind: "درس" },
  { day: "الإثنين", time: "06:30 م", title: "مراجعة الرياضيات", duration: "60 دقيقة", kind: "مذاكرة" },
  { day: "الثلاثاء", time: "05:00 م", title: "حصة اللغة الإنجليزية", duration: "90 دقيقة", kind: "درس" }
];

export default function HomePage() {
  const [active, setActive] = useState<Section>("الرئيسية");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [stage, setStage] = useState("الأولى بكالوريا");
  const [subject, setSubject] = useState("اللغة العربية");
  const [question, setQuestion] = useState("");
  const [query, setQuery] = useState("");
  const [notice, setNotice] = useState("");
  const [task, setTask] = useState("");
  const [tasks, setTasks] = useState(["مراجعة درس النحو", "حل تدريبات الوحدة الأولى"]);
  const [done, setDone] = useState<string[]>([]);
  const [sessionTitle, setSessionTitle] = useState("");
  const [sessionTime, setSessionTime] = useState("");
  const [sessions, setSessions] = useState(sampleSchedule);
  const [quizCount, setQuizCount] = useState("10");
  const [quizType, setQuizType] = useState("متنوع");
  const [quizNotice, setQuizNotice] = useState("");
  const [groupCode, setGroupCode] = useState("");
  const [cardIndex, setCardIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [saved, setSaved] = useState<string[]>([]);
  const [fileName, setFileName] = useState("");

  const filteredSubjects = useMemo(() => subjects.filter(s => s.name.includes(query.trim())), [query]);
  const heading = active === "الرئيسية" ? "مساحة تعلّمك" : active;

  function go(section: Section) {
    setActive(section);
    setMobileOpen(false);
    setNotice("");
  }

  function addTask() {
    if (!task.trim()) return;
    setTasks(current => [...current, task.trim()]);
    setTask("");
  }

  function askTutor() {
    if (!question.trim()) return;
    setNotice("تم تسجيل السؤال في الواجهة. لتوليد إجابة حقيقية مرتبطة بمذكرتك، يجب توصيل واجهة الخادم بمزود الذكاء الاصطناعي وفهرس الملفات.");
  }

  function addSession() {
    if (!sessionTitle.trim() || !sessionTime) return;
    setSessions(current => [...current, { day: "موعد جديد", time: sessionTime, title: sessionTitle, duration: "حدد المدة في إعدادات الموعد", kind: "موعد" }]);
    setSessionTitle("");
    setSessionTime("");
  }

  const cards = [
    { q: "ما الفكرة الأساسية في الدرس؟", a: "اكتب إجابة من ذاكرتك، ثم قارنها بشرح الدرس." },
    { q: "ما المصطلحات التي يجب أن تتذكرها؟", a: "استخرج المصطلحات المهمة من المذكرة وأضف تعريف كل مصطلح." },
    { q: "ما الجزء الذي يحتاج إلى مراجعة؟", a: "حدد النقطة التي أخطأت فيها وارجع إلى شرحها قبل إعادة الاختبار." }
  ];

  return (
    <main className="app-shell">
      <aside className={`sidebar ${mobileOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-mark"><GraduationCap size={24}/></div>
          <div><strong>StudyGPT <span>Pro</span></strong><small>منظومة التعلّم الشخصي</small></div>
          <button className="mobile-close" onClick={() => setMobileOpen(false)} aria-label="إغلاق القائمة"><X size={19}/></button>
        </div>
        <div className="workspace-label">مساحة الطالب</div>
        <nav className="side-nav">
          {navigation.map(({label, icon: Icon}) => <button key={label} className={`nav-item ${active === label ? "active" : ""}`} onClick={() => go(label)}><Icon size={18}/><span>{label}</span>{label === "المعلم الذكي" && <i className="nav-dot"/>}</button>)}
        </nav>
        <div className="sidebar-spacer"/>
        <div className="sidebar-tip"><div className="tip-icon"><Sparkles size={17}/></div><strong>التفوق خطة، مش صدفة</strong><p>خلي كل جلسة مذاكرة لها هدف واضح ووقت محدد.</p><div className="tip-progress"><span/></div><small>ابدأ بخطوة صغيرة اليوم</small></div>
        <button className="nav-item settings" onClick={() => go("الإعدادات")}><Settings2 size={19}/><span>الإعدادات</span></button>
        <div className="profile"><div className="avatar">ط</div><a className="profile-text" href="/login" style={{textDecoration:"none",color:"inherit"}}><strong>حساب الطالب</strong><small>سجّل الدخول لحفظ تقدمك</small></a><a className="profile-more" href="/login">···</a></div>
      </aside>
      {mobileOpen && <button className="scrim" onClick={() => setMobileOpen(false)} aria-label="إغلاق القائمة"/>}
      <section className="main-area">
        <header className="topbar">
          <div className="topbar-right"><button className="menu-toggle" onClick={() => setMobileOpen(true)} aria-label="فتح القائمة"><Menu size={21}/></button><div className="breadcrumb">StudyGPT Pro <ChevronLeft size={15}/> <b>{heading}</b></div></div>
          <div className="topbar-left"><div className="today"><Bell size={16}/> تنبيهاتك الدراسية</div><button className="icon-button" onClick={() => go("المواد الدراسية")} aria-label="بحث"><Search size={19}/></button><a className="top-avatar" href="/login">ط</a></div>
        </header>
        <div className="content">
          {active === "الرئيسية" && <>
            <section className="welcome-row"><div><div className="eyebrow"><span className="eyebrow-line"/> خطتك الدراسية في مكان واحد</div><h1>أهلاً بك في <span>StudyGPT Pro</span></h1><p className="welcome-sub">مساعدك لفهم المنهج، تنظيم وقتك، وقياس تقدمك خطوة بخطوة.</p></div><div className="welcome-badge"><div className="badge-orbit"><GraduationCap size={28}/></div><span>رحلتك نحو<br/>إتقان المنهج</span></div></section>
            <section className="hero-panel"><div className="hero-copy"><div className="hero-kicker"><Sparkles size={15}/> مساعد دراسي يتابع أهدافك</div><h2>افهم بعمق،<br/><em>وتدرّب بذكاء.</em></h2><p>اسأل عن أي نقطة في دروسك، ارفع مذكرتك، أو أنشئ اختبارًا يقيس فهمك بدل الحفظ فقط.</p><div className="hero-actions"><button className="primary-btn" onClick={() => go("المعلم الذكي")}>ابدأ جلسة مع المعلم <ArrowLeft size={17}/></button><span className="secure-note"><ShieldCheck size={14}/> مساحة تعليمية منظمة</span></div></div><div className="hero-art" aria-hidden="true"><div className="art-glow"/><div className="art-orbit orbit-one"/><div className="art-orbit orbit-two"/><div className="book-stack"><div className="book book-back"/><div className="book book-mid"/><div className="book book-front"><span>STUDY<br/>SMART</span><GraduationCap size={30}/></div></div><div className="floating-note note-one"><BrainCircuit size={17}/><span>فهم أعمق</span></div><div className="floating-note note-two"><Zap size={17}/><span>تقدم ثابت</span></div><div className="spark spark-a">✦</div><div className="spark spark-b">✧</div></div><div className="hero-bottom"><span>01</span><div/><span>اسأل، افهم، اختبر، ثم راجع نقاط ضعفك</span></div></section>
            <section className="section-block"><div className="section-heading"><div><span className="section-kicker">YOUR LEARNING TOOLS</span><h3>كل أدواتك الدراسية</h3><p>انتقل مباشرة إلى المهمة التي تريد إنجازها.</p></div></div><div className="feature-grid">{[
              {icon:MessageCircle,title:"المعلم الذكي",desc:"شرح مبسط وإجابات مرتبطة بمذكرتك.",tone:"blue",tag:"اسأل وافهم",to:"المعلم الذكي" as Section},
              {icon:Target,title:"الامتحانات",desc:"اختبارات متنوعة وقياس حقيقي للفهم.",tone:"violet",tag:"تدريب",to:"الامتحانات" as Section},
              {icon:CalendarDays,title:"جدولي",desc:"مواعيد الدروس والتنبيهات وخطة اليوم.",tone:"amber",tag:"تنظيم",to:"جدولي" as Section},
              {icon:Activity,title:"تحليل الأداء",desc:"اعرف نقاط القوة والموضوعات التي تحتاج مراجعة.",tone:"green",tag:"تطوير",to:"تحليل الأداء" as Section}
            ].map(({icon:Icon,title,desc,tone,tag,to})=><button className="feature-card" key={title} onClick={()=>go(to)}><div className={`feature-icon ${tone}`}><Icon size={21}/></div><span className="feature-tag">{tag}</span><strong>{title}</strong><p>{desc}</p><span className="card-arrow"><ArrowUpLeft size={17}/></span></button>)}</div></section>
            <section className="lower-grid"><div className="panel subjects-panel"><div className="panel-heading"><div><span className="section-kicker">YOUR CURRICULUM</span><h3>موادك الدراسية</h3></div><button className="round-link" onClick={()=>go("المواد الدراسية")}><ArrowLeft size={16}/></button></div><div className="subject-list">{subjects.slice(0,4).map((s,i)=><div className="subject-row" key={s.name}><div className={`subject-symbol ${s.color}`}>{s.short}</div><div className="subject-info"><strong>{s.name}</strong><div className="progress-track"><span style={{width:[42,28,64,35][i]+"%"}}/></div></div><b>{[42,28,64,35][i]}%</b></div>)}</div><div className="panel-footnote"><CircleHelp size={14}/> نسب تجريبية؛ ستُحسب من نتائجك بعد تفعيل الحساب.</div></div><div className="panel progress-panel"><div className="panel-heading"><div><span className="section-kicker">TODAY'S TARGETS</span><h3>أهداف اليوم</h3></div><span className="week-pill">{done.length} من {tasks.length} مكتمل</span></div><div className="task-list">{tasks.map((t,i)=><label className="task-row" key={i}><input type="checkbox" checked={done.includes(t)} onChange={e=>setDone(v=>e.target.checked?[...v,t]:v.filter(x=>x!==t))}/><span>{t}</span></label>)}</div><form className="task-add" onSubmit={e=>{e.preventDefault();addTask();}}><input value={task} onChange={e=>setTask(e.target.value)} placeholder="أضف هدفًا جديدًا..."/><button type="submit" aria-label="إضافة هدف"><Plus size={17}/></button></form></div></section>
          </>}

          {active === "المعلم الذكي" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">YOUR PERSONAL STUDY TUTOR</span><h1>المعلم الذكي</h1><p>حدد مرحلتك ومادتك، واسأل عن الدرس أو ارفع المذكرة ليكون الشرح مبنيًا على محتواها.</p></div><div className="tutor-workspace"><div className="tutor-welcome"><div className="tutor-orb"><Sparkles size={29}/></div><h2>ما الذي تريد فهمه اليوم؟</h2><p>ابدأ بسؤال واضح، أو اطلب شرحًا مبسطًا، أو حدد نقطة صعبة.</p></div><div className="tutor-composer"><div className="composer-tools"><label className="subject-select"><GraduationCap size={15}/><select value={stage} onChange={e=>setStage(e.target.value)}><option>الأولى بكالوريا</option><option>الثانية بكالوريا</option></select><ChevronDown size={14}/></label><label className="subject-select"><BookOpen size={15}/><select value={subject} onChange={e=>setSubject(e.target.value)}>{subjects.map(s=><option key={s.name}>{s.name}</option>)}</select><ChevronDown size={14}/></label></div><textarea value={question} onChange={e=>setQuestion(e.target.value)} rows={4} placeholder="مثال: اشرح لي المفعول المطلق مع أمثلة من مستوى البكالوريا..."/><div className="composer-bottom"><span>تجنب إدخال بيانات شخصية في السؤال.</span><button onClick={askTutor} disabled={!question.trim()}><Send size={17}/></button></div></div><div className="suggestion-row">{["اشرح الدرس خطوة بخطوة","اختبر فهمي في هذا الموضوع","بسّط هذه الفقرة من المذكرة"].map(s=><button key={s} onClick={()=>setQuestion(s)}>{s}</button>)}</div><label className="upload-strip"><FileText size={17}/><span>{fileName || "ارفع مذكرة أو ملف درس لاستخدامه كمصدر للشرح"}</span><input type="file" accept=".pdf,.doc,.docx,.txt" onChange={e=>setFileName(e.target.files?.[0]?.name || "")}/></label>{notice&&<div className="notice" role="status"><CircleHelp size={16}/>{notice}</div>}</div></section>}

          {active === "المواد الدراسية" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">CURRICULUM</span><h1>المواد الدراسية</h1><p>اختر المرحلة والمادة لتنظيم مصادر مذاكرتك.</p></div><div className="toolbar"><label className="subject-select"><GraduationCap size={16}/><select value={stage} onChange={e=>setStage(e.target.value)}><option>الأولى بكالوريا</option><option>الثانية بكالوريا</option></select></label><div className="search-field"><Search size={17}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="ابحث عن مادة..."/></div><span>{filteredSubjects.length} مواد تجريبية</span></div><div className="subject-cards">{filteredSubjects.map(s=><article className="subject-card" key={s.name}><div className={`subject-symbol ${s.color}`}>{s.short}</div><h3>{s.name}</h3><p>{stage} · أضف وحداتك ومصادرك</p><div className="subject-card-foot"><b>ابدأ المذاكرة</b><button onClick={()=>{setSubject(s.name);go("المعلم الذكي");}}>اسأل المعلم <ArrowLeft size={14}/></button></div></article>)}</div></section>}

          {active === "الامتحانات" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">ASSESSMENT CENTER</span><h1>الامتحانات والتدريب</h1><p>أنشئ تدريبًا من عشرة أسئلة على الأقل، ووازن بين أنواع الأسئلة ومستويات الصعوبة.</p></div><div className="builder-card"><div className="builder-icon"><ClipboardList size={23}/></div><h2>إعداد اختبار تدريبي</h2><p>اختَر إعدادات الامتحان؛ يحتاج توليد الأسئلة والتصحيح الآلي إلى تفعيل محرك الذكاء الاصطناعي وبنك المحتوى.</p><div className="builder-fields"><label>المادة<select value={subject} onChange={e=>setSubject(e.target.value)}>{subjects.map(s=><option key={s.name}>{s.name}</option>)}</select></label><label>عدد الأسئلة<select value={quizCount} onChange={e=>setQuizCount(e.target.value)}>{["10","15","20","25","30","40","50"].map(n=><option key={n} value={n}>{n} سؤالًا</option>)}</select></label><label>نوع الأسئلة<select value={quizType} onChange={e=>setQuizType(e.target.value)}><option>متنوع</option><option>اختيار من متعدد</option><option>صح وخطأ</option><option>مقالي</option></select></label></div><button className="primary-btn builder-submit" onClick={()=>setQuizNotice(`تم إعداد طلب اختبار من ${quizCount} سؤالًا في ${subject} بنمط ${quizType}. لم يتم توليد أسئلة فعلية بعد لأن خدمة التوليد غير مربوطة.`)}><Play size={16}/> تجهيز الاختبار</button>{quizNotice&&<div className="notice"><CircleHelp size={16}/>{quizNotice}</div>}</div><div className="panel recent-exams"><h3>سجل الاختبارات</h3><div className="empty-state"><FileText size={27}/><b>لا توجد نتائج محفوظة بعد</b><span>ستظهر محاولاتك ودرجاتك هنا بعد ربط الحسابات.</span></div></div></section>}

          {active === "البطاقات الذكية" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">ACTIVE RECALL</span><h1>البطاقات الذكية</h1><p>اختبر استرجاع المعلومة ثم راجع الإجابة.</p></div><div className="flashcard-area"><div className="flashcard-count">بطاقة {cardIndex+1} من {cards.length}</div><button className={`flashcard ${flipped?"flipped":""}`} onClick={()=>setFlipped(v=>!v)}><span>{flipped?"الإجابة":"السؤال"}</span><strong>{flipped?cards[cardIndex].a:cards[cardIndex].q}</strong><small>اضغط لقلب البطاقة</small></button><div className="flashcard-controls"><button onClick={()=>{setCardIndex(i=>(i+cards.length-1)%cards.length);setFlipped(false);}}><ArrowLeft size={16}/> السابقة</button><button onClick={()=>{setCardIndex(i=>(i+1)%cards.length);setFlipped(false);}}>التالية <ArrowLeft size={16}/></button></div><button className="save-card" onClick={()=>setSaved(s=>s.includes(cards[cardIndex].q)?s.filter(x=>x!==cards[cardIndex].q):[...s,cards[cardIndex].q])}><Bookmark size={15}/>{saved.includes(cards[cardIndex].q)?"إزالة من المحفوظات":"حفظ البطاقة"}</button></div></section>}

          {active === "مكتبة المذاكرة" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">YOUR STUDY LIBRARY</span><h1>مكتبة المذاكرة</h1><p>نظّم ملفات الدروس والملخصات والمصادر التي تعتمد عليها.</p></div><div className="library-grid"><article><div className="library-icon"><BookOpen size={22}/></div><h3>ملخصات الدروس</h3><p>ملخصات مرتبة حسب المرحلة والمادة والوحدة.</p><span>بانتظار ربط مساحة التخزين</span></article><article><div className="library-icon"><FileText size={22}/></div><h3>ملفات المذكرات</h3><p>ارفع ملفاتك ليستخدمها المعلم الذكي كمراجع.</p><span>رفع الملفات الفعلي يحتاج مساحة تخزين</span></article><article><div className="library-icon"><Bookmark size={22}/></div><h3>العناصر المحفوظة</h3><p>{saved.length} بطاقات محفوظة في هذه الجلسة.</p><button onClick={()=>go("البطاقات الذكية")}>فتح البطاقات <ArrowLeft size={14}/></button></article></div></section>}

          {active === "جدولي" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">SCHEDULE & REMINDERS</span><h1>جدولي الدراسي</h1><p>أضف مواعيد المدرسة والدروس والمذاكرة، وحدد وقت كل موعد لتخطيط يومك.</p></div><div className="builder-card"><div className="builder-icon"><CalendarCheck size={23}/></div><h2>إضافة موعد</h2><div className="builder-fields"><label>اسم الموعد<input value={sessionTitle} onChange={e=>setSessionTitle(e.target.value)} placeholder="مثال: درس الفيزياء"/></label><label>الوقت والتاريخ<input type="datetime-local" value={sessionTime} onChange={e=>setSessionTime(e.target.value)}/></label></div><button className="primary-btn builder-submit" onClick={addSession}><Plus size={16}/> إضافة إلى الجدول</button><div className="panel-footnote"><Bell size={14}/> هذه النسخة تعرض المواعيد داخل الصفحة فقط؛ إرسال تنبيه فعلي يحتاج خدمة إشعارات.</div></div><div className="panel"><div className="panel-heading"><h3>المواعيد المسجلة</h3><span className="week-pill">{sessions.length} مواعيد</span></div><div className="schedule-list">{sessions.map((s,i)=><div className="schedule-row" key={i}><div className="schedule-time"><b>{s.time}</b><small>{s.day}</small></div><div className="schedule-info"><strong>{s.title}</strong><small>{s.duration}</small></div><span className="week-pill">{s.kind}</span></div>)}</div></div></section>}

          {active === "تحليل الأداء" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">LEARNING ANALYTICS</span><h1>تحليل مستواك</h1><p>الهدف هو اكتشاف المهارات التي أتقنتها وتلك التي تحتاج تدريبًا إضافيًا.</p></div><div className="analytics-grid"><article><span>مهام مكتملة</span><strong>{done.length}</strong><small>من قائمة أهدافك الحالية</small></article><article><span>بطاقات محفوظة</span><strong>{saved.length}</strong><small>للمراجعة لاحقًا</small></article><article><span>مواعيد مسجلة</span><strong>{sessions.length}</strong><small>في جدولك الدراسي</small></article></div><div className="panel analytics-panel"><div className="panel-heading"><h3>المهارات التي سنقيسها</h3><span className="week-pill">بانتظار نتائج الاختبارات</span></div>{["الفهم والاستيعاب","التطبيق وحل المسائل","التذكر واسترجاع المعلومات","التعبير والإجابة المقالية"].map((s,i)=><div className="analytics-subject" key={s}><span>{s}</span><div className="progress-track"><span style={{width:[25,15,35,10][i]+"%"}}/></div><b>—</b></div>)}<p className="panel-footnote"><Activity size={14}/> لن نعرض نسبة إتقان تقديرية على أنها نتيجة حقيقية؛ القياس يبدأ بعد أداء الاختبارات.</p></div></section>}

          {active === "مجموعات المدرسين" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">TEACHER CLASSROOMS</span><h1>مجموعات المدرسين</h1><p>انضم إلى مجموعة مدرس باستخدام رمز الدعوة الذي يرسله لك.</p></div><div className="builder-card"><div className="builder-icon"><GraduationCap size={23}/></div><h2>الانضمام إلى مجموعة</h2><p>سيتم ربط المجموعة بحسابك بعد التحقق من رمز الدعوة وصلاحيات المدرس.</p><div className="builder-fields"><label>رمز المجموعة<input value={groupCode} onChange={e=>setGroupCode(e.target.value.toUpperCase())} placeholder="أدخل رمز الدعوة"/></label></div><button className="primary-btn builder-submit" onClick={()=>setNotice(groupCode.trim()?"تم إدخال الرمز. التحقق الفعلي يتطلب ربط المجموعات بقاعدة البيانات.":"أدخل رمز المجموعة أولًا.")}>متابعة <ArrowLeft size={16}/></button>{notice&&<div className="notice"><CircleHelp size={16}/>{notice}</div>}</div></section>}

          {active === "الإعدادات" && <section className="workspace-page"><div className="page-intro"><span className="section-kicker">ACCOUNT & PREFERENCES</span><h1>الإعدادات</h1><p>إعداد المرحلة والحساب والتنبيهات.</p></div><div className="settings-card"><div><h3>المرحلة الدراسية</h3><p>اختر المرحلة لعرض موادها ومحتواها.</p></div><select value={stage} onChange={e=>setStage(e.target.value)}><option>الأولى بكالوريا</option><option>الثانية بكالوريا</option></select></div><div className="settings-card"><div><h3>الحساب الشخصي</h3><p>سجّل الدخول لحفظ بياناتك ومزامنتها بين الأجهزة.</p></div><a href="/login">تسجيل الدخول <ArrowLeft size={15}/></a></div><div className="settings-card"><div><h3>اللغة والواجهة</h3><p>اللغة العربية واتجاه العرض من اليمين إلى اليسار.</p></div><span className="setting-value">العربية · RTL</span></div><div className="settings-card"><div><h3>حماية الاختبارات</h3><p>تسجيل محاولات الخروج وتبديل التبويب لا يمنع الغش تقنيًا بشكل مضمون.</p></div><span className="setting-value pending">سياسة نزاهة</span></div></section>}
          <footer><span>© 2026 StudyGPT Pro</span><span>منصة تعليمية للمرحلتين الأولى والثانية بكالوريا.</span><span className="footer-status"><i/> نسخة تطوير</span></footer>
        </div>
      </section>
    </main>
  );
}
