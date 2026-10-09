type Task = {
  id: number;
  title: string;
  milestone?: string;
  duration_days?: number;
};

export default function TimelineView({ tasks }: { tasks: Task[] }) {
  return (
    <section className="card space-y-3">
      <h2 className="font-display text-2xl text-slate-900">Timeline</h2>
      <div className="space-y-3">
        {tasks.map((task, index) => (
          <div key={task.id} className="relative rounded-xl border border-black/5 bg-white p-3">
            <div className="absolute left-0 top-0 h-full w-1 rounded-l-xl bg-teal-600" />
            <p className="text-xs text-slate-600">Step {index + 1}</p>
            <p className="font-semibold text-slate-900">{task.title}</p>
            <p className="text-sm text-slate-700">
              Milestone: {task.milestone || "-"} | Duration: {task.duration_days || 0}d
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
