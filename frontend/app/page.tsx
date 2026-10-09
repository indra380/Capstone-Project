import GoalIntakeForm from "@/components/GoalIntakeForm";

export default function HomePage() {
  return (
    <main className="mx-auto grid min-h-screen w-full max-w-6xl items-center gap-8 px-6 py-12 lg:grid-cols-2">
      <section className="space-y-5">
        <p className="inline-flex rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-900">
          Project 15 Capstone
        </p>
        <h1 className="font-display text-4xl leading-tight text-emerald-950 sm:text-5xl">
          The AI Project Manager
        </h1>
        <p className="max-w-xl text-lg text-emerald-900/90">
          Turn a high-level goal into an execution-ready plan with supervised AI orchestration,
          risk visibility, and stakeholder reporting.
        </p>
        <div className="grid gap-3 sm:grid-cols-3">
          <div className="card p-4">
            <p className="text-sm text-emerald-700">Planning</p>
            <p className="text-xl font-bold">Automated</p>
          </div>
          <div className="card p-4">
            <p className="text-sm text-emerald-700">Risk Alerts</p>
            <p className="text-xl font-bold">Real-Time</p>
          </div>
          <div className="card p-4">
            <p className="text-sm text-emerald-700">Governance</p>
            <p className="text-xl font-bold">Audit-Ready</p>
          </div>
        </div>
      </section>
      <GoalIntakeForm />
    </main>
  );
}
