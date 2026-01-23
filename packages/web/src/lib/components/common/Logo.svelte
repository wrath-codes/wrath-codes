<script lang="ts">
import { cn } from "$lib/utils"

interface Props {
	class?: string
	size?: "sm" | "md" | "lg"
}

let { class: className, size = "sm" }: Props = $props()

const sizeClasses = {
	sm: "w-6 h-6 text-xs",
	md: "w-8 h-8 text-sm",
	lg: "w-10 h-10 text-base",
}
</script>

<div
	class={cn(
		"flex items-center justify-center rounded-md bg-primary text-primary-foreground font-mono font-bold",
		sizeClasses[size],
		className
	)}
>
	W
</div>
