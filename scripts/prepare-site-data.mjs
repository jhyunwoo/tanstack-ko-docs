import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const ROOT = process.cwd();
const CONTENT_DIR = path.join(ROOT, "ko");
const META_DIR = path.join(CONTENT_DIR, "_meta");
const MANIFEST_PATH = path.join(META_DIR, "translation-manifest.json");
const PUBLIC_DIR = path.join(ROOT, "public");
const SEARCH_INDEX_PATH = path.join(PUBLIC_DIR, "search-index.json");
const SITE_STATS_PATH = path.join(PUBLIC_DIR, "site-stats.json");
const PUBLIC_MANIFEST_PATH = path.join(PUBLIC_DIR, "translation-manifest.json");
const DEFAULT_SITE_URL = "https://tanstack-query-docs-ko.vercel.app";

const PLACEHOLDER_PATTERN = /ZXQ[A-Z0-9_-]*/g;

function walkMarkdownFiles(dir, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkMarkdownFiles(fullPath, acc);
      continue;
    }

    if (entry.isFile() && fullPath.endsWith(".md")) {
      acc.push(fullPath);
    }
  }

  return acc;
}

function stripExtension(filePath) {
  return filePath.replace(/\.md$/u, "");
}

function outputPathToRoute(outputPath, publicRoute) {
  if (publicRoute) {
    return `/${publicRoute}`;
  }

  const normalized = outputPath.replace(/^_source-only\//u, "");
  return `/source-only/${stripExtension(normalized)}`;
}

function humanizeSegment(segment) {
  return segment
    .replace(/[-_]/gu, " ")
    .replace(/\b\w/gu, (char) => char.toUpperCase());
}

function frameworkBucket(parts) {
  const candidate = parts[2];
  if (!candidate) {
    return "overview";
  }

  if (["guides", "reference", "examples", "plugins"].includes(candidate)) {
    return candidate;
  }

  return "overview";
}

function buildSectionLabel(route, sourceOnly) {
  const cleaned = route.replace(/^\/+/u, "");
  const parts = cleaned.split("/").filter(Boolean);

  if (sourceOnly) {
    return "Source-only";
  }

  if (parts[0] === "framework" && parts[1]) {
    const framework = humanizeSegment(parts[1]);
    const bucket = humanizeSegment(frameworkBucket(parts));
    return `Framework / ${framework} / ${bucket}`;
  }

  if (parts[0] === "eslint") {
    return "ESLint";
  }

  if (parts[0] === "reference") {
    return "Reference";
  }

  return parts[0] ? humanizeSegment(parts[0]) : "Docs";
}

function stripMarkdown(source) {
  let text = source;

  text = text.replace(/^```[\s\S]*?^```$/gmu, " ");
  text = text.replace(/^---[\s\S]*?---\s*/u, "");
  text = text.replace(/!\[[^\]]*\]\([^)]+\)/gu, " ");
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/gu, "$1");
  text = text.replace(/[`*_>#-]/gu, " ");
  text = text.replace(/\s+/gu, " ").trim();

  return text;
}

function extractHeadings(source) {
  const headings = [];
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

    const match = /^(#{1,6})\s+(.*)$/u.exec(line);
    if (!match) {
      continue;
    }

    const value = match[2].trim();
    if (value) {
      headings.push(value);
    }
  }

  return headings;
}

function extractExcerpt(source) {
  const stripped = stripMarkdown(source);
  if (!stripped) {
    return "";
  }

  const sentences = stripped.split(/(?<=[.!?])\s+/u);
  return sentences[0].slice(0, 220).trim();
}

function main() {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8"));
  const markdownFiles = walkMarkdownFiles(CONTENT_DIR);
  const placeholderHits = [];

  for (const filePath of markdownFiles) {
    const content = fs.readFileSync(filePath, "utf8");
    const matches = [...content.matchAll(PLACEHOLDER_PATTERN)].map((match) => match[0]);
    if (matches.length > 0) {
      placeholderHits.push({
        file: path.relative(ROOT, filePath),
        matches,
      });
    }
  }

  if (placeholderHits.length > 0) {
    console.error("Found unresolved placeholder tokens:");
    for (const hit of placeholderHits) {
      console.error(`- ${hit.file}: ${hit.matches.join(", ")}`);
    }
    process.exit(1);
  }

  fs.mkdirSync(PUBLIC_DIR, { recursive: true });

  if (!process.env.NEXT_PUBLIC_SITE_URL) {
    console.warn(
      `NEXT_PUBLIC_SITE_URL is not set. SEO metadata will fall back to ${DEFAULT_SITE_URL}. Override it for the production domain.`,
    );
  }

  const searchIndex = manifest.map((entry) => {
    const filePath = path.join(CONTENT_DIR, entry.output_path);
    if (!fs.existsSync(filePath)) {
      throw new Error(`Missing translated file for manifest entry: ${entry.output_path}`);
    }

    const raw = fs.readFileSync(filePath, "utf8");
    const parsed = matter(raw);
    const route = outputPathToRoute(entry.output_path, entry.public_route);
    const sourceOnly = !entry.public_route;

    return {
      title: entry.title_ko || parsed.data.title || entry.title_en || route,
      route,
      section: buildSectionLabel(route, sourceOnly),
      excerpt: extractExcerpt(parsed.content),
      headings: extractHeadings(parsed.content),
      sourceOnly,
    };
  });

  fs.writeFileSync(SEARCH_INDEX_PATH, `${JSON.stringify(searchIndex, null, 2)}\n`);
  fs.writeFileSync(PUBLIC_MANIFEST_PATH, `${JSON.stringify(manifest, null, 2)}\n`);
  fs.writeFileSync(
    SITE_STATS_PATH,
    `${JSON.stringify(
      {
        generatedAt: new Date().toISOString(),
        publicCount: manifest.filter((entry) => entry.public_route).length,
        sourceOnlyCount: manifest.filter((entry) => !entry.public_route).length,
        totalCount: manifest.length,
      },
      null,
      2,
    )}\n`,
  );

  console.log(
    `Prepared ${searchIndex.length} docs for search (${searchIndex.filter((item) => item.sourceOnly).length} source-only).`,
  );
}

main();
