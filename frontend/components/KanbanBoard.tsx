type Task = {
  id: number;
  title: string;
  status: string;
};

const columns = ["not_started", "in_progress", "blocked", "done"] as const;

export default function KanbanBoard({ tasks }: { tasks: Task[] }) {
  return (
    <section className="card space-y-3">
      <h2 className="font-display text-2xl text-slate-900">Kanban</h2>
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {columns.map((status) => (
          <article key={status} className="rounded-xl bg-slate-100/70 p-3">
            <p className="mb-2 text-sm font-bold uppercase tracking-wide text-slate-700">
              {status.replaceAll("_", " ")}
            </p>
            <div className="grid gap-2">
              {tasks
                .filter((task) => String(task.status) === status)
                .map((task) => (
                  <div key={task.id} className="rounded-lg bg-white p-2 text-sm shadow-sm">
                    {task.title}
                  </div>
                ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
