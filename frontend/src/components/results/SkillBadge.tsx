type Props = {
  skill: string;
  matched: boolean;
};

export default function SkillBadge({
  skill,
  matched,
}: Props) {
  return (
    <span
      className={`rounded-full px-4 py-2 text-sm font-medium ${
        matched
          ? "bg-green-100 text-green-700"
          : "bg-red-100 text-red-700"
      }`}
    >
      {matched ? "✔" : "✖"} {skill}
    </span>
  );
}