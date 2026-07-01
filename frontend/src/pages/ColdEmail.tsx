import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { generateColdEmail } from "../api/coldEmail";
import AppLayout from "../components/layout/AppLayout";
import ColdEmailResult from "../components/results/ColdEmailResult";
import { toast } from "sonner";

export default function ColdEmail() {
  const { token } = useAuth();

  const [resume, setResume] = useState("");
  const [jd, setJD] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    if (!token) {
      toast.warning("Please login first");
      return;
    }

    setLoading(true);

    try {
      const data = await generateColdEmail(
        resume,
        jd,
        token
      );

      console.log("Response:", JSON.stringify(data, null, 2));

      setResult(data);
      toast.success("Cold emails generated");

    } catch (err: any) {
      console.error(err);
      console.log(err.response?.data);
      toast.error("Failed to generate cold emails");
    } finally {
      setLoading(false);
    }
  }

  return (
  <AppLayout>

    <div className="mx-auto max-w-7xl">

      <h1 className="mb-8 text-4xl font-bold">
        Cold Email Generator
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
        onClick={handleGenerate}
        disabled={loading}
        className="rounded-xl bg-blue-600 px-8 py-3 text-white"
      >
        {loading ? "Generating..." : "Generate Email"}
      </button>

      {result && (
        <ColdEmailResult result={result} />
      )}

    </div>

  </AppLayout>
);
}