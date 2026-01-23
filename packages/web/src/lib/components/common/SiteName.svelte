<script lang="ts">
import { cn } from "$lib/utils"

interface Props {
	class?: string
}

let { class: className }: Props = $props()
</script>

<span class={cn("font-mono text-sm text-green transition-colors hover:text-peach", className)}>wrath.codes</span>
