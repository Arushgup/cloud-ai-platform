type StatCardProps = {
  title: string;
  value: number;
  suffix?: string;
  subtitle?: string;
};

export default function StatCard({
  title,
  value,
  suffix = "",
  subtitle,
}: StatCardProps) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-md hover:shadow-xl transition-shadow">
      <p className="text-sm text-gray-500">
        {title}
      </p>

      <h2 className="mt-3 text-4xl font-bold text-slate-900">
        {value}
        {suffix}
      </h2>

      {subtitle && (
        <p className="mt-3 text-gray-500">
          {subtitle}
        </p>
      )}
    </div>
  );
}