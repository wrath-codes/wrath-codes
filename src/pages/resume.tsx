import Head from "next/head";
import {
  SiExpress,
  SiGit,
  SiHtml5,
  SiJavascript,
  SiMongodb,
  SiNextdotjs,
  SiNodedotjs,
  SiPostgresql,
  SiPrisma,
  SiReact,
  SiTailwindcss,
  SiTypescript,
} from "react-icons/si";

import Header from "../components/Header";

import type { NextPage } from "next";

const icons = [
  {
    title: "HTML",
    icon: <SiHtml5 />,
  },
  {
    title: "CSS",
    icon: <SiHtml5 />,
  },
  {
    title: "JavaScript",
    icon: <SiJavascript />,
  },
  {
    title: "TailwindCSS",
    icon: <SiTailwindcss />,
  },
  {
    title: "React",
    icon: <SiReact />,
  },
  {
    title: "NextJS",
    icon: <SiNextdotjs />,
  },
  {
    title: "TypeScript",
    icon: <SiTypescript />,
  },
  {
    title: "NodeJS",
    icon: <SiNodedotjs />,
  },
  {
    title: "MongoDB",
    icon: <SiMongodb />,
  },
  {
    title: "ExpressJS",
    icon: <SiExpress />,
  },
  {
    title: "PostgreSQL",
    icon: <SiPostgresql />,
  },
  {
    title: "Prisma",
    icon: <SiPrisma />,
  },
  {
    title: "Git",
    icon: <SiGit />,
  },
];

const devExperiences = [
  {
    title: "Full Stack Developer ",
    company: "Clark Seguros",
    location: "Niterói, RJ, Brazil",
    start: "June 2021",
    end: "Present",
    description: [
      "▪ Developed backend funccionality with NodeJS, ExpressJS and EJS.",
      "▪ Data modeling and database creation withMongoDB and Mongoose.",
      "▪ Front-end funcionality with React, Tailwindcss, HTML, CSS and Javascript.",
      "▪ Developed an excel importer in order mass import data into the database with multer.",
      "▪ Created an access area managing state with redux toolkit.",
      "▪ Later swiched to MySQL with Prisma as an ORM and started to use NextJs.",
    ],
  },
];

const threeDeeExperiences = [
  {
    title: "3D Prop Artist",
    company: "Ruthless Games Studio",
    location: "Remote",
    start: "March 2021",
    end: "June 2021",
    description: [
      "▪ Hard-surface modeling using Autodesk Maya.",
      "▪ Organic modeling using Zbrush.",
      "▪ Texture creation using Substance Painter and Substance Designer.",
      "▪ Tiling texture creation using Substance Designer and Photoshop.",
      "▪ Retopology using Maya and Topogun.",
      "▪ UV mapping using Maya and UVLayout.",
      "▪ Asset setup on Unreal Engine 4.",
    ],
  },
  {
    title: "Freelance 3D Artist",
    company: "Self-Employed",
    location: "Remote",
    start: "December 2017",
    end: "March 2021",
    description: [
      "▪ Hard-surface modeling using Autodesk Maya.",
      "▪ Organic modeling using Zbrush.",
      "▪ Texture creation using Substance Painter and Substance Designer.",
      "▪ Tiling texture creation using Substance Designer and Photoshop.",
      "▪ Retopology using Maya and Topogun.",
      "▪ UV mapping using Maya and UVLayout.",
      "▪ Asset setup on Unreal Engine 4.",
    ],
  },
  {
    title: "Test Analyst 2",
    company: "Microsoft",
    location: "Redmond, WA, USA",
    start: "April 2017",
    end: "December 2017",
    description: [
      "▪ Collaborated with software and hardware developers, engineers, testers, and other team members  on various tasks.",
      "▪ Responsible for daily/nightly data reports and spreadsheet generation.",
      "▪ Directed and ran BVT tests for XBox R&D OS and Platform",
      "▪ Conducted test cases; investigated and documented bugs in detail; tested dozens of titles(AAA, Arcade, and Indie) on XBox One and XBox One X.",
    ],
  },
  {
    title: "Hard Surface 3D Artist",
    company: "Razor Edge Games",
    location: "Remote",
    start: "August 2016",
    end: "April 2017",
    description: [
      "▪ Hard-surface modeling using Autodesk Maya.",
      "▪ Organic modeling using Zbrush.",
      "▪ Texture creation using Substance Painter and Substance Designer.",
      "▪ Tiling texture creation using Substance Designer and Photoshop.",
      "▪ Retopology using Maya and Topogun.",
      "▪ UV mapping using Maya and UVLayout.",
      "▪ Asset setup on Unreal Engine 4.",
    ],
  },
  {
    title: "Q&A Tester",
    company: "Pole to Win",
    location: "Lynnwood, WA, USA",
    start: "September 2016",
    end: "Octuber 2016",
    description: [
      "▪ Tested computer, console, and mobile games.",
      "▪ Found, documented, and reported bugs.",
      "▪ Corrected translation for foreign languages.",
    ],
  },
  {
    title: "Environmental/Prop Artist Intern",
    company: "Full Sail University",
    location: "Winter Park, FL, USA",
    start: "January 2016",
    end: "July 2016",
    description: [
      "▪ Hard-surface modeling using Autodesk Maya.",
      "▪ Organic modeling using Zbrush.",
      "▪ Texture creation using Substance Painter and Substance Designer.",
      "▪ Tiling texture creation using Substance Designer and Photoshop.",
      "▪ Retopology using Maya and Topogun.",
      "▪ UV mapping using Maya and UVLayout.",
      "▪ Asset setup on Unreal Engine 4.",
    ],
  },
];

