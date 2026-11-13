<script lang="ts">
import { cn } from "$lib/utils"

interface Props {
	class?: string
}

let { class: className }: Props = $props()
</script>

<span class={cn("font-mono text-sm text-foreground transition-colors hover:text-lavender", className)}>wrath.codes</span>
