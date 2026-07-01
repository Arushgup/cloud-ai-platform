type Props = {
  result: any;
};

export default function JobAnalysisResult({ result }: Props) {
  const analysis = result.analyzed || result;

  const skills =
    analysis.required_skills ??
    analysis.skills ??
    [];

  const responsibilities =
    analysis.responsibilities ??
    [];

  const education =
    analysis.education ??
    analysis.required_education ??
    "Not Specified";

  const experience =
    analysis.experience ??
    analysis.required_experience ??
    "Not Specified";

  const seniority =
    analysis.seniority ??
    "Not Specified";

  return (
    <div className="mt-10 rounded-2xl bg-white p-8 shadow-lg">

      <h2 className="mb-8 text-3xl font-bold text-blue-600">
        Job Analysis
      </h2>

      <div className="grid gap-6 md:grid-cols-2">

        <div className="rounded-xl bg-slate-50 p-6">
          <h3 className="mb-3 text-xl font-bold">
            Experience
          </h3>

          <p>{experience}</p>
        </div>

        <div className="rounded-xl bg-slate-50 p-6">
          <h3 className="mb-3 text-xl font-bold">
            Education
          </h3>

          <p>{education}</p>
        </div>

        <div className="rounded-xl bg-slate-50 p-6">
          <h3 className="mb-3 text-xl font-bold">
            Seniority
          </h3>

          <p>{seniority}</p>
        </div>

      </div>

      <div className="mt-10">

        <h3 className="mb-4 text-xl font-bold">
          Required Skills
        </h3>

        <div className="flex flex-wrap gap-3">

          {skills.map((skill: string) => (

            <span
              key={skill}
              className="rounded-full bg-blue-100 px-4 py-2 text-blue-700"
            >
              {skill}
            </span>

          ))}

        </div>

      </div>

      <div className="mt-10">

        <h3 className="mb-4 text-xl font-bold">
          Responsibilities
        </h3>

        <ul className="list-disc space-y-2 pl-5">

          {responsibilities.map(
            (item: string, index: number) => (
              <li key={index}>{item}</li>
            )
          )}

        </ul>

      </div>

    </div>
  );
}