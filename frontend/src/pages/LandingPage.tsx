import { motion } from "framer-motion";
import { Link } from "react-router-dom";

import {
  ArrowRight,
  Upload,
  Target,
  Sparkles,
  Mail,
  Bot,
  Briefcase,
} from "lucide-react";

const features = [
  {
    icon: <Upload size={36} />,
    title: "Resume Upload",
    description: "Upload your resume securely and let AI analyze it.",
  },
  {
    icon: <Target size={36} />,
    title: "ATS Score",
    description: "See how likely your resume is to pass ATS screening.",
  },
  {
    icon: <Sparkles size={36} />,
    title: "Resume Optimizer",
    description: "Improve your resume with AI-powered suggestions.",
  },
  {
    icon: <Briefcase size={36} />,
    title: "Job Analyzer",
    description: "Extract required skills and responsibilities from any job description.",
  },
  {
    icon: <Mail size={36} />,
    title: "Cold Email Generator",
    description: "Generate recruiter-ready outreach emails instantly.",
  },
  {
    icon: <Bot size={36} />,
    title: "AI Pipeline",
    description: "Run the complete AI workflow in one click.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* NAVBAR */}

      <nav className="mx-auto flex max-w-7xl items-center justify-between px-8 py-6">

        <h1 className="text-3xl font-bold text-blue-500">
          AI Job Copilot
        </h1>

        <Link
          to="/login"
          className="rounded-lg bg-blue-600 px-5 py-2 font-semibold transition hover:bg-blue-700"
        >
          Login
        </Link>

      </nav>

      {/* HERO */}

      <section className="mx-auto flex max-w-7xl flex-col items-center px-8 py-24 text-center">

        <motion.h1
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="max-w-4xl text-6xl font-extrabold leading-tight"
        >
          Land Your Dream Job
          <span className="text-blue-500"> Using AI</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mt-8 max-w-3xl text-xl text-slate-400"
        >
          Upload your resume, calculate ATS score, optimize it,
          analyze job descriptions, generate recruiter emails,
          and run the complete AI hiring pipeline.
        </motion.p>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-12"
        >
          <Link
            to="/login"
            className="inline-flex items-center gap-3 rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold transition hover:bg-blue-700"
          >
            Get Started

            <ArrowRight size={22} />
          </Link>
        </motion.div>

      </section>

      {/* FEATURES */}

      <section className="mx-auto max-w-7xl px-8 py-16">

        <h2 className="mb-12 text-center text-4xl font-bold">
          Everything You Need
        </h2>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">

          {features.map((feature) => (

            <motion.div
              whileHover={{
                y: -8,
                scale: 1.02,
              }}
              key={feature.title}
              className="rounded-2xl border border-slate-800 bg-slate-900 p-8"
            >

              <div className="text-blue-500">
                {feature.icon}
              </div>

              <h3 className="mt-6 text-2xl font-bold">
                {feature.title}
              </h3>

              <p className="mt-4 text-slate-400">
                {feature.description}
              </p>

            </motion.div>

          ))}

        </div>

      </section>

      {/* HOW IT WORKS */}

      <section className="mx-auto max-w-6xl px-8 py-20">

        <h2 className="mb-12 text-center text-4xl font-bold">
          How It Works
        </h2>

        <div className="grid gap-8 md:grid-cols-4">

          {[
            "Upload Resume",
            "Analyze Job",
            "Optimize Resume",
            "Apply with Confidence",
          ].map((step, index) => (

            <motion.div
              whileHover={{ scale: 1.05 }}
              key={step}
              className="rounded-2xl bg-slate-900 p-8 text-center"
            >

              <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-full bg-blue-600 text-xl font-bold">
                {index + 1}
              </div>

              <h3 className="font-semibold">
                {step}
              </h3>

            </motion.div>

          ))}

        </div>

      </section>

      {/* CTA */}

      <section className="px-8 py-24">

        <div className="mx-auto max-w-5xl rounded-3xl bg-gradient-to-r from-blue-600 to-indigo-700 p-14 text-center">

          <h2 className="text-4xl font-bold">
            Ready to Supercharge Your Job Search?
          </h2>

          <p className="mt-6 text-lg text-blue-100">
            Join AI Job Copilot and let AI help you build stronger resumes,
            improve ATS scores, and generate recruiter-ready emails.
          </p>

          <Link
            to="/login"
            className="mt-10 inline-flex items-center gap-3 rounded-xl bg-white px-8 py-4 text-lg font-bold text-blue-700 transition hover:scale-105"
          >
            Start Now

            <ArrowRight size={22} />
          </Link>

        </div>

      </section>

      {/* FOOTER */}

      <footer className="border-t border-slate-800 py-8 text-center text-slate-500">

        © 2026 AI Job Copilot • Built with React, Spring Boot, FastAPI & AI

      </footer>

    </div>
  );
}