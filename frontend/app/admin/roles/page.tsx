"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import { http } from "@/lib/http";

type RoleRow = { id: number; name: string; description: string };

export default function AdminRolesPage() {
  const [rows, setRows] = useState<RoleRow[]>([]);

  useEffect(() => {
    http.get("/admin/roles").then((response) => setRows(response.data || [])).catch(() => setRows([]));
  }, []);

  return (
    <AppShell title="Role Management" subtitle="Manage role catalog" permission="users:manage">
      <section className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left">
              <th>ID</th><th>Name</th><th>Description</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id} className="border-t border-slate-200">
                <td className="py-2">{row.id}</td>
                <td>{row.name}</td>
                <td>{row.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </AppShell>
  );
}
