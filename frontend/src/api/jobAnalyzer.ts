import api from "./axios";

export const analyzeJob = async (
  jdText: string,
  token: string
) => {
  const response = await api.post(
    "/api/v1/jobs/analyze",
    {
      job_id: "frontend-job",
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