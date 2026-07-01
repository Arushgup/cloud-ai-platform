import api from "./axios";

export async function getDashboard(token: string) {
  const response = await api.get("/api/dashboard", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
}