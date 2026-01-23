<script lang="ts">
	import type { Snippet } from "svelte"
	import { cn } from "$lib/utils"

	interface Props {
		class?: string
		size?: "sm" | "md"
		children: Snippet
	}

	let { class: className, size = "sm", children }: Props = $props()

	const sizeClasses = {
		sm: "text-xs",
		md: "text-base",
	}
</script>

<kbd
	class={cn(
		"pointer-events-none inline-flex h-6 select-none items-center gap-1 rounded border border-border bg-muted px-2 font-mono font-medium text-muted-foreground",
		sizeClasses[size],
		className
	)}
>
	{@render children()}
</kbd>
