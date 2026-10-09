"use client";

import AppNavbar from "@/components/AppNavbar";
import AppSidebar from "@/components/AppSidebar";
import { useAuthGuard } from "@/lib/auth";

export default function AppShell({
  title,
  subtitle,
  requiresAuth = true,
  permission,
  children,
}: {
  title: string;
  subtitle: string;
  requiresAuth?: boolean;
  permission?: string;
  children: React.ReactNode;
}) {
  useAuthGuard({ requiresAuth, permission });

  return (
    <main className="mx-auto grid min-h-screen w-full max-w-7xl gap-4 px-4 py-4 lg:grid-cols-[16rem_1fr]">
      <AppSidebar />
      <section className="grid gap-4">
        <AppNavbar title={title} subtitle={subtitle} />
        {children}
      </section>
    </main>
  );
}
