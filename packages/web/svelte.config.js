import adapter from "@sveltejs/adapter-static"
import { mdsvex } from "mdsvex"
import { createHighlighter } from "shiki"

const highlighter = await createHighlighter({
	themes: ["catppuccin-mocha"],
	langs: ["javascript", "typescript", "svelte", "bash", "json", "css", "html", "markdown", "rust", "python", "go", "lua"],
})

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: [".svelte", ".svx", ".mdx"],
	preprocess: [
		mdsvex({
			extensions: [".svx", ".mdx"],
			highlight: {
				highlighter: async (code, lang) => {
					const html = highlighter.codeToHtml(code, {
						lang: lang || "text",
						theme: "catppuccin-mocha",
					})
					return `{@html \`${html.replace(/`/g, "\\`")}\`}`
				},
			},
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
