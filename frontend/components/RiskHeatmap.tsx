type Risk = {
  id: number;
  title: string;
  severity: string;
};

function severityColor(severity: string) {
  if (severity === "critical") return "bg-rose-700";
  if (severity === "high") return "bg-rose-500";
  if (severity === "medium") return "bg-amber-500";
  return "bg-emerald-500";
}

export default function RiskHeatmap({ risks }: { risks: Risk[] }) {
  return (
    <section className="card space-y-3">
      <h2 className="font-display text-2xl text-slate-900">Risk Heatmap</h2>
      <div className="grid gap-2 sm:grid-cols-2">
        {risks.map((risk) => (
          <div key={risk.id} className="rounded-xl border border-black/5 bg-white p-3">
            <div className="mb-2 flex items-center justify-between gap-2">
              <p className="text-sm font-semibold text-slate-900">{risk.title}</p>
              <span className={`rounded-full px-2 py-1 text-xs font-bold uppercase text-white ${severityColor(risk.severity)}`}>
                {risk.severity}
              </span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-200">
              <div
                className={`h-2 rounded-full ${severityColor(risk.severity)}`}
                style={{
                  width:
                    risk.severity === "critical"
                      ? "100%"
                      : risk.severity === "high"
                        ? "75%"
                        : risk.severity === "medium"
                          ? "50%"
                          : "25%",
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
