"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";

import AppShell from "@/components/AppShell";
import Button from "@/components/ui/button";
import Input from "@/components/ui/input";
import { http, setAuthToken } from "@/lib/http";

type FormData = {
  full_name: string;
  email: string;
  password: string;
};

export default function LoginPage() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm<FormData>();
  const [message, setMessage] = useState("");

  async function login(values: FormData) {
    setMessage("");
    try {
      const response = await http.post("/login", { email: values.email, password: values.password });
      const token = response.data?.access_token as string;
      const refreshToken = response.data?.refresh_token as string | undefined;
      window.localStorage.setItem("access_token", token);
      window.localStorage.setItem("user_email", values.email);
      if (refreshToken) {
        window.localStorage.setItem("refresh_token", refreshToken);
      }
      setAuthToken(token);
      setMessage("Login successful.");
      return;
    } catch {
      // Try register if login fails.
    }

    try {
      const response = await http.post("/register", values);
      const token = response.data?.access_token as string;
      window.localStorage.setItem("access_token", token);
      setAuthToken(token);
      setMessage("Account created and signed in.");
    } catch {
      setMessage("Authentication failed. Check backend and credentials.");
    }
  }

  return (
    <AppShell title="Login" subtitle="Authenticate and continue to dashboard" requiresAuth={false}>
      <section className="card max-w-xl">
        <form className="grid gap-3" onSubmit={handleSubmit(login)}>
          <label className="text-sm font-semibold">
            Full Name
            <Input {...register("full_name")} placeholder="Project Manager" />
          </label>
          <label className="text-sm font-semibold">
            Email
            <Input type="email" {...register("email", { required: true })} placeholder="name@example.com" />
          </label>
          <label className="text-sm font-semibold">
            Password
            <Input type="password" {...register("password", { required: true })} placeholder="********" />
          </label>
          <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Please wait..." : "Login / Register"}</Button>
          {message ? <p className="text-sm font-semibold text-teal-800">{message}</p> : null}
        </form>
      </section>
    </AppShell>
  );
}
