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
  role: string;
};

export default function RegisterPage() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm<FormData>({
    defaultValues: { role: "viewer" },
  });
  const [message, setMessage] = useState("");

  async function submit(values: FormData) {
    setMessage("");
    try {
      await http.post("/register", values);
      const loginResponse = await http.post("/login", { email: values.email, password: values.password });
      const token = loginResponse.data?.access_token as string;
      const refreshToken = loginResponse.data?.refresh_token as string | undefined;
      window.localStorage.setItem("access_token", token);
      window.localStorage.setItem("user_email", values.email);
      if (refreshToken) {
        window.localStorage.setItem("refresh_token", refreshToken);
      }
      setAuthToken(token);
      setMessage("Registration successful.");
    } catch {
      setMessage("Registration failed.");
    }
  }

  return (
    <AppShell title="Register" subtitle="Create a new account" requiresAuth={false}>
      <section className="card max-w-xl">
        <form className="grid gap-3" onSubmit={handleSubmit(submit)}>
          <label className="text-sm font-semibold">
            Full Name
            <Input {...register("full_name", { required: true })} placeholder="Your name" />
          </label>
          <label className="text-sm font-semibold">
            Email
            <Input type="email" {...register("email", { required: true })} placeholder="name@example.com" />
          </label>
          <label className="text-sm font-semibold">
            Password
            <Input type="password" {...register("password", { required: true })} placeholder="********" />
          </label>
          <label className="text-sm font-semibold">
            Role
            <select className="input" {...register("role", { required: true })}>
              <option value="viewer">Viewer</option>
              <option value="team_member">Team Member</option>
              <option value="team_lead">Team Lead</option>
              <option value="project_manager">Project Manager</option>
              <option value="stakeholder">Stakeholder</option>
            </select>
          </label>
          <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Please wait..." : "Register"}</Button>
          {message ? <p className="text-sm font-semibold text-teal-800">{message}</p> : null}
        </form>
      </section>
    </AppShell>
  );
}
