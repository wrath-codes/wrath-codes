<script lang="ts">
import { cn } from "$lib/utils"
import KeyboardHint from "../common/KeyboardHint.svelte"
import Logo from "../common/Logo.svelte"
import SiteName from "../common/SiteName.svelte"
import SocialLinks from "../common/SocialLinks.svelte"

interface Props {
	class?: string
	onMenuClick?: () => void
}

let { class: className, onMenuClick }: Props = $props()
</script>

<header
	class={cn(
		"sticky top-0 z-40 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60",
		className
	)}
>
	<div class="container mx-auto flex h-14 items-center justify-between px-4">
		<a href="/" class="flex items-center gap-2">
			<Logo />
			<SiteName />
		</a>

		<div class="flex items-center gap-4">
			<KeyboardHint />
			<SocialLinks size="sm" class="hidden sm:flex" />

			<button
				type="button"
				class="flex h-9 w-9 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent/10 hover:text-foreground sm:hidden"
				onclick={() => onMenuClick?.()}
				aria-label="Open menu"
			>
				<span style="font-family: var(--font-icons)" class="text-xl"></span>
			</button>
		</div>
	</div>
</header>
