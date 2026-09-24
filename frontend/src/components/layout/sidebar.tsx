"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { removeToken } from "@/lib/auth";


const navigation = [
  {
    name: "Overview",
    href: "/dashboard",
  },
  {
    name: "Energy",
    href: "/energy",
  },
  {
    name: "Solar",
    href: "/solar",
  },
  {
    name: "AI Assistant",
    href: "/assistant",
  },
];


export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  function logout() {
    removeToken();
    router.push("/login");
  }

  return (
    <aside className="flex h-screen w-64 flex-col border-r border-neutral-800 bg-neutral-950 p-6">
      <div>
        <p className="text-sm text-emerald-400">
          HelioSL
        </p>

        <h2 className="mt-1 text-xl font-semibold text-white">
          Energy Intelligence
        </h2>
      </div>

      <nav className="mt-10 space-y-2">
        {navigation.map((item) => {
          const active = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block rounded-lg px-4 py-3 text-sm transition ${
                active
                  ? "bg-neutral-800 text-white"
                  : "text-neutral-400 hover:bg-neutral-900 hover:text-white"
              }`}
            >
              {item.name}
            </Link>
          );
        })}
      </nav>

      <button
        onClick={logout}
        className="mt-auto rounded-lg border border-neutral-700 px-4 py-3 text-sm text-neutral-300"
      >
        Log out
      </button>
    </aside>
  );
}