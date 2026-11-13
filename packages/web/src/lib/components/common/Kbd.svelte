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
		"pointer-events-none inline-flex h-5 select-none items-center gap-1 border border-border px-1 text-muted-foreground",
		sizeClasses[size],
		className
	)}
>
	{@render children()}
</kbd>
