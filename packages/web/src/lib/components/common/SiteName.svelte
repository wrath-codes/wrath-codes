<script lang="ts">
import { cn } from "$lib/utils"

interface Props {
	class?: string
}

let { class: className }: Props = $props()
</script>

<span class={cn("font-mono text-sm text-muted-foreground", className)}>wrath.codes</span>
