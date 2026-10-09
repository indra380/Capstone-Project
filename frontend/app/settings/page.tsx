"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import Button from "@/components/ui/button";
import Input from "@/components/ui/input";
import { http } from "@/lib/http";

export default function SettingsPage() {
  const [cadence, setCadence] = useState("daily");
  const [escalationHours, setEscalationHours] = useState(4);
  const [highRiskThreshold, setHighRiskThreshold] = useState(2);

  useEffect(() => {
    http.get("/admin/settings").then((response) => {
      const payload = response.data;
      setCadence(payload.report_cadence);
      setEscalationHours(payload.escalation_hours);
      setHighRiskThreshold(payload.high_risk_threshold);
    }).catch(() => undefined);
  }, []);

  async function save() {
    await http.put("/admin/settings", {
      report_cadence: cadence,
      escalation_hours: escalationHours,
      high_risk_threshold: highRiskThreshold,
    }, {
      headers: {
        "X-Role": "admin",
      },
    });
  }

  return (
    <AppShell title="Settings" subtitle="System governance and reporting controls">
      <section className="card grid max-w-xl gap-3">
        <label className="text-sm font-semibold">
          Report Cadence
          <select
            className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
            value={cadence}
            onChange={(event) => setCadence(event.target.value)}
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
          </select>
        </label>
        <label className="text-sm font-semibold">
          Escalation Hours
          <Input
            type="number"
            value={escalationHours}
            onChange={(event) => setEscalationHours(Number(event.target.value))}
          />
        </label>
        <label className="text-sm font-semibold">
          High Risk Threshold
          <Input
            type="number"
            value={highRiskThreshold}
            onChange={(event) => setHighRiskThreshold(Number(event.target.value))}
          />
        </label>
        <Button onClick={save}>Save Settings</Button>
      </section>
    </AppShell>
  );
}
