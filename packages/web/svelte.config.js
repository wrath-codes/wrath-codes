import adapter from "@sveltejs/adapter-static"
import { mdsvex } from "mdsvex"

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: [".svelte", ".svx", ".mdx"],
	preprocess: [
		mdsvex({
			extensions: [".svx", ".mdx"],
		}),
	],
	kit: {
		adapter: adapter({
			pages: "build",
			assets: "build",
			fallback: undefined,
			precompress: false,
			strict: true,
		}),
		alias: {
			$components: "src/lib/components",
			$content: "src/lib/content",
			$stores: "src/lib/stores",
			$styles: "src/lib/styles",
		},
	},
}

export default config
