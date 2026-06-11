/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        pitch: "#0f3d2e",
        ink: "#18211f",
        mint: "#d8f5e7",
        clay: "#b95b32",
        gold: "#f3bd4a",
      },
      boxShadow: {
        panel: "0 16px 40px rgba(14, 31, 27, 0.12)",
      },
    },
  },
  plugins: [],
};

