import Link from "next/link";
import { getOverview, getRisks, getTasks } from "@/lib/api";
import DashboardActions from "@/components/DashboardActions";

type PageProps = {
  params: { projectId: string };
};

export default async function ProjectDashboardPage({ params }: PageProps) {
  const projectId = Number(params.projectId);
  const [overview, tasks, risks] = await Promise.all([
    getOverview(projectId),
    getTasks(projectId),
    getRisks(projectId),
  ]);

  return (
    <main className="mx-auto min-h-screen w-full max-w-6xl space-y-6 px-6 py-8">
      <header className="card flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-emerald-700">Project</p>
          <h1 className="font-display text-3xl text-emerald-950">{overview.project_name}</h1>
        </div>
        <Link
          href="/"
          className="rounded-xl border border-emerald-300 bg-white px-4 py-2 text-sm font-semibold text-emerald-900"
        >
          Create New Project
        </Link>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card">
          <p className="text-sm text-emerald-700">Completion</p>
          <p className="text-3xl font-bold text-emerald-950">{overview.completion_percent}%</p>
        </div>
        <div className="card">
          <p className="text-sm text-emerald-700">Blocked Tasks</p>
          <p className="text-3xl font-bold text-emerald-950">{overview.blocked_tasks}</p>
        </div>
        <div className="card">
          <p className="text-sm text-emerald-700">High Risks</p>
          <p className="text-3xl font-bold text-emerald-950">{overview.high_risks}</p>
        </div>
        <div className="card">
          <p className="text-sm text-emerald-700">Report Cadence</p>
          <p className="text-3xl font-bold capitalize text-emerald-950">{overview.report_cadence}</p>
        </div>
      </section>

      <section className="card space-y-2">
        <h2 className="font-display text-2xl">AI Insights</h2>
        <p className="text-emerald-900/90">{(overview as any).ai_summary || "AI summary will appear after orchestration."}</p>
        {Array.isArray((overview as any).ai_recommendations) && (overview as any).ai_recommendations.length > 0 ? (
          <ul className="list-disc space-y-1 pl-5 text-sm text-emerald-900">
            {(overview as any).ai_recommendations.map((item: string, index: number) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        ) : null}
      </section>

      <DashboardActions projectId={projectId} tasks={tasks} />

      <section className="grid gap-6 lg:grid-cols-2">
        <article className="card space-y-3">
          <h2 className="font-display text-2xl">Plan Board</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b border-emerald-100 text-emerald-900">
                  <th className="py-2">Task</th>
                  <th className="py-2">Status</th>
                  <th className="py-2">Milestone</th>
                  <th className="py-2">Duration</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task: any) => (
                  <tr key={task.id} className="border-b border-emerald-50">
                    <td className="py-2 pr-3">{task.title}</td>
                    <td className="py-2 pr-3 capitalize">{String(task.status).replaceAll("_", " ")}</td>
                    <td className="py-2 pr-3">{task.milestone || "-"}</td>
                    <td className="py-2 pr-3">{task.duration_days}d</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>

        <article className="card space-y-3">
          <h2 className="font-display text-2xl">Risk Register</h2>
          {risks.length === 0 ? (
            <p className="text-emerald-900/80">No risks available.</p>
          ) : (
            <ul className="space-y-3">
              {risks.map((risk: any) => (
                <li key={risk.id} className="rounded-xl border border-emerald-100 bg-emerald-50/50 p-3">
                  <p className="font-semibold text-emerald-950">{risk.title}</p>
                  <p className="text-sm capitalize text-emerald-800">Severity: {risk.severity}</p>
                  <p className="text-sm text-emerald-900/90">Mitigation: {risk.mitigation}</p>
                </li>
              ))}
            </ul>
          )}
        </article>
      </section>
    </main>
  );
}
