"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowDown, ArrowLeft, ArrowUp, BookOpen, ChevronDown, FileText, GraduationCap, Menu, MessageCircle, Paperclip, Plus, Send, Settings2, Sparkles, SquarePen } from "lucide-react";

const suggestions=["اشرح لي مفهومًا صعبًا بطريقة بسيطة","اعمل لي أسئلة اختيار من متعدد","لخّص الدرس في نقاط مرتبة"];
export default function TutorPage(){
 const [question,setQuestion]=useState("");
 const [subject,setSubject]=useState("اختر المادة");
 const [sent,setSent]=useState(false);
 const [notice,setNotice]=useState("");
 function send(){if(!question.trim())return;setSent(true);setNotice("تم تسجيل سؤالك في النموذج التجريبي. سيتم توصيله بمحرك الذكاء الاصطناعي بعد إعداد الـ Backend.");setQuestion("");}
 return <main className="tutor-shell" dir="rtl">
  <aside className="tutor-sidebar"><Link href="/" className="auth-logo tutor-logo"><span><GraduationCap size={22}/></span><b>StudyGPT <i>Pro</i></b></Link><Link href="/login" className="tutor-new"><Plus size={17}/> محادثة جديدة</Link><div className="tutor-side-label">مساحة التعلم</div><Link href="/" className="tutor-side-link"><BookOpen size={17}/> لوحة الطالب</Link><button className="tutor-side-link active"><MessageCircle size={17}/> المعلم الذكي</button><div className="tutor-side-label recent-label">الأخيرة</div><div className="tutor-empty-history">ستظهر محادثاتك هنا بعد تسجيل الدخول.</div><div className="tutor-sidebar-bottom"><Settings2 size={17}/> إعدادات المساعد</div></aside>
  <section className="tutor-main"><header className="tutor-top"><div><span className="tutor-status-dot"/> المعلم الذكي <small>مساحة المساعدة الدراسية</small></div><Link href="/login" className="tutor-account">تسجيل الدخول <ArrowLeft size={14}/></Link></header>
   <div className="tutor-content">{!sent?<div className="tutor-welcome"><div className="tutor-orb"><Sparkles size={29}/></div><span className="section-kicker">STUDYGPT AI TUTOR</span><h1>أهلاً بك في مساحة <em>الفهم.</em></h1><p>اسأل عن أي درس أو فكرة، وابدأ بفهمها خطوة بخطوة.</p><div className="tutor-suggestions">{suggestions.map(s=><button key={s} onClick={()=>setQuestion(s)}>{s}<ArrowUp size={15}/></button>)}</div></div>:<div className="tutor-response"><div className="student-message">{notice}</div><div className="assistant-placeholder"><span><Sparkles size={17}/></span><div><b>StudyGPT Pro</b><p>هذه نسخة واجهة تجريبية. عند ربط خدمة الذكاء الاصطناعي ستظهر الإجابة هنا مع خطوات الشرح والمصادر الدراسية.</p></div></div><button className="new-question" onClick={()=>setSent(false)}><SquarePen size={15}/> سؤال جديد</button></div>}
    <div className="tutor-composer"><div className="composer-tools"><label className="subject-select"><BookOpen size={15}/><select value={subject} onChange={e=>setSubject(e.target.value)}><option>اختر المادة</option><option>اللغة العربية</option><option>اللغة الإنجليزية</option><option>الرياضيات</option><option>التاريخ</option><option>الفلسفة</option><option>العلوم المتكاملة</option><option>البرمجة</option></select><ChevronDown size={14}/></label><button type="button" onClick={()=>setNotice("رفع الملفات سيتم تفعيله بعد تجهيز التخزين الآمن.")}><Paperclip size={16}/> إرفاق ملف</button></div><textarea value={question} onChange={e=>setQuestion(e.target.value)} onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send();}}} placeholder="اكتب سؤالك هنا... (اضغط Enter للإرسال)" rows={3}/><div className="composer-bottom"><span>راجع الإجابة مع كتابك المدرسي ومصادرك المعتمدة.</span><button onClick={send} disabled={!question.trim()} aria-label="إرسال السؤال"><Send size={17}/></button></div></div>
    <div className="tutor-disclaimer">قد تحتاج الإجابات إلى مراجعة. سيتم إظهار المراجع الدراسية عند اكتمال قاعدة المحتوى.</div>
   </div>
  </section>
 </main>;
}