const Resume: NextPage = (props) => {
  return (
    <>
      <Head>
        <title>wrathCodes - Resume</title>
        <meta name="description" content="Generated by create-t3-app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Header />
      <main className="flex min-h-screen flex-col items-center bg-gradient-to-b from-white to-gray-200">
        <div className="container mt-12 flex flex-col items-center justify-center gap-4 px-4">
          <h2 className="mb-4 text-5xl font-extrabold tracking-tight text-violet-500 sm:text-[3rem]">Resume</h2>
          <Divider title="Skills" />
          <div className="mb-16 grid grid-cols-2 gap-4 rounded-lg bg-violet-500/10  px-5 py-10 md:grid-cols-3 md:gap-8 lg:grid-cols-4 xl:grid-cols-5">
            {icons.map((icon) => (
              <Technololy key={icon.title} {...icon} />
            ))}
          </div>
          <Divider title="Experience" />
          <div className="text-left font-medium text-violet-500/75">
            <p className="mb-2 text-2xl font-bold">Web Development</p>
          </div>
          <div className="container mb-10 flex max-w-2xl flex-col items-center gap-4">
            {devExperiences.map((experience) => (
              <Experience key={experience.company} {...experience} />
            ))}
          </div>
          <div className="text-left font-medium text-violet-500/75">
            <p className="mb-2 text-2xl font-bold">3D Art</p>
          </div>
          <div className="container mb-5 flex max-w-2xl flex-col items-center gap-4">
            {threeDeeExperiences.map((experience) => (
              <Experience key={experience.company} {...experience} />
            ))}
          </div>
        </div>
      </main>
    </>
  );
};

export default Resume;

interface ITechnology {
  title: string;
  icon: JSX.Element;
}

const Technololy = ({ title, icon }: ITechnology) => {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="mb-1 flex items-center justify-center rounded-full text-5xl text-violet-800/75">{icon}</div>
      <div className="text-sm font-semibold text-gray-600">{title}</div>
    </div>
  );
};

interface IDivider {
  title: string;
}

const Divider = ({ title }: IDivider) => {
  return (
    <div className="flex flex-row items-center justify-center gap-4">
      <span className="w-full bg-violet-500 px-5 py-0.5 md:px-16 lg:px-24 xl:px-32 "></span>
      <div className="justify-center text-center text-2xl font-semibold text-violet-800/75">{title}</div>
      <span className="w-full bg-violet-500 px-5 py-0.5 md:px-16 lg:px-24 xl:px-32 "></span>
    </div>
  );
};

interface IExperience {
  title: string;
  company: string;
  location: string;
  start: string;
  end: string;
  description: string[];
}

const Experience = ({ title, company, location, start, end, description }: IExperience) => {
  return (
    <div className="flex min-w-full flex-col items-start gap-4 rounded-md bg-violet-500/20 px-5 py-2">
      <div className="flex flex-col gap-2">
        <div className="text-2xl font-semibold text-violet-500">{title}</div>
        <div className="flex w-full flex-row justify-between gap-5 text-violet-800/50">
          <div className="text-sm font-semibold ">{company}</div>
          <div className="text-sm font-medium ">{location}</div>
          <div className="flex flex-row items-center justify-center gap-4">
            <div className="text-sm font-semibold ">{start}</div>
            <div className="text-sm font-semibold ">-</div>
            <div className="text-sm font-semibold ">{end}</div>
          </div>
        </div>
      </div>
      <div className="text-sm font-medium text-gray-600">
        {description.map((desc) => (
          <div key={desc} className="flex flex-col items-start gap-2">
            {desc}
          </div>
        ))}
      </div>
    </div>
  );
};
