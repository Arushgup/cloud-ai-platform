import {
  Home,
  FileText,
  Target,
  Sparkles,
  Briefcase,
  Mail,
  Bot,
  LogOut,
} from "lucide-react";

import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const menu = [
  {
    name: "Dashboard",
    path: "/dashboard",
    icon: Home,
  },
  {
    name: "Resume Upload",
    path: "/resume",
    icon: FileText,
  },
  {
    name: "ATS Score",
    path: "/ats",
    icon: Target,
  },
  {
    name: "Resume Optimizer",
    path: "/optimizer",
    icon: Sparkles,
  },
  {
    name: "Job Analyzer",
    path: "/analyze",
    icon: Briefcase,
  },
  {
    name: "Cold Email",
    path: "/email",
    icon: Mail,
  },
  {
    name: "AI Pipeline",
    path: "/pipeline",
    icon: Bot,
  },
];

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="flex h-screen w-72 flex-col bg-slate-950 text-white">

      {/* Logo */}

      <div className="border-b border-slate-800 p-8">

        <h1 className="text-3xl font-bold text-blue-500">
          AI Job Copilot
        </h1>

        <p className="mt-2 text-sm text-slate-400">
          AI Career Assistant
        </p>

      </div>

      {/* Navigation */}

      <nav className="mt-8 flex-1 space-y-2 px-4">

        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-4 rounded-xl px-5 py-4 transition-all ${
                  isActive
                    ? "bg-blue-600 text-white shadow-lg"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`
              }
            >
              <Icon size={22} />

              <span className="font-medium">
                {item.name}
              </span>

            </NavLink>
          );
        })}

      </nav>

      {/* Footer */}

      <div className="border-t border-slate-800 p-6">

        <button
          onClick={logout}
          className="flex w-full items-center gap-4 rounded-xl bg-red-600 px-5 py-4 font-semibold transition hover:bg-red-700"
        >
          <LogOut size={20} />

          Logout
        </button>

      </div>

    </aside>
  );
}