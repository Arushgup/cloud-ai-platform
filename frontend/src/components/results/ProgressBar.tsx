type Props = {
  label: string;
  value: number;
};

export default function ProgressBar({
  label,
  value,
}: Props) {
  return (
    <div className="mb-5">

      <div className="mb-2 flex justify-between">

        <span className="font-medium">
          {label}
        </span>

        <span className="font-bold">
          {value}%
        </span>

      </div>

      <div className="h-3 rounded-full bg-gray-200">

        <div
          className="h-3 rounded-full bg-blue-600 transition-all duration-700"
          style={{
            width: `${value}%`,
          }}
        />

      </div>

    </div>
  );
}