import "server-only";

import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import GithubSlugger from "github-slugger";

export type ManifestEntry = {
  output_path: string;
  source_kind: string;
  source_path: string | null;
  source_url: string | null;
  source_commit: string;
  public_route: string | null;
  title_en: string | null;
  title_ko: string | null;
  notes?: string[];
};

export type TocItem = {
  id: string;
  depth: number;
  value: string;
};

export type Breadcrumb = {
  label: string;
  href?: string;
};

export type DocSummary = {
  order: number;
  route: string;
  slug: string[];
  outputPath: string;
  filePath: string;
  title: string;
  titleEn: string;
  description: string;
  sourceOnly: boolean;
  publicRoute: string | null;
  sourcePath: string | null;
  sourceKind: string;
  sourceUrl: string | null;
  sourceCommit: string;
  notes: string[];
  framework?: string;
  bucket?: string;
  section: string;
};

export type DocPageData = DocSummary & {
  frontmatter: Record<string, unknown>;
  rawContent: string;
  toc: TocItem[];
  breadcrumbs: Breadcrumb[];
  previous: DocSummary | null;
  next: DocSummary | null;
};

export type SidebarNode = {
  key: string;
  label: string;
  href?: string;
  items?: SidebarNode[];
  order: number;
};

export type SidebarSection = {
  key: string;
  label: string;
  items: SidebarNode[];
  order: number;
};

export type HomeFrameworkCard = {
  slug: string;
  label: string;
  href: string;
  description: string;
  docCount: number;
};

export type HomeData = {
  frameworkCards: HomeFrameworkCard[];
  publicCount: number;
  sourceOnlyCount: number;
  totalCount: number;
  topSections: Array<{ label: string; count: number }>;
};

const ROOT = process.cwd();
const CONTENT_DIR = path.join(ROOT, "ko");
const MANIFEST_PATH = path.join(CONTENT_DIR, "_meta", "translation-manifest.json");
const posix = path.posix;

const SEGMENT_LABELS: Record<string, string> = {
  framework: "Framework",
  guides: "Guides & Concepts",
  guide: "Guides & Concepts",
  reference: "Reference",
  examples: "Examples",
  plugins: "Plugins",
  overview: "Overview",
  eslint: "ESLint",
  source: "Source",
  "source-only": "Source-only",
  react: "React",
  angular: "Angular",
  vue: "Vue",
  solid: "Solid",
  svelte: "Svelte",
  preact: "Preact",
};

let docsCache: DocPageData[] | null = null;
let routeMapCache: Map<string, DocPageData> | null = null;
let outputRouteMapCache: Map<string, string> | null = null;

function toSummary(doc: DocPageData): DocSummary {
  const {
    order,
    route,
    slug,
    outputPath,
    filePath,
    title,
    titleEn,
    description,
    sourceOnly,
    publicRoute,
    sourcePath,
    sourceKind,
    sourceUrl,
    sourceCommit,
    notes,
    framework,
    bucket,
    section,
  } = doc;

  return {
    order,
    route,
    slug,
    outputPath,
    filePath,
    title,
    titleEn,
    description,
    sourceOnly,
    publicRoute,
    sourcePath,
    sourceKind,
    sourceUrl,
    sourceCommit,
    notes,
    framework,
    bucket,
    section,
  };
}

function stripExtension(filePath: string) {
  return filePath.replace(/\.md$/u, "");
}

function toTitleCase(value: string) {
  return value
    .replace(/[-_]/gu, " ")
    .replace(/\b\w/gu, (char) => char.toUpperCase());
}

export function humanizeSegment(segment: string) {
  return SEGMENT_LABELS[segment] ?? toTitleCase(segment);
}

