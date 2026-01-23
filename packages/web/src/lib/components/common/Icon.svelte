<script lang="ts">
import type { Component } from "svelte"
import { cn } from "$lib/utils"

interface Props {
	icon?: Component<{ class?: string }>
	nerd?: string
	class?: string
	size?: "sm" | "md" | "lg"
}

let { icon: LucideIcon, nerd, class: className, size = "md" }: Props = $props()

const sizeClasses = {
	sm: "w-4 h-4 text-sm",
	md: "w-5 h-5 text-base",
	lg: "w-6 h-6 text-lg",
}
</script>

{#if LucideIcon}
	<LucideIcon class={cn(sizeClasses[size], className)} />
{:else if nerd}
	<span
		class={cn("inline-flex items-center justify-center", sizeClasses[size], className)}
		style="font-family: var(--font-icons)"
	>
		{nerd}
	</span>
{/if}
