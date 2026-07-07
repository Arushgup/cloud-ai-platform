import api from "./axios";

export const uploadResume = async (resume: string, token: string) => {

    const response = await api.post(
        "/resume",
        resume,
        {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "text/plain"
            }
        }
    );

    return response.data;
};