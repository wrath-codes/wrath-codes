<script lang="ts">
import "../app.css"
import { CommandPalette } from "$lib/components/command"
import { Footer, Header, MobileDrawer } from "$lib/components/layout"
import { externalLinks, navigationItems } from "$lib/content/navigation"
import { commandPaletteAtom, registry } from "$lib/stores"

let { children } = $props()

let drawerOpen = $state(false)

const allItems = [...navigationItems, ...externalLinks]

function handleGlobalKeydown(e: KeyboardEvent) {
	const isMod = e.metaKey || e.ctrlKey

	if (isMod && e.key === "p") {
		e.preventDefault()
		registry.set(commandPaletteAtom, {
			open: true,
			mode: "nav",
			query: "",
			selectedIndex: 0,
		})
	} else if (isMod && e.key === "k") {
		e.preventDefault()
		registry.set(commandPaletteAtom, {
			open: true,
			mode: "search",
			query: "",
			selectedIndex: 0,
		})
	}
}
</script>

<svelte:window onkeydown={handleGlobalKeydown} />

<div class="flex min-h-screen flex-col">
	<Header onMenuClick={() => (drawerOpen = true)} />

	<main class="flex-1">
		{@render children()}
	</main>

	<Footer />
</div>

<CommandPalette items={allItems} />
<MobileDrawer bind:open={drawerOpen} />
