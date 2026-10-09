"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";

import AppShell from "@/components/AppShell";
import Button from "@/components/ui/button";
import Input from "@/components/ui/input";
import { http } from "@/lib/http";

type FormData = { token: string; new_password: string };

export default function ResetPasswordPage() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm<FormData>();
  const [message, setMessage] = useState("");

  async function submit(values: FormData) {
    try {
      await http.post("/reset-password", values);
      setMessage("Password reset successful.");
    } catch {
      setMessage("Reset failed.");
    }
  }

  return (
    <AppShell title="Reset Password" subtitle="Set a new password with reset token" requiresAuth={false}>
      <section className="card max-w-xl">
        <form className="grid gap-3" onSubmit={handleSubmit(submit)}>
          <label className="text-sm font-semibold">
            Token
            <Input {...register("token", { required: true })} placeholder="paste reset token" />
          </label>
          <label className="text-sm font-semibold">
            New Password
            <Input type="password" {...register("new_password", { required: true })} placeholder="********" />
          </label>
          <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Please wait..." : "Reset"}</Button>
          {message ? <p className="text-sm font-semibold text-teal-800">{message}</p> : null}
        </form>
      </section>
    </AppShell>
  );
}
