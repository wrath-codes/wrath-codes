<script lang="ts">
	import { cn } from "$lib/utils"

	interface Props {
		class?: string
		size?: "sm" | "md" | "lg"
	}

	let { class: className, size = "sm" }: Props = $props()

	const sizeClasses = {
		sm: "h-6 w-auto",
		md: "h-8 w-auto",
		lg: "h-10 w-auto",
	}
</script>

<img src="/logo.svg" alt="wrath.codes logo" class={cn(sizeClasses[size], className)} />
