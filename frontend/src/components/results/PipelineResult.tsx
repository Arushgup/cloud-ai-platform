type Props = {
  result: any;
};

export default function PipelineResult({ result }: Props) {
  return (
    <div className="mt-10 space-y-8">

      {/* Pipeline Status */}

      <div className="rounded-2xl bg-white p-8 shadow-lg">

        <h2 className="mb-6 text-3xl font-bold">
          AI Pipeline
        </h2>

        <div className="space-y-4">

          {result.completed_nodes?.map((node: string) => (

            <div
              key={node}
              className="flex items-center rounded-lg bg-green-50 p-4"
            >
              <span className="mr-4 text-2xl">
                ✅
              </span>

              <span className="font-medium">
                {node}
              </span>

            </div>

          ))}

        </div>

      </div>

      {/* ATS */}

      {result.ats_score_original && (

        <div className="rounded-2xl bg-white p-8 shadow-lg">

          <h2 className="mb-4 text-2xl font-bold">
            Original ATS Score
          </h2>

          <p className="text-5xl font-bold text-blue-600">
            {result.ats_score_original.overall_ats_score}%
          </p>

        </div>

      )}

      {/* Optimized ATS */}

      {result.ats_score_optimized && (

        <div className="rounded-2xl bg-white p-8 shadow-lg">

          <h2 className="mb-4 text-2xl font-bold">
            Optimized ATS Score
          </h2>

          <p className="text-5xl font-bold text-green-600">
            {result.ats_score_optimized.overall_ats_score}%
          </p>

        </div>

      )}

      {/* Match Score */}

      {result.match_score && (

        <div className="rounded-2xl bg-white p-8 shadow-lg">

          <h2 className="mb-4 text-2xl font-bold">
            Resume Match
          </h2>

          <p className="text-5xl font-bold text-purple-600">
            {result.match_score}%
          </p>

        </div>

      )}

      {/* Resume */}

      {result.optimization?.optimized_resume && (

        <div className="rounded-2xl bg-white p-8 shadow-lg">

          <h2 className="mb-4 text-2xl font-bold">
            Optimized Resume
          </h2>

          <div className="max-h-[500px] overflow-y-auto whitespace-pre-wrap rounded-lg border bg-gray-50 p-4">
            {result.optimization.optimized_resume}
          </div>

        </div>

      )}

      {/* Email */}

      {result.cold_emails && (

        <div className="rounded-2xl bg-white p-8 shadow-lg">

          <h2 className="mb-4 text-2xl font-bold">
            Cold Email Generated
          </h2>

          <pre className="overflow-auto rounded-lg bg-gray-100 p-4 text-sm">
            {JSON.stringify(result.cold_emails, null, 2)}
          </pre>

        </div>

      )}

    </div>
  );
}