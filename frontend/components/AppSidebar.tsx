"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { getClientPermissions } from "@/lib/auth";

const links = [
  ["/dashboard", "Dashboard", "dashboard:view"],
  ["/projects", "Projects", "projects:view_assigned"],
  ["/tasks", "Tasks", "tasks:view_assigned"],
  ["/resources", "Resources", "projects:view_assigned"],
  ["/risks", "Risks", "risks:view"],
  ["/reports", "Reports", "reports:view"],
  ["/settings", "Settings", "settings:manage"],
  ["/admin/users", "User Management", "users:manage"],
  ["/admin/roles", "Role Management", "users:manage"],
  ["/admin/permissions", "Permission Management", "users:manage"],
  ["/my-account", "My Account", "projects:view_assigned"],
  ["/change-password", "Change Password", "projects:view_assigned"],
  ["/login", "Login", "public"],
] as const;

export default function AppSidebar() {
  const pathname = usePathname();
  const permissions = getClientPermissions();

  const visibleLinks = links.filter(([, , permission]) => {
    if (permission === "public") {
      return true;
    }
    return permissions.has("*") || permissions.has(permission);
  });

  return (
    <aside className="card h-fit w-full lg:sticky lg:top-4 lg:w-64">
      <p className="font-display text-2xl text-teal-950">AI PM</p>
      <p className="mb-4 text-sm text-teal-800/80">Project Control Center</p>
      <nav className="grid gap-2">
        {visibleLinks.map(([href, label]) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`rounded-xl px-3 py-2 text-sm font-semibold transition ${
                active
                  ? "bg-teal-700 text-white"
                  : "bg-white/70 text-slate-800 hover:bg-white"
              }`}
            >
              {label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
