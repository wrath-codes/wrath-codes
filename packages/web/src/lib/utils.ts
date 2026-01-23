import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import type { Component } from "svelte"

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs))
}

export type WithElementRef<T, E extends HTMLElement = HTMLElement> = T & {
	ref?: E | null
}

export type WithoutChildren<T> = T extends { children?: unknown }
	? Omit<T, "children">
	: T

export type WithoutChildrenOrChild<T> = T extends { children?: unknown; child?: unknown }
	? Omit<T, "children" | "child">
	: T

// biome-ignore lint/suspicious/noExplicitAny: Required for component type inference
export type ComponentProps<T extends Component<any>> =
	T extends Component<infer P> ? P : never
