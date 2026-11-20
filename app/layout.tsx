import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "StudyGPT Pro | تعلّم بذكاء",
  description: "منصتك التعليمية الذكية لطلاب مصر. افهم دروسك، تدرب، وتابع تقدمك في مكان واحد.",
  applicationName: "StudyGPT Pro"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
