import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite"; // 👈 Ensure this plugin package is active

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
