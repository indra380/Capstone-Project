import AppShell from "@/components/AppShell";

export default function ForbiddenPage() {
  return (
    <AppShell title="403 Forbidden" subtitle="You do not have permission to access this page" requiresAuth={false}>
      <section className="card max-w-2xl">
        <h2 className="font-display text-3xl text-red-700">Access denied</h2>
        <p className="mt-2 text-sm text-slate-700">
          Your account does not have the required permission for this route.
        </p>
      </section>
    </AppShell>
  );
}
