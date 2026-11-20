"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, ArrowUp, BookOpen, ChevronDown, GraduationCap, MessageCircle, Paperclip, Plus, Send, Settings2, Sparkles, SquarePen } from "lucide-react";

const suggestions = ["اشرح لي مفهومًا صعبًا بطريقة بسيطة", "اعمل لي أسئلة اختيار من متعدد", "لخّص الدرس في نقاط مرتبة"];
const subjects = ["اللغة العربية", "اللغة الإنجليزية", "الرياضيات", "التاريخ", "الفلسفة", "العلوم المتكاملة", "البرمجة"];

type ChatMessage = { role: "user" | "assistant"; content: string };

export default function TutorPage() {
  const [question, setQuestion] = useState("");
  const [subject, setSubject] = useState("اللغة العربية");
  const [stage, setStage] = useState("الأولى بكالوريا");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [materialText, setMaterialText] = useState("");

  async function send() {
    const prompt = question.trim();
    if (!prompt || busy) return;
    setQuestion("");
    setNotice("");
    setMessages(current => [...current, { role: "user", content: prompt }]);
    setBusy(true);
    try {
      const response = await fetch("/api/tutor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: prompt, subject, stage, materialText })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "تعذر الحصول على إجابة.");
      setMessages(current => [...current, { role: "assistant", content: data.answer }]);
    } catch (error) {
      const message = error instanceof Error ? error.message : "حدث خطأ غير متوقع.";
      setNotice(message);
    } finally {
      setBusy(false);
    }
  }

  function handleFile(file?: File) {
    if (!file) return;
    if (file.size > 2 * 1024 * 1024) {
      setNotice("حجم الملف أكبر من 2 ميجابايت. حاليًا أرفق نصًا من المذكرة أو ملفًا صغيرًا.");
      return;
    }
    if (!file.name.toLowerCase().endsWith(".txt")) {
      setNotice("قراءة PDF وWord لم تُفعّل بعد. يمكنك نسخ نص الجزء المطلوب ووضعه في خانة محتوى المذكرة.");
      return;
    }
    const reader = new FileReader();
    reader.onload = () => setMaterialText(String(reader.result || "").slice(0, 18000));
    reader.onerror = () => setNotice("تعذر قراءة الملف.");
    reader.readAsText(file);
    setNotice("تم تحميل نص الملف محليًا لهذه الجلسة. لم يُحفظ على الخادم.");
  }

  return <main className="tutor-shell" dir="rtl">
    <aside className="tutor-sidebar">
      <Link href="/" className="auth-logo tutor-logo"><span><GraduationCap size={22}/></span><b>StudyGPT <i>Pro</i></b></Link>
      <button className="tutor-new" onClick={() => { setMessages([]); setNotice(""); }}><Plus size={17}/> محادثة جديدة</button>
      <div className="tutor-side-label">مساحة التعلم</div>
      <Link href="/" className="tutor-side-link"><BookOpen size={17}/> لوحة الطالب</Link>
      <div className="tutor-side-link active"><MessageCircle size={17}/> المعلم الذكي</div>
      <div className="tutor-side-label recent-label">المحادثة الحالية</div>
      <div className="tutor-empty-history">{messages.length ? messages.length + " رسائل في هذه الجلسة" : "ابدأ بسؤال دراسي جديد."}</div>
      <div className="tutor-sidebar-bottom"><Settings2 size={17}/> إعدادات المساعد</div>
    </aside>
    <section className="tutor-main">
      <header className="tutor-top"><div><span className="tutor-status-dot"/> المعلم الذكي <small>مساعدك الدراسي</small></div><Link href="/login" className="tutor-account">تسجيل الدخول <ArrowLeft size={14}/></Link></header>
      <div className="tutor-content">
        {messages.length === 0 ? <div className="tutor-welcome">
          <div className="tutor-orb"><Sparkles size={29}/></div>
          <span className="section-kicker">STUDYGPT AI TUTOR</span>
          <h1>أهلاً بك في مساحة <em>الفهم.</em></h1>
          <p>اختر مرحلتك ومادتك، ثم اسأل عن أي درس أو فكرة.</p>
          <div className="tutor-suggestions">{suggestions.map(s => <button key={s} onClick={() => setQuestion(s)}>{s}<ArrowUp size={15}/></button>)}</div>
        </div> : <div className="tutor-response">
          {messages.map((message, index) => <div key={index} className={message.role === "user" ? "student-message" : "assistant-placeholder"}>
            {message.role === "assistant" && <span><Sparkles size={17}/></span>}
            <div>{message.role === "assistant" && <b>StudyGPT Pro</b>}<p>{message.content}</p></div>
          </div>)}
          {busy && <div className="assistant-placeholder"><span><Sparkles size={17}/></span><p>يتم إعداد الشرح...</p></div>}
        </div>}
        <div className="tutor-composer">
          <div className="composer-tools">
            <label className="subject-select"><GraduationCap size={15}/><select value={stage} onChange={e => setStage(e.target.value)}><option>الأولى بكالوريا</option><option>الثانية بكالوريا</option></select><ChevronDown size={14}/></label>
            <label className="subject-select"><BookOpen size={15}/><select value={subject} onChange={e => setSubject(e.target.value)}>{subjects.map(s => <option key={s}>{s}</option>)}</select><ChevronDown size={14}/></label>
            <label className="tutor-attach"><Paperclip size={16}/> نص مذكرة<input type="file" accept=".txt,text/plain" onChange={e => handleFile(e.target.files?.[0])}/></label>
          </div>
          <textarea value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} placeholder="اكتب سؤالك هنا... (Enter للإرسال)" rows={3}/>
          <div className="composer-bottom"><span>{materialText ? "تم إرفاق نص مذكرة لهذه الجلسة" : "الإجابات تعليمية؛ راجعها مع كتابك المدرسي."}</span><button onClick={send} disabled={!question.trim() || busy} aria-label="إرسال السؤال"><Send size={17}/></button></div>
        </div>
        {notice && <div className="auth-message" role="alert">{notice}</div>}
        <div className="tutor-disclaimer">لا تضع بيانات شخصية. لن تُحفظ المحادثة بين الزيارات قبل تفعيل الحسابات.</div>
      </div>
    </section>
  </main>;
}
