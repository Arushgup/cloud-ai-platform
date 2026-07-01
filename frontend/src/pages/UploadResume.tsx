import { useState } from "react";
import { uploadResume } from "../api/resume";
import { useAuth } from "../context/AuthContext";

export default function UploadResume() {

    const { token } = useAuth();

    const [resume, setResume] = useState("");

    const [message, setMessage] = useState("");

    async function handleUpload() {

        if (!token) return;

        try {

            const data = await uploadResume(resume, token);

            setMessage("Resume uploaded successfully!");

            console.log(data);

        } catch (e) {

            setMessage("Upload failed");

        }

    }

    return (

        <div className="p-10">

            <h1 className="mb-6 text-3xl font-bold">

                Upload Resume

            </h1>

            <textarea

                rows={18}

                value={resume}

                onChange={(e)=>setResume(e.target.value)}

                className="w-full rounded-lg border p-4"

                placeholder="Paste your resume here..."

            />

            <button

                onClick={handleUpload}

                className="mt-5 rounded-lg bg-blue-600 px-6 py-3 text-white"

            >
                Upload Resume

            </button>

            <p className="mt-4">

                {message}

            </p>

        </div>

    );

}