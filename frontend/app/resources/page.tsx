"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import { http } from "@/lib/http";

export default function ResourcesPage() {
  const [resources, setResources] = useState<any[]>([]);

  useEffect(() => {
    http.get("/resources").then((response) => setResources(response.data || [])).catch(() => undefined);
  }, []);

  return (
    <AppShell title="Resources" subtitle="Team capacity and capability view">
      <section className="card overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-black/10">
              <th className="py-2">Name</th>
              <th className="py-2">Role</th>
              <th className="py-2">Skills</th>
              <th className="py-2">Availability</th>
            </tr>
          </thead>
          <tbody>
            {resources.map((item) => (
              <tr key={item.id} className="border-b border-black/5">
                <td className="py-2">{item.name}</td>
                <td className="py-2">{item.role}</td>
                <td className="py-2">{item.skills_csv}</td>
                <td className="py-2">{item.availability_percent}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </AppShell>
  );
}
