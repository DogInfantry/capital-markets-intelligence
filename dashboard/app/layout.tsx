import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Capital Markets Intelligence | DogInfantry",
  description: "Production-grade capital markets intelligence platform — IPO event studies, sovereign risk scoring, M&A screening, and yield curve decomposition.",
  keywords: "capital markets, IPO, M&A, sovereign risk, yield curve, quantitative finance",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body>{children}</body>
    </html>
  );
}
