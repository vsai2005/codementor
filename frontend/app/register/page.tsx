"use client";

import { Suspense } from "react";
import { AuthForm } from "@/components/auth/AuthForm";

export default function RegisterPage() {
  return (
    <Suspense fallback={<div className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4" />}>
      <AuthForm initialMode="register" />
    </Suspense>
  );
}
