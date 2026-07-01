import { useState } from "react";
import { getATSScore } from "../api/ai";
import { useAuth } from "../context/AuthContext";
import ATSResult from "../components/results/ATSResult";
import AppLayout from "../components/layout/AppLayout";
import { toast } from "sonner";

export default function ATSScore() {
  const { token } = useAuth();

  const [resume, setResume] = useState("");
  const [jd, setJD] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function scoreResume() {
    if (!token) {
      toast.warning("Please login first");
      return;
    }

    setLoading(true);

    try {
      const data = await getATSScore(
        resume,
        jd,
        token
      );

      console.log("ATS Response:", data);

      setResult(data);
      toast.success("ATS Score Generated");

    } catch (err) {
      console.error(err);
      toast.error("Failed to calculate ATS Score");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppLayout>

      <div className="mx-auto max-w-6xl">

        <h1 className="mb-8 text-4xl font-bold">
          ATS Score Analyzer
        </h1>

        <textarea
          rows={8}
          placeholder="Paste Resume"
          value={resume}
          onChange={(e) => setResume(e.target.value)}
          className="mb-5 w-full rounded-xl border border-gray-300 p-4 shadow-sm focus:border-blue-500 focus:outline-none"
        />

        <textarea
          rows={8}
          placeholder="Paste Job Description"
          value={jd}
          onChange={(e) => setJD(e.target.value)}
          className="mb-6 w-full rounded-xl border border-gray-300 p-4 shadow-sm focus:border-blue-500 focus:outline-none"
        />

        <button
          onClick={scoreResume}
          disabled={loading}
          className="rounded-xl bg-blue-600 px-8 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? "Calculating..." : "Calculate ATS Score"}
        </button>

        {result && (
          <ATSResult result={result} />
        )}

      </div>

    </AppLayout>
  );
}