"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import RiskHeatmap from "@/components/RiskHeatmap";
import { http } from "@/lib/http";

export default function RisksPage() {
  const [risks, setRisks] = useState<any[]>([]);

  useEffect(() => {
    http.get("/risks").then((response) => setRisks(response.data || [])).catch(() => undefined);
  }, []);

  return (
    <AppShell title="Risks" subtitle="Risk register and heatmap monitoring">
      <RiskHeatmap risks={risks} />
      <section className="card overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-black/10">
              <th className="py-2">Title</th>
              <th className="py-2">Severity</th>
              <th className="py-2">Mitigation</th>
            </tr>
          </thead>
          <tbody>
            {risks.map((risk) => (
              <tr key={risk.id} className="border-b border-black/5">
                <td className="py-2">{risk.title}</td>
                <td className="py-2">{risk.severity}</td>
                <td className="py-2">{risk.mitigation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </AppShell>
  );
}
