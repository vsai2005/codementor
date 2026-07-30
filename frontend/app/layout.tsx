import type { Metadata } from "next";
import { Playfair_Display, Work_Sans } from "next/font/google";

import "./globals.css";
import { Providers } from "./providers";

const display = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-display",
  display: "swap",
});

const body = Work_Sans({
  subsets: ["latin"],
  variable: "--font-body",
  display: "swap",
});

export const metadata: Metadata = {
  title: "CodeMentor AI",
  description: "Coding practice with a senior engineer as your reviewer.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable}`}>
      <body className="min-h-screen bg-bg font-body text-ink antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
