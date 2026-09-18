"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuth } from "@/lib/auth";
import { ThemeToggle } from "./ThemeToggle";

const NAV = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/learning", label: "Learning" },
  { href: "/sap", label: "SAP" },
  { href: "/practice", label: "Practice" },
  { href: "/tutor", label: "Tutor" },
  { href: "/profile", label: "Profile" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const { user, loading, signOut } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  const isPublicPath =
    pathname.startsWith("/sap") ||
    pathname.startsWith("/learning") ||
    pathname === "/";

  useEffect(() => {
    if (!loading && !user && !isPublicPath) router.replace("/login");
  }, [loading, user, router, isPublicPath]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="font-body text-sm text-muted">Loading…</p>
      </div>
    );
  }

  if (!user && !isPublicPath) return null;

  return (
    <div className="min-h-screen">
      <header className="border-b-2 border-ink bg-surface">
        <div className="mx-auto flex max-w-[1600px] flex-wrap items-center gap-3 px-3 py-3 sm:px-4">
          <Link href="/dashboard" className="font-display text-lg font-bold">
            CodeMentor<span className="text-accent">.</span>
          </Link>

          <nav className="flex flex-wrap gap-1" aria-label="Main">
            {NAV.map((item) => {
              const active = pathname.startsWith(item.href);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`border-2 px-2 py-1 font-body text-xs font-semibold ${
                    active ? "border-ink bg-ink text-bg" : "border-transparent text-muted"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>

          <ThemeToggle className="ml-auto" />
          {user ? (
            <button type="button" onClick={signOut} className="btn px-2 py-1 text-xs">
              Sign out
            </button>
          ) : (
            <Link href="/login" className="btn px-2 py-1 text-xs">
              Sign in
            </Link>
          )}
        </div>
      </header>

      <main>{children}</main>
    </div>
  );
}
