import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { optimizeResume } from "../api/optimizer";
import ResumeOptimizationResult from "../components/results/ResumeOptimizationResult";
import AppLayout from "../components/layout/AppLayout";
import { toast } from "sonner";

export default function ResumeOptimizer() {
  const { token } = useAuth();

  const [resume, setResume] = useState("");
  const [jd, setJD] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  console.log("Rendering Resume Optimizer");
  console.log("Current Result:", result);

  async function handleOptimize() {
    console.log("Optimize Button Clicked");

    if (!token) {
    toast.warning("Please login first");
    return;
}

    console.log("Token Found");

    setLoading(true);

    try {
      const data = await optimizeResume(
        resume,
        jd,
        token
      );

      console.log("SUCCESS");
      console.log("Response:", JSON.stringify(data, null, 2));

      setResult(data);
      toast.success("Resume optimized successfully!");

      console.log("After setResult:", data);

    } catch (err: any) {
      toast.error("Resume optimization failed");
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
Resume Optimizer
</h1>

<textarea
rows={10}
placeholder="Paste Resume"
value={resume}
onChange={(e)=>setResume(e.target.value)}
className="mb-5 w-full rounded-xl border p-4"
/>

<textarea
rows={10}
placeholder="Paste Job Description"
value={jd}
onChange={(e)=>setJD(e.target.value)}
className="mb-6 w-full rounded-xl border p-4"
/>

<button
onClick={handleOptimize}
disabled={loading}
className="rounded-xl bg-blue-600 px-8 py-3 text-white"
>
{loading ? "Optimizing..." : "Optimize Resume"}
</button>

{result && (

<ResumeOptimizationResult
result={{
...result,
original_resume: resume,
}}
/>

)}

</div>

</AppLayout>

);
}