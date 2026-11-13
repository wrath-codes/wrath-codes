<script lang="ts">
	import type { Component } from "svelte";
	import { cn } from "$lib/utils";
	import Icon from "../common/Icon.svelte";
	import Kbd from "../common/Kbd.svelte";

	interface Props {
		icon?: Component<{ class?: string }>;
		nerd?: string;
		label: string;
		shortcut?: string;
		selected?: boolean;
		onSelect?: () => void;
		class?: string;
	}

	let {
		icon,
		nerd,
		label,
		shortcut,
		selected = false,
		onSelect,
		class: className,
	}: Props = $props();

	let buttonRef: HTMLButtonElement | null = $state(null);

	$effect(() => {
		if (selected && buttonRef) {
			buttonRef.scrollIntoView({ block: "nearest", behavior: "smooth" });
		}
	});

	function handleClick() {
		onSelect?.();
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === "Enter") {
			e.preventDefault();
			onSelect?.();
		}
	}
</script>

<button
	bind:this={buttonRef}
	type="button"
	class={cn(
		"flex w-full cursor-pointer items-center gap-2 px-3 py-1.5 text-left text-sm transition-colors text-muted-foreground",
		"hover:bg-muted/30",
		selected && "bg-mauve/20 text-foreground",
		className,
	)}
	onclick={handleClick}
	onkeydown={handleKeydown}
	data-selected={selected}
>
	{#if selected}
		<span
			style="font-family: var(--font-icons)"
			class="blinking-cursor text-mauve">{"\uf44a"}</span
		>
	{:else if icon || nerd}
		<Icon {icon} {nerd} size="sm" class="text-muted-foreground" />
	{:else}
		<span class="w-3"></span>
	{/if}
	<span class="flex-1">{label}</span>
	{#if shortcut}
		<span class="text-xs text-muted-foreground">[{shortcut}]</span>
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
