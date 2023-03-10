import Head from "next/head";
import Link from "next/link";

import Header from "../../components/Header";

import type { NextPage } from "next";

const projects: IProject[] = [
  {
    title: "Todo App",
    url: "/projects/todo-app",
    description: "A todo app built with Next.js, Tailwind CSS, TypeScript and TRPC",
    technologies: ["Next.js", "Tailwind CSS", "TypeScript", "TRPC"],
  },
];

const Projects: NextPage = (props) => {
  return (
    <>
      <Head>
        <title>wrathCodes - Projects</title>
        <meta name="description" content="Generated by create-t3-app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Header />
      <main className="flex min-h-screen flex-col items-center bg-gradient-to-b from-white to-gray-200">
        <div className="container mt-12 flex flex-col items-center justify-center gap-12 px-4">
          <h2 className="text-5xl font-extrabold tracking-tight text-violet-500 sm:text-[3rem]">Projects</h2>
          <div className="flex w-full max-w-3xl flex-row items-center justify-between">
            <div className="text-md rounded-md bg-violet-100 px-2 py-1 text-violet-500">Projects</div>
            <div className="text-md rounded-md bg-violet-100 px-2 py-1 text-violet-500">{projects?.length}</div>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-1 md:gap-8">
            {projects?.map((project: IProject) => (
              <Project key={project.title} {...project} />
            ))}
          </div>
        </div>
      </main>
    </>
  );
};

export default Projects;

interface IProject {
  title: string;
  url: string;
  description: string;
  technologies: string[];
}

const Project = ({ title, url, description, technologies }: IProject) => {
  return (
    <Link
      className="group flex max-w-3xl flex-col gap-4 rounded-xl border-2  bg-transparent p-4 transition-all duration-200 ease-in-out hover:border-violet-500 hover:bg-violet-500/20"
      href={url}
    >
      <h3 className="text-2xl font-bold text-violet-300 transition-all duration-200 ease-in-out group-hover:text-violet-900">
        {title}
      </h3>
      <div className="text-lg text-gray-500 transition-all duration-200 ease-in-out group-hover:text-gray-900">
        {description}
      </div>

      <div className="flex flex-row items-center gap-2">
        {technologies?.map((technology: string) => (
          // eslint-disable-next-line react/jsx-key
          <div className="rounded-sm bg-violet-500/30 px-2 text-sm text-violet-700 transition-all duration-200 ease-in-out group-hover:bg-violet-800/20 group-hover:text-gray-900">
            {technology}
          </div>
        ))}
      </div>
    </Link>
  );
};
