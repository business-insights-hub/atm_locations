import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BOB ATM Strategy Dashboard",
  description: "Next.js + TypeScript dashboard for ATM network analysis and expansion planning"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
