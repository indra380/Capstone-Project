"use client";

import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type Task = {
  id: number;
  status: string;
};

type Risk = {
  id: number;
  severity: string;
};

export default function AnalyticsCharts({ tasks, risks }: { tasks: Task[]; risks: Risk[] }) {
  const taskChart = [
    { name: "Not Started", value: tasks.filter((t) => String(t.status) === "not_started").length },
    { name: "In Progress", value: tasks.filter((t) => String(t.status) === "in_progress").length },
    { name: "Blocked", value: tasks.filter((t) => String(t.status) === "blocked").length },
    { name: "Done", value: tasks.filter((t) => String(t.status) === "done").length },
  ];

  const riskChart = [
    { name: "Low", value: risks.filter((r) => String(r.severity) === "low").length },
    { name: "Medium", value: risks.filter((r) => String(r.severity) === "medium").length },
    { name: "High", value: risks.filter((r) => String(r.severity) === "high").length },
    { name: "Critical", value: risks.filter((r) => String(r.severity) === "critical").length },
  ];

  return (
    <section className="grid gap-4 xl:grid-cols-2">
      <article className="card">
        <h2 className="mb-3 font-display text-2xl text-slate-900">Task Distribution</h2>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={taskChart}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#0f766e" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </article>

      <article className="card">
        <h2 className="mb-3 font-display text-2xl text-slate-900">Risk Distribution</h2>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={riskChart}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#be123c" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </article>
    </section>
  );
}
