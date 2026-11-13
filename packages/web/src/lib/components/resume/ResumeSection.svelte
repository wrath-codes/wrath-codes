<script lang="ts">
	import { Badge } from "$lib/components/ui/badge";
	import type { Resume } from "$lib/content/resume";
	import { cn } from "$lib/utils";

	interface Props {
		resume: Resume;
		class?: string;
	}

	let { resume, class: className }: Props = $props();

	const skillsByCategory = $derived(
		resume.skills.reduce(
			(acc, skill) => {
				if (!acc[skill.category]) acc[skill.category] = [];
				acc[skill.category].push(skill.name);
				return acc;
			},
			{} as Record<string, string[]>,
		),
	);

	const categoryLabels: Record<string, string> = {
		language: "languages",
		framework: "frameworks",
		tool: "tools",
		platform: "platforms",
		database: "databases",
		other: "other",
	};

	const categoryColors: Record<string, string> = {
		language: "text-lavender",
		framework: "text-lavender",
		tool: "text-lavender",
		platform: "text-lavender",
		database: "text-lavender",
		other: "text-muted-foreground",
	};

	function formatDate(date: string): string {
		const [year, month] = date.split("-");
		const monthNames = [
			"Jan",
			"Feb",
			"Mar",
			"Apr",
			"May",
			"Jun",
			"Jul",
			"Aug",
			"Sep",
			"Oct",
			"Nov",
			"Dec",
		];
		return `${monthNames[parseInt(month, 10) - 1]} ${year}`;
	}
</script>

<div class={cn("space-y-6", className)}>
	<!-- Header -->
	<header class="border border-border p-4 space-y-2">
		<div class="text-mauve text-sm font-bold">profile</div>
		<h1 class="text-xl text-foreground">{resume.name}</h1>
		<p class="text-lavender text-sm">{resume.title}</p>
		<p class="text-muted-foreground text-sm leading-relaxed">
			{resume.summary}
		</p>
		<div
			class="flex flex-wrap gap-4 pt-2 text-xs text-muted-foreground border-t border-border mt-2 pt-2"
		>
			<span class="flex items-center gap-1">
				<span style="font-family: var(--font-icons)" class="text-mauve"
				></span>
				{resume.contact.email}
			</span>
			<span class="flex items-center gap-1">
				<span
					style="font-family: var(--font-icons)"
					class="text-lavender"
				></span>
				{resume.contact.location}
			</span>
			{#if resume.contact.website}
				<a
					href={resume.contact.website}
					class="flex items-center gap-1 text-blue hover:text-lavender transition-colors"
				>
					<span style="font-family: var(--font-icons)"></span>
					{resume.contact.website.replace("https://", "")}
				</a>
			{/if}
			{#if resume.contact.github}
				<a
					href={resume.contact.github}
					class="flex items-center gap-1 hover:text-blue transition-colors"
				>
					<span style="font-family: var(--font-icons)"></span>
					github
				</a>
			{/if}
			{#if resume.contact.linkedin}
				<a
					href={resume.contact.linkedin}
					class="flex items-center gap-1 hover:text-mauve transition-colors"
				>
					<span style="font-family: var(--font-icons)"></span>
					linkedin
				</a>
			{/if}
		</div>
	</header>

	<!-- Skills -->
	<section class="space-y-2">
		<h2 class="text-sm text-mauve font-bold">skills</h2>
		<div class="border border-border p-4 space-y-2">
			{#each Object.entries(skillsByCategory) as [category, skills]}
				<div class="flex flex-wrap items-baseline gap-2 text-xs">
					<span class={cn("w-20", categoryColors[category])}>
						{categoryLabels[category] ?? category}:
					</span>
					<span class="text-muted-foreground">
						{skills.join(" · ")}
					</span>
				</div>
			{/each}
		</div>
	</section>

	<!-- Experience -->
	<section class="space-y-2">
		<h2 class="text-sm text-mauve font-bold">experience</h2>
		<div class="border border-border divide-y divide-border">
			{#each resume.experience as exp}
				<article class="p-4 space-y-2">
					<div
						class="flex flex-col sm:flex-row sm:items-baseline sm:justify-between gap-1"
					>
						<div class="text-sm">
							<span class="text-foreground">{exp.position}</span>
							<span class="text-muted-foreground"> @ </span>
							<span class="text-mauve">{exp.company}</span>
						</div>
						<span class="text-xs text-mauve">
							{formatDate(exp.startDate)} - {exp.current
								? "present"
								: exp.endDate
									? formatDate(exp.endDate)
									: ""}
						</span>
					</div>
					<p class="text-xs text-lavender">{exp.location}</p>
					<ul class="space-y-1 text-xs text-muted-foreground">
						{#each exp.highlights as highlight}
							<li class="flex items-start gap-2">
								<span class="text-mauve font-bold">-</span>
								<span>{highlight}</span>
							</li>
						{/each}
					</ul>
					<div class="flex flex-wrap gap-1 pt-1 text-xs">
						{#each exp.technologies as tech}
							<div class="flex items-center gap-1">
								<span class="text-lavender">[{tech}]</span>
							</div>
						{/each}
					</div>
				</article>
			{/each}
		</div>
	</section>

	<!-- Education -->
	<section class="space-y-2">
		<h2 class="text-sm text-mauve font-bold">education</h2>
		<div class="border border-border divide-y divide-border">
			{#each resume.education as edu}
				<article class="p-4 space-y-1">
					<div
						class="flex flex-col sm:flex-row sm:items-baseline sm:justify-between gap-1"
					>
						<div class="text-sm">
							<span class="text-foreground">{edu.degree}</span>
							<span class="text-mauve"> in </span>
							<span class="text-foreground">{edu.field}</span>
						</div>
						<span class="text-xs text-mauve">
							{formatDate(edu.startDate)} - {edu.current
								? "present"
								: edu.endDate
									? formatDate(edu.endDate)
									: "present"}
						</span>
					</div>
					<p class="text-xs text-lavender">{edu.institution}</p>
					{#if edu.location}
						<p class="text-xs text-muted-foreground">
							{edu.location}
						</p>
					{/if}
				</article>
			{/each}
		</div>
	</section>

	<!-- Certifications -->
	{#if resume.certifications && resume.certifications.length > 0}
		<section class="space-y-2">
			<h2 class="text-sm text-accent">// certifications</h2>
			<div class="border border-border divide-y divide-border">
				{#each resume.certifications as cert}
					<article
						class="p-4 flex flex-col sm:flex-row sm:items-baseline sm:justify-between gap-1"
					>
						<div class="text-sm">
							{#if cert.url}
								<a
									href={cert.url}
									class="text-blue hover:text-lavender transition-colors"
									>{cert.name}</a
								>
							{:else}
								<span class="text-foreground">{cert.name}</span>
							{/if}
							<span class="text-muted-foreground">
								· {cert.issuer}</span
							>
						</div>
						<span class="text-xs text-mauve"
							>{formatDate(cert.date)}</span
						>
					</article>
				{/each}
			</div>
		</section>
	{/if}
</div>
