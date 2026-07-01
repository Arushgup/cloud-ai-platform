import api from "./axios";

export const getATSScore = async (
  resumeText: string,
  jdText: string,
  token: string
) => {

  const response = await api.post(
    "/api/v1/ats/score",
    {
      job_id: "frontend-job",
      resume_text: resumeText,
      jd_text: jdText
    },
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );

  return response.data;
};