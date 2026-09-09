"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

import { api } from "./api";
import type { User } from "./types";

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

  // Authenticate session via HttpOnly cookie transport (no localStorage dependency)
  useEffect(() => {
    api
      .me()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const register = useCallback(
    async (username: string, password: string, email?: string, name?: string) => {
      const result = await api.register({ username, password, email, name });
      setUser(result.user);
    },
    [],
  );

  const login = useCallback(async (identifier: string, password: string) => {
    const result = await api.login({ identifier, password });
    setUser(result.user);
  }, []);

  const signOut = useCallback(() => {
    api.logout().catch(() => {});
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
