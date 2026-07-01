import {
  CircularProgressbar,
  buildStyles,
} from "react-circular-progressbar";

import "react-circular-progressbar/dist/styles.css";

type Props = {
  score: number;
};

export default function CircularScore({
  score,
}: Props) {
  return (
    <div className="mx-auto h-56 w-56">
      <CircularProgressbar
        value={score}
        text={`${score}%`}
        styles={buildStyles({
          textSize: "18px",
          pathColor: "#2563eb",
          textColor: "#1e293b",
          trailColor: "#e5e7eb",
          strokeLinecap: "round",
        })}
      />

      <p className="mt-6 text-center text-lg font-semibold text-slate-700">
        ATS Score
      </p>
    </div>
  );
}