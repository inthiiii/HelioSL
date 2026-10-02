import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: {
    root: __dirname,
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "www.solanra.com",
      },
      {
        protocol: "https",
        hostname: "macksonssolar.com",
      },
      {
        protocol: "https",
        hostname: "www.dimolanka.com",
      },
    ],
  },
};

export default nextConfig;
