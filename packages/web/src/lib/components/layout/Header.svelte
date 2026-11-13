<script lang="ts">
	import { cn } from "$lib/utils";
	import KeyboardHint from "../common/KeyboardHint.svelte";
	import Logo from "../common/Logo.svelte";
	import SiteName from "../common/SiteName.svelte";
	import SocialLinks from "../common/SocialLinks.svelte";

	interface Props {
		class?: string;
		onMenuClick?: () => void;
	}

	let { class: className, onMenuClick }: Props = $props();
</script>

<header class={cn("sticky top-0 z-40 w-full bg-crust", className)}>
	<div class="container mx-auto flex h-12 items-center justify-between px-4">
		<a href="/" class="flex items-center gap-2">
			<Logo />
			<SiteName />
		</a>

		<div class="flex items-center gap-4">
			<KeyboardHint />

			<button
				type="button"
				class="flex h-8 w-8 items-center justify-center text-muted-foreground transition-colors hover:text-foreground sm:hidden"
				onclick={() => onMenuClick?.()}
				aria-label="Open menu"
			>
				<span style="font-family: var(--font-icons)" class="text-lg"
				></span>
			</button>
		</div>
	</div>
</header>
