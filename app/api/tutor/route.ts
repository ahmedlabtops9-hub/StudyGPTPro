import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

type TutorRequest = {
  question?: string;
  subject?: string;
  stage?: string;
  materialText?: string;
};

const allowedStages = new Set(["الأولى بكالوريا", "الثانية بكالوريا"]);
const allowedSubjects = new Set([
  "اللغة العربية", "اللغة الإنجليزية", "الرياضيات", "التاريخ",
  "الفلسفة", "العلوم المتكاملة", "البرمجة"
]);

export async function POST(request: NextRequest) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      { error: "خدمة المعلم الذكي غير مفعّلة بعد. أضف OPENAI_API_KEY إلى متغيرات البيئة على الاستضافة." },
      { status: 503 }
    );
  }

  let body: TutorRequest;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "صيغة الطلب غير صحيحة." }, { status: 400 });
  }

  const question = typeof body.question === "string" ? body.question.trim() : "";
  const subject = typeof body.subject === "string" && allowedSubjects.has(body.subject) ? body.subject : "غير محددة";
  const stage = typeof body.stage === "string" && allowedStages.has(body.stage) ? body.stage : "غير محددة";
  const materialText = typeof body.materialText === "string" ? body.materialText.slice(0, 18000) : "";

  if (!question) return NextResponse.json({ error: "اكتب سؤالك أولًا." }, { status: 400 });
  if (question.length > 5000) return NextResponse.json({ error: "السؤال طويل جدًا؛ اختصره إلى 5000 حرف." }, { status: 400 });

  const systemPrompt = [
    "أنت معلم متخصص في شرح المناهج لطلاب البكالوريا في مصر.",
    "أجب بالعربية الواضحة المناسبة لعمر الطالب، واشرح خطوة بخطوة مع أمثلة قصيرة.",
    "لا تخترع معلومة أو مرجعًا. إذا لم تكن متأكدًا فاذكر ذلك بوضوح.",
    "إذا أرفق الطالب نص مذكرة، اجعلها المصدر الأساسي وميّز أي معلومة إضافية عنها.",
    "لا تعطِ الإجابة النهائية فقط في المسائل؛ وضّح طريقة التفكير التعليمية دون كشف سلاسل التفكير الداخلية، وقدّم خطوات الحل المفيدة."
  ].join(" ");

  const userContent = [
    "المرحلة: " + stage,
    "المادة: " + subject,
    materialText ? "نص من مذكرة الطالب:\n" + materialText : "",
    "سؤال الطالب:\n" + question
  ].filter(Boolean).join("\n\n");

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: process.env.OPENAI_MODEL || "gpt-4o-mini",
        temperature: 0.35,
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userContent }
        ]
      }),
      signal: AbortSignal.timeout(45000)
    });

    if (!response.ok) {
      const providerError = await response.text();
      console.error("Tutor provider error:", response.status, providerError.slice(0, 1000));
      return NextResponse.json({ error: "تعذر الحصول على إجابة من خدمة الذكاء الاصطناعي حاليًا." }, { status: 502 });
    }

    const data = await response.json();
    const answer = data?.choices?.[0]?.message?.content;
    if (typeof answer !== "string" || !answer.trim()) {
      return NextResponse.json({ error: "وصل رد غير مكتمل من خدمة الذكاء الاصطناعي." }, { status: 502 });
    }

    return NextResponse.json({ answer: answer.trim(), model: process.env.OPENAI_MODEL || "gpt-4o-mini" });
  } catch (error) {
    console.error("Tutor request failed:", error);
    return NextResponse.json({ error: "حدث خطأ أثناء الاتصال بخدمة المعلم الذكي." }, { status: 502 });
  }
}
