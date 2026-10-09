"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createProject } from "@/lib/api";

export default function GoalIntakeForm() {
  const router = useRouter();
  const [name, setName] = useState("Customer Support Chatbot Launch");
  const [goal, setGoal] = useState(
    "Launch a customer support chatbot in 4 weeks with a 4-person team while maintaining quality and timeline health.",
  );
  const [deadline, setDeadline] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const result = await createProject({
        name,
        goal,
        deadline: deadline || undefined,
      });
      router.push(`/projects/${result.project_id}`);
    } catch (err) {
      setError("Could not generate project plan. Check backend connection.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="card animate-rise space-y-4">
      <h2 className="font-display text-2xl">Goal Intake</h2>
      <div className="space-y-1">
        <label className="text-sm font-semibold">Project Name</label>
        <input
          className="w-full rounded-xl border border-emerald-200 bg-white px-3 py-2 outline-none focus:border-emerald-500"
          value={name}
          onChange={(event) => setName(event.target.value)}
          required
        />
      </div>
      <div className="space-y-1">
        <label className="text-sm font-semibold">Project Goal</label>
        <textarea
          className="min-h-28 w-full rounded-xl border border-emerald-200 bg-white px-3 py-2 outline-none focus:border-emerald-500"
          value={goal}
          onChange={(event) => setGoal(event.target.value)}
          required
        />
      </div>
      <div className="space-y-1">
        <label className="text-sm font-semibold">Deadline (optional)</label>
        <input
          type="date"
          className="w-full rounded-xl border border-emerald-200 bg-white px-3 py-2 outline-none focus:border-emerald-500"
          value={deadline}
          onChange={(event) => setDeadline(event.target.value)}
        />
      </div>
      {error ? <p className="text-sm font-semibold text-red-700">{error}</p> : null}
      <button
        disabled={loading}
        className="w-full rounded-xl bg-emerald-700 px-4 py-2 font-semibold text-white transition hover:bg-emerald-800 disabled:opacity-60"
      >
        {loading ? "Generating..." : "Generate Plan"}
      </button>
    </form>
  );
}
