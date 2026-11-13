<script lang="ts">
	import { SocialLinks, SponsorLinks } from "$lib/components/common";
	import { Badge } from "$lib/components/ui/badge";
	import { resumeData } from "$lib/content/resume";
</script>

<svelte:head>
	<title>About | wrath.codes</title>
	<meta
		name="description"
		content="Data Engineer & Python Developer focused on high-performance data pipelines and backend systems."
	/>
</svelte:head>

<div class="container mx-auto max-w-4xl px-4 py-8">
	<!-- Hero Section -->
	<section class="border border-border p-4 space-y-3">
		<h2 class="text-mauve font-bold text-sm">about</h2>
		<div class="space-y-1">
			<h1 class="text-2xl font-medium">
				<span class="text-foreground">{resumeData.name}</span>
			</h1>
			<p class="text-lavender">{resumeData.title}</p>
		</div>
		<p class="text-muted-foreground text-sm leading-relaxed">
			{resumeData.summary}
		</p>
		<div
			class="flex flex-wrap items-center gap-4 pt-2 text-sm text-muted-foreground border-t border-border mt-3 pt-3"
		>
			<span class="flex items-center gap-1">
				<span
					style="font-family: var(--font-icons)"
					class="text-lavender"
				></span>
				{resumeData.contact.location}
			</span>
			<a
				href="mailto:{resumeData.contact.email}"
				class="flex items-center gap-1 hover:text-blue transition-colors"
			>
				<span style="font-family: var(--font-icons)" class="text-mauve"
				></span>
				{resumeData.contact.email}
			</a>
		</div>
		<div class="flex flex-wrap gap-4 pt-2">
			<SponsorLinks />
		</div>
	</section>

	<!-- What I Work With -->
	<section class="mt-6 space-y-3">
		<h2 class="text-sm text-mauve font-bold">skills</h2>
		<div class="border border-border p-4">
			<div class="flex flex-wrap gap-2">
				{#each resumeData.skills.slice(0, 14) as skill}
					<Badge variant="outline" class="text-xs">{skill.name}</Badge
					>
				{/each}
			</div>
		</div>
	</section>

	<!-- Current Focus -->
	<section class="mt-6 space-y-3">
		<h2 class="text-sm text-mauve font-bold">focus</h2>
		<div class="grid gap-px sm:grid-cols-2 border border-border">
			<div
				class="p-4 space-y-2 border-b sm:border-b-0 sm:border-r border-border"
			>
				<div class="flex items-center gap-2 text-sm">
					<span
						style="font-family: var(--font-icons)"
						class="text-lavender">{"\uF445"}</span
					>
					<span class="text-foreground">Data Engineering</span>
				</div>
				<p class="text-xs text-muted-foreground pl-4">
					High-performance pipelines with Polars, Prefect, Dagster
				</p>
			</div>
			<div class="p-4 space-y-2 border-b sm:border-b-0 border-border">
				<div class="flex items-center gap-2 text-sm">
					<span
						style="font-family: var(--font-icons)"
						class="text-lavender">{"\uF445"}</span
					>
					<span class="text-foreground">Python & Rust</span>
				</div>
				<p class="text-xs text-muted-foreground pl-4">
					I/O plugins for Polars using Rust and pyo3
				</p>
			</div>
			<div
				class="p-4 space-y-2 border-b sm:border-b-0 sm:border-r border-border"
			>
				<div class="flex items-center gap-2 text-sm">
					<span
						style="font-family: var(--font-icons)"
						class="text-lavender">{"\uF445"}</span
					>
					<span class="text-foreground">Backend APIs</span>
				</div>
				<p class="text-xs text-muted-foreground pl-4">
					Async APIs with FastAPI and Pydantic validation
				</p>
			</div>
			<div class="p-4 space-y-2">
				<div class="flex items-center gap-2 text-sm">
					<span
						style="font-family: var(--font-icons)"
						class="text-lavender">{"\uF445"}</span
					>
					<span class="text-foreground">AI Integration</span>
				</div>
				<p class="text-xs text-muted-foreground pl-4">
					LangChain for workflow automation
				</p>
			</div>
		</div>
	</section>

	<!-- Open Source -->
	<section class="mt-6 space-y-3">
		<h2 class="text-sm text-mauve font-bold">open source</h2>
		<a
			href="https://pypi.org/project/klaw-dbase/"
			target="_blank"
			rel="noopener noreferrer"
			class="block border border-border p-4 space-y-2 hover:border-blue transition-colors"
		>
			<div class="flex items-center justify-between text-sm">
				<span class="text-foreground">klaw-dbase</span>
				<span class="text-lavender text-xs">pypi.org →</span>
			</div>
			<p class="text-xs text-muted-foreground">
				Polars I/O plugin for DBF and DATASUS (.DBC) formats. Built with
				Rust and pyo3.
			</p>
		</a>
	</section>

	<!-- Navigation -->
	<section class="mt-6 space-y-3">
		<h2 class="text-sm text-mauve font-bold">navigate</h2>
		<div class="grid gap-px sm:grid-cols-3 border border-border">
			<a
				href="/projects"
				class="group p-4 border-b sm:border-b-0 sm:border-r border-border hover:bg-muted/20 transition-colors"
			>
				<div class="flex items-center gap-2 text-sm">
					<span
						class="text-lavender group-hover:text-mauve transition-colors"
						>></span
					>
					<span class="group-hover:text-mauve transition-colors"
						>projects</span
					>
				</div>
			</a>
			<a
				href="/blog"
				class="group p-4 border-b sm:border-b-0 sm:border-r border-border hover:bg-muted/20 transition-colors"
			>
				<div class="flex items-center gap-2 text-sm">
					<span
						class="text-lavender group-hover:text-mauve transition-colors"
						>></span
					>
					<span class="group-hover:text-mauve transition-colors"
						>blog</span
					>
				</div>
			</a>
			<a
				href="/resume"
				class="group p-4 hover:bg-muted/20 transition-colors"
			>
				<div class="flex items-center gap-2 text-sm">
					<span
						class="text-lavender group-hover:text-mauve transition-colors"
						>></span
					>
					<span class="group-hover:text-mauve transition-colors"
						>resume</span
					>
				</div>
			</a>
		</div>
	</section>
</div>
