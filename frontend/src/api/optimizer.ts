import api from "./axios";

export const optimizeResume = async (
  resumeText: string,
  jdText: string,
  token: string
) => {
  const response = await api.post(
    "/v1/resume/optimize",
    {
      resume_id: "frontend-resume",
      job_id: "frontend-job",
      resume_text: resumeText,
      jd_text: jdText,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
};