import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "rgb(var(--bg) / <alpha-value>)",
        surface: "rgb(var(--surface) / <alpha-value>)",
        surfaceStrong: "rgb(var(--surface-strong) / <alpha-value>)",
        text: "rgb(var(--text) / <alpha-value>)",
        muted: "rgb(var(--muted) / <alpha-value>)",
        border: "rgb(var(--border) / <alpha-value>)",
        accent: "rgb(var(--accent) / <alpha-value>)",
        accentSoft: "rgb(var(--accent-soft) / <alpha-value>)",
      },
      fontFamily: {
        sans: ["var(--font-body)", "sans-serif"],
        display: ["var(--font-display)", "sans-serif"],
      },
      boxShadow: {
        glow: "0 20px 45px -25px rgba(14, 165, 233, 0.4)",
      },
      maxWidth: {
        prose: "78ch",
      },
      typography: {
        DEFAULT: {
          css: {
            "--tw-prose-body": "rgb(var(--text))",
            "--tw-prose-headings": "rgb(var(--text))",
            "--tw-prose-links": "rgb(var(--accent))",
            "--tw-prose-bold": "rgb(var(--text))",
            "--tw-prose-counters": "rgb(var(--muted))",
            "--tw-prose-bullets": "rgb(var(--border))",
            "--tw-prose-hr": "rgb(var(--border))",
            "--tw-prose-quotes": "rgb(var(--text))",
            "--tw-prose-quote-borders": "rgb(var(--accent-soft))",
            "--tw-prose-captions": "rgb(var(--muted))",
            "--tw-prose-code": "rgb(var(--text))",
            "--tw-prose-pre-bg": "rgb(var(--surface-strong))",
            "--tw-prose-th-borders": "rgb(var(--border))",
            "--tw-prose-td-borders": "rgb(var(--border))",
            maxWidth: "none",
            code: {
              fontWeight: "600",
            },
            "code::before": {
              content: '""',
            },
            "code::after": {
              content: '""',
            },
            pre: {
              borderRadius: "1rem",
            },
            img: {
              borderRadius: "1rem",
            },
          },
        },
      },
    },
  },
  plugins: [typography],
};

export default config;
