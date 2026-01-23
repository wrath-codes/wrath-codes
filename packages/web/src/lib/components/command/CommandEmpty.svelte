<script lang="ts">
import { cn } from "$lib/utils"

interface Props {
	class?: string
}

let { class: className }: Props = $props()
</script>

<div class={cn("py-6 text-center text-sm text-muted-foreground", className)}>No results found.</div>
