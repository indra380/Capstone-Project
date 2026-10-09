"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import Button from "@/components/ui/button";
import { http } from "@/lib/http";

export default function ReportsPage() {
  const [reports, setReports] = useState<any[]>([]);

  async function load() {
    const response = await http.get("/reports");
    setReports(response.data || []);
  }

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  async function generate() {
    await http.post("/reports/generate", { project_id: 1, cadence: "daily", channel: "email" });
    await load();
  }

  return (
    <AppShell title="Reports" subtitle="Generate and review status communications">
      <section className="card">
        <Button onClick={generate}>Generate Daily Report For Project 1</Button>
      </section>
      <section className="card overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-black/10">
              <th className="py-2">ID</th>
              <th className="py-2">Project</th>
              <th className="py-2">Cadence</th>
              <th className="py-2">Created</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => (
              <tr key={report.id} className="border-b border-black/5">
                <td className="py-2">{report.id}</td>
                <td className="py-2">{report.project_id}</td>
                <td className="py-2">{report.cadence}</td>
                <td className="py-2">{report.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </AppShell>
  );
}
