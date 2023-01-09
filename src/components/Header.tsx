import { Disclosure, Menu, Transition } from "@headlessui/react";
import { Bars3Icon, BellIcon, MagnifyingGlassIcon, XMarkIcon } from "@heroicons/react/20/solid";
import { signIn, signOut, useSession } from "next-auth/react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/router";
import { Fragment } from "react";

import frontLogo from "../../public/wrathCodes_front_logo.svg";
import sideLogo from "../../public/wrathCodes_side_logo.svg";
import { trpc } from "../utils/trpc";

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const navigation = [
  { name: "Home", href: "/", current: true },
  { name: "Contact", href: "/contact", current: false },
  { name: "Blog", href: "/blog", current: false },
  { name: "Projects", href: "/projects", current: false },
  { name: "Resume", href: "/resume", current: false },
  { name: "Story", href: "/story", current: false },
];

export default function Header() {
  const { data: sessionData } = useSession();
  const router = useRouter();
  const isActive = router.asPath;

  return (
    <Disclosure as="nav" className="bg-white shadow">
      {({ open }) => (
        <>
          <div className="mx-auto max-w-7xl px-2 sm:px-4 lg:divide-y lg:divide-gray-700 lg:px-8">
            <div className="relative flex h-16 justify-between">
              <div className="relative z-10 flex px-2 lg:px-0">
                <div className="flex flex-shrink-0 items-center">
                  <Link href="/">
                    <Image src={frontLogo} alt="wrath codes logo" width={32} />
                  </Link>
                </div>
              </div>
              <div className="relative z-0 flex flex-1 items-center justify-center px-2 sm:absolute sm:inset-0 sm:ml-10 sm:px-0">
                <div className="w-full sm:max-w-xs">
                  <label htmlFor="search" className="sr-only">
                    Search
                  </label>
                  <div className="relative">
                    <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                      <MagnifyingGlassIcon
                        className="mr-2 h-5 w-5 text-violet-400"
                        aria-hidden="true"
                      />
                    </div>
                    <input
                      placeholder="Search"
                      type="search"
                      name="search"
                      id="search"
                      className="block w-full cursor-pointer rounded-md border border-transparent bg-gray-50 py-2 pl-10 pr-3 text-sm placeholder-gray-400 focus:border-violet-500 focus:bg-violet-100 focus:text-gray-900 focus:placeholder-gray-500 focus:outline-none focus:ring-violet-500 sm:text-sm"
                    />
                  </div>
                </div>
              </div>
              <div className="relative z-10 flex items-center lg:hidden">
                {/* Mobile menu button */}
                <Disclosure.Button className="inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-violet-500">
                  <span className="sr-only">Open main menu</span>
                  {open ? (
                    <XMarkIcon
                      className="block h-6 w-6 text-violet-500"
                      aria-hidden="true"
                    />
                  ) : (
                    <Bars3Icon
                      className="block h-6 w-6 text-violet-500"
                      aria-hidden="true"
                    />
                  )}
                </Disclosure.Button>
              </div>
              <div className="hidden lg:relative lg:z-10 lg:ml-4 lg:flex lg:items-center">
                {/* Profile dropdown */}
                <Login />
              </div>
            </div>
            <nav className="hidden lg:flex lg:space-x-32 lp:py-2 justify-center" aria-label="Global">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={classNames(
                    isActive === item.href
                      ? 'bg-violet-100 text-violet-500 border-violet-900 mt-2'
                      : 'mt-2 text-gray-400 hover:bg-violet-50 hover:text-violet-400',
                    'block rounded-md py-1 px-3 text-base font-medium'
                  )}
                  aria-current={item.current ? "page" : undefined}
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>
          <Disclosure.Panel as="nav" className="lg:hidden" aria-label="Global">
            <div className="space-y-1 px-2 pt-2 pb-3">
              {navigation.map((item) => (
                <Disclosure.Button
                  key={item.name}
                  as="a"
                  href={item.href}
                  className={classNames(
                    isActive === item.href
                      ? 'bg-violet-100 text-violet-500 border-violet-900 mt-2'
                      : 'mt-2 text-gray-400 hover:bg-gray-200 hover:text-violet-300',
                    'block rounded-md py-2 px-3 text-base font-medium'
                  )}

                  aria-current={item.current ? 'page' : undefined}
                >
                  {item.name}
                </Disclosure.Button>
              ))}
            </div>
            <LoginMobile />
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
}


const Login = () => {
  const { data: sessionData } = useSession();

  const { data: secretMessage } = trpc.auth.getSecretMessage.useQuery(
    undefined, // no input
    { enabled: sessionData?.user !== undefined }
  );

  return (
    <>

      {sessionData ? (
        <>
          <button className="flex-shrink-0 rounded-full bg-transparent p-1 text-violet-500 hover:text-violet-900 focus:outline-none focus:ring-violet-500 focus:ring-offset-violet-900">
            <span className="sr-only">View Notifications</span>
            <BellIcon className="h-6 w-6" aria-hidden="true" />
          </button>
          <Menu as="div" className="relative ml-4 flex-shrink-0">
            <div className="hidden lg:relative lg:z-10 lg:ml-4 lg:flex lg:items-center">
              {/* View Notifications Button */}
              <Menu.Button className="flex rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800">
                <span className="sr-only">Open user menu</span>
                <Image
                  className="h-8 w-8 rounded-full"
                  src={sessionData?.user?.image || sideLogo}
                  width={32}
                  height={32}
                  alt=""
                />
              </Menu.Button>
            </div>
            <Transition
              as={Fragment}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 w-48 mt-2 origin-top-right bg-white divide-y divide-gray-100 rounded-md shadow-lg ring-1 ring-violet-500 ring-opacity-5 focus:outline-none text-center">
                <div className="px-1 py-1 ">
                  <Menu.Item>
                    <p className="text-center text-2xl text-violet-500">
                      {sessionData && <span>{sessionData.user?.name}</span>}
                      {secretMessage && <span> - {secretMessage}</span>}
                    </p>

                  </Menu.Item>
                  <Menu.Item>
                    <button
                      className="rounded-full bg-violet-500 px-10 py-3 font-semibold text-white no-underline transition hover:bg-violet-900"
                      onClick={() => signOut()}
                    >
                      {"Sign out"}
                    </button>
                  </Menu.Item>
                </div>
              </Menu.Items>
            </Transition>
          </Menu>
        </>
      ) : (
        <div className="cursor-pointer rounded-md bg-violet-500 px-2 py-1 font-semibold text-white no-underline transition hover:bg-violet-900 ml-4"
          onClick={() => signIn()}
        >
          Sign In
        </div>
      )}
    </>

  );
};

const LoginMobile = () => {
  const { data: sessionData } = useSession();

  return (
    <>
      {sessionData ? (
        <div className="flex items-center flex-col w-full px-2 pt-2 pb-3 space-y-1">
          <div className="border-t border-gray-700 pt-4 pb-3 w-full">
            <div className="flex items-center px-4">
              <div className="flex-shrink-0">
                <img className="h-10 w-10 rounded-full" src={useSession()?.data?.user?.image || "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y"} alt="" />
              </div>
              <div className="ml-3 flex text-center">
                <div className="text-base font-medium text-center text-violet-500">{useSession().data?.user?.name}</div>
              </div>
              <button
                type="button"
                className="ml-auto flex-shrink-0 rounded-full bg-transparent p-1 text-violet-500 hover:text-violet-800 focus:outline-none focus:ring-2 focus:ring-violet focus:ring-offset-2 focus:ring-offset-gray-800"
              >
                <span className="sr-only">View notifications</span>
                <BellIcon className="h-6 w-6" aria-hidden="true" />
              </button>
            </div>
            <div className="text-sm text-center font-medium text-gray-400">{useSession()?.data?.user?.email}</div>
          </div>
          <div className="mt-3 px-2 space-y-1">
            <button
              className="rounded-md bg-violet-500 px-10 py-3 font-semibold text-white no-underline transition hover:bg-violet-900"
              onClick={() => signOut()}
            >
              {"Sign out"}
            </button>
          </div>
        </div>
      )
        : (
          <div className="rounded-md bg-violet-500 px-10 py-3 font-semibold text-white no-underline transition hover:bg-violet-900 text-center cursor-pointer max-w-xs mx-auto"
            onClick={() => signIn()}
          >
            Sign In
          </div>
        )
      }
    </>
  );
};