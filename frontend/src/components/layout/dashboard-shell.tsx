import { ReactNode } from "react";

import { Sidebar } from "./sidebar";


export function DashboardShell({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="flex min-h-screen flex-col bg-neutral-950 lg:flex-row">
      <Sidebar />

      <main className="min-w-0 flex-1 p-4 sm:p-6 lg:p-10">
        {children}
      </main>
    </div>
  );
}
