import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "股票營收觀察工具",
  description: "Taiwan Stock Revenue Observation Tool",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-TW">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
