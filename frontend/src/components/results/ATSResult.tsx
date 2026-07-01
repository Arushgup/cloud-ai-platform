import CircularScore from "./CircularScore";
import ProgressBar from "./ProgressBar";
import SkillBadge from "./SkillBadge";

type Props = {
  result: any;
};

export default function ATSResult({ result }: Props) {
  const score = result.score;

  return (
    <div className="mt-10 rounded-2xl bg-white p-8 shadow-xl">

      {/* Header */}

      <h2 className="text-center text-3xl font-bold">
        ATS Analysis Report
      </h2>

      {/* Circular Score */}

      <div className="my-10 text-center">

        <CircularScore
          score={score.overall_ats_score}
        />

        <p className="mt-6 text-xl font-semibold">

          {score.will_pass_ats
            ? "✅ Likely to Pass ATS"
            : "❌ Needs Improvement"}

        </p>

        <p className="mt-3 text-gray-500">
          {score.verdict}
        </p>

      </div>

      {/* Score Breakdown */}

      <div className="rounded-xl bg-slate-50 p-6">

        <h3 className="mb-6 text-2xl font-bold">
          Score Breakdown
        </h3>

        <ProgressBar
          label="Keyword Match"
          value={score.keyword_match_score}
        />

        <ProgressBar
          label="Format"
          value={score.format_score}
        />

        <ProgressBar
          label="Relevance"
          value={score.relevance_score}
        />

      </div>

      {/* Skills */}

      <div className="mt-10 grid gap-8 lg:grid-cols-2">

        {/* Matched */}

        <div>

          <h3 className="mb-4 text-xl font-bold text-green-600">
            ✅ Matched Skills
          </h3>

          <div className="flex flex-wrap gap-3">

            {score.matched_keywords.map((skill: string) => (

              <SkillBadge
                key={skill}
                skill={skill}
                matched
              />

            ))}

          </div>

        </div>

        {/* Missing */}

        <div>

          <h3 className="mb-4 text-xl font-bold text-red-600">
            ❌ Missing Skills
          </h3>

          <div className="flex flex-wrap gap-3">

            {score.missing_critical_keywords.map(
              (skill: string) => (

                <SkillBadge
                  key={skill}
                  skill={skill}
                  matched={false}
                />

              )
            )}

          </div>

        </div>

      </div>

      {/* Recommendations */}

      <div className="mt-10 rounded-xl bg-blue-50 p-6">

        <h3 className="mb-5 text-2xl font-bold">
          💡 AI Recommendations
        </h3>

        <div className="space-y-4">

          {score.recommended_fixes.map(
            (fix: string, index: number) => (

              <div
                key={index}
                className="rounded-lg bg-white p-4 shadow"
              >
                {fix}
              </div>

            )
          )}

        </div>

      </div>

    </div>
  );
}