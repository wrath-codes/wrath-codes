import type { Component } from "svelte"

export interface CommandItemData {
	id: string
	label: string
	href?: string
	action?: () => void
	icon?: Component<{ class?: string }>
	nerd?: string
	shortcut?: string
	group?: string
}
