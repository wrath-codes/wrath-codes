import { describe, expect, it } from "@effect/vitest"
import { Effect } from "effect"
import { filterItems, groupItems } from "$lib/stores"
import type { CommandItemData } from "./types"

const mockItems: CommandItemData[] = [
	{ id: "home", label: "About", href: "/", group: "Navigation" },
	{ id: "projects", label: "Projects", href: "/projects", group: "Navigation" },
	{ id: "blog", label: "Blog", href: "/blog", group: "Navigation" },
	{ id: "github", label: "GitHub", href: "https://github.com", group: "External" },
]

const clampIndex = (index: number, length: number): number => {
	if (length === 0) return 0
	return Math.min(Math.max(0, index), length - 1)
}

describe("CommandPalette filtering", () => {
	it.effect("filters items by partial label match", () =>
		Effect.gen(function* () {
			const filtered = filterItems(mockItems, "proj")
			expect(filtered).toHaveLength(1)
			expect(filtered[0].id).toBe("projects")
		}),
	)

	it.effect("returns all items for empty query", () =>
		Effect.gen(function* () {
			const filtered = filterItems(mockItems, "")
			expect(filtered).toHaveLength(4)
		}),
	)

	it.effect("matches case-insensitively", () =>
		Effect.gen(function* () {
			const filtered = filterItems(mockItems, "ABOUT")
			expect(filtered).toHaveLength(1)
			expect(filtered[0].id).toBe("home")
		}),
	)

	it.effect("returns empty array when no match", () =>
		Effect.gen(function* () {
			const filtered = filterItems(mockItems, "nonexistent")
			expect(filtered).toHaveLength(0)
		}),
	)
})

describe("CommandPalette grouping", () => {
	it.effect("groups items by group property", () =>
		Effect.gen(function* () {
			const groups = groupItems(mockItems)
			expect(Object.keys(groups)).toEqual(["Navigation", "External"])
			expect(groups.Navigation).toHaveLength(3)
			expect(groups.External).toHaveLength(1)
		}),
	)

	it.effect("uses 'Commands' as default group", () =>
		Effect.gen(function* () {
			const itemsWithoutGroup: CommandItemData[] = [{ id: "test", label: "Test" }]
			const groups = groupItems(itemsWithoutGroup)
			expect(Object.keys(groups)).toEqual(["Commands"])
		}),
	)
})

describe("CommandPalette navigation index", () => {
	it.effect("clamps index to valid range", () =>
		Effect.gen(function* () {
			expect(clampIndex(5, 3)).toBe(2)
			expect(clampIndex(-1, 3)).toBe(0)
			expect(clampIndex(1, 3)).toBe(1)
		}),
	)

	it.effect("handles empty list", () =>
		Effect.gen(function* () {
			expect(clampIndex(0, 0)).toBe(0)
			expect(clampIndex(5, 0)).toBe(0)
		}),
	)

	it.effect("arrow down increases index within bounds", () =>
		Effect.gen(function* () {
			const length = 3
			let index = 0
			index = Math.min(index + 1, length - 1)
			expect(index).toBe(1)
			index = Math.min(index + 1, length - 1)
			expect(index).toBe(2)
			index = Math.min(index + 1, length - 1)
			expect(index).toBe(2) // stays at max
		}),
	)

	it.effect("arrow up decreases index within bounds", () =>
		Effect.gen(function* () {
			let index = 2
			index = Math.max(index - 1, 0)
			expect(index).toBe(1)
			index = Math.max(index - 1, 0)
			expect(index).toBe(0)
			index = Math.max(index - 1, 0)
			expect(index).toBe(0) // stays at min
		}),
	)
})
