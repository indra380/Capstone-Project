"use client";

import { useState } from "react";
import {
  exportProjectUrl,
  generateReport,
  overrideTaskOwner,
  updateTaskStatus,
} from "@/lib/api";

type TaskItem = {
  id: number;
  title: string;
  status: string;
  owner_id?: number;
};

type Props = {
  projectId: number;
  tasks: TaskItem[];
};

export default function DashboardActions({ projectId, tasks }: Props) {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [taskId, setTaskId] = useState<number>(tasks[0]?.id ?? 0);
  const [ownerId, setOwnerId] = useState<number>(1);

  async function runTaskUpdate(status: string) {
    if (!taskId) return;
    setBusy(true);
    setMessage("");
    try {
      await updateTaskStatus(projectId, taskId, status, "Updated from dashboard action panel");
      setMessage(`Task ${taskId} updated to ${status}. Refresh page to see latest state.`);
    } catch (err) {
      setMessage("Task update failed.");
    } finally {
      setBusy(false);
    }
  }

  async function runOverride() {
    if (!taskId) return;
    setBusy(true);
    setMessage("");
    try {
      await overrideTaskOwner(projectId, taskId, ownerId, "Manager override from dashboard");
      setMessage(`Task ${taskId} owner overridden to ${ownerId}.`);
    } catch (err) {
      setMessage("Override failed.");
    } finally {
      setBusy(false);
    }
  }

  async function runReport() {
    setBusy(true);
    setMessage("");
    try {
      await generateReport(projectId, "daily", "email");
      setMessage("Report generated and notification flow triggered.");
    } catch (err) {
      setMessage("Report generation failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="card space-y-4">
      <h2 className="font-display text-2xl">Operations Panel</h2>
      <p className="text-sm text-emerald-900/80">
        Update status, apply manual override, generate reports, and export project data.
      </p>

      <div className="grid gap-3 sm:grid-cols-3">
        <label className="text-sm font-semibold">
          Task
          <select
            className="mt-1 w-full rounded-xl border border-emerald-200 bg-white px-3 py-2"
            value={taskId}
            onChange={(e) => setTaskId(Number(e.target.value))}
          >
            {tasks.map((task) => (
              <option key={task.id} value={task.id}>
                {task.id}: {task.title}
              </option>
            ))}
          </select>
        </label>

        <label className="text-sm font-semibold">
          Override Owner ID
          <input
            type="number"
            className="mt-1 w-full rounded-xl border border-emerald-200 bg-white px-3 py-2"
            value={ownerId}
            onChange={(e) => setOwnerId(Number(e.target.value))}
          />
        </label>

        <div className="flex items-end gap-2">
          <button
            disabled={busy}
            onClick={() => runTaskUpdate("in_progress")}
            className="rounded-xl bg-emerald-700 px-3 py-2 text-sm font-semibold text-white"
          >
            Set In Progress
          </button>
          <button
            disabled={busy}
            onClick={() => runTaskUpdate("done")}
            className="rounded-xl bg-emerald-900 px-3 py-2 text-sm font-semibold text-white"
          >
            Set Done
          </button>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        <button
          disabled={busy}
          onClick={runOverride}
          className="rounded-xl border border-emerald-300 bg-white px-3 py-2 text-sm font-semibold text-emerald-900"
        >
          Manual Override
        </button>
        <button
          disabled={busy}
          onClick={runReport}
          className="rounded-xl border border-emerald-300 bg-white px-3 py-2 text-sm font-semibold text-emerald-900"
        >
          Generate Report
        </button>
        <a
          className="rounded-xl border border-emerald-300 bg-white px-3 py-2 text-sm font-semibold text-emerald-900"
          href={exportProjectUrl(projectId, "json")}
          target="_blank"
          rel="noreferrer"
        >
          Export JSON
        </a>
        <a
          className="rounded-xl border border-emerald-300 bg-white px-3 py-2 text-sm font-semibold text-emerald-900"
          href={exportProjectUrl(projectId, "csv")}
          target="_blank"
          rel="noreferrer"
        >
          Export CSV
        </a>
      </div>

      {message ? <p className="text-sm font-semibold text-emerald-800">{message}</p> : null}
    </section>
  );
}
