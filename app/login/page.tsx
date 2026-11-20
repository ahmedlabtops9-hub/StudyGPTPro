"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, BookOpen, Eye, EyeOff, GraduationCap, LockKeyhole, Mail, ShieldCheck, Sparkles } from "lucide-react";

export default function LoginPage() {
  const [mode,setMode]=useState<"login"|"signup">("login");
  const [showPassword,setShowPassword]=useState(false);
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const [name,setName]=useState("");
  const [message,setMessage]=useState("");

  function submit(e:React.FormEvent<HTMLFormElement>){
    e.preventDefault();
    setMessage("واجهة تجريبية فقط — سيتم تفعيل تسجيل الدخول الآمن وربطه بقاعدة البيانات في مرحلة الربط.");
  }

  return <main className="auth-page" dir="rtl">
    <div className="auth-brand"><Link href="/" className="auth-logo"><span><GraduationCap size={23}/></span><b>StudyGPT <i>Pro</i></b></Link><Link href="/" className="back-home">العودة للرئيسية <ArrowLeft size={15}/></Link></div>
    <div className="auth-layout">
      <section className="auth-aside">
        <div className="auth-aside-content">
          <div className="auth-eyebrow"><Sparkles size={15}/> مستقبلك الدراسي يبدأ بخطوة</div>
          <h1>مكان واحد<br/>لكل <em>أفكارك الكبيرة.</em></h1>
          <p>افهم دروسك، اختبر مستواك، وتابع تقدمك مع أدوات تعليمية مصممة لرحلتك في البكالوريا المصرية.</p>
          <div className="auth-benefits"><div><span><BookOpen size={17}/></span><b>مذاكرة منظمة</b><small>موادك وأدواتك في مساحة واحدة</small></div><div><span><ShieldCheck size={17}/></span><b>مساحة خاصة بك</b><small>تقدمك محفوظ في حسابك بعد التفعيل</small></div></div>
        </div>
        <div className="auth-decoration"><div className="auth-ring ring-a"/><div className="auth-ring ring-b"/><div className="auth-cap"><GraduationCap size={60}/></div><span className="auth-star star-a">✦</span><span className="auth-star star-b">✧</span></div>
        <small className="auth-aside-foot">STUDY SMART · BUILD YOUR FUTURE</small>
      </section>
      <section className="auth-form-side">
        <div className="auth-form-wrap">
          <div className="auth-form-heading"><span className="form-icon"><GraduationCap size={22}/></span><div className="section-kicker">مساحة الطالب</div><h2>{mode==="login"?"أهلاً بعودتك":"أنشئ حسابك"}</h2><p>{mode==="login"?"سجّل دخولك وكمّل رحلتك التعليمية.":"ابدأ رحلتك التعليمية مع StudyGPT Pro."}</p></div>
          <div className="auth-tabs"><button className={mode==="login"?"selected":""} onClick={()=>{setMode("login");setMessage("");}}>تسجيل الدخول</button><button className={mode==="signup"?"selected":""} onClick={()=>{setMode("signup");setMessage("");}}>حساب جديد</button></div>
          <form className="auth-form" onSubmit={submit}>
            {mode==="signup"&&<label>الاسم بالكامل<div className="field-wrap"><input required value={name} onChange={e=>setName(e.target.value)} placeholder="اكتب اسمك"/><GraduationCap size={17}/></div></label>}
            <label>البريد الإلكتروني<div className="field-wrap"><input required type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="name@example.com"/><Mail size={17}/></div></label>
            <label>كلمة المرور<div className="field-wrap"><input required minLength={8} type={showPassword?"text":"password"} value={password} onChange={e=>setPassword(e.target.value)} placeholder="8 أحرف على الأقل"/><LockKeyhole size={17}/><button type="button" className="password-toggle" onClick={()=>setShowPassword(!showPassword)} aria-label="إظهار كلمة المرور">{showPassword?<EyeOff size={16}/>:<Eye size={16}/>}</button></div></label>
            {mode==="login"&&<div className="auth-options"><label className="remember"><input type="checkbox"/> تذكرني</label><button type="button" onClick={()=>setMessage("سيتم إضافة استعادة كلمة المرور عند ربط نظام الحسابات.")}>نسيت كلمة المرور؟</button></div>}
            <button className="auth-submit" type="submit">{mode==="login"?"دخول إلى حسابي":"إنشاء الحساب"} <ArrowLeft size={17}/></button>
          </form>
          {message&&<div className="auth-message" role="status">{message}</div>}
          <div className="auth-terms">بالمتابعة، أنت توافق على شروط الاستخدام وسياسة الخصوصية عند تفعيل الخدمة.</div>
        </div>
      </section>
    </div>
  </main>;
}
