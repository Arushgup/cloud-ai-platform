import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import type { ReactNode } from "react";

interface AuthContextType {
  token: string | null;
  userEmail: string | null;
  login: (token: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface Props {
  children: ReactNode;
}

export function AuthProvider({ children }: Props) {
  const [token, setToken] = useState<string | null>(null);
  const [userEmail, setUserEmail] = useState<string | null>(null);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedEmail = localStorage.getItem("email");

    if (savedToken) setToken(savedToken);
    if (savedEmail) setUserEmail(savedEmail);
  }, []);

  const login = (jwt: string) => {
    localStorage.setItem("token", jwt);

    setToken(jwt);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("email");

    setToken(null);
    setUserEmail(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        userEmail,
        login,
        logout,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}