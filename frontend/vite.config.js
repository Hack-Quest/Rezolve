import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      // Forward /api/* to the FastAPI backend — avoids CORS preflight from EventSource
      "/api": "http://localhost:8000",
    },
  },
});
