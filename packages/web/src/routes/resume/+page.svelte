<script lang="ts">
import { Download } from "@lucide/svelte"
import { Icon } from "$lib/components/common"
import { ResumeSection } from "$lib/components/resume"
import { Button } from "$lib/components/ui/button"
import { resumeData } from "$lib/content/resume"
</script>

<svelte:head>
	<title>Resume | wrath.codes</title>
	<meta name="description" content="Professional resume and experience of wrath.codes" />
</svelte:head>

<div class="container mx-auto max-w-4xl px-4 py-8 sm:py-12">
	<div class="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
		<h1 class="text-2xl font-bold text-foreground">Resume</h1>
		<Button variant="outline" href="/resume.pdf" download="resume.pdf" class="gap-2">
			<Icon icon={Download} size="sm" />
			Download PDF
		</Button>
	</div>

	<ResumeSection resume={resumeData} />
</div>
