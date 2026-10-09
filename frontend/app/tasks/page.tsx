"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import { http } from "@/lib/http";

export default function TasksPage() {
  const [tasks, setTasks] = useState<any[]>([]);

  useEffect(() => {
    http.get("/tasks").then((response) => setTasks(response.data || [])).catch(() => undefined);
  }, []);

  return (
    <AppShell title="Tasks" subtitle="Track and update work items">
      <section className="card overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-black/10">
              <th className="py-2">ID</th>
              <th className="py-2">Title</th>
              <th className="py-2">Status</th>
              <th className="py-2">Project</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.id} className="border-b border-black/5">
                <td className="py-2">{task.id}</td>
                <td className="py-2">{task.title}</td>
                <td className="py-2">{String(task.status)}</td>
                <td className="py-2">{task.project_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </AppShell>
  );
}
