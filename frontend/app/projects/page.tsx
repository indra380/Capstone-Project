"use client";

import { useEffect, useState } from "react";

import AppShell from "@/components/AppShell";
import Button from "@/components/ui/button";
import Input from "@/components/ui/input";
import Textarea from "@/components/ui/textarea";
import { http, withManagerRole } from "@/lib/http";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([]);
  const [name, setName] = useState("AI Support Assistant Rollout");
  const [goal, setGoal] = useState("Deliver AI assistant with quality tracking and stakeholder reporting.");

  async function load() {
    const response = await http.get("/projects");
    setProjects(response.data || []);
  }

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  async function createProject() {
    await http.post("/projects", { name, goal }, withManagerRole());
    await load();
  }

  return (
    <AppShell title="Projects" subtitle="Create and manage project records">
      <section className="card grid gap-3 lg:grid-cols-3">
        <label className="text-sm font-semibold lg:col-span-1">
          Name
          <Input value={name} onChange={(event) => setName(event.target.value)} />
        </label>
        <label className="text-sm font-semibold lg:col-span-2">
          Goal
          <Textarea value={goal} onChange={(event) => setGoal(event.target.value)} />
        </label>
        <Button onClick={createProject} className="lg:col-span-3">Create Project</Button>
      </section>

      <section className="card overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-black/10">
              <th className="py-2">ID</th>
              <th className="py-2">Name</th>
              <th className="py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {projects.map((project) => (
              <tr key={project.id} className="border-b border-black/5">
                <td className="py-2">{project.id}</td>
                <td className="py-2">{project.name}</td>
                <td className="py-2">{project.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </AppShell>
  );
}
