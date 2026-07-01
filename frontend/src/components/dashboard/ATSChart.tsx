import {
  LineChart,
  Line,
  XAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { day: "Mon", score: 61 },
  { day: "Tue", score: 69 },
  { day: "Wed", score: 73 },
  { day: "Thu", score: 79 },
  { day: "Fri", score: 82 },
];

export default function ATSChart() {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-lg">

      <h2 className="mb-6 text-2xl font-bold">
        ATS Trend
      </h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>

          <XAxis dataKey="day" />

          <Tooltip />

          <Line
            dataKey="score"
            stroke="#2563eb"
            strokeWidth={4}
          />

        </LineChart>
      </ResponsiveContainer>

    </div>
  );
}