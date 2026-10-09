"use client";

import { useEffect, useState } from "react";

import AnalyticsCharts from "@/components/AnalyticsCharts";
import AppShell from "@/components/AppShell";
import CalendarView from "@/components/CalendarView";
import KanbanBoard from "@/components/KanbanBoard";
import ProgressCards from "@/components/ProgressCards";
import RiskHeatmap from "@/components/RiskHeatmap";
import TimelineView from "@/components/TimelineView";
import { getOverview, getRisks, getTasks } from "@/lib/api";

type Overview = {
  completion_percent: number;
  blocked_tasks: number;
  high_risks: number;
  report_cadence: string;
};

export default function DashboardPage() {
  const [projectId, setProjectId] = useState<number>(1);
  const [overview, setOverview] = useState<Overview>({
    completion_percent: 0,
    blocked_tasks: 0,
    high_risks: 0,
    report_cadence: "daily",
  });
  const [tasks, setTasks] = useState<any[]>([]);
  const [risks, setRisks] = useState<any[]>([]);

  useEffect(() => {
    async function run() {
      try {
        const o = await getOverview(projectId);
        const t = await getTasks(projectId);
        const r = await getRisks(projectId);
        setOverview(o as any);
        setTasks(t as any[]);
        setRisks(r as any[]);
      } catch {
        // Keep dashboard visible even if data is unavailable.
      }
    }
    run();
  }, [projectId]);

  return (
    <AppShell title="Dashboard" subtitle="Portfolio telemetry, progress, and risk intelligence">
      <section className="card flex items-center gap-2">
        <label className="text-sm font-semibold text-slate-700">Project ID</label>
        <input
          value={projectId}
          onChange={(event) => setProjectId(Number(event.target.value || 1))}
          className="w-24 rounded-lg border border-black/10 bg-white px-2 py-1 text-sm"
        />
      </section>
      <ProgressCards data={overview} />
      <AnalyticsCharts tasks={tasks} risks={risks} />
      <KanbanBoard tasks={tasks} />
      <TimelineView tasks={tasks} />
      <RiskHeatmap risks={risks} />
      <CalendarView />
    </AppShell>
  );
}