function outputPathToRoute(outputPath: string, publicRoute: string | null) {
  if (publicRoute) {
    return `/${publicRoute}`;
  }

  const normalized = outputPath.replace(/^_source-only\//u, "");
  return `/source-only/${stripExtension(normalized)}`;
}

function frameworkBucket(parts: string[]) {
  const candidate = parts[2];
  if (!candidate) {
    return "overview";
  }

  if (["guides", "reference", "examples", "plugins"].includes(candidate)) {
    return candidate;
  }

  return "overview";
}

function routeToSlug(route: string) {
  return route.replace(/^\/+/u, "").split("/").filter(Boolean);
}

function bucketFromParts(parts: string[], sourceOnly: boolean) {
  if (sourceOnly) {
    return "source-only";
  }

  if (parts[0] === "framework") {
    return frameworkBucket(parts);
  }

  return parts[0] ?? "docs";
}

function buildSectionLabel(parts: string[], sourceOnly: boolean) {
  if (sourceOnly) {
    return "Source-only";
  }

  if (parts[0] === "framework" && parts[1]) {
    return `Framework / ${humanizeSegment(parts[1])} / ${humanizeSegment(frameworkBucket(parts))}`;
  }

  if (parts[0] === "eslint") {
    return "ESLint";
  }

  if (parts[0] === "reference") {
    return "Reference";
  }

  return parts[0] ? humanizeSegment(parts[0]) : "Docs";
}

function stripMarkdown(source: string) {
  let value = source;
  value = value.replace(/^```[\s\S]*?^```$/gmu, " ");
  value = value.replace(/!\[[^\]]*\]\([^)]+\)/gu, " ");
  value = value.replace(/\[([^\]]+)\]\([^)]+\)/gu, "$1");
  value = value.replace(/[`*_>#-]/gu, " ");
  value = value.replace(/\s+/gu, " ").trim();
  return value;
}

function extractDescription(source: string) {
  const text = stripMarkdown(source);
  if (!text) {
    return "";
  }

  return text.slice(0, 220).trim();
}

function extractToc(source: string) {
  const toc: TocItem[] = [];
  const slugger = new GithubSlugger();
  let inFence = false;

  for (const rawLine of source.split(/\r?\n/u)) {
    const line = rawLine.trim();
    if (line.startsWith("```")) {
      inFence = !inFence;
      continue;
    }

    if (inFence) {
      continue;
    }

    const match = /^(#{2,4})\s+(.*)$/u.exec(line);
    if (!match) {
      continue;
    }

    const depth = match[1].length;
    const value = match[2].trim();

    if (!value) {
      continue;
    }

    toc.push({
      depth,
      value,
      id: slugger.slug(value),
    });
  }

  return toc;
}

function buildBreadcrumbs(doc: DocSummary) {
  const breadcrumbs: Breadcrumb[] = [{ label: "홈", href: "/" }];
  const parts = doc.slug;

  if (doc.sourceOnly) {
    breadcrumbs.push({ label: "Source-only" });
    for (const segment of parts.slice(1, -1)) {
      breadcrumbs.push({ label: humanizeSegment(segment) });
    }
    breadcrumbs.push({ label: doc.title });
    return breadcrumbs;
  }

  if (parts[0] === "framework" && parts[1]) {
    breadcrumbs.push({ label: humanizeSegment(parts[1]) });
    if (parts[2]) {
      breadcrumbs.push({ label: humanizeSegment(parts[2]) });
    }
    breadcrumbs.push({ label: doc.title });
    return breadcrumbs;
  }

  if (parts.length > 1) {
    breadcrumbs.push({ label: humanizeSegment(parts[0]) });
  }
  breadcrumbs.push({ label: doc.title });
  return breadcrumbs;
}

function sortNodes(nodes: SidebarNode[]): SidebarNode[] {
  return nodes
    .map((node) => ({
      ...node,
      items: node.items ? sortNodes(node.items) : undefined,
    }))
    .sort((left, right) => left.order - right.order || left.label.localeCompare(right.label, "ko"));
}

function buildNodeKey(prefix: string, value: string) {
  return `${prefix}:${value}`;
}

function ensureGroup(container: SidebarNode[], key: string, label: string, order: number) {
  let group = container.find((item) => item.key === key);
  if (!group) {
    group = { key, label, order, items: [] };
    container.push(group);
  }

  if (!group.items) {
    group.items = [];
  }

  return group;
}

