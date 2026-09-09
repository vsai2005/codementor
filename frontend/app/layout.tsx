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

// Runs before paint: resolve the saved theme (or system preference) and stamp
// it on <html> so there is no light-mode flash before React hydrates.
const themeInit = `(function(){try{var t=localStorage.getItem('codementor.theme');if(t!=='dark'&&t!=='light'){t=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';}document.documentElement.dataset.theme=t;}catch(e){document.documentElement.dataset.theme='light';}})();`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${display.variable} ${body.variable}`}
      suppressHydrationWarning
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
      </head>
      <body className="min-h-screen bg-bg font-body text-ink antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
