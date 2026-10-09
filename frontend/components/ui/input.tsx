import { InputHTMLAttributes } from "react";

export default function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={`w-full rounded-xl border border-black/10 bg-white/90 px-3 py-2 text-sm outline-none focus:border-teal-600 ${props.className || ""}`}
    />
  );
}
