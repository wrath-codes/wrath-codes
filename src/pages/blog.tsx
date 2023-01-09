import Head from "next/head";
import Link from "next/link";

import Header from "../components/Header";
import { trpc } from "../utils/trpc";

import type { NextPage } from "next";


const Blog: NextPage = (props) => {
  const articles: IArticle[] = trpc.devto.getWrathArticles.useQuery().data;
  return (
    <>
      <Head>
        <title>wrathCodes - Blog</title>
        <meta name="description" content="Generated by create-t3-app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Header />
      <main className="flex min-h-screen flex-col items-center bg-gradient-to-b from-white to-gray-200">
        <div className="container flex flex-col items-center justify-center gap-12 px-4 mt-12">
          <h2 className="text-5xl font-extrabold tracking-tight text-violet-500 sm:text-[3rem]">
            Blog
          </h2>
          <div className="flex flex-row justify-between items-center w-full max-w-3xl">
            <div className="text-md text-violet-500 bg-violet-100 rounded-md px-2 py-1">
              Articles
            </div>
            <div className="text-md text-violet-500 bg-violet-100 rounded-md px-2 py-1">
              {articles?.length}
            </div>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-1 md:gap-8">
            {articles?.map((article: IArticle) => (
              <Article key={article.id} {...article} />
            ))}
          </div>

        </div>
      </main>
    </>
  );
};

export default Blog;


interface IArticle {
  id: number;
  title: string;
  url: string;
  description: string;
  tag_list: string[];
  readable_publish_date: string;
}

const Article = ({ title, url, description, tag_list, readable_publish_date }: IArticle) => {
  return (
    <Link
      className="flex max-w-3xl flex-col gap-4 rounded-xl bg-transparent p-4  hover:bg-violet-500/20 border-2 hover:border-violet-500 group transition-all duration-200 ease-in-out"
      href={url}
      target="_blank"
    >
      <h3 className="text-2xl text-violet-300 font-bold group-hover:text-violet-900 transition-all duration-200 ease-in-out">
        {title}
      </h3>
      <div className="text-lg text-gray-500 group-hover:text-gray-900 transition-all duration-200 ease-in-out">
        {description}
      </div>

      <div className="flex flex-row justify-between">
        <div className="flex flex-wrap gap-2">
          {/*Tags for the Article*/}
          {tag_list.map((tag) => (
            <span className="text-sm text-violet-300 bg-violet-50 rounded-md px-2 py-1 border-2 border-violet-200 group-hover:text-violet-500 group-hover:border-violet-400 transition-all duration-200 ease-in-out">
              {tag}
            </span>
          ))}
        </div>
        {/*Published Date*/}
        <div className="text-sm text-violet-300 group-hover:text-violet-500 transition-all duration-200 ease-in-out">
          {readable_publish_date}
        </div>
      </div>
    </Link>
  )
};

