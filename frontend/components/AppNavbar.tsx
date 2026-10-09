"use client";

import DarkModeToggle from "@/components/DarkModeToggle";

export default function AppNavbar({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <header className="card flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 className="font-display text-3xl text-teal-950">{title}</h1>
        <p className="text-sm text-teal-900/80">{subtitle}</p>
      </div>
      <DarkModeToggle />
    </header>
  );
}
