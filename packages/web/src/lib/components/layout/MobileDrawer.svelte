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
		class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
		onclick={handleBackdropClick}
		onkeydown={handleKeydown}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
	>
		<div
			class={cn(
				"fixed inset-y-0 left-0 z-50 h-full w-3/4 max-w-sm border-r border-border bg-background p-6 shadow-lg transition-transform",
				className
			)}
		>
			<div class="flex items-center justify-between">
				<a href="/" class="flex items-center gap-2" onclick={() => close()}>
					<Logo />
					<SiteName />
				</a>
				<button
					type="button"
					class="flex h-9 w-9 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent/10 hover:text-foreground"
					onclick={() => close()}
					aria-label="Close menu"
				>
					<span style="font-family: var(--font-icons)" class="text-xl"></span>
				</button>
			</div>

			<nav class="mt-8 flex flex-col gap-2">
				{#each navigationItems as item}
					<button
						type="button"
						class="flex items-center gap-3 rounded-md px-3 py-2 text-left text-sm text-foreground transition-colors hover:bg-accent/10"
						onclick={() => item.href && navigate(item.href)}
					>
						{#if item.nerd}
							<span style="font-family: var(--font-icons)" class="text-muted-foreground">
								{item.nerd}
							</span>
						{/if}
						<span>{item.label}</span>
					</button>
				{/each}
			</nav>

			<div class="absolute bottom-6 left-6">
				<SocialLinks size="md" />
			</div>
		</div>
	</div>
{/if}
