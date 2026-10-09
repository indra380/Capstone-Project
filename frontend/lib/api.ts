const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1";

export type ProjectOverview = {
  project_id: number;
  project_name: string;
  completion_percent: number;
  blocked_tasks: number;
  high_risks: number;
  report_cadence: string;
};

export async function createProject(payload: {
  name: string;
  goal: string;
  deadline?: string;
}) {
  const response = await fetch(`${API_BASE}/projects`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Role": "project_manager",
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error("Failed to create project");
  }
  return response.json();
}

export async function getOverview(projectId: number): Promise<ProjectOverview> {
  const response = await fetch(`${API_BASE}/projects/${projectId}/overview`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Failed to fetch project overview");
  }
  return response.json();
}

export async function getTasks(projectId: number) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/tasks`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Failed to fetch tasks");
  }
  return response.json();
}

export async function getRisks(projectId: number) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/risks`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Failed to fetch risks");
  }
  return response.json();
}

export async function updateTaskStatus(projectId: number, taskId: number, status: string, reason = "") {
  const response = await fetch(`${API_BASE}/projects/${projectId}/tasks/${taskId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-Role": "project_manager",
    },
    body: JSON.stringify({ status, reason }),
  });
  if (!response.ok) {
    throw new Error("Failed to update task status");
  }
  return response.json();
}

export async function overrideTaskOwner(projectId: number, taskId: number, ownerId: number, rationale: string) {
  const response = await fetch(`${API_BASE}/projects/${projectId}/override`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Role": "project_manager",
    },
    body: JSON.stringify({ task_id: taskId, owner_id: ownerId, rationale }),
  });
  if (!response.ok) {
    throw new Error("Failed to override task owner");
  }
  return response.json();
}

export async function generateReport(projectId: number, cadence = "daily", channel = "email") {
  const response = await fetch(
    `${API_BASE}/projects/${projectId}/reports?cadence=${encodeURIComponent(cadence)}&channel=${encodeURIComponent(channel)}`,
    {
      method: "POST",
      headers: {
        "X-Role": "project_manager",
      },
    },
  );
  if (!response.ok) {
    throw new Error("Failed to generate report");
  }
  return response.json();
}

export function exportProjectUrl(projectId: number, format: "json" | "csv") {
  return `${API_BASE}/projects/${projectId}/export?format=${format}`;
}
