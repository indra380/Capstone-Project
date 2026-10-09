"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";

import AppShell from "@/components/AppShell";
import Button from "@/components/ui/button";
import Input from "@/components/ui/input";
import { http } from "@/lib/http";

type FormData = { current_password: string; new_password: string };

export default function ChangePasswordPage() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm<FormData>();
  const [message, setMessage] = useState("");

  async function submit(values: FormData) {
    try {
      await http.post("/change-password", values);
      setMessage("Password changed successfully.");
    } catch {
      setMessage("Unable to change password.");
    }
  }

  return (
    <AppShell title="Change Password" subtitle="Update your account password" permission="projects:view_assigned">
      <section className="card max-w-xl">
        <form className="grid gap-3" onSubmit={handleSubmit(submit)}>
          <label className="text-sm font-semibold">
            Current Password
            <Input type="password" {...register("current_password", { required: true })} placeholder="********" />
          </label>
          <label className="text-sm font-semibold">
            New Password
            <Input type="password" {...register("new_password", { required: true })} placeholder="********" />
          </label>
          <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Please wait..." : "Change Password"}</Button>
          {message ? <p className="text-sm font-semibold text-teal-800">{message}</p> : null}
        </form>
      </section>
    </AppShell>
  );
}
