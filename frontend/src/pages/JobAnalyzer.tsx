import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { analyzeJob } from "../api/jobAnalyzer";
import AppLayout from "../components/layout/AppLayout";
import JobAnalysisResult from "../components/results/JobAnalysisResult";
import { toast } from "sonner";

export default function JobAnalyzer() {
  const { token } = useAuth();

  const [jd, setJD] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  console.log("Rendering Job Analyzer");
  console.log("Current Result:", result);

  async function handleAnalyze() {
    console.log("Analyze Button Clicked");

    if (!token) {
    toast.warning("Please login first");
    return;
}

    console.log("Token Found");

    setLoading(true);

    try {
      const data = await analyzeJob(jd, token);

      console.log("SUCCESS");
      console.log("Response:", JSON.stringify(data, null, 2));

      setResult(data);
    toast.success("Job analysis completed");
      console.log("After setResult:", data);
    } catch (err: any) {
      toast.error("Job analysis failed");
      console.log(err);
      console.log(err.response);
      console.log(err.response?.data);
    } finally {
      setLoading(false);
    }
  }

  return (
  <AppLayout>

    <div className="mx-auto max-w-7xl">

      <h1 className="mb-8 text-4xl font-bold">
        Job Description Analyzer
      </h1>

      <textarea
        rows={15}
        placeholder="Paste Job Description"
        value={jd}
        onChange={(e) => setJD(e.target.value)}
        className="mb-6 w-full rounded-xl border p-4"
      />

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="rounded-xl bg-blue-600 px-8 py-3 text-white"
      >
        {loading ? "Analyzing..." : "Analyze Job"}
      </button>

      {result && (
        <JobAnalysisResult result={result} />
      )}

    </div>

  </AppLayout>
);
}