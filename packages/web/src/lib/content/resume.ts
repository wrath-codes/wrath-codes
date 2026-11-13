import { Schema } from "effect"

export const ContactInfo = Schema.Struct({
	email: Schema.String,
	phone: Schema.optional(Schema.String),
	location: Schema.String,
	website: Schema.optional(Schema.String),
	linkedin: Schema.optional(Schema.String),
	github: Schema.optional(Schema.String),
})

export type ContactInfo = typeof ContactInfo.Type

export const Skill = Schema.Struct({
	name: Schema.String,
	category: Schema.Union(
		Schema.Literal("language"),
		Schema.Literal("framework"),
		Schema.Literal("tool"),
		Schema.Literal("platform"),
		Schema.Literal("database"),
		Schema.Literal("other"),
	),
})

export type Skill = typeof Skill.Type

export const Experience = Schema.Struct({
	id: Schema.String,
	company: Schema.String,
	position: Schema.String,
	location: Schema.String,
	startDate: Schema.String,
	endDate: Schema.optional(Schema.String),
	current: Schema.optional(Schema.Boolean),
	description: Schema.String,
	highlights: Schema.Array(Schema.String),
	technologies: Schema.Array(Schema.String),
})

export type Experience = typeof Experience.Type

export const Education = Schema.Struct({
	id: Schema.String,
	institution: Schema.String,
	degree: Schema.String,
	field: Schema.String,
	location: Schema.optional(Schema.String),
	startDate: Schema.String,
	endDate: Schema.optional(Schema.String),
	current: Schema.optional(Schema.Boolean),
	gpa: Schema.optional(Schema.String),
	honors: Schema.optional(Schema.Array(Schema.String)),
})

export type Education = typeof Education.Type

export const Certification = Schema.Struct({
	id: Schema.String,
	name: Schema.String,
	issuer: Schema.String,
	date: Schema.String,
	url: Schema.optional(Schema.String),
})

export type Certification = typeof Certification.Type

export const Resume = Schema.Struct({
	name: Schema.String,
	title: Schema.String,
	summary: Schema.String,
	contact: ContactInfo,
	skills: Schema.Array(Skill),
	experience: Schema.Array(Experience),
	education: Schema.Array(Education),
	certifications: Schema.optional(Schema.Array(Certification)),
})

export type Resume = typeof Resume.Type

