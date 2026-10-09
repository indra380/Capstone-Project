type Snapshot = {
  completion_percent: number;
  blocked_tasks: number;
  high_risks: number;
  report_cadence: string;
};

export default function ProgressCards({ data }: { data: Snapshot }) {
  return (
    <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
      <article className="card">
        <p className="text-xs uppercase tracking-wide text-slate-600">Completion</p>
        <p className="text-3xl font-bold text-teal-950">{data.completion_percent}%</p>
      </article>
      <article className="card">
        <p className="text-xs uppercase tracking-wide text-slate-600">Blocked Tasks</p>
        <p className="text-3xl font-bold text-rose-700">{data.blocked_tasks}</p>
      </article>
      <article className="card">
        <p className="text-xs uppercase tracking-wide text-slate-600">High Risks</p>
        <p className="text-3xl font-bold text-amber-700">{data.high_risks}</p>
      </article>
      <article className="card">
        <p className="text-xs uppercase tracking-wide text-slate-600">Cadence</p>
        <p className="text-3xl font-bold capitalize text-slate-900">{data.report_cadence}</p>
      </article>
    </section>
  );
}
