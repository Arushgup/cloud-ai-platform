import { useState } from "react";

import {
  Upload,
  Target,
  Sparkles,
  Briefcase,
  Mail,
  Bot,
} from "lucide-react";

import AppLayout from "../components/layout/AppLayout";
import StatCard from "../components/cards/StatCard";
import FeatureCard from "../components/cards/FeatureCard";
import RecentActivity from "../components/dashboard/RecentActivity";
import ATSChart from "../components/dashboard/ATSChart";

export default function Dashboard() {

  const [dashboard] = useState({
    atsScore: 82,
    resumeMatch: 91,
    applications: 12,

    recentActivity: [
      "Resume Uploaded",
      "ATS Score Generated",
      "Resume Optimized",
      "Cold Email Generated",
      "Pipeline Completed",
    ],
  });

  return (
    <AppLayout>

      <div className="space-y-10">

        {/* Header */}

        <div>

          <h1 className="text-5xl font-bold">
            Welcome Back 👋
          </h1>

          <p className="mt-3 text-lg text-gray-500">
            Your AI-powered career assistant.
          </p>

        </div>

        {/* Stats */}

        <div className="grid gap-6 md:grid-cols-3">

          <StatCard
            title="ATS Score"
            value={dashboard.atsScore}
            suffix="%"
            subtitle="Latest Resume"
          />

          <StatCard
            title="Resume Match"
            value={dashboard.resumeMatch}
            suffix="%"
            subtitle="Backend Engineer"
          />

          <StatCard
            title="Applications"
            value={dashboard.applications}
            subtitle="Tracked"
          />

        </div>

        {/* Chart */}

        <ATSChart />

        {/* AI Tools */}

        <div>

          <h2 className="mb-6 text-3xl font-bold">
            AI Tools
          </h2>

          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">

            <FeatureCard
              title="Resume Upload"
              description="Upload and manage your latest resume."
              path="/resume"
              icon={<Upload size={38} />}
              emoji="📄"
            />

            <FeatureCard
              title="ATS Score"
              description="Analyze ATS compatibility."
              path="/ats"
              icon={<Target size={38} />}
              emoji="🎯"
            />

            <FeatureCard
              title="Resume Optimizer"
              description="Improve your resume with AI."
              path="/optimizer"
              icon={<Sparkles size={38} />}
              emoji="✨"
            />

            <FeatureCard
              title="Job Analyzer"
              description="Analyze any job description."
              path="/analyze"
              icon={<Briefcase size={38} />}
              emoji="💼"
            />

            <FeatureCard
              title="Cold Email"
              description="Generate recruiter outreach emails."
              path="/email"
              icon={<Mail size={38} />}
              emoji="📧"
            />

            <FeatureCard
              title="AI Pipeline"
              description="Run the complete AI workflow."
              path="/pipeline"
              icon={<Bot size={38} />}
              emoji="🤖"
            />

          </div>

        </div>

        {/* Activity */}

        <RecentActivity
          activities={dashboard.recentActivity}
        />

      </div>

    </AppLayout>
  );
}