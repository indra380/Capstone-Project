"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

const ROLE_PERMISSIONS: Record<string, string[]> = {
  super_admin: ["*"],
  admin: ["users:manage", "projects:manage", "settings:manage", "analytics:view", "logs:view"],
  project_manager: [
    "projects:create",
    "projects:edit",
    "projects:delete_own",
    "members:assign",
    "ai:plan",
    "ai:allocate",
    "progress:manage",
    "risk:manage",
    "reports:generate",
    "dashboard:view",
  ],
  team_lead: [
    "projects:view_assigned",
    "tasks:create",
    "tasks:assign",
    "tasks:update",
    "progress:view_team",
    "reports:generate_team",
    "team:communicate",
  ],
  team_member: [
    "tasks:view_assigned",
    "tasks:update",
    "documents:upload",
    "comments:add",
    "timeline:view",
    "team:communicate",
  ],
  stakeholder: ["dashboard:view", "reports:view", "risks:view", "milestones:view", "progress:view"],
  viewer: ["projects:view_assigned"],
};

type JwtPayload = {
  roles?: string[];
  role?: string;
};

export function parseJwt(token?: string): JwtPayload {
  if (!token) {
    return {};
  }
  try {
    const base64 = token.split(".")[1];
    const normalized = base64.replace(/-/g, "+").replace(/_/g, "/");
    const payload = JSON.parse(window.atob(normalized));
    return payload as JwtPayload;
  } catch {
    return {};
  }
}

export function getClientRoles(): string[] {
  if (typeof window === "undefined") {
    return [];
  }
  const token = window.localStorage.getItem("access_token") || undefined;
  const payload = parseJwt(token);
  if (payload.roles && payload.roles.length > 0) {
    return payload.roles;
  }
  if (payload.role) {
    return [payload.role];
  }
  return [];
}

export function getClientPermissions(): Set<string> {
  const roles = getClientRoles();
  const permissions = new Set<string>();
  for (const role of roles) {
    const grants = ROLE_PERMISSIONS[role] || [];
    for (const permission of grants) {
      permissions.add(permission);
    }
  }
  return permissions;
}

export function useAuthGuard({ requiresAuth = true, permission }: { requiresAuth?: boolean; permission?: string }) {
  const router = useRouter();

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const token = window.localStorage.getItem("access_token");
    if (!requiresAuth) {
      return;
    }
    if (!token) {
      router.replace("/login");
      return;
    }

    if (!permission) {
      return;
    }

    const permissions = getClientPermissions();
    if (!permissions.has("*") && !permissions.has(permission)) {
      router.replace("/forbidden");
    }
  }, [permission, requiresAuth, router]);
}
