<script lang="ts">
	import { cn } from "$lib/utils";
	import SocialLinks from "../common/SocialLinks.svelte";

	interface Props {
		class?: string;
	}

	let { class: className }: Props = $props();

	const currentYear = new Date().getFullYear();
</script>

<footer class={cn("bg-crust", className)}>
	<div class="container mx-auto flex h-12 items-center justify-between px-4">
		<p class="text-xs text-mauve">
			© {currentYear} <span class="text-foreground">wrath.codes</span>
		</p>
		<SocialLinks size="sm" />
	</div>
</footer>
