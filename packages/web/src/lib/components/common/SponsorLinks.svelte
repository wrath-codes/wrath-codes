<script lang="ts">
import { cn } from "$lib/utils"

interface SponsorLink {
	name: string
	href: string
	icon: string
	label: string
}

interface Props {
	class?: string
}

let { class: className }: Props = $props()

const links: SponsorLink[] = [
	{
		name: "GitHub Sponsors",
		href: "https://github.com/sponsors/wrath-codes",
		icon: "",
		label: "Sponsor on GitHub",
	},
	{
		name: "Buy Me a Coffee",
		href: "https://buymeacoffee.com/wrathcodes",
		icon: "",
		label: "Buy Me a Coffee",
	},
]
</script>

<div class={cn("flex items-center gap-4", className)}>
	{#each links as link}
		<a
			href={link.href}
			target="_blank"
			rel="noopener noreferrer"
			aria-label={link.label}
			class="flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
		>
			<span style="font-family: var(--font-icons)">{link.icon}</span>
			<span class="hidden sm:inline">{link.name}</span>
		</a>
	{/each}
</div>
