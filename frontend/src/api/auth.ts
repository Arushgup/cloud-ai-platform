import api from "./axios";

export const login = async (email: string, password: string) => {
  return (
    await api.post("/auth/login", {
      email,
      password,
    })
  ).data;
};

export const register = async (
  name: string,
  email: string,
  password: string
) => {
  return (
    await api.post("/auth/register", {
      name,
      email,
      password,
    })
  ).data;
};