<script lang="ts">
	import { goto } from "$app/navigation"
	import { commandPaletteAtom, filterItems, groupItems, useWritableAtom } from "$lib/stores"
	import { cn } from "$lib/utils"
	import CommandEmpty from "./CommandEmpty.svelte"
	import CommandInput from "./CommandInput.svelte"
	import CommandItemRow from "./CommandItem.svelte"
	import CommandList from "./CommandList.svelte"
	import type { CommandItemData } from "./types"

	interface Props {
		navItems?: CommandItemData[]
		searchItems?: CommandItemData[]
		class?: string
	}

	let { navItems = [], searchItems = [], class: className }: Props = $props()

	const palette = useWritableAtom(commandPaletteAtom)
	let inputRef: HTMLInputElement | null = $state(null)

	const isNavMode = $derived(palette.value.mode === "nav")
	const currentItems = $derived(isNavMode ? navItems : searchItems)

	const filteredItems = $derived(
		isNavMode
			? filterItems(currentItems, palette.value.query)
			: palette.value.query.length > 0
				? filterItems(currentItems, palette.value.query)
				: []
	)
	const grouped = $derived(groupItems(filteredItems))
	const showEmptySearch = $derived(!isNavMode && palette.value.query.length === 0)

	$effect(() => {
		if (palette.value.open && inputRef) {
			inputRef.focus()
		}
	})

	$effect(() => {
		if (filteredItems.length > 0 && palette.value.selectedIndex >= filteredItems.length) {
			palette.update((s) => ({ ...s, selectedIndex: filteredItems.length - 1 }))
		}
	})

	function close() {
		palette.set({ open: false, mode: "nav", query: "", selectedIndex: 0 })
	}

	function selectItem(item: CommandItemData) {
		if (item.href) {
			goto(item.href)
		} else if (item.action) {
			item.action()
		}
		close()
	}

	function handleKeydown(e: KeyboardEvent) {
		if (!palette.value.open) return

		switch (e.key) {
			case "Escape":
				e.preventDefault()
				close()
				break
			case "ArrowDown":
			case "j":
				if (e.key === "j" && !e.ctrlKey && document.activeElement?.tagName === "INPUT") break
				e.preventDefault()
				palette.update((s) => ({
					...s,
					selectedIndex: Math.min(s.selectedIndex + 1, filteredItems.length - 1),
				}))
				break
			case "ArrowUp":
			case "k":
				if (e.key === "k" && !e.ctrlKey && document.activeElement?.tagName === "INPUT") break
				e.preventDefault()
				palette.update((s) => ({
					...s,
					selectedIndex: Math.max(s.selectedIndex - 1, 0),
				}))
				break
			case "Enter":
				e.preventDefault()
				if (filteredItems[palette.value.selectedIndex]) {
					selectItem(filteredItems[palette.value.selectedIndex])
				}
				break
		}
	}

	function handleBackdropClick(e: MouseEvent) {
		if (e.target === e.currentTarget) {
			close()
		}
	}

	function handleQueryChange(query: string) {
		palette.update((s) => ({ ...s, query, selectedIndex: 0 }))
	}
</script>

<svelte:window onkeydown={handleKeydown} />

{#if palette.value.open}
	<div
		class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
		onclick={handleBackdropClick}
		onkeydown={(e) => e.key === "Escape" && close()}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
	>
		<div
			class={cn(
				"fixed left-1/2 top-1/4 z-50 w-full max-w-lg -translate-x-1/2 rounded-lg border border-border bg-popover p-0 shadow-lg",
				className
			)}
		>
			<CommandInput
				value={palette.value.query}
				placeholder={isNavMode ? "Where to?" : "Search..."}
				oninput={handleQueryChange}
				bind:ref={inputRef}
			/>
			<CommandList>
				{#if showEmptySearch}
					<div class="py-6 text-center text-sm text-muted-foreground">
						Type to search...
					</div>
				{:else if filteredItems.length === 0}
					<CommandEmpty />
				{:else}
					{#each Object.entries(grouped) as [group, groupItems]}
						<div class="px-2 py-1.5">
							<p class="px-2 text-xs font-medium text-muted-foreground">{group}</p>
						</div>
						{#each groupItems as item}
							{@const globalIndex = filteredItems.indexOf(item)}
							<div class="px-2">
								<CommandItemRow
									icon={item.icon}
									nerd={item.nerd}
									label={item.label}
									shortcut={item.shortcut}
									selected={globalIndex === palette.value.selectedIndex}
									onSelect={() => selectItem(item)}
								/>
							</div>
						{/each}
					{/each}
				{/if}
			</CommandList>
			<div
				class="flex items-center justify-between border-t border-border px-3 py-2 text-xs text-muted-foreground"
			>
				<span>↑↓ to navigate</span>
				<span>↵ to select</span>
				<span>esc to close</span>
			</div>
		</div>
	</div>
{/if}
