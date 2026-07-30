"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

import { api, clearToken, getToken, setToken } from "./api";
import type { User } from "./types";

/** PRD 4.1 names NextAuth.js. This uses Google Identity Services directly and
 *  exchanges the ID token for our own JWT at POST /api/auth/google, because the
 *  backend already issues and owns the session token — adding NextAuth would
 *  mean two session systems to keep in sync for no gain. */

interface AuthState {
  user: User | null;
  loading: boolean;
  signOut: () => void;
  register: (
    username: string,
    password: string,
    email?: string,
    name?: string,
  ) => Promise<void>;
  login: (identifier: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getToken()) {
      setLoading(false);
      return;
    }
    api
      .me()
      .then(setUser)
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  const register = useCallback(
    async (username: string, password: string, email?: string, name?: string) => {
      const result = await api.register({ username, password, email, name });
      setToken(result.access_token);
      setUser(result.user);
    },
    [],
  );

  const login = useCallback(async (identifier: string, password: string) => {
    const result = await api.login({ identifier, password });
    setToken(result.access_token);
    setUser(result.user);
  }, []);

  const signOut = useCallback(() => {
    clearToken();
    setUser(null);
  }, []);

  const value = useMemo<AuthState>(
    () => ({ user, loading, signOut, register, login }),
    [user, loading, signOut, register, login],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}
