import { svelte } from "@sveltejs/vite-plugin-svelte"
import { defineConfig } from "vitest/config"
import path from "node:path"

export default defineConfig({
	plugins: [svelte({ hot: false })],
	resolve: {
		alias: {
			$lib: path.resolve(__dirname, "./src/lib"),
		},
	},
	test: {
		include: ["src/**/*.{test,spec}.{js,ts}"],
		environment: "jsdom",
		globals: true,
		coverage: {
			provider: "v8",
			reporter: ["text", "json", "html"],
			include: ["src/**/*.{ts,svelte}"],
			exclude: ["src/**/*.test.ts", "src/**/*.d.ts"],
		},
	},
})
