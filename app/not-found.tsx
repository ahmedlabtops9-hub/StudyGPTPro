import Link from "next/link";
import { ArrowRight, GraduationCap } from "lucide-react";
export default function NotFound(){return <main className="not-found" dir="rtl"><GraduationCap size={42}/><h1>الصفحة غير موجودة</h1><p>قد يكون الرابط غير صحيح أو أن الصفحة نُقلت.</p><Link href="/">العودة إلى الرئيسية <ArrowRight size={16}/></Link></main>}
