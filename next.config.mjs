/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        domains: [], // Add your Supabase storage domain here
        remotePatterns: [
            {
                protocol: 'https',
                hostname: '**.supabase.co',
            },
        ],
    },
};

export default nextConfig;
