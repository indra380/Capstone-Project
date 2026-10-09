"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useEffect, useState } from "react";

import ThemeProvider from "@/components/ThemeProvider";
import { setAuthToken } from "@/lib/http";

export default function Providers({ children }: { children: React.ReactNode }) {
  const [client] = useState(() => new QueryClient());

  useEffect(() => {
    const token = window.localStorage.getItem("access_token") || undefined;
    setAuthToken(token);
  }, []);

  return (
    <ThemeProvider>
      <QueryClientProvider client={client}>{children}</QueryClientProvider>
    </ThemeProvider>
  );
}
