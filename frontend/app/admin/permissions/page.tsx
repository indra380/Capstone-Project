"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import { http } from "@/lib/http";

type PermissionRow = { id: number; code: string; name: string; description: string };

export default function AdminPermissionsPage() {
  const [rows, setRows] = useState<PermissionRow[]>([]);

  useEffect(() => {
    http.get("/admin/permissions").then((response) => setRows(response.data || [])).catch(() => setRows([]));
  }, []);

  return (
    <AppShell title="Permission Management" subtitle="View permission catalog" permission="users:manage">
      <section className="card overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left">
              <th>ID</th><th>Code</th><th>Name</th><th>Description</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id} className="border-t border-slate-200">
                <td className="py-2">{row.id}</td>
                <td>{row.code}</td>
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
