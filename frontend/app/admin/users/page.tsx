"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import { http } from "@/lib/http";

type UserRow = { id: number; full_name: string; email: string; role: string; is_active: boolean };

export default function AdminUsersPage() {
  const [rows, setRows] = useState<UserRow[]>([]);

  useEffect(() => {
    http.get("/admin/users").then((response) => setRows(response.data || [])).catch(() => setRows([]));
  }, []);

  return (
    <AppShell title="User Management" subtitle="Manage enterprise users" permission="users:manage">
      <section className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left">
              <th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id} className="border-t border-slate-200">
                <td className="py-2">{row.id}</td>
                <td>{row.full_name}</td>
                <td>{row.email}</td>
                <td>{row.role}</td>
                <td>{row.is_active ? "active" : "inactive"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </AppShell>
  );
}
