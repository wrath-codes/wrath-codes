import type { CommandItemData } from "$lib/components/command"

export const navigationItems: CommandItemData[] = [
	{
		id: "home",
		label: "About",
		href: "/",
		nerd: "",
		shortcut: "1",
		group: "Navigation",
	},
	{
		id: "projects",
		label: "Projects",
		href: "/projects",
		nerd: "",
		shortcut: "2",
		group: "Navigation",
	},
	{
		id: "blog",
		label: "Blog",
		href: "/blog",
		nerd: "",
		shortcut: "3",
		group: "Navigation",
	},
	{
		id: "resume",
		label: "Resume",
		href: "/resume",
		nerd: "",
		shortcut: "4",
		group: "Navigation",
	},
	{
		id: "contact",
		label: "Contact",
		href: "/contact",
		nerd: "",
		shortcut: "5",
		group: "Navigation",
	},
]

export const externalLinks: CommandItemData[] = [
	{
		id: "github",
		label: "GitHub",
		href: "https://github.com/wrath-codes",
		nerd: "",
		group: "External",
	},
	{
		id: "linkedin",
		label: "LinkedIn",
		href: "https://linkedin.com/in/wrath-codes",
		nerd: "",
		group: "External",
	},
	{
		id: "twitter",
		label: "X (Twitter)",
		href: "https://x.com/wrath_codes",
		nerd: "",
		group: "External",
	},
]