function buildDocs() {
  if (docsCache) {
    return docsCache;
  }

  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8")) as ManifestEntry[];
  const docs = manifest.map((entry, order) => {
    const route = outputPathToRoute(entry.output_path, entry.public_route);
    const slug = routeToSlug(route);
    const filePath = path.join(CONTENT_DIR, entry.output_path);
    const raw = fs.readFileSync(filePath, "utf8");
    const parsed = matter(raw);
    const parts = slug;
    const sourceOnly = !entry.public_route;

    const summary: DocSummary = {
      order,
      route,
      slug,
      outputPath: entry.output_path,
      filePath,
      title: entry.title_ko || String(parsed.data.title || entry.title_en || route),
      titleEn: entry.title_en || "",
      description:
        typeof parsed.data.description === "string"
          ? parsed.data.description
          : extractDescription(parsed.content),
      sourceOnly,
      publicRoute: entry.public_route,
      sourcePath: entry.source_path,
      sourceKind: entry.source_kind,
      sourceUrl: entry.source_url,
      sourceCommit: entry.source_commit,
      notes: Array.isArray(entry.notes) ? entry.notes : [],
      framework: parts[0] === "framework" ? parts[1] : undefined,
      bucket: bucketFromParts(parts, sourceOnly),
      section: buildSectionLabel(parts, sourceOnly),
    };

    return {
      ...summary,
      frontmatter: parsed.data as Record<string, unknown>,
      rawContent: parsed.content,
      toc: extractToc(parsed.content),
      breadcrumbs: [] as Breadcrumb[],
      previous: null as DocSummary | null,
      next: null as DocSummary | null,
    } satisfies DocPageData;
  });

  const publicDocs = docs.filter((doc) => !doc.sourceOnly);
  const sourceDocs = docs.filter((doc) => doc.sourceOnly);

  for (const doc of docs) {
    const siblings = doc.sourceOnly ? sourceDocs : publicDocs;
    const index = siblings.findIndex((candidate) => candidate.route === doc.route);
    const previous = index > 0 ? siblings[index - 1] : null;
    const next = index >= 0 && index < siblings.length - 1 ? siblings[index + 1] : null;

    doc.breadcrumbs = buildBreadcrumbs(doc);
    doc.previous = previous ? toSummary(previous) : null;
    doc.next = next ? toSummary(next) : null;
  }

  docsCache = docs;
  return docs;
}

function buildRouteMap() {
  if (!routeMapCache) {
    routeMapCache = new Map(buildDocs().map((doc) => [doc.route, doc]));
  }
  return routeMapCache;
}

function buildOutputRouteMap() {
  if (!outputRouteMapCache) {
    outputRouteMapCache = new Map(buildDocs().map((doc) => [doc.outputPath, doc.route]));
  }
  return outputRouteMapCache;
}

export function getAllDocs() {
  return buildDocs();
}

export function getPublicDocs() {
  return buildDocs().filter((doc) => !doc.sourceOnly);
}

function getFrameworkOverviewRoute(framework: string, docs = getPublicDocs()) {
  return (
    docs.find((doc) => doc.route === `/framework/${framework}/overview`)?.route ??
    docs.find((doc) => doc.framework === framework)?.route ??
    "/"
  );
}

export function getDocByRoute(route: string) {
  return buildRouteMap().get(route) ?? null;
}

export function getDocBySlug(slug: string[] | undefined) {
  const route = slug && slug.length > 0 ? `/${slug.join("/")}` : "/";
  if (route === "/") {
    return null;
  }
  return getDocByRoute(route);
}

export function getStaticParams() {
  return getAllDocs().map((doc) => ({
    slug: doc.slug,
  }));
}

export function getSidebarSections(currentRoute = "/") {
  const publicDocs = getPublicDocs();
  const currentParts = routeToSlug(currentRoute);
  const activeFramework = currentParts[0] === "framework" ? currentParts[1] : null;
  const sections: SidebarSection[] = [
    { key: "frameworks", label: "Frameworks", order: 0, items: [] },
    { key: "eslint", label: "ESLint", order: 1, items: [] },
    { key: "reference", label: "Reference", order: 2, items: [] },
    { key: "other", label: "Other", order: 3, items: [] },
  ];

  const sectionMap = new Map(sections.map((section) => [section.key, section]));
  const frameworkDocsByName = new Map<string, DocPageData[]>();

  for (const doc of publicDocs.filter((candidate) => candidate.framework)) {
    const framework = doc.framework!;
    const group = frameworkDocsByName.get(framework) ?? [];
    group.push(doc);
    frameworkDocsByName.set(framework, group);
  }

  const frameworkSection = sectionMap.get("frameworks");
  if (frameworkSection) {
    for (const [framework, docs] of [...frameworkDocsByName.entries()].sort(
      (left, right) => left[1][0].order - right[1][0].order,
    )) {
      if (framework !== activeFramework) {
        frameworkSection.items.push({
          key: buildNodeKey("framework", framework),
          label: humanizeSegment(framework),
          href: getFrameworkOverviewRoute(framework, publicDocs),
          order: docs[0].order,
        });
        continue;
      }

      const frameworkGroup: SidebarNode = {
        key: buildNodeKey("framework", framework),
        label: humanizeSegment(framework),
        href: getFrameworkOverviewRoute(framework, publicDocs),
        order: docs[0].order,
        items: [],
      };

      for (const doc of docs) {
        const parts = doc.slug;
        const bucket = frameworkBucket(parts);
        const bucketGroup = ensureGroup(
          frameworkGroup.items ?? [],
          buildNodeKey(`framework:${framework}`, bucket),
          humanizeSegment(bucket),
          doc.order,
        );
        bucketGroup.items?.push({
          key: doc.route,
          label: doc.title,
          href: doc.route,
          order: doc.order,
        });
      }

      frameworkSection.items.push(frameworkGroup);
    }
  }

  for (const doc of publicDocs.filter((candidate) => !candidate.framework)) {
    const parts = doc.slug;
    const sectionKey = parts[0] === "eslint" || parts[0] === "reference" ? parts[0] : "other";
    const section = sectionMap.get(sectionKey);
    if (!section) {
      continue;
    }

    if (parts.length === 1) {
      section.items.push({
        key: doc.route,
        label: doc.title,
        href: doc.route,
        order: doc.order,
      });
      continue;
    }

    let cursor = section.items;
    for (const [index, segment] of parts.slice(1, -1).entries()) {
      const group = ensureGroup(
        cursor,
        buildNodeKey(`${sectionKey}:${index}`, segment),
        humanizeSegment(segment),
        doc.order,
      );
      cursor = group.items ?? [];
    }

    cursor.push({
      key: doc.route,
      label: doc.title,
      href: doc.route,
      order: doc.order,
    });
  }

  return sections
    .map((section) => ({
      ...section,
      items: sortNodes(section.items),
    }))
    .filter((section) => section.items.length > 0);
}

export function getHomeData(): HomeData {
  const docs = getAllDocs();
  const publicDocs = docs.filter((doc) => !doc.sourceOnly);
  const frameworkMap = new Map<string, HomeFrameworkCard>();

  for (const doc of publicDocs) {
    if (!doc.framework) {
      continue;
    }

    const existing = frameworkMap.get(doc.framework);
    const href =
      publicDocs.find((candidate) => candidate.route === `/framework/${doc.framework}/overview`)?.route ??
      publicDocs.find((candidate) => candidate.framework === doc.framework)?.route ??
      "/";
    const description =
      publicDocs.find((candidate) => candidate.route === href)?.description ?? `${humanizeSegment(doc.framework)} 문서`;

    frameworkMap.set(doc.framework, {
      slug: doc.framework,
      label: humanizeSegment(doc.framework),
      href,
      description,
      docCount: (existing?.docCount ?? 0) + 1,
    });
  }

  const frameworkCards = [...frameworkMap.values()].sort((left, right) =>
    left.label.localeCompare(right.label, "en"),
  );
  const topSections = [
    { label: "Frameworks", count: publicDocs.filter((doc) => doc.slug[0] === "framework").length },
    { label: "ESLint", count: publicDocs.filter((doc) => doc.slug[0] === "eslint").length },
    { label: "Reference", count: publicDocs.filter((doc) => doc.slug[0] === "reference").length },
  ];

  return {
    frameworkCards,
    publicCount: publicDocs.length,
    sourceOnlyCount: docs.length - publicDocs.length,
    totalCount: docs.length,
    topSections,
  };
}

export function getOutputPathRouteMap() {
  return buildOutputRouteMap();
}

function isExternalHref(href: string) {
  return /^(?:[a-z][a-z\d+.-]*:)?\/\//iu.test(href) || href.startsWith("mailto:") || href.startsWith("tel:");
}

export function rewriteMarkdownHref(href: string, currentOutputPath: string) {
  if (!href || href.startsWith("#") || href.startsWith("?") || isExternalHref(href)) {
    return href;
  }

  const hashIndex = href.indexOf("#");
  const hash = hashIndex >= 0 ? href.slice(hashIndex) : "";
  const withoutHash = hashIndex >= 0 ? href.slice(0, hashIndex) : href;
  const queryIndex = withoutHash.indexOf("?");
  const query = queryIndex >= 0 ? withoutHash.slice(queryIndex) : "";
  const pathname = queryIndex >= 0 ? withoutHash.slice(0, queryIndex) : withoutHash;

  if (!pathname) {
    return `${query}${hash}`;
  }

  let candidate: string | null = null;

  if (pathname.startsWith("/")) {
    if (pathname.endsWith(".md")) {
      candidate = pathname.replace(/^\/+/u, "");
    } else {
      return href;
    }
  } else if (pathname.endsWith(".md")) {
    candidate = posix.normalize(posix.join(posix.dirname(currentOutputPath), pathname));
  }

  if (!candidate) {
    return href;
  }

  const route = buildOutputRouteMap().get(candidate);
  if (!route) {
    return href;
  }

  return `${route}${query}${hash}`;
}
