type Props = {
  result: any;
};

export default function ResumeOptimizationResult({ result }: Props) {
  const optimization = result.optimization || result;

  const optimizedResume =
    optimization.optimized_resume ??
    optimization.optimized_resume_text ??
    optimization.optimized_text ??
    optimization.resume ??
    "No optimized resume returned.";

  const changes =
    optimization.changes ??
    optimization.improvements ??
    optimization.suggestions ??
    [];

  return (
    <div className="mt-10">

      <div className="rounded-2xl bg-white p-8 shadow-lg">

        <h2 className="mb-8 text-3xl font-bold text-green-600">
          Resume Optimized Successfully 🎉
        </h2>

        <div className="grid gap-8 lg:grid-cols-2">

          {/* Original Resume */}

          <div>

            <h3 className="mb-4 text-xl font-bold">
              Original Resume
            </h3>

            <div className="h-[600px] overflow-y-auto rounded-xl border bg-gray-50 p-5 whitespace-pre-wrap">
              {result.original_resume ??
                optimization.original_resume ??
                "Original resume unavailable"}
            </div>

          </div>

          {/* Optimized Resume */}

          <div>

            <h3 className="mb-4 text-xl font-bold text-blue-600">
              Optimized Resume
            </h3>

            <div className="h-[600px] overflow-y-auto rounded-xl border bg-blue-50 p-5 whitespace-pre-wrap">
              {optimizedResume}
            </div>

          </div>

        </div>

        {changes.length > 0 && (

          <div className="mt-10">

            <h3 className="mb-5 text-xl font-bold">
              AI Improvements
            </h3>

            <ul className="space-y-3">

              {changes.map((item: string, index: number) => (

                <li
                  key={index}
                  className="rounded-lg bg-green-50 p-4"
                >
                  ✅ {item}
                </li>

              ))}

            </ul>

          </div>

        )}

      </div>

    </div>
  );
}