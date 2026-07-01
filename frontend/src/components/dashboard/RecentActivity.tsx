type Props = {
  activities: string[];
};

export default function RecentActivity({
  activities,
}: Props) {
  return (
    <div className="rounded-2xl bg-white p-6 shadow-lg">

      <h2 className="mb-6 text-2xl font-bold">
        Recent Activity
      </h2>

      <div className="space-y-4">

        {activities.map((activity, index) => (

          <div
            key={index}
            className="flex items-center gap-3 rounded-lg bg-green-50 p-4"
          >

            <span className="text-green-600 text-xl">
              ✓
            </span>

            <span>
              {activity}
            </span>

          </div>

        ))}

      </div>

    </div>
  );
}