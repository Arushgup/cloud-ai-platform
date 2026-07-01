import api from "./axios";

export const login = async (email: string, password: string) => {
  const response = await api.post("/api/auth/login", {
    email,
    password,
  });

  return response.data;
};

export const register = async (
  email: string,
  password: string
) => {
  const response = await api.post("/api/auth/register", {
    email,
    password,
  });

  return response.data;
};