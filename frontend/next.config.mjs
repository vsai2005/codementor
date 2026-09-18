/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  typescript: { ignoreBuildErrors: false },
  eslint: { ignoreDuringBuilds: true },
  async rewrites() {
    const rawUrl =
      process.env.BACKEND_URL ||
      process.env.NEXT_PUBLIC_API_URL ||
      process.env.NEXT_PUBLIC_API_BASE_URL ||
      (process.env.NODE_ENV === "production" ? "" : "http://localhost:8000");

    const destinationUrl = rawUrl.replace(/\/+$/, "").replace(/\/api$/, "");
    if (!destinationUrl) return [];

    return [
      {
        source: "/health",
        destination: `${destinationUrl}/health`,
      },
      {
        source: "/api/:path*",
        destination: `${destinationUrl}/api/:path*`,
      },
    ];
  },
};
export default nextConfig;
