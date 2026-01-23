<script lang="ts">
import { cn } from "$lib/utils"

interface SocialLink {
	name: string
	href: string
	icon: string
	label: string
}

interface Props {
	class?: string
	size?: "sm" | "md"
}

let { class: className, size = "md" }: Props = $props()

const links: SocialLink[] = [
	{ name: "GitHub", href: "https://github.com/wrath-codes", icon: "", label: "GitHub" },
	{
		name: "LinkedIn",
		href: "https://linkedin.com/in/wrath-codes",
		icon: "",
		label: "LinkedIn",
	},
	{ name: "X", href: "https://x.com/wrath_codes", icon: "", label: "X (Twitter)" },
]

const sizeClasses = {
	sm: "text-lg gap-3",
	md: "text-xl gap-4",
}
</script>

<div class={cn("flex items-center", sizeClasses[size], className)}>
	{#each links as link}
		<a
			href={link.href}
			target="_blank"
			rel="noopener noreferrer"
			aria-label={link.label}
			class="text-muted-foreground transition-colors hover:text-foreground"
			style="font-family: var(--font-icons)"
		>
			{link.icon}
		</a>
	{/each}
</div>
