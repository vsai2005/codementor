"use client";

import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { ApiError } from "@/lib/api";
import { useAuth } from "@/lib/auth";

type Mode = "login" | "register";

export default function LoginPage() {
  const { user, login, register } = useAuth();
  const router = useRouter();

  const [mode, setMode] = useState<Mode>("login");
  const [identifier, setIdentifier] = useState(""); // login: username or email
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user) router.replace("/dashboard");
  }, [user, router]);

  const submit = useCallback(async () => {
    setError(null);
    setBusy(true);
    try {
      if (mode === "login") {
        await login(identifier.trim(), password);
      } else {
        await register(username.trim(), password, email.trim() || undefined, name.trim() || undefined);
      }
      router.replace("/dashboard");
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Couldn't reach the server. Is the backend running on :8000?",
      );
    } finally {
      setBusy(false);
    }
  }, [mode, identifier, username, email, name, password, login, register, router]);

  const canSubmit =
    password.length >= 1 &&
    (mode === "login" ? identifier.trim().length > 0 : username.trim().length >= 3);

  return (
    <div className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4">
      <div className="card p-6">
        <h1 className="font-display text-2xl font-bold">
          {mode === "login" ? "Welcome back" : "Create your account"}
        </h1>
        <p className="mt-2 font-body text-sm text-muted">
          {mode === "login"
            ? "Sign in with your username or email and password."
            : "Pick a username and password. Your progress gets its own private space."}
        </p>

        <div
          className="mt-6 space-y-3"
          onKeyDown={(e) => {
            if (e.key === "Enter" && canSubmit && !busy) void submit();
          }}
        >
          {mode === "login" ? (
            <input
              type="text"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="Username or email"
              autoComplete="username"
              className="w-full border-2 border-ink bg-surface p-2 font-body text-sm outline-none focus:shadow-hard-sm"
            />
          ) : (
            <>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value.toLowerCase())}
                placeholder="Username (3–20 chars)"
                autoComplete="username"
                className="w-full border-2 border-ink bg-surface p-2 font-body text-sm outline-none focus:shadow-hard-sm"
              />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email (optional)"
                autoComplete="email"
                className="w-full border-2 border-ink bg-surface p-2 font-body text-sm outline-none focus:shadow-hard-sm"
              />
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Display name (optional)"
                className="w-full border-2 border-ink bg-surface p-2 font-body text-sm outline-none focus:shadow-hard-sm"
              />
            </>
          )}

          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder={mode === "register" ? "Password (min 6 chars)" : "Password"}
            autoComplete={mode === "register" ? "new-password" : "current-password"}
            className="w-full border-2 border-ink bg-surface p-2 font-body text-sm outline-none focus:shadow-hard-sm"
          />

          <button
            type="button"
            className="btn btn-primary w-full"
            onClick={submit}
            disabled={busy || !canSubmit}
          >
            {busy
              ? mode === "login"
                ? "Signing in…"
                : "Creating account…"
              : mode === "login"
                ? "Sign in"
                : "Create account"}
          </button>
        </div>

        <p className="mt-4 font-body text-sm text-muted">
          {mode === "login" ? "New here? " : "Already have an account? "}
          <button
            type="button"
            className="font-semibold underline"
            onClick={() => {
              setMode(mode === "login" ? "register" : "login");
              setError(null);
            }}
          >
            {mode === "login" ? "Create an account" : "Sign in"}
          </button>
        </p>

        {error && (
          <p className="mt-4 card-flat border-l-4 border-l-accent p-3 font-body text-sm" role="alert">
            {error}
          </p>
        )}
      </div>
    </div>
  );
}
