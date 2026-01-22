import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Economics Past Papers",
    description: "A-Level Economics Past Paper Viewer",
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
