"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import { getClientRoles } from "@/lib/auth";

export default function MyAccountPage() {
  const [email, setEmail] = useState("");
  const [roles, setRoles] = useState<string[]>([]);

  useEffect(() => {
    setEmail(window.localStorage.getItem("user_email") || "unknown");
    setRoles(getClientRoles());
  }, []);

  return (
    <AppShell title="My Account" subtitle="Profile and session information" permission="projects:view_assigned">
      <section className="card max-w-2xl grid gap-3">
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Roles:</strong> {roles.length ? roles.join(", ") : "none"}</p>
      </section>
    </AppShell>
  );
}