export const resumeData: Resume = {
	name: "Raphael Vaz Nogueira",
	title: "Data Engineer / Python Developer",
	summary:
		"Python developer focused on data systems and high-performance pipelines. Experience in backend APIs, asynchronous programming, data validation, and I/O optimization using FastAPI, Polars, Prefect, and Dagster. Developer of I/O plugins for Polars published on PyPI, integrating Python and Rust for efficient production data ingestion.",
	contact: {
		email: "raphael@wrath.codes",
		phone: "+55 (21) 99710-5477",
		location: "Rio de Janeiro, Brazil",
		website: "https://wrath.codes",
		linkedin: "https://linkedin.com/in/wrath-codes",
		github: "https://github.com/wrath-codes",
	},
	skills: [
		{ name: "Python", category: "language" },
		{ name: "Rust", category: "language" },
		{ name: "TypeScript", category: "language" },
		{ name: "JavaScript", category: "language" },
		{ name: "SQL", category: "language" },
		{ name: "FastAPI", category: "framework" },
		{ name: "Polars", category: "framework" },
		{ name: "Prefect", category: "framework" },
		{ name: "Dagster", category: "framework" },
		{ name: "LangChain", category: "framework" },
		{ name: "Pydantic", category: "framework" },
		{ name: "NodeJS", category: "platform" },
		{ name: "Express", category: "framework" },
		{ name: "Pandera", category: "framework" },
		{ name: "Typer", category: "framework" },
		{ name: "Textual", category: "framework" },
		{ name: "MySQL", category: "database" },
		{ name: "MongoDB", category: "database" },
		{ name: "Apache Doris", category: "database" },
		{ name: "Prisma ORM", category: "tool" },
		{ name: "Docker", category: "tool" },
		{ name: "Git", category: "tool" },
		{ name: "uv", category: "tool" },
		{ name: "ruff", category: "tool" },
		{ name: "mypy", category: "tool" },
		{ name: "pytest", category: "tool" },
		{ name: "mkdocs", category: "tool" },
		{ name: "FlightSQL", category: "tool" },
		{ name: "Arrow", category: "tool" },
	],
	experience: [
		{
			id: "exp-eco",
			company: "Eco Sistemas",
			position: "Data Engineer",
			location: "Rio de Janeiro, RJ, Brazil",
			startDate: "2024-03",
			current: true,
			description:
				"Building Python backend services and high-performance data pipelines for data ingestion and processing.",
			highlights: [
				"Developed Python backend services/APIs using FastAPI for data ingestion and processing",
				"Architected scalable pipelines with asyncio and aiofiles, reducing execution time from 8–12 hours to 50 minutes–2 hours",
				"Implemented data validation/governance with Polars and Pandera",
				"Designed high-performance data access layers using Polars DataFrames, arrow-odbc, FlightSQL, Apache Doris, and fireducks",
				"Developed observable workflows with Prefect and Dagster",
				"Authored and published klaw-dbase (Polars I/O plugin) on PyPI using Rust and pyo3",
				"Reduced test execution time by ~50% using pytest, pytest-xdist, and pytest-asyncio",
				"Integrated AI components via LangChain for workflow automation (Slack/WhatsApp)",
			],
			technologies: [
				"Python",
				"FastAPI",
				"Polars",
				"Rust",
				"Prefect",
				"Dagster",
				"Apache Doris",
				"LangChain",
			],
		},
		{
			id: "exp-clark",
			company: "Clark Seguros",
			position: "Full Stack Developer",
			location: "Niterói, RJ, Brazil",
			startDate: "2021-03",
			endDate: "2024-03",
			description: "Developed data-oriented backend APIs for insurance platforms.",
			highlights: [
				"Developed data-oriented backend APIs for insurance platforms",
				"Optimized data models using MySQL and Prisma ORM",
				"Implemented backend services with NodeJS, Express, and MongoDB",
				"Handled frontend-backend integration for API consumption",
			],
			technologies: ["NodeJS", "Express", "MongoDB", "MySQL", "Prisma ORM"],
		},
		{
			id: "exp-ruthless",
			company: "Ruthless Game Studio",
			position: "3D Props Artist",
			location: "Remote",
			startDate: "2020-03",
			endDate: "2020-11",
			description: "Created 3D prop assets for game development.",
			highlights: ["Created 3D prop assets for game development projects"],
			technologies: ["3D Modeling", "Game Development"],
		},
		{
			id: "exp-microsoft",
			company: "Microsoft",
			position: "Test Analyst 2",
			location: "Redmond, WA, USA",
			startDate: "2017-04",
			endDate: "2017-11",
			description: "Quality assurance and testing for Microsoft products.",
			highlights: ["Quality assurance and testing for Microsoft products"],
			technologies: ["QA", "Testing"],
		},
	],
	education: [
		{
			id: "edu-xp",
			institution: "XP Educação",
			degree: "Postgraduate",
			field: "Data Architecture and Engineering with AI Focus",
			startDate: "2025-01",
			current: true,
		},
		{
			id: "edu-puc-pos",
			institution: "PUC-Rio",
			degree: "Postgraduate",
			field: "Full Stack Development",
			startDate: "2023-01",
			endDate: "2023-12",
		},
		{
			id: "edu-fullsail",
			institution: "Full Sail University",
			degree: "Bachelor's Degree",
			field: "Game Art",
			location: "Winter Park, FL, USA",
			startDate: "2012-01",
			endDate: "2015-12",
		},
		{
			id: "edu-puc",
			institution: "PUC-Rio",
			degree: "Bachelor's Degree (Incomplete)",
			field: "Computer Science",
			location: "Rio de Janeiro, Brazil",
			startDate: "2010-01",
			endDate: "2012-12",
		},
	],
}
