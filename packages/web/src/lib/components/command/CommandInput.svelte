<script lang="ts">
import { cn } from "$lib/utils"

interface Props {
	value?: string
	placeholder?: string
	class?: string
	oninput?: (value: string) => void
	ref?: HTMLInputElement | null
}

let {
	value = $bindable(""),
	placeholder = "Type a command...",
	class: className,
	oninput,
	ref = $bindable(null),
}: Props = $props()

function handleInput(e: Event) {
	const target = e.target as HTMLInputElement
	value = target.value
	oninput?.(value)
}
</script>

<div class={cn("flex items-center border-b border-border px-3", className)}>
	<span class="mr-2 text-muted-foreground" style="font-family: var(--font-icons)"></span>
	<input
		bind:this={ref}
		type="text"
		{value}
		{placeholder}
		oninput={handleInput}
		class="flex h-11 w-full bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50"
	/>
</div>
