"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";

import AppShell from "@/components/AppShell";
import Button from "@/components/ui/button";
import Input from "@/components/ui/input";
import { http } from "@/lib/http";

type FormData = { email: string };

export default function ForgotPasswordPage() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm<FormData>();
  const [message, setMessage] = useState("");

  async function submit(values: FormData) {
    try {
      const response = await http.post("/forgot-password", values);
      const token = response.data?.reset_token;
      setMessage(token ? `Reset token: ${token}` : "If your account exists, reset instructions were sent.");
    } catch {
      setMessage("Unable to process request.");
    }
  }

  return (
    <AppShell title="Forgot Password" subtitle="Generate a password reset token" requiresAuth={false}>
      <section className="card max-w-xl">
        <form className="grid gap-3" onSubmit={handleSubmit(submit)}>
          <label className="text-sm font-semibold">
            Email
            <Input type="email" {...register("email", { required: true })} placeholder="name@example.com" />
          </label>
          <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Please wait..." : "Request reset"}</Button>
          {message ? <p className="text-sm font-semibold text-teal-800">{message}</p> : null}
        </form>
      </section>
    </AppShell>
  );
}
