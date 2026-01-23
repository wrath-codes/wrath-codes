<script lang="ts">
import type { Snippet } from "svelte"
import { cn } from "$lib/utils"

interface Props {
	class?: string
	children: Snippet
}

let { class: className, children }: Props = $props()
</script>

<div
	class={cn("max-h-72 overflow-y-auto overscroll-contain scrollbar-none", className)}
	role="listbox"
	tabindex="-1"
>
	{@render children()}
</div>

<style>
	.scrollbar-none {
		scrollbar-width: none;
		-ms-overflow-style: none;
	}
	.scrollbar-none::-webkit-scrollbar {
		display: none;
	}
</style>
