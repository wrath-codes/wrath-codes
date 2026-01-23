import { Atom } from "@effect-atom/atom"
import type { CommandItemData } from "$lib/components/command/types"

export interface CommandPaletteState {
	open: boolean
	mode: "nav" | "search"
	query: string
	selectedIndex: number
}

const initialState: CommandPaletteState = {
	open: false,
	mode: "nav",
	query: "",
	selectedIndex: 0,
}

export const commandPaletteAtom = Atom.make(initialState)

export const filterItems = (items: CommandItemData[], query: string): CommandItemData[] =>
	items.filter((item) => item.label.toLowerCase().includes(query.toLowerCase()))

export const groupItems = (items: CommandItemData[]): Record<string, CommandItemData[]> => {
	const groups: Record<string, CommandItemData[]> = {}
	for (const item of items) {
		const group = item.group ?? "Commands"
		if (!groups[group]) groups[group] = []
		groups[group].push(item)
	}
	return groups
}
