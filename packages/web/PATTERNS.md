# Development Patterns

## Stack

- **Runtime**: Bun
- **Framework**: SvelteKit 5 (static adapter)
- **State**: effect-atom with custom Svelte hooks
- **Styling**: TailwindCSS v4 + shadcn-svelte
- **Testing**: Vitest + @effect/vitest
- **Linting**: Biome

## Theme: Catppuccin Mocha

Custom colors defined in `src/app.css`:

```css
--primary: oklch(0.762 0.152 304.987);  /* mauve */
--peach: oklch(0.838 0.128 62.986);
--green: oklch(0.839 0.134 143.537);
--mantle: oklch(0.214 0.017 264.182);
```

Use via Tailwind: `text-peach`, `bg-mauve`, `text-green`, `bg-mantle`

## Component Structure

```
src/lib/components/
├── ui/           # shadcn-svelte base components
├── common/       # Logo, SiteName, Kbd, KeyboardHint, Icon, SocialLinks
├── command/      # CommandPalette, CommandInput, CommandList, CommandItem
└── layout/       # Header, Footer, MobileDrawer
```

## Svelte 5 Patterns

### Props with $props()

```svelte
<script lang="ts">
  interface Props {
    class?: string
    size?: "sm" | "md"
  }

  let { class: className, size = "sm" }: Props = $props()
</script>
```

### Reactive state with $state and $derived

```svelte
<script lang="ts">
  let count = $state(0)
  const doubled = $derived(count * 2)
</script>
```

### Effects with $effect

```svelte
<script lang="ts">
  $effect(() => {
    // runs when dependencies change
    return () => {
      // cleanup
    }
  })
</script>
```

### Snippets for children

```svelte
<script lang="ts">
  import type { Snippet } from "svelte"

  interface Props {
    children: Snippet
  }

  let { children }: Props = $props()
</script>

{@render children()}
```

## effect-atom Integration

### Registry (singleton)

```ts
// src/lib/stores/registry.ts
import { Registry } from "@effect-atom/atom"
export const registry = Registry.make()
```

### Creating atoms

```ts
// src/lib/stores/command-palette.ts
import { Atom } from "@effect-atom/atom"

export const commandPaletteAtom = Atom.make({
  open: false,
  mode: "nav" as "nav" | "search",
  query: "",
  selectedIndex: 0,
})
```

### Svelte hooks for atoms

```ts
// src/lib/stores/use-atom.svelte.ts
import { registry } from "./registry"

export function useWritableAtom<R, W>(atom: Writable<R, W>) {
  let value = $state(registry.get(atom))

  $effect(() => {
    const unsubscribe = registry.subscribe(atom, (newValue) => {
      value = newValue
    })
    return unsubscribe
  })

  return {
    get value() { return value },
    set(newValue: W) { registry.set(atom, newValue) },
    update(fn: (current: R) => W) { registry.update(atom, fn) },
  }
}
```

### Using atoms in components

```svelte
<script lang="ts">
  import { useWritableAtom, commandPaletteAtom } from "$lib/stores"

  const palette = useWritableAtom(commandPaletteAtom)

  // Read
  if (palette.value.open) { ... }

  // Write
  palette.set({ ...palette.value, open: true })

  // Update
  palette.update((s) => ({ ...s, selectedIndex: s.selectedIndex + 1 }))
</script>
```

## cn() Utility

Merge Tailwind classes with clsx + tailwind-merge:

```svelte
<script lang="ts">
  import { cn } from "$lib/utils"
</script>

<div class={cn("base-classes", conditional && "conditional-class", className)} />
```

## Testing with @effect/vitest

```ts
import { describe, it, expect } from "@effect/vitest"
import { Effect } from "effect"

describe("feature", () => {
  it.effect("test name", () =>
    Effect.gen(function* () {
      const result = someFunction()
      expect(result).toBe(expected)
    })
  )
})
```

Run tests: `bunx vitest run`

## Keyboard Navigation Pattern

```svelte
<script lang="ts">
  function handleKeydown(e: KeyboardEvent) {
    switch (e.key) {
      case "ArrowDown":
      case "j":
        if (e.key === "j" && !e.ctrlKey && document.activeElement?.tagName === "INPUT") break
        e.preventDefault()
        // move down
        break
      case "ArrowUp":
      case "k":
        if (e.key === "k" && !e.ctrlKey && document.activeElement?.tagName === "INPUT") break
        e.preventDefault()
        // move up
        break
      case "Enter":
        e.preventDefault()
        // select
        break
      case "Escape":
        e.preventDefault()
        // close
        break
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />
```

## Auto-scroll to selected item

```svelte
<script lang="ts">
  let buttonRef: HTMLButtonElement | null = $state(null)

  $effect(() => {
    if (selected && buttonRef) {
      buttonRef.scrollIntoView({ block: "nearest", behavior: "smooth" })
    }
  })
</script>

<button bind:this={buttonRef}>...</button>
```

## Hide scrollbar CSS

```svelte
<style>
  .scrollbar-none {
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  .scrollbar-none::-webkit-scrollbar {
    display: none;
  }
</style>
```

## Static Assets

Place in `static/`:
- `/logo.svg` - site logo
- `/favicons/` - favicon files
- `/fonts/` - custom fonts

Reference as `/logo.svg` in components.

## Barrel Exports

Each component folder has an `index.ts`:

```ts
// src/lib/components/common/index.ts
export { default as Logo } from "./Logo.svelte"
export { default as SiteName } from "./SiteName.svelte"
// ...
```

Import: `import { Logo, SiteName } from "$lib/components/common"`
