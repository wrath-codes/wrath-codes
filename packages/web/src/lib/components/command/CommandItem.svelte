<script lang="ts">
import type { Component } from "svelte"
import { cn } from "$lib/utils"
import Icon from "../common/Icon.svelte"
import Kbd from "../common/Kbd.svelte"

interface Props {
	icon?: Component<{ class?: string }>
	nerd?: string
	label: string
	shortcut?: string
	selected?: boolean
	onSelect?: () => void
	class?: string
}

let { icon, nerd, label, shortcut, selected = false, onSelect, class: className }: Props = $props()

function handleClick() {
	onSelect?.()
}

function handleKeydown(e: KeyboardEvent) {
	if (e.key === "Enter") {
		e.preventDefault()
		onSelect?.()
	}
}
</script>

<button
	type="button"
	class={cn(
		"flex w-full cursor-pointer items-center gap-3 rounded-md px-3 py-2 text-left text-sm transition-colors",
		"hover:bg-accent/10",
		selected && "bg-accent/10 text-accent-foreground",
		className
	)}
	onclick={handleClick}
	onkeydown={handleKeydown}
	data-selected={selected}
>
	{#if icon || nerd}
		<Icon {icon} {nerd} size="sm" class="text-muted-foreground" />
	{/if}
	<span class="flex-1">{label}</span>
	{#if shortcut}
		<Kbd>{shortcut}</Kbd>
	{/if}
</button>
