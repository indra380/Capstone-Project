"use client";

import { useThemeMode } from "@/components/ThemeProvider";

export default function DarkModeToggle() {
  const { mode, toggle } = useThemeMode();

  return (
    <button
      onClick={toggle}
      className="rounded-xl border border-black/10 bg-white/70 px-3 py-2 text-sm font-semibold text-slate-800 transition hover:bg-white"
    >
      {mode === "light" ? "Switch To Dark" : "Switch To Light"}
    </button>
  );
}
