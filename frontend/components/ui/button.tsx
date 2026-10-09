import { ButtonHTMLAttributes } from "react";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary";
};

export default function Button({ variant = "primary", className = "", ...props }: Props) {
  const style =
    variant === "primary"
      ? "bg-teal-700 text-white hover:bg-teal-800"
      : "bg-white text-slate-900 border border-black/10 hover:bg-slate-50";

  return <button className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${style} ${className}`} {...props} />;
}
