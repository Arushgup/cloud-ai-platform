import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../api/auth";
import { useAuth } from "../context/AuthContext";
import { toast } from "sonner";

export default function Login() {
  const navigate = useNavigate();
  const { login: saveLogin } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      const data = await login(email, password);

      saveLogin(data.accessToken);

      localStorage.setItem("email", email);

      toast.success("Login Successful");

navigate("/dashboard");
    } catch {
      setError("Invalid email or password");
toast.error("Invalid email or password");
    }

    setLoading(false);
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950">
      <div className="w-full max-w-md rounded-xl bg-slate-900 p-8 shadow-2xl">

        <h1 className="mb-2 text-center text-3xl font-bold text-white">
          AI Job Copilot
        </h1>

        <p className="mb-8 text-center text-slate-400">
          Welcome back
        </p>

        <form onSubmit={handleLogin} className="space-y-5">

          <input
            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-blue-500"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
          />

          <input
            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-blue-500"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
          />

          {error && (
            <p className="text-sm text-red-500">
              {error}
            </p>
          )}

          <button
            className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? "Signing In..." : "Login"}
          </button>

          <p className="text-center text-slate-400">
            Don't have an account?
            <Link
              to="/register"
              className="ml-2 text-blue-500"
            >
              Register
            </Link>
          </p>

        </form>
      </div>
    </div>
  );
}