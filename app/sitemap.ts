import fs from "node:fs";

import type { MetadataRoute } from "next";

import { getPublicDocs } from "@/lib/docs";
import { toAbsoluteUrl } from "@/lib/site";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  const docs = getPublicDocs();

  return [
    {
      url: toAbsoluteUrl("/"),
      changeFrequency: "weekly",
      priority: 1,
    },
    ...docs.map((doc) => ({
      url: toAbsoluteUrl(doc.route),
      lastModified: fsSafeMtime(doc.filePath),
      changeFrequency: "monthly" as const,
      priority: doc.route.endsWith("/overview") || doc.route.endsWith("/installation") ? 0.9 : 0.7,
    })),
  ];
}

function fsSafeMtime(filePath: string) {
  try {
    return fs.statSync(filePath).mtime;
  } catch {
    return new Date();
  }
}
