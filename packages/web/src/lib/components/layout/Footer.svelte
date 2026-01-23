<script lang="ts">
import { cn } from "$lib/utils"
import SocialLinks from "../common/SocialLinks.svelte"

interface Props {
	class?: string
}

let { class: className }: Props = $props()

const currentYear = new Date().getFullYear()
</script>

<footer class={cn("border-t border-border py-6", className)}>
	<div class="container mx-auto flex flex-col items-center gap-4 px-4">
		<SocialLinks size="sm" />
		<p class="text-center text-sm text-muted-foreground">
			© {currentYear} wrath.codes. All rights reserved.
		</p>
	</div>
</footer>
