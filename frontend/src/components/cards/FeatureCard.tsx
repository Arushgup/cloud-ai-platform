import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { type ReactNode } from "react";

type Props = {
  title: string;
  description: string;
  path: string;
  icon: ReactNode;
  emoji: string;
};

export default function FeatureCard({
  title,
  description,
  path,
  icon,
}: Props) {
  const navigate = useNavigate();

  return (
    <motion.div
      whileHover={{
        y: -6,
        scale: 1.02,
      }}
      transition={{ duration: 0.2 }}
      onClick={() => navigate(path)}
      className="cursor-pointer rounded-2xl bg-white p-6 shadow-md hover:shadow-xl"
    >
      <div className="text-blue-600">
        {icon}
      </div>

      <h2 className="mt-5 text-xl font-bold">
        {title}
      </h2>

      <p className="mt-3 text-gray-500">
        {description}
      </p>

      <div className="mt-6 flex items-center gap-2 text-blue-600 font-semibold">
        Open

        <ArrowRight size={18} />
      </div>
    </motion.div>
  );
}