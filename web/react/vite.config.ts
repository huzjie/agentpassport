import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: { "/passports": "http://127.0.0.1:8420", "/audit": "http://127.0.0.1:8420",
             "/doctor": "http://127.0.0.1:8420", "/healthz": "http://127.0.0.1:8420" },
  },
});
