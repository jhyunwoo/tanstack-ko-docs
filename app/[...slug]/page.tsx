import { ArrowLeft, ArrowRight } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { HomePage } from "@/components/home-page";
import { JsonLd } from "@/components/json-ld";
import { Sidebar } from "@/components/sidebar";
import { SiteHeader } from "@/components/site-header";
import { TableOfContents } from "@/components/table-of-contents";
import { renderDocContent } from "@/lib/markdown";
import { getDocBySlug, getSidebarSections, getStaticParams, humanizeSegment } from "@/lib/docs";
import { siteConfig, toAbsoluteUrl, withTrailingSlash } from "@/lib/site";

export const dynamicParams = false;

type PageProps = {
  params: Promise<{
    slug?: string[];
  }>;
};

export async function generateStaticParams() {
  return getStaticParams();
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug = [] } = await params;

  if (slug.length === 0) {
    return {};
  }

  const doc = getDocBySlug(slug);
  if (!doc) {
    return {
      title: "문서를 찾을 수 없습니다",
      robots: {
        index: false,
        follow: false,
      },
    };
  }

  const canonicalPath = withTrailingSlash(doc.route);
  const canonicalUrl = toAbsoluteUrl(doc.route);

  return {
    title: doc.title,
    description: doc.description,
    keywords: [doc.title, doc.titleEn, doc.section, doc.framework ? humanizeSegment(doc.framework) : ""].filter(
      Boolean,
    ),
    alternates: {
      canonical: canonicalPath,
      languages: {
        "ko-KR": canonicalPath,
      },
    },
    openGraph: {
      type: "article",
      url: canonicalUrl,
      title: `${doc.title} | ${siteConfig.title}`,
      description: doc.description,
      locale: siteConfig.locale,
      siteName: siteConfig.name,
      images: [
        {
          url: toAbsoluteUrl(siteConfig.defaultOgImage),
          width: 1200,
          height: 630,
          alt: `${doc.title} | ${siteConfig.title}`,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: `${doc.title} | ${siteConfig.title}`,
      description: doc.description,
      images: [toAbsoluteUrl(siteConfig.defaultOgImage)],
    },
    robots: doc.sourceOnly
      ? {
          index: false,
          follow: true,
          googleBot: {
            index: false,
            follow: true,
            "max-image-preview": "large",
            "max-snippet": -1,
            "max-video-preview": -1,
          },
        }
      : {
          index: true,
          follow: true,
          googleBot: {
            index: true,
            follow: true,
            "max-image-preview": "large",
            "max-snippet": -1,
            "max-video-preview": -1,
          },
        },
  };
}

export default async function CatchAllPage({ params }: PageProps) {
  const { slug = [] } = await params;

  if (slug.length === 0) {
    return <HomePage />;
  }

  const doc = getDocBySlug(slug);
  if (!doc) {
    notFound();
  }

  const sidebar = <Sidebar sections={getSidebarSections(doc.route)} currentRoute={doc.route} />;
  const content = await renderDocContent(doc);
  const breadcrumbItems = [
    {
      "@type": "ListItem",
      position: 1,
      name: "홈",
      item: toAbsoluteUrl("/"),
    },
    ...(doc.framework
      ? [
          {
            "@type": "ListItem",
            position: 2,
            name: humanizeSegment(doc.framework),
            item: toAbsoluteUrl(`/framework/${doc.framework}/overview`),
          },
        ]
      : []),
    {
      "@type": "ListItem",
      position: doc.framework ? 3 : 2,
      name: doc.title,
      item: toAbsoluteUrl(doc.route),
    },
  ];
  const breadcrumbJsonLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: breadcrumbItems,
  };
  const articleJsonLd = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    headline: doc.title,
    description: doc.description,
    inLanguage: siteConfig.language,
    url: toAbsoluteUrl(doc.route),
    isAccessibleForFree: true,
    articleSection: doc.section,
    about: doc.framework ? [humanizeSegment(doc.framework), "TanStack Query"] : ["TanStack Query"],
    isPartOf: {
      "@type": "WebSite",
      name: siteConfig.name,
      url: toAbsoluteUrl("/"),
    },
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": toAbsoluteUrl(doc.route),
    },
  };

  return (
    <div className="min-h-screen">
      <JsonLd data={breadcrumbJsonLd} />
      {!doc.sourceOnly ? <JsonLd data={articleJsonLd} /> : null}
      <SiteHeader sidebar={sidebar} />
      <div className="mx-auto grid max-w-[1600px] gap-8 px-4 pb-16 pt-6 lg:grid-cols-[280px_minmax(0,1fr)] xl:grid-cols-[280px_minmax(0,1fr)_250px] lg:px-6">
        <aside className="hidden lg:block">
          <div className="sticky top-24 max-h-[calc(100vh-7rem)] overflow-y-auto pr-2">{sidebar}</div>
        </aside>

        <main className="min-w-0">
          <div className="doc-card p-6 md:p-10">
            <div className="mb-6 flex flex-wrap items-center gap-3 text-sm text-muted">
              {doc.breadcrumbs.map((breadcrumb, index) => (
                <div key={`${breadcrumb.label}-${index}`} className="flex items-center gap-3">
                  {breadcrumb.href ? (
                    <Link href={breadcrumb.href} prefetch={false} className="transition hover:text-text">
                      {breadcrumb.label}
                    </Link>
                  ) : (
                    <span>{breadcrumb.label}</span>
                  )}
                  {index < doc.breadcrumbs.length - 1 ? <span className="text-border">/</span> : null}
                </div>
              ))}
            </div>

            <div className="mb-10 flex flex-wrap items-center gap-3">
              {doc.sourceOnly ? (
                <span className="rounded-full border border-border/70 bg-surfaceStrong/80 px-3 py-1 text-xs font-medium uppercase tracking-[0.18em] text-muted">
                  source-only
                </span>
              ) : null}
              {doc.framework ? (
                <span className="rounded-full border border-border/70 bg-surfaceStrong/80 px-3 py-1 text-xs font-medium uppercase tracking-[0.18em] text-muted">
                  {humanizeSegment(doc.framework)}
                </span>
              ) : null}
              <span className="rounded-full border border-border/70 bg-surfaceStrong/80 px-3 py-1 text-xs font-medium uppercase tracking-[0.18em] text-muted">
                {doc.section}
              </span>
            </div>

            <article className="doc-prose">{content}</article>

            <div className="mt-12 grid gap-4 border-t border-border/70 pt-8 md:grid-cols-2">
              {doc.previous ? (
                <Link
                  href={doc.previous.route}
                  prefetch={false}
                  className="rounded-[1.5rem] border border-border/70 bg-surfaceStrong/60 p-5 transition hover:border-accent/60"
                >
                  <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.22em] text-accent">
                    <ArrowLeft className="h-3.5 w-3.5" />
                    Previous
                  </p>
                  <p className="mt-3 font-medium text-text">{doc.previous.title}</p>
                  <p className="mt-1 text-sm text-muted">{doc.previous.route}</p>
                </Link>
              ) : (
                <div />
              )}

              {doc.next ? (
                <Link
                  href={doc.next.route}
                  prefetch={false}
                  className="rounded-[1.5rem] border border-border/70 bg-surfaceStrong/60 p-5 text-right transition hover:border-accent/60"
                >
                  <p className="flex items-center justify-end gap-2 text-xs font-semibold uppercase tracking-[0.22em] text-accent">
                    Next
                    <ArrowRight className="h-3.5 w-3.5" />
                  </p>
                  <p className="mt-3 font-medium text-text">{doc.next.title}</p>
                  <p className="mt-1 text-sm text-muted">{doc.next.route}</p>
                </Link>
              ) : null}
            </div>
          </div>
        </main>

        <aside className="hidden xl:block">
          <TableOfContents items={doc.toc} />
        </aside>
      </div>
    </div>
  );
}
