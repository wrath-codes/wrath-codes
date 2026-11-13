<script lang="ts">
import { goto } from "$app/navigation"
import { navigationItems } from "$lib/content/navigation"
import { cn } from "$lib/utils"
import Logo from "../common/Logo.svelte"
import SiteName from "../common/SiteName.svelte"
import SocialLinks from "../common/SocialLinks.svelte"

interface Props {
	open?: boolean
	onClose?: () => void
	class?: string
}

let { open = $bindable(false), onClose, class: className }: Props = $props()

function close() {
	open = false
	onClose?.()
}

function navigate(href: string) {
	goto(href)
	close()
}

function handleKeydown(e: KeyboardEvent) {
	if (e.key === "Escape") {
		close()
	}
}

function handleBackdropClick(e: MouseEvent) {
	if (e.target === e.currentTarget) {
		close()
	}
}
</script>

{#if open}
	<div
		class="fixed inset-0 z-50 bg-background/90"
		onclick={handleBackdropClick}
		onkeydown={handleKeydown}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
	>
		<div
			class={cn(
				"fixed inset-y-0 left-0 z-50 h-full w-3/4 max-w-sm border-r border-border bg-background p-4",
				className
			)}
		>
			<div class="flex items-center justify-between border-b border-border pb-3">
				<a href="/" class="flex items-center gap-2" onclick={() => close()}>
					<Logo />
					<SiteName />
				</a>
				<button
					type="button"
					class="flex h-8 w-8 items-center justify-center text-muted-foreground transition-colors hover:text-foreground"
					onclick={() => close()}
					aria-label="Close menu"
				>
					<span style="font-family: var(--font-icons)" class="text-lg"></span>
				</button>
			</div>

			<nav class="mt-4 flex flex-col">
				<div class="text-xs text-muted-foreground mb-2">// navigation</div>
				{#each navigationItems as item}
					<button
						type="button"
						class="flex items-center gap-2 px-2 py-1.5 text-left text-sm text-foreground transition-colors hover:bg-muted/30"
						onclick={() => item.href && navigate(item.href)}
					>
						<span class="text-muted-foreground">></span>
						<span>{item.label.toLowerCase()}</span>
					</button>
				{/each}
			</nav>

			<div class="absolute bottom-4 left-4">
				<SocialLinks size="sm" />
			</div>
		</div>
	</div>
{/if}
