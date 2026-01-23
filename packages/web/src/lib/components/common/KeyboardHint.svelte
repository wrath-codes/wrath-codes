<script lang="ts">
import { cn } from "$lib/utils"
import Kbd from "./Kbd.svelte"

interface Props {
	class?: string
}

let { class: className }: Props = $props()

const isMac = typeof navigator !== "undefined" && /Mac|iPod|iPhone|iPad/.test(navigator.platform)
const modKey = isMac ? "⌘" : "Ctrl"
</script>

<div class={cn("hidden items-center gap-3 text-xs text-muted-foreground sm:flex", className)}>
	<span class="flex items-center gap-1">
		<Kbd size="md">{modKey}</Kbd>
		<span>+</span>
		<Kbd>P</Kbd>
		<span>nav</span>
	</span>
	<span class="text-border">·</span>
	<span class="flex items-center gap-1">
		<Kbd size="md">{modKey}</Kbd>
		<span>+</span>
		<Kbd>K</Kbd>
		<span>search</span>
	</span>
</div>
