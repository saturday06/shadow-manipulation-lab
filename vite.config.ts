import { defineConfig } from "vite-plus";

export default defineConfig({
  fmt: {
    ignorePatterns: [
      ".local/**",
      "CHANGELOG.md",
      "pnpm-lock.yaml",
    ],
  },
  lint: {
    ignorePatterns: [".local/**"],
  },
});
