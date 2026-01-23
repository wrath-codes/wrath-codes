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

	let { icon, nerd, label, shortcut, selected = false, onSelect, class: className }: Props =
		$props()

	let buttonRef: HTMLButtonElement | null = $state(null)

	$effect(() => {
		if (selected && buttonRef) {
			buttonRef.scrollIntoView({ block: "nearest", behavior: "smooth" })
		}
	})

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
	bind:this={buttonRef}
	type="button"
	class={cn(
		"flex w-full cursor-pointer items-center gap-3 rounded-md px-3 py-2 text-left text-sm transition-colors",
		"hover:bg-mauve/10",
		selected && "bg-mauve/20 text-peach",
		className
	)}
	onclick={handleClick}
	onkeydown={handleKeydown}
	data-selected={selected}
>
	{#if selected}
		<span class="blinking-cursor text-peach">▌</span>
	{:else if icon || nerd}
		<Icon {icon} {nerd} size="sm" class="text-muted-foreground" />
	{:else}
		<span class="w-4"></span>
	{/if}
	<span class="flex-1">{label}</span>
	{#if shortcut}
		<Kbd>{shortcut}</Kbd>
	{/if}
</button>

<style>
	@keyframes blink {
		0%,
		50% {
			opacity: 1;
		}
		51%,
		100% {
			opacity: 0;
		}
	}

	.blinking-cursor {
		animation: blink 1s step-end infinite;
	}
</style>
