export default function CalendarView() {
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  return (
    <section className="card space-y-3">
      <h2 className="font-display text-2xl text-slate-900">Calendar</h2>
      <div className="grid grid-cols-7 gap-2 text-center text-xs font-semibold uppercase tracking-wide text-slate-600">
        {days.map((day) => (
          <div key={day}>{day}</div>
        ))}
      </div>
      <div className="grid grid-cols-7 gap-2">
        {Array.from({ length: 35 }).map((_, index) => (
          <div key={index} className="aspect-square rounded-lg border border-black/5 bg-white/80 p-2 text-xs text-slate-600">
            {(index % 30) + 1}
          </div>
        ))}
      </div>
    </section>
  );
}
