import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { runPipeline } from "../api/pipeline";
import AppLayout from "../components/layout/AppLayout";
import PipelineResult from "../components/results/PipelineResult";
import { toast } from "sonner";

export default function Pipeline() {
  const { token } = useAuth();

  const [resume, setResume] = useState("");
  const [jd, setJD] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleRunPipeline() {
    if (!token) {
      toast.warning("Please login first");
      return;
    }

    setLoading(true);
const loadingToast = toast.loading("Running AI Pipeline...");
    try {
        
      const data = await runPipeline(
        resume,
        jd,
        token
      );

      toast.dismiss(loadingToast);
      toast.success("AI Pipeline completed successfully");

      console.log("Pipeline Response");
      console.log(JSON.stringify(data, null, 2));

      setResult(data);

    } catch (err: any) {
      console.log(err.response?.data);
      console.error(err);
      
      toast.dismiss(loadingToast);
toast.error("Pipeline failed");
    } finally {
      setLoading(false);
    }
  }

  return (
  <AppLayout>

    <div className="mx-auto max-w-7xl">

      <h1 className="mb-8 text-4xl font-bold">
        AI Pipeline
      </h1>

      <textarea
        rows={10}
        placeholder="Paste Resume"
        value={resume}
        onChange={(e) => setResume(e.target.value)}
        className="mb-5 w-full rounded-xl border p-4"
      />

      <textarea
        rows={10}
        placeholder="Paste Job Description"
        value={jd}
        onChange={(e) => setJD(e.target.value)}
        className="mb-6 w-full rounded-xl border p-4"
      />

      <button
        onClick={handleRunPipeline}
        disabled={loading}
        className="rounded-xl bg-blue-600 px-8 py-3 text-white"
      >
        {loading ? "Running AI..." : "Run Complete AI Pipeline"}
      </button>

      {result && (
        <PipelineResult result={result} />
      )}

    </div>

  </AppLayout>
);
}