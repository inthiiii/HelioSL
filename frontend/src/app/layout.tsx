import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HelioSL · Energy Intelligence",
  description: "Renewable energy intelligence for Sri Lanka",
  icons: {
    icon: "/heliosl-mark.svg",
    shortcut: "/heliosl-mark.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
