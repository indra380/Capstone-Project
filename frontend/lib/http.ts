import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1";

export const http = axios.create({
  baseURL: API_BASE,
  timeout: 20000,
});

export function setAuthToken(token?: string) {
  if (!token) {
    delete http.defaults.headers.common.Authorization;
    return;
  }
  http.defaults.headers.common.Authorization = `Bearer ${token}`;
}

export function withManagerRole() {
  return { headers: { "X-Role": "project_manager" } };
}
