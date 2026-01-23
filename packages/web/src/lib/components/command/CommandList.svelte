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
	class={cn("max-h-72 overflow-y-auto overscroll-contain", className)}
	role="listbox"
	tabindex="-1"
>
	{@render children()}
</div>
