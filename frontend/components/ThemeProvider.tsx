"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

type ThemeMode = "light" | "dark";

type ThemeContextValue = {
  mode: ThemeMode;
  toggle: () => void;
};

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export default function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [mode, setMode] = useState<ThemeMode>("light");

  useEffect(() => {
    const saved = window.localStorage.getItem("theme-mode");
    if (saved === "dark" || saved === "light") {
      setMode(saved);
    }
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = mode;
    window.localStorage.setItem("theme-mode", mode);
  }, [mode]);

  const value = useMemo(
    () => ({ mode, toggle: () => setMode((prev) => (prev === "light" ? "dark" : "light")) }),
    [mode],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useThemeMode() {
  const value = useContext(ThemeContext);
  if (!value) {
    throw new Error("useThemeMode must be used inside ThemeProvider");
  }
  return value;
}
