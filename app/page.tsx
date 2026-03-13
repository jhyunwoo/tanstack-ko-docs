import type { Metadata } from "next";

import { JsonLd } from "@/components/json-ld";
import { HomePage } from "@/components/home-page";
import { siteConfig, toAbsoluteUrl } from "@/lib/site";

export const metadata: Metadata = {
  alternates: {
    canonical: "/",
    languages: {
      "ko-KR": "/",
    },
  },
  openGraph: {
    url: "/",
  },
};

export default function Page() {
  const websiteJsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: siteConfig.name,
    url: toAbsoluteUrl("/"),
    inLanguage: siteConfig.language,
    description: siteConfig.description,
  };

  const collectionJsonLd = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: siteConfig.title,
    url: toAbsoluteUrl("/"),
    inLanguage: siteConfig.language,
    description: siteConfig.description,
    isPartOf: {
      "@type": "WebSite",
      name: siteConfig.name,
      url: toAbsoluteUrl("/"),
    },
  };

  return (
    <>
      <JsonLd data={websiteJsonLd} />
      <JsonLd data={collectionJsonLd} />
      <HomePage />
    </>
  );
}
