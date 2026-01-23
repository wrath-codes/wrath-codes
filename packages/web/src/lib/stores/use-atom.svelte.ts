import type { Atom, Writable } from "@effect-atom/atom/Atom"
import { registry } from "./registry"

export function useAtom<A>(atom: Atom<A>): { readonly value: A } {
	let value = $state(registry.get(atom))

	$effect(() => {
		const unsubscribe = registry.subscribe(atom, (newValue) => {
			value = newValue
		})
		return unsubscribe
	})

	return {
		get value() {
			return value
		},
	}
}

export function useWritableAtom<R, W>(
	atom: Writable<R, W>,
): { readonly value: R; set: (value: W) => void; update: (fn: (current: R) => W) => void } {
	let value = $state(registry.get(atom))

	$effect(() => {
		const unsubscribe = registry.subscribe(atom, (newValue) => {
			value = newValue
		})
		return unsubscribe
	})

	return {
		get value() {
			return value
		},
		set(newValue: W) {
			registry.set(atom, newValue)
		},
		update(fn: (current: R) => W) {
			registry.update(atom, fn)
		},
	}
}
