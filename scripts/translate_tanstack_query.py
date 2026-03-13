#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import posixpath
import re
import sys
import time
from http.client import RemoteDisconnected
from dataclasses import dataclass, field
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import yaml


SOURCE_COMMIT = "489359a569fd865f3afd7aac8fa43dfc429309e3"
SOURCE_REPO_PAIR = "TanStack/query"
SOURCE_REPO_ROOT = Path(os.environ.get("TANSTACK_QUERY_SOURCE_ROOT", "/tmp/tanstack-query-docs-scan"))
OUTPUT_ROOT = Path(__file__).resolve().parents[1] / "ko"
META_ROOT = OUTPUT_ROOT / "_meta"
CACHE_ROOT = Path(__file__).resolve().parents[1] / ".cache"
TRANSLATION_CACHE_PATH = CACHE_ROOT / "google-translate-cache.json"
VERIFICATION_REPORT_PATH = META_ROOT / "verification-report.json"
MANIFEST_PATH = META_ROOT / "translation-manifest.json"
MAX_TRANSLATE_CHARS = 3200
REQUEST_DELAY_SECONDS = float(os.environ.get("GOOGLE_TRANSLATE_DELAY", "0.25"))
MAX_RETRY_COUNT = 8
RESUME_EXISTING_OUTPUTS = os.environ.get("RESUME_EXISTING_OUTPUTS", "1") != "0"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"}
SPECIAL_PUBLIC_ALIAS_ROUTE = "framework/react/reference/functions/HydrationBoundary"
SPECIAL_PUBLIC_ALIAS_SOURCE = "docs/framework/preact/reference/functions/HydrationBoundary.md"
SPECIAL_FALLBACK_ROUTE = "framework/react/examples/nextjs-suspense-streaming"
SPECIAL_FALLBACK_LABEL = "Next.js app with streaming"

NON_TRANSLATABLE_FRONTMATTER_KEYS = {
    "id",
    "ref",
    "replace",
    "url",
    "published",
    "slug",
    "path",
    "to",
}
NON_OUTPUT_FRONTMATTER_KEYS = {"ref", "replace"}

STATIC_PROTECTED_TERMS = [
    "TanStack Query",
    "React Query",
    "Angular Query",
    "Solid Query",
    "Vue Query",
    "Svelte Query",
    "Preact Query",
    "HydrationBoundary",
    "QueryClient",
    "QueryCache",
    "MutationCache",
    "QueryObserver",
    "QueriesObserver",
    "InfiniteQueryObserver",
    "useSuspenseInfiniteQuery",
    "useSuspenseQueries",
    "useSuspenseQuery",
    "useInfiniteQuery",
    "useIsFetching",
    "useIsMutating",
    "useMutationState",
    "useMutation",
    "useQueries",
    "useQueryClient",
    "useQuery",
    "injectInfiniteQuery",
    "injectMutationState",
    "injectMutation",
    "injectQueries",
    "injectQueryClient",
    "injectQuery",
    "createInfiniteQuery",
    "createMutation",
    "createQueries",
    "createQueryClient",
    "createQuery",
    "prefetchInfiniteQuery",
    "prefetchQuery",
    "ensureQueryData",
    "getQueryData",
    "setQueryData",
    "queryKey",
    "queryFn",
    "mutationFn",
    "staleTime",
    "gcTime",
    "networkMode",
    "retryDelay",
    "initialData",
    "placeholderData",
    "throwOnError",
    "suspense",
    "Suspense",
    "mutation",
    "mutations",
    "Mutation",
    "Mutations",
    "query",
    "queries",
    "Query",
    "Queries",
    "hydration",
    "Hydration",
    "React Router",
    "Apollo Client",
    "Apollo",
    "SWR",
    "Redux",
    "Redux Toolkit",
    "GraphQL",
    "Promise",
    "TypeScript",
    "JavaScript",
    "Next.js",
    "SvelteKit",
    "SolidStart",
    "create-svelte",
    "stable-hash",
    "GitHub",
    "CodeSandbox",
    "StackBlitz",
    "N/A",
    "Route Change",
    "Route Path",
    "Loader Run",
    "Stale While Revalidate",
]

MARKDOWN_LINK_RE = re.compile(r"(!?)\[([^\]]*?)\]\(([^)\n]+)\)")
HTML_TAG_RE = re.compile(r"<[^>\n]+>")
INLINE_CODE_RE = re.compile(r"(``[^`]*``|`[^`\n]+`)")
MARKDOWN_REFERENCE_DEFINITION_RE = re.compile(r"(?m)^\[[^\]\n]+\]:[^\n]*$")
MARKDOWN_REFERENCE_ID_RE = re.compile(r"(?<=\]\[)[^\]\n]+(?=\])")
MARKDOWN_INLINE_LINK_RE = re.compile(r"(!?\[)([^\]\n]+)(\]\([^)]+\))")
MARKDOWN_REFERENCE_LINK_RE = re.compile(r"(!?\[)([^\]\n]+)(\]\[[^\]\n]+\])")
MARKDOWN_STRUCTURAL_COMMENT_RE = re.compile(r"^\[//\]: # '.*?'\s*$", re.MULTILINE)
CODE_FENCE_START_RE = re.compile(r"^(```+|~~~+)(.*)$")
CODE_FENCE_END_TEMPLATE = r"^{fence}\s*$"
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$")
HTML_ATTR_RE = re.compile(r"""(?P<attr>\b(?:src|href)\b)\s*=\s*(?P<quote>['"])(?P<value>.*?)(?P=quote)""")
HTML_TRANSLATABLE_ATTR_RE = re.compile(r"""(?P<attr>\b(?:alt|title)\b)\s*=\s*(?P<quote>['"])(?P<value>.*?)(?P=quote)""")
RAW_URL_RE = re.compile(r"https?://[^\s<>)]+")
DOCS_URL_RE = re.compile(
    r"^(?:https?://tanstack\.com)?/query/latest/docs/(?P<route>[^?#]+?)(?:\.md)?(?P<suffix>[?#].*)?$"
)
DOCS_URL_RE_2 = re.compile(
    r"^https?://tanstack\.com/query/latest/docs/(?P<route>[^?#]+?)(?:\.md)?(?P<suffix>[?#].*)?$"
)
RAW_QUERY_RE = re.compile(
    r"https?://raw\.githubusercontent\.com/TanStack/query/[^/]+/(?P<path>.+)$",
    re.IGNORECASE,
)
GITHUB_BLOB_TREE_RE = re.compile(
    r"^https?://github\.com/TanStack/query/(?P<kind>blob|tree)/[^/]+/(?P<path>.+)$",
    re.IGNORECASE,
)
SECTION_REGEX = re.compile(r"\[//\]: # '([a-zA-Z\d]*)'[\S\s]*?\[//\]: # '([a-zA-Z\d]*)'")
PACKAGE_NAME_RE = re.compile(r"(?<![A-Za-z0-9_`])@?[A-Za-z0-9_.]+/[A-Za-z0-9_.-]+")
LOWER_CAMEL_IDENTIFIER_RE = re.compile(r"\b[a-z]+(?:[A-Z][A-Za-z0-9]*)+\b")
PASCAL_IDENTIFIER_RE = re.compile(r"\b[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*\b")
TYPE_PARAMETER_RE = re.compile(r"\bT[A-Z][A-Za-z0-9]*\b")
TECHNICAL_HINTS = (
    "Query",
    "Queries",
    "Mutation",
    "Hydration",
    "Boundary",
    "Client",
    "Cache",
    "Observer",
    "Provider",
    "Options",
    "Result",
    "Results",
    "State",
    "Context",
    "Accessor",
    "Persister",
    "Router",
    "Refetch",
    "Infinite",
    "Suspense",
    "Placeholder",
    "InitialData",
    "Undefined",
    "Defined",
    "Dehydrated",
    "Restoring",
)


@dataclass
class ParsedFrontmatter:
    data: dict[str, Any]
    body: str
    raw: str
    raw_text: str


@dataclass
class ResolvedDocument:
    source_path: str
    source_kind: str
    source_frontmatter: dict[str, Any]
    source_body: str
    final_body: str
    final_source_path: str | None
    title_en: str
    notes: list[str] = field(default_factory=list)


@dataclass
class OutputDocument:
    output_path: str
    source_kind: str
    source_path: str | None
    source_url: str | None
    source_commit: str
    public_route: str | None
    title_en: str
    title_ko: str
    notes: list[str]


class TranslationCache:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            self.data = json.loads(path.read_text())
        else:
            self.data = {}
        self.pending_writes = 0

    def get(self, key: str) -> str | None:
        return self.data.get(key)

    def set(self, key: str, value: str) -> None:
        self.data[key] = value
        self.pending_writes += 1
        if self.pending_writes >= 50:
            self.flush()

    def flush(self) -> None:
        self.path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
        self.pending_writes = 0


class Translator:
    def __init__(self, cache: TranslationCache, protected_terms: list[str]) -> None:
        self.cache = cache
        self.protected_terms = sorted({term for term in protected_terms if term}, key=len, reverse=True)

    def translate_text(self, text: str) -> str:
        if not text or not text.strip():
            return text
        cache_key = f"v1::{text}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached
        translated = self._translate_large_text(text)
        self.cache.set(cache_key, translated)
        return translated

    def _translate_large_text(self, text: str) -> str:
        if len(text) <= MAX_TRANSLATE_CHARS:
            return self._translate_via_google(text)
        chunks = split_large_text(text, MAX_TRANSLATE_CHARS)
        return "".join(self._translate_via_google(chunk) for chunk in chunks)

    def _translate_via_google(self, text: str) -> str:
        translated = self._translate_via_google_mobile(text)
        if translated is not None:
            return translated
        return self._translate_via_google_api(text)

    def _translate_via_google_mobile(self, text: str) -> str | None:
        query = urlencode({"sl": "en", "tl": "ko", "q": text})
        url = f"https://translate.google.com/m?{query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        delay = REQUEST_DELAY_SECONDS
        for _attempt in range(MAX_RETRY_COUNT):
            try:
                request = Request(url, headers=headers)
                with urlopen(request, timeout=30) as response:
                    html = response.read().decode("utf-8", "replace")
                match = re.search(r'class="result-container"[^>]*>(.*?)<', html, re.DOTALL)
                if not match:
                    match = re.search(r'class="t0"[^>]*>(.*?)<', html, re.DOTALL)
                if not match:
                    return None
                translated = unescape(match.group(1))
                time.sleep(REQUEST_DELAY_SECONDS)
                return translated
            except HTTPError as exc:
                if exc.code == 429:
                    time.sleep(max(delay, 20.0))
                    delay = max(delay * 2, 20.0)
                else:
                    time.sleep(delay)
                    delay *= 2
            except (URLError, TimeoutError, json.JSONDecodeError, RemoteDisconnected, OSError) as exc:
                time.sleep(delay)
                delay *= 2
        return None

    def _translate_via_google_api(self, text: str) -> str:
        query = urlencode({"client": "gtx", "sl": "en", "tl": "ko", "dt": "t", "q": text})
        url = f"https://translate.googleapis.com/translate_a/single?{query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        delay = REQUEST_DELAY_SECONDS
        last_error: Exception | None = None
        for _attempt in range(MAX_RETRY_COUNT):
            try:
                request = Request(url, headers=headers)
                with urlopen(request, timeout=30) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                translated = "".join(part[0] for part in payload[0] if part and part[0] is not None)
                time.sleep(REQUEST_DELAY_SECONDS)
                return translated
            except HTTPError as exc:
                last_error = exc
                if exc.code == 429:
                    time.sleep(max(delay, 20.0))
                    delay = max(delay * 2, 20.0)
                else:
                    time.sleep(delay)
                    delay *= 2
            except (URLError, TimeoutError, json.JSONDecodeError, RemoteDisconnected, OSError) as exc:
                last_error = exc
                time.sleep(delay)
                delay *= 2
        raise RuntimeError(f"Translation failed after retries: {last_error}")


def split_large_text(text: str, limit: int) -> list[str]:
    if len(text) <= limit:
        return [text]
    pieces: list[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= limit:
            pieces.append(remaining)
            break
        cut = remaining.rfind("\n\n", 0, limit)
        if cut < limit // 2:
            cut = remaining.rfind("\n", 0, limit)
        if cut < limit // 2:
            cut = remaining.rfind(". ", 0, limit)
        if cut < limit // 2:
            cut = limit
        if cut <= 0:
            cut = limit
        pieces.append(remaining[:cut])
        remaining = remaining[cut:]
    return pieces


def parse_frontmatter(text: str) -> ParsedFrontmatter:
    if not text.startswith("---\n"):
        return ParsedFrontmatter(data={}, body=text, raw="", raw_text=text)
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        return ParsedFrontmatter(data={}, body=text, raw="", raw_text=text)
    raw = match.group(1)
    body = text[match.end() :]
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        data = {}
    return ParsedFrontmatter(data=data, body=body, raw=raw, raw_text=text)


def dump_frontmatter(data: dict[str, Any]) -> str:
    if not data:
        return ""
    dumped = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        width=100000,
        default_flow_style=False,
    ).strip()
    return f"---\n{dumped}\n---\n\n"


def replace_content(text: str, frontmatter: ParsedFrontmatter) -> str:
    replace_map = frontmatter.data.get("replace")
    result = text
    if isinstance(replace_map, dict):
        for key, value in replace_map.items():
            result = re.sub(key, str(value), result)
    return result


def replace_sections(text: str, frontmatter: ParsedFrontmatter) -> str:
    result = text
    section_marker_regex = re.compile(r"\[//\]: # '([a-zA-Z\d]*)'")
    substitutes: dict[str, re.Match[str]] = {}
    for match in SECTION_REGEX.finditer(frontmatter.body):
        if match.group(1) == match.group(2):
            substitutes[match.group(1)] = match
    sections: dict[str, re.Match[str]] = {}
    for match in SECTION_REGEX.finditer(result):
        if match.group(1) == match.group(2):
            sections[match.group(1)] = match
    for key, substitute in reversed(list(substitutes.items())):
        section = sections.get(key)
        if section is None:
            continue
        result = result[: section.start()] + substitute.group(0) + result[section.end() :]
    return section_marker_regex.sub("", result)


def pin_raw_query_urls(text: str) -> str:
    return RAW_QUERY_RE.sub(
        lambda match: f"https://raw.githubusercontent.com/TanStack/query/{SOURCE_COMMIT}/{match.group('path')}",
        text,
    )


def read_upstream_text(source_path: str) -> str:
    path = SOURCE_REPO_ROOT / source_path
    return path.read_text()


def title_from_frontmatter_or_body(frontmatter: dict[str, Any], body: str, fallback: str) -> str:
    title = frontmatter.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    heading_match = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()
    return fallback


def resolve_document(source_path: str, source_kind: str, title_fallback: str, extra_notes: list[str] | None = None) -> ResolvedDocument:
    source_text = read_upstream_text(source_path)
    source_parsed = parse_frontmatter(source_text)
    current_path = source_path
    origin_frontmatter: ParsedFrontmatter | None = None
    final_path: str | None = source_path
    for _ in range(4):
        text = read_upstream_text(current_path)
        parsed = parse_frontmatter(text)
        ref = parsed.data.get("ref")
        if not ref:
            resolved_text = text
            if origin_frontmatter is not None:
                resolved_text = replace_content(resolved_text, origin_frontmatter)
                resolved_text = replace_sections(resolved_text, origin_frontmatter)
            resolved_text = pin_raw_query_urls(resolved_text)
            resolved_parsed = parse_frontmatter(resolved_text)
            return ResolvedDocument(
                source_path=source_path,
                source_kind=source_kind,
                source_frontmatter=source_parsed.data,
                source_body=source_parsed.body,
                final_body=resolved_parsed.body,
                final_source_path=current_path,
                title_en=title_from_frontmatter_or_body(source_parsed.data, resolved_parsed.body, title_fallback),
                notes=list(extra_notes or []),
            )
        origin_frontmatter = parsed
        current_path = str(ref)
        final_path = current_path
    raise RuntimeError(f"Ref resolution exceeded depth limit for {source_path} -> {final_path}")


def public_routes_from_config(config: dict[str, Any]) -> list[dict[str, str]]:
    routes: list[dict[str, str]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            to_value = node.get("to")
            label_value = node.get("label")
            if isinstance(to_value, str):
                routes.append({"to": to_value, "label": label_value or posixpath.basename(to_value)})
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(config.get("sections", []))
    deduped: dict[str, dict[str, str]] = {}
    for route in routes:
        deduped[route["to"]] = route
    return list(deduped.values())


def is_markdown_file(path: Path) -> bool:
    return path.suffix.lower() == ".md"


def all_source_markdown_paths() -> tuple[list[str], list[str]]:
    doc_paths = sorted(
        str(path.relative_to(SOURCE_REPO_ROOT)).replace(os.sep, "/")
        for path in (SOURCE_REPO_ROOT / "docs").rglob("*.md")
        if is_markdown_file(path)
    )
    example_paths = sorted(
        str(path.relative_to(SOURCE_REPO_ROOT)).replace(os.sep, "/")
        for path in (SOURCE_REPO_ROOT / "examples").rglob("README.md")
    )
    return doc_paths, example_paths


def route_to_source_path(route: str) -> tuple[str | None, str, list[str]]:
    if route == SPECIAL_PUBLIC_ALIAS_ROUTE:
        return SPECIAL_PUBLIC_ALIAS_SOURCE, "doc", ["config-typo-alias"]
    if route == SPECIAL_FALLBACK_ROUTE:
        return None, "rendered-page-fallback", ["rendered-page-fallback"]
    if "/examples/" in route:
        match = re.match(r"^framework/([^/]+)/examples/(.+)$", route)
        if not match:
            raise RuntimeError(f"Unexpected example route: {route}")
        framework, example_slug = match.groups()
        source_path = f"examples/{framework}/{example_slug}/README.md"
        if not (SOURCE_REPO_ROOT / source_path).exists():
            raise FileNotFoundError(source_path)
        return source_path, "example", []
    source_path = f"docs/{route}.md"
    if not (SOURCE_REPO_ROOT / source_path).exists():
        raise FileNotFoundError(source_path)
    return source_path, "doc", []


def output_path_for_public_route(route: str) -> str:
    return f"{route}.md"


def output_path_for_source_only(source_path: str) -> str:
    return f"_source-only/{source_path}"


def convert_blob_or_tree_url_to_commit(url: str) -> str:
    match = GITHUB_BLOB_TREE_RE.match(url)
    if not match:
        return url
    kind = match.group("kind")
    path = match.group("path")
    return f"https://github.com/TanStack/query/{kind}/{SOURCE_COMMIT}/{path}"


def source_url_for_path(source_path: str) -> str:
    return f"https://raw.githubusercontent.com/TanStack/query/{SOURCE_COMMIT}/{source_path}"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://") or value.startswith("mailto:")


def looks_like_identifier(value: str) -> bool:
    if not value:
        return False
    if "/" in value or "\\" in value:
        return True
    if re.fullmatch(r"[A-Za-z0-9._@:-]+", value):
        return True
    return False


def looks_like_technical_label(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return False
    if stripped.startswith("@"):
        return True
    if stripped in STATIC_PROTECTED_TERMS:
        return True
    if stripped.endswith("()"):
        return True
    if re.fullmatch(r"[A-Za-z0-9_.()/:@-]+", stripped):
        if re.search(r"[a-z][A-Z]", stripped):
            return True
        if any(hint in stripped for hint in TECHNICAL_HINTS):
            return True
        if "/" in stripped or "_" in stripped:
            return True
        if "-" in stripped and stripped.lower() != stripped:
            return True
        if PACKAGE_NAME_RE.fullmatch(stripped):
            return True
    return False


def build_protected_terms(doc_paths: list[str], example_paths: list[str]) -> list[str]:
    protected = set(STATIC_PROTECTED_TERMS)
    for source_path in doc_paths + example_paths:
        parsed = parse_frontmatter(read_upstream_text(source_path))
        candidates = [
            parsed.data.get("id"),
            parsed.data.get("title"),
            Path(source_path).stem,
            title_from_frontmatter_or_body(parsed.data, parsed.body, ""),
        ]
        for candidate in candidates:
            if not isinstance(candidate, str):
                continue
            normalized = candidate.strip()
            if not normalized:
                continue
            if looks_like_technical_label(normalized):
                protected.add(normalized)
    return sorted(protected, key=len, reverse=True)


def translate_frontmatter_value(translator: Translator, value: Any, key: str | None = None) -> Any:
    if isinstance(value, dict):
        if key in NON_TRANSLATABLE_FRONTMATTER_KEYS:
            return value
        return {k: translate_frontmatter_value(translator, v, key=k) for k, v in value.items()}
    if isinstance(value, list):
        return [translate_frontmatter_value(translator, item, key=key) for item in value]
    if isinstance(value, str):
        if key in {"title", "description"}:
            return translate_protected_text(translator, value)
        if key in NON_TRANSLATABLE_FRONTMATTER_KEYS:
            return value
        if looks_like_url(value) or looks_like_identifier(value):
            return value
        return translate_protected_text(translator, value)
    return value


def should_preserve_title_english(title: str, output_path: str) -> bool:
    if not isinstance(title, str) or not title.strip():
        return False
    if "/plugins/" in output_path:
        return True
    if "/reference/" in output_path:
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_.()/:-]*", title):
            return True
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_.()/:-]* \([A-Za-z ]+\)", title):
            return True
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_.()/:-]*", title):
        if re.search(r"[a-z][A-Z]", title):
            return True
        if any(token in title for token in ["Query", "Mutation", "Hydration", "Persister", "Boundary", "Provider", "Client", "Options", "Result", "Feature", "Context", "Accessor"]):
            return True
    return False


def build_output_frontmatter(
    translator: Translator,
    source_frontmatter: dict[str, Any],
    output_path: str,
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in source_frontmatter.items():
        if key in NON_OUTPUT_FRONTMATTER_KEYS:
            continue
        if key == "title" and isinstance(value, str) and should_preserve_title_english(value, output_path):
            result[key] = value
            continue
        result[key] = translate_frontmatter_value(translator, value, key=key)
    return result


def translate_protected_text(translator: Translator, text: str) -> str:
    protected_text, restore_map = protect_terms(text, translator.protected_terms)
    translated = translator.translate_text(protected_text)
    return restore_placeholders(canonicalize_translated_text(translated), restore_map)


def protect_terms(text: str, protected_terms: list[str]) -> tuple[str, dict[str, str]]:
    restore_map: dict[str, str] = {}
    result = text
    for index, term in enumerate(protected_terms):
        token = f"ZXQTERM{index:04d}QXZ"
        pattern = re.compile(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])")
        if pattern.search(result):
            result = pattern.sub(token, result)
            restore_map[token] = term
    return result, restore_map


def protect_pattern_matches(
    text: str,
    pattern: re.Pattern[str],
    restore_map: dict[str, str],
    predicate: Any | None = None,
) -> str:
    counter = len(restore_map)

    def replace_match(match: re.Match[str]) -> str:
        nonlocal counter
        original = match.group(0)
        if predicate is not None and not predicate(original):
            return original
        token = f"@@ZXQAUTO{counter:04d}@@"
        counter += 1
        restore_map[token] = original
        return token

    return pattern.sub(replace_match, text)


def protect_markdown_link_labels(text: str, restore_map: dict[str, str]) -> str:
    def protect_label(match: re.Match[str]) -> str:
        prefix, label, suffix = match.groups()
        if not looks_like_technical_label(label):
            return match.group(0)
        token = f"@@ZXQLABEL{len(restore_map):04d}@@"
        restore_map[token] = label
        return f"{prefix}{token}{suffix}"

    updated = MARKDOWN_INLINE_LINK_RE.sub(protect_label, text)
    return MARKDOWN_REFERENCE_LINK_RE.sub(protect_label, updated)


def restore_placeholders(text: str, restore_map: dict[str, str]) -> str:
    restored = text
    for token, original in restore_map.items():
        restored = restored.replace(token, original)
    return restored


def canonicalize_translated_text(text: str) -> str:
    normalized = text
    replacements = [
        ("반응 라우터", "React Router"),
        ("반응하다", "React"),
        ("리덕스", "Redux"),
        ("아폴로 클라이언트", "Apollo Client"),
        ("아폴로", "Apollo"),
        ("날씬한 만들기", "create-svelte"),
        ("노선변경", "라우트 변경"),
        ("경로 경로", "라우트 경로"),
        ("통화 서명", "호출 시그니처"),
        ("유형 매개변수", "타입 매개변수"),
        ("반품", "반환값"),
        ("약속", "Promise"),
        ("재검증하는 동안 유효하지 않음", "Stale While Revalidate"),
    ]
    for old, new in replacements:
        normalized = normalized.replace(old, new)
    normalized = re.sub(r"(?m)^정의:\s+", "정의 위치: ", normalized)
    normalized = re.sub(r"(?m)^(#+)\s+보다\s*$", r"\1 참고", normalized)
    normalized = re.sub(r"(?m)^(#+)\s+통화 서명\s*$", r"\1 호출 시그니처", normalized)
    normalized = re.sub(r"(?m)^(#+)\s+유형 매개변수\s*$", r"\1 타입 매개변수", normalized)
    normalized = re.sub(r"(?m)^(#+)\s+반품\s*$", r"\1 반환값", normalized)
    normalized = re.sub(r"(?m)^(#+)\s+메모\s*$", r"\1 참고 사항", normalized)
    return normalized


def current_output_absolute(output_path: str) -> Path:
    return OUTPUT_ROOT / output_path


def rewrite_destination(
    destination: str,
    *,
    is_image: bool,
    current_output_path: str,
    current_base_source: str | None,
    route_to_output: dict[str, str],
    source_only_output_map: dict[str, str],
    public_source_output_map: dict[str, str],
) -> str:
    if not destination or destination.startswith("#") or destination.startswith("mailto:") or destination.startswith("tel:"):
        return destination
    if destination.startswith("<http://") or destination.startswith("<https://"):
        return destination

    destination = normalize_translated_destination(destination)

    absolute_match = DOCS_URL_RE.match(destination) or DOCS_URL_RE_2.match(destination)
    if absolute_match:
        route = absolute_match.group("route").rstrip("/")
        suffix = absolute_match.group("suffix") or ""
        target_output = route_to_output.get(route)
        if target_output:
            return relative_link(current_output_path, target_output) + suffix
        return destination

    if destination.startswith("/query/latest/docs/"):
        route = destination.removeprefix("/query/latest/docs/").split("?", 1)[0].split("#", 1)[0].rstrip("/")
        suffix = destination[len("/query/latest/docs/") + len(route) :]
        if route.endswith(".md"):
            route = route[:-3]
        target_output = route_to_output.get(route)
        if target_output:
            return relative_link(current_output_path, target_output) + suffix
        return destination

    raw_match = RAW_QUERY_RE.match(destination)
    if raw_match:
        return f"https://raw.githubusercontent.com/TanStack/query/{SOURCE_COMMIT}/{raw_match.group('path')}"

    if destination.startswith("http://") or destination.startswith("https://"):
        return convert_blob_or_tree_url_to_commit(destination)

    base, suffix = split_suffix(destination)
    route_relative = resolve_relative_public_route(base, current_output_path, route_to_output)
    if route_relative:
        return relative_link(current_output_path, route_relative) + suffix
    resolved = resolve_relative_source_path(base, current_base_source)
    if is_image and resolved:
        resolved_path = SOURCE_REPO_ROOT / resolved
        if resolved_path.exists() and resolved_path.suffix.lower() in IMAGE_EXTENSIONS:
            return source_url_for_path(resolved) + suffix

    if resolved:
        if resolved in source_only_output_map:
            return relative_link(current_output_path, source_only_output_map[resolved]) + suffix
        if resolved in public_source_output_map:
            return relative_link(current_output_path, public_source_output_map[resolved]) + suffix
        resolved_path = SOURCE_REPO_ROOT / resolved
        if resolved_path.exists() and resolved_path.is_file():
            return f"https://github.com/TanStack/query/blob/{SOURCE_COMMIT}/{resolved}" + suffix
        if resolved_path.exists() and resolved_path.is_dir():
            return f"https://github.com/TanStack/query/tree/{SOURCE_COMMIT}/{resolved}" + suffix

    return destination


def normalize_translated_destination(destination: str) -> str:
    replacements = {
        "인터페이스/": "interfaces/",
        "유형 별칭/": "type-aliases/",
        "type-aliases/": "type-aliases/",
        "변수/": "variables/",
        "함수/": "functions/",
        "기능/": "functions/",
        "가이드/": "guides/",
        " mutation-속성-순서.md": "mutation-property-order.md",
        "mutation-속성-순서.md": "mutation-property-order.md",
        "페이지 매김-queries.md": "paginated-queries.md",
        "종속-queries.md": "dependent-queries.md",
        " migration-from-v5-to-v6.md": "migrate-from-v5-to-v6.md",
    }
    normalized = destination.strip()
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


def resolve_relative_public_route(base_destination: str, current_output_path: str, route_to_output: dict[str, str]) -> str | None:
    if current_output_path.startswith("_source-only/"):
        return None
    current_route = current_output_path[:-3] if current_output_path.endswith(".md") else current_output_path
    candidate_route = posixpath.normpath(posixpath.join(posixpath.dirname(current_route), base_destination))
    candidate_route = candidate_route.lstrip("./")
    if candidate_route in route_to_output:
        return route_to_output[candidate_route]
    if not candidate_route.endswith(".md") and f"{candidate_route}.md" in route_to_output.values():
        return f"{candidate_route}.md"
    return None


def split_suffix(destination: str) -> tuple[str, str]:
    anchor_index = len(destination)
    for symbol in ("#", "?"):
        index = destination.find(symbol)
        if index != -1 and index < anchor_index:
            anchor_index = index
    if anchor_index == len(destination):
        return destination, ""
    return destination[:anchor_index], destination[anchor_index:]


def resolve_relative_source_path(base_destination: str, current_base_source: str | None) -> str | None:
    if not current_base_source:
        return None
    if looks_like_url(base_destination):
        return None
    base_dir = posixpath.dirname(current_base_source)
    candidate = posixpath.normpath(posixpath.join(base_dir, base_destination))
    if candidate.startswith("../"):
        return None
    if candidate.endswith("/"):
        candidate = candidate[:-1]
    if (SOURCE_REPO_ROOT / candidate).exists():
        return candidate
    if not posixpath.splitext(candidate)[1]:
        md_candidate = f"{candidate}.md"
        if (SOURCE_REPO_ROOT / md_candidate).exists():
            return md_candidate
        readme_candidate = posixpath.join(candidate, "README.md")
        if (SOURCE_REPO_ROOT / readme_candidate).exists():
            return readme_candidate
    return None


def relative_link(current_output_path: str, target_output_path: str) -> str:
    current_dir = posixpath.dirname(current_output_path) or "."
    rel = posixpath.relpath(target_output_path, current_dir)
    return rel


def rewrite_markdown_links_and_html(
    text: str,
    *,
    current_output_path: str,
    current_base_source: str | None,
    route_to_output: dict[str, str],
    source_only_output_map: dict[str, str],
    public_source_output_map: dict[str, str],
) -> str:
    def replace_markdown_link(match: re.Match[str]) -> str:
        bang, label, destination = match.groups()
        is_image = bang == "!"
        rewritten = rewrite_destination(
            destination,
            is_image=is_image,
            current_output_path=current_output_path,
            current_base_source=current_base_source,
            route_to_output=route_to_output,
            source_only_output_map=source_only_output_map,
            public_source_output_map=public_source_output_map,
        )
        return f"{bang}[{label}]({rewritten})"

    def replace_html_tag(match: re.Match[str]) -> str:
        tag = match.group(0)

        def replace_attr(attr_match: re.Match[str]) -> str:
            attr = attr_match.group("attr")
            quote = attr_match.group("quote")
            value = attr_match.group("value")
            rewritten = rewrite_destination(
                value,
                is_image=(attr == "src"),
                current_output_path=current_output_path,
                current_base_source=current_base_source,
                route_to_output=route_to_output,
                source_only_output_map=source_only_output_map,
                public_source_output_map=public_source_output_map,
            )
            return f'{attr}={quote}{rewritten}{quote}'

        return HTML_ATTR_RE.sub(replace_attr, tag)

    rewritten = MARKDOWN_LINK_RE.sub(replace_markdown_link, text)
    rewritten = HTML_TAG_RE.sub(replace_html_tag, rewritten)
    return rewritten


def translate_markdown_chunk(
    translator: Translator,
    text: str,
    *,
    current_output_path: str,
    current_base_source: str | None,
    route_to_output: dict[str, str],
    source_only_output_map: dict[str, str],
    public_source_output_map: dict[str, str],
) -> str:
    rewritten = rewrite_markdown_links_and_html(
        text,
        current_output_path=current_output_path,
        current_base_source=current_base_source,
        route_to_output=route_to_output,
        source_only_output_map=source_only_output_map,
        public_source_output_map=public_source_output_map,
    )
    parts = re.split(r"(\n\s*\n)", rewritten)
    translated_parts: list[str] = []
    for part in parts:
        if not part:
            continue
        if re.fullmatch(r"\n\s*\n", part):
            translated_parts.append(part)
            continue
        translated_parts.append(translate_markdown_block(translator, part))
    return "".join(translated_parts)


def translate_markdown_block(translator: Translator, block: str) -> str:
    if not block.strip():
        return block
    if all(MARKDOWN_STRUCTURAL_COMMENT_RE.match(line.rstrip("\r\n") or line) for line in block.splitlines()):
        return block
    if is_table_block(block):
        return translate_table_block(translator, block)
    return translate_prose_fragment(translator, block)


def is_table_block(block: str) -> bool:
    lines = [line for line in block.splitlines() if line.strip()]
    if len(lines) < 2:
        return False
    pipe_lines = sum(1 for line in lines if "|" in line)
    return pipe_lines >= 2 and any(TABLE_SEPARATOR_RE.match(line) for line in lines)


def translate_table_block(translator: Translator, block: str) -> str:
    output_lines: list[str] = []
    for line in block.splitlines(keepends=True):
        raw_line = line.rstrip("\r\n")
        newline = line[len(raw_line) :]
        if TABLE_SEPARATOR_RE.match(raw_line):
            output_lines.append(line)
            continue
        if "|" not in raw_line:
            output_lines.append(translate_prose_fragment(translator, raw_line) + newline)
            continue
        leading_pipe = raw_line.startswith("|")
        trailing_pipe = raw_line.endswith("|")
        cells = raw_line.strip("|").split("|")
        translated_cells = [translate_prose_fragment(translator, cell.strip()) for cell in cells]
        rebuilt = "|".join(translated_cells)
        if leading_pipe:
            rebuilt = "|" + rebuilt
        if trailing_pipe:
            rebuilt = rebuilt + "|"
        output_lines.append(rebuilt + newline)
    return "".join(output_lines)


def translate_prose_fragment(translator: Translator, text: str) -> str:
    if not text or not text.strip():
        return text
    placeholder_map: dict[str, str] = {}

    def stash(value: str) -> str:
        token = f"ZXQPH{len(placeholder_map):04d}QXZ"
        placeholder_map[token] = value
        return token

    protected = MARKDOWN_STRUCTURAL_COMMENT_RE.sub(lambda m: stash(m.group(0)), text)
    protected = INLINE_CODE_RE.sub(lambda m: stash(m.group(0)), protected)
    protected = MARKDOWN_REFERENCE_DEFINITION_RE.sub(lambda m: stash(m.group(0)), protected)
    protected = protect_pattern_matches(protected, MARKDOWN_REFERENCE_ID_RE, placeholder_map)
    protected = protect_markdown_link_labels(protected, placeholder_map)
    protected = protect_pattern_matches(protected, PACKAGE_NAME_RE, placeholder_map)
    protected = protect_pattern_matches(protected, LOWER_CAMEL_IDENTIFIER_RE, placeholder_map)
    protected = protect_pattern_matches(protected, PASCAL_IDENTIFIER_RE, placeholder_map, looks_like_technical_label)
    protected = protect_pattern_matches(protected, TYPE_PARAMETER_RE, placeholder_map)
    protected, term_restore_map = protect_terms(protected, translator.protected_terms)
    translated = translator.translate_text(protected)
    translated = canonicalize_translated_text(translated)
    translated = restore_placeholders(translated, term_restore_map)
    translated = restore_placeholders(translated, placeholder_map)
    return translated


def scan_line_comment_position(line: str, marker: str) -> int | None:
    if not line.strip():
        return None
    quote_state: str | None = None
    escape = False
    index = 0
    while index < len(line):
        char = line[index]
        next_two = line[index : index + 2]
        if escape:
            escape = False
            index += 1
            continue
        if char == "\\":
            escape = True
            index += 1
            continue
        if quote_state:
            if quote_state == char:
                quote_state = None
            elif quote_state == "`" and char == "$" and index + 1 < len(line) and line[index + 1] == "{":
                pass
            index += 1
            continue
        if char in {"'", '"', "`"}:
            quote_state = char
            index += 1
            continue
        if marker == "//" and next_two == "//":
            if index == 0 or line[index - 1] != ":":
                return index
        if marker == "#" and char == "#":
            return index
        index += 1
    return None


def translate_code_content(translator: Translator, code: str, language: str) -> str:
    lines = code.splitlines(keepends=True)
    translated_lines: list[str] = []
    line_marker = "//"
    if language in {"py", "python", "sh", "bash", "zsh", "yaml", "yml", "toml", "rb", "dockerfile"}:
        line_marker = "#"
    if language in {"html", "xml"}:
        line_marker = ""
    for line in lines:
        if line_marker:
            position = scan_line_comment_position(line, line_marker)
            if position is not None:
                comment_text = line[position + len(line_marker) :]
                prefix = line[: position + len(line_marker)]
                newline = ""
                if comment_text.endswith("\r\n"):
                    newline = "\r\n"
                    comment_text = comment_text[:-2]
                elif comment_text.endswith("\n"):
                    newline = "\n"
                    comment_text = comment_text[:-1]
                translated_comment = translate_protected_text(translator, comment_text.strip())
                if comment_text.strip():
                    left_padding = re.match(r"^\s*", comment_text).group(0)
                    translated_lines.append(f"{prefix}{left_padding}{translated_comment}{newline}")
                else:
                    translated_lines.append(line)
                continue
        translated_lines.append(line)
    translated = "".join(translated_lines)
    translated = re.sub(
        r"/\*(.*?)\*/",
        lambda m: f"/* {translate_protected_text(translator, m.group(1).strip())} */" if m.group(1).strip() else m.group(0),
        translated,
        flags=re.DOTALL,
    )
    translated = re.sub(
        r"<!--(.*?)-->",
        lambda m: f"<!-- {translate_protected_text(translator, m.group(1).strip())} -->" if m.group(1).strip() else m.group(0),
        translated,
        flags=re.DOTALL,
    )
    return translated


def translate_markdown_body(
    translator: Translator,
    body: str,
    *,
    current_output_path: str,
    current_base_source: str | None,
    route_to_output: dict[str, str],
    source_only_output_map: dict[str, str],
    public_source_output_map: dict[str, str],
) -> str:
    lines = body.splitlines(keepends=True)
    output_parts: list[str] = []
    buffer: list[str] = []
    in_code_fence = False
    fence = ""
    language = ""
    code_buffer: list[str] = []

    def flush_buffer() -> None:
        if not buffer:
            return
        output_parts.append(
            translate_markdown_chunk(
                translator,
                "".join(buffer),
                current_output_path=current_output_path,
                current_base_source=current_base_source,
                route_to_output=route_to_output,
                source_only_output_map=source_only_output_map,
                public_source_output_map=public_source_output_map,
            )
        )
        buffer.clear()

    for line in lines:
        if not in_code_fence:
            start_match = CODE_FENCE_START_RE.match(line.rstrip("\r\n"))
            if start_match:
                flush_buffer()
                in_code_fence = True
                fence = start_match.group(1)
                language = start_match.group(2).strip().split()[0].lower() if start_match.group(2).strip() else ""
                output_parts.append(line)
                code_buffer = []
            else:
                buffer.append(line)
        else:
            end_pattern = re.compile(CODE_FENCE_END_TEMPLATE.format(fence=re.escape(fence)))
            if end_pattern.match(line.rstrip("\r\n")):
                code_text = "".join(code_buffer)
                output_parts.append(translate_code_content(translator, code_text, language))
                output_parts.append(line)
                in_code_fence = False
                fence = ""
                language = ""
                code_buffer = []
            else:
                code_buffer.append(line)
    flush_buffer()
    return canonicalize_translated_text("".join(output_parts))


def count_headings(text: str) -> int:
    return len(re.findall(r"^#{1,6}\s", text, re.MULTILINE))


def count_code_fences(text: str) -> int:
    return len(re.findall(r"^(```+|~~~+)", text, re.MULTILINE))


def count_table_rows(text: str) -> int:
    return len([line for line in text.splitlines() if "|" in line])


def strip_code_fences(text: str) -> str:
    return re.sub(r"```[\s\S]*?```|~~~[\s\S]*?~~~", "", text)


def has_long_english_paragraph(text: str) -> bool:
    without_code = strip_code_fences(text)
    return bool(re.search(r"(?:\b[A-Za-z][A-Za-z'-]*\b(?:\s+|$)){12,}", without_code))


def collect_internal_links(text: str) -> list[str]:
    links: list[str] = []
    for _, _, destination in MARKDOWN_LINK_RE.findall(text):
        if destination.startswith("http://") or destination.startswith("https://") or destination.startswith("#"):
            continue
        links.append(destination)
    for tag in HTML_TAG_RE.findall(text):
        for attr_match in HTML_ATTR_RE.finditer(tag):
            destination = attr_match.group("value")
            if destination.startswith("http://") or destination.startswith("https://") or destination.startswith("#"):
                continue
            links.append(destination)
    return links


def verify_internal_links(output_path: str, text: str) -> list[str]:
    errors: list[str] = []
    output_file = current_output_absolute(output_path)
    for destination in collect_internal_links(text):
        base, _suffix = split_suffix(destination)
        target = (output_file.parent / base).resolve()
        if not target.exists():
            errors.append(f"broken-link:{destination}")
    return errors


def load_existing_output(output_path: str) -> tuple[dict[str, Any], str, str]:
    output_file = current_output_absolute(output_path)
    parsed = parse_frontmatter(output_file.read_text())
    title_ko = title_from_frontmatter_or_body(parsed.data, parsed.body, posixpath.basename(output_path))
    return parsed.data, parsed.body, title_ko


def fetch_fallback_example_markdown(translator: Translator) -> tuple[str, str]:
    url = "https://tanstack.com/query/latest/docs/framework/react/examples/nextjs-suspense-streaming"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = ""
    delay = REQUEST_DELAY_SECONDS
    for _ in range(MAX_RETRY_COUNT):
        try:
            with urlopen(request, timeout=30) as response:
                html = response.read().decode("utf-8", "replace")
            break
        except (HTTPError, URLError, TimeoutError):
            time.sleep(delay)
            delay *= 2
    if not html:
        raise RuntimeError("Failed to fetch rendered-page fallback example")

    title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    description_match = re.search(
        r'<meta name="description" content="(.*?)"',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    title = unescape(title_match.group(1).strip()) if title_match else "React TanStack Query Nextjs Suspense Streaming Example"
    description = unescape(description_match.group(1).strip()) if description_match else ""

    all_urls = sorted(set(re.findall(r"https://[^\"'<> ]+", html)))
    github_urls = sorted(
        {
            convert_blob_or_tree_url_to_commit(url)
            for url in all_urls
            if "github.com/TanStack/query" in url and "examples/react/nextjs-suspense-streaming" in url
        }
    )
    sandbox_urls = sorted(
        {
            url
            for url in all_urls
            if "codesandbox.io" in url or "stackblitz.com" in url
        }
    )

    repo_root = SOURCE_REPO_ROOT / "examples/react/nextjs-suspense-streaming"
    local_files = sorted(
        str(path.relative_to(SOURCE_REPO_ROOT)).replace(os.sep, "/")
        for path in repo_root.rglob("*")
        if path.is_file()
    )
    lines = [
        f"# {translate_protected_text(translator, 'React Example: Nextjs Suspense Streaming')}",
        "",
    ]
    if description:
        lines.extend([translate_protected_text(translator, description), ""])

    if sandbox_urls or github_urls:
        lines.extend([f"## {translate_protected_text(translator, 'Links')}", ""])
        if github_urls:
            root_link = next((url for url in github_urls if url.endswith("/examples/react/nextjs-suspense-streaming")), None)
            if root_link:
                lines.append(f"- [GitHub]({root_link})")
        for url in sandbox_urls:
            label = "CodeSandbox" if "codesandbox" in url else "StackBlitz"
            lines.append(f"- [{label}]({url})")
        lines.append("")

    if local_files:
        lines.extend([f"## {translate_protected_text(translator, 'Source Files')}", ""])
        for file_path in local_files:
            file_url = f"https://github.com/TanStack/query/blob/{SOURCE_COMMIT}/{file_path}"
            lines.append(f"- [{file_path.removeprefix('examples/react/nextjs-suspense-streaming/')}]({file_url})")
        lines.append("")

    return title, "\n".join(lines).rstrip() + "\n"


def generate_documents() -> tuple[list[OutputDocument], dict[str, Any]]:
    if not SOURCE_REPO_ROOT.exists():
        raise FileNotFoundError(
            f"Upstream source root not found: {SOURCE_REPO_ROOT}. Set TANSTACK_QUERY_SOURCE_ROOT to the cloned TanStack/query repo."
        )

    config = json.loads((SOURCE_REPO_ROOT / "docs/config.json").read_text())
    public_routes = public_routes_from_config(config)
    if len(public_routes) != 362:
        raise RuntimeError(f"Expected 362 public routes, found {len(public_routes)}")

    doc_paths, example_paths = all_source_markdown_paths()
    if len(doc_paths) != 429:
        raise RuntimeError(f"Expected 429 docs markdown files, found {len(doc_paths)}")
    if len(example_paths) != 59:
        raise RuntimeError(f"Expected 59 example README files, found {len(example_paths)}")

    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    META_ROOT.mkdir(parents=True, exist_ok=True)
    cache = TranslationCache(TRANSLATION_CACHE_PATH)
    translator = Translator(cache, build_protected_terms(doc_paths, example_paths))

    route_to_output: dict[str, str] = {}
    public_source_output_map: dict[str, str] = {}
    special_public_docs: list[tuple[dict[str, str], list[str]]] = []
    special_fallback_docs: list[tuple[dict[str, str], list[str]]] = []
    public_outputs: list[tuple[dict[str, str], ResolvedDocument | None, list[str]]] = []
    excluded_source_paths: set[str] = set()

    for route_item in public_routes:
        route = route_item["to"]
        label = route_item["label"]
        output_path = output_path_for_public_route(route)
        route_to_output[route] = output_path
        source_path, source_kind, notes = route_to_source_path(route)
        if source_kind == "rendered-page-fallback":
            special_fallback_docs.append((route_item, notes))
            public_outputs.append((route_item, None, notes))
            continue
        assert source_path is not None
        resolved = resolve_document(source_path, source_kind, label, notes)
        public_outputs.append((route_item, resolved, notes))
        if route != SPECIAL_PUBLIC_ALIAS_ROUTE:
            excluded_source_paths.add(source_path)
            public_source_output_map[source_path] = output_path
        else:
            special_public_docs.append((route_item, notes))

    source_only_paths = sorted(
        [path for path in doc_paths + example_paths if path not in excluded_source_paths]
    )
    if len(source_only_paths) != 128:
        raise RuntimeError(f"Expected 128 source-only paths, found {len(source_only_paths)}")

    source_only_output_map = {
        source_path: output_path_for_source_only(source_path) for source_path in source_only_paths
    }

    manifest_entries: list[OutputDocument] = []
    verification_entries: list[dict[str, Any]] = []
    total_outputs = len(public_outputs) + len(source_only_paths)
    processed_outputs = 0

    for route_item, resolved, notes in public_outputs:
        route = route_item["to"]
        output_path = output_path_for_public_route(route)
        processed_outputs += 1
        print(f"[{processed_outputs}/{total_outputs}] {output_path}", flush=True)
        output_file = current_output_absolute(output_path)
        ensure_parent(output_file)
        if RESUME_EXISTING_OUTPUTS and output_file.exists():
            translated_frontmatter, body_ko, title_ko = load_existing_output(output_path)
            output_text = output_file.read_text()
            if resolved is None:
                title_en = route_item["label"]
                source_url = "https://tanstack.com/query/latest/docs/framework/react/examples/nextjs-suspense-streaming"
                notes_for_manifest = list(notes)
                source_kind = "rendered-page-fallback"
                final_body_en = body_ko
                current_base_source = "examples/react/nextjs-suspense-streaming/README.md"
            else:
                source_url = source_url_for_path(resolved.source_path)
                notes_for_manifest = list(resolved.notes)
                source_kind = resolved.source_kind
                final_body_en = resolved.final_body
                current_base_source = resolved.final_source_path
        elif resolved is None:
            title_en, body_ko = fetch_fallback_example_markdown(translator)
            output_text = body_ko
            title_ko = title_from_frontmatter_or_body({}, body_ko, route_item["label"])
            source_url = url = "https://tanstack.com/query/latest/docs/framework/react/examples/nextjs-suspense-streaming"
            notes_for_manifest = list(notes)
            current_base_source = "examples/react/nextjs-suspense-streaming/README.md"
            source_kind = "rendered-page-fallback"
            final_body_en = body_ko
        else:
            translated_frontmatter = build_output_frontmatter(
                translator,
                resolved.source_frontmatter,
                output_path,
            )
            body_ko = translate_markdown_body(
                translator,
                resolved.final_body,
                current_output_path=output_path,
                current_base_source=resolved.final_source_path,
                route_to_output=route_to_output,
                source_only_output_map=source_only_output_map,
                public_source_output_map=public_source_output_map,
            )
            output_text = dump_frontmatter(translated_frontmatter) + body_ko
            title_ko = title_from_frontmatter_or_body(translated_frontmatter, body_ko, resolved.title_en)
            source_url = source_url_for_path(resolved.source_path)
            notes_for_manifest = list(resolved.notes)
            current_base_source = resolved.final_source_path
            source_kind = resolved.source_kind
            final_body_en = resolved.final_body
        output_file.write_text(output_text)
        manifest_entries.append(
            OutputDocument(
                output_path=output_path,
                source_kind=source_kind,
                source_path=resolved.source_path if resolved else None,
                source_url=source_url,
                source_commit=SOURCE_COMMIT,
                public_route=route,
                title_en=resolved.title_en if resolved else title_en,
                title_ko=title_ko,
                notes=notes_for_manifest,
            )
        )
        verification_entries.append(
            {
                "output_path": output_path,
                "public_route": route,
                "source_path": resolved.source_path if resolved else None,
                "heading_count_en": count_headings(final_body_en) if resolved else None,
                "heading_count_ko": count_headings(body_ko),
                "code_fence_count_en": count_code_fences(final_body_en) if resolved else None,
                "code_fence_count_ko": count_code_fences(body_ko),
                "table_rows_en": count_table_rows(final_body_en) if resolved else None,
                "table_rows_ko": count_table_rows(body_ko),
                "internal_link_errors": verify_internal_links(output_path, output_text),
                "english_paragraph_warning": has_long_english_paragraph(output_text),
                "final_source_path": current_base_source,
            }
        )

    for source_path in source_only_paths:
        source_kind = "example" if source_path.startswith("examples/") else "doc"
        resolved = resolve_document(source_path, source_kind, posixpath.basename(source_path), [])
        output_path = output_path_for_source_only(source_path)
        processed_outputs += 1
        print(f"[{processed_outputs}/{total_outputs}] {output_path}", flush=True)
        output_file = current_output_absolute(output_path)
        ensure_parent(output_file)
        if RESUME_EXISTING_OUTPUTS and output_file.exists():
            translated_frontmatter, body_ko, title_ko = load_existing_output(output_path)
            output_text = output_file.read_text()
        else:
            translated_frontmatter = build_output_frontmatter(
                translator,
                resolved.source_frontmatter,
                output_path,
            )
            body_ko = translate_markdown_body(
                translator,
                resolved.final_body,
                current_output_path=output_path,
                current_base_source=resolved.final_source_path,
                route_to_output=route_to_output,
                source_only_output_map=source_only_output_map,
                public_source_output_map=public_source_output_map,
            )
            output_text = dump_frontmatter(translated_frontmatter) + body_ko
            output_file.write_text(output_text)
            title_ko = title_from_frontmatter_or_body(translated_frontmatter, body_ko, resolved.title_en)
        manifest_entries.append(
            OutputDocument(
                output_path=output_path,
                source_kind=resolved.source_kind,
                source_path=resolved.source_path,
                source_url=source_url_for_path(resolved.source_path),
                source_commit=SOURCE_COMMIT,
                public_route=None,
                title_en=resolved.title_en,
                title_ko=title_ko,
                notes=list(resolved.notes),
            )
        )
        verification_entries.append(
            {
                "output_path": output_path,
                "public_route": None,
                "source_path": resolved.source_path,
                "heading_count_en": count_headings(resolved.final_body),
                "heading_count_ko": count_headings(body_ko),
                "code_fence_count_en": count_code_fences(resolved.final_body),
                "code_fence_count_ko": count_code_fences(body_ko),
                "table_rows_en": count_table_rows(resolved.final_body),
                "table_rows_ko": count_table_rows(body_ko),
                "internal_link_errors": verify_internal_links(output_path, output_text),
                "english_paragraph_warning": has_long_english_paragraph(output_text),
                "final_source_path": resolved.final_source_path,
            }
        )

    cache.flush()

    manifest_entries = sorted(manifest_entries, key=lambda item: item.output_path)
    manifest_payload = [
        {
            "output_path": entry.output_path,
            "source_kind": entry.source_kind,
            "source_path": entry.source_path,
            "source_url": entry.source_url,
            "source_commit": entry.source_commit,
            "public_route": entry.public_route,
            "title_en": entry.title_en,
            "title_ko": entry.title_ko,
            "notes": entry.notes,
        }
        for entry in manifest_entries
    ]
    MANIFEST_PATH.write_text(json.dumps(manifest_payload, ensure_ascii=False, indent=2) + "\n")

    public_count = sum(1 for entry in manifest_entries if entry.public_route)
    source_only_count = sum(1 for entry in manifest_entries if not entry.public_route)
    total_count = len(manifest_entries)

    verification_payload = {
        "public_count": public_count,
        "source_only_count": source_only_count,
        "total_count": total_count,
        "expected_public_count": 362,
        "expected_source_only_count": 128,
        "expected_total_count": 490,
        "entries": verification_entries,
        "special_cases": {
            "hydration_boundary_alias": SPECIAL_PUBLIC_ALIAS_ROUTE,
            "hydration_boundary_source": SPECIAL_PUBLIC_ALIAS_SOURCE,
            "nextjs_suspense_streaming_fallback": SPECIAL_FALLBACK_ROUTE,
        },
    }
    VERIFICATION_REPORT_PATH.write_text(
        json.dumps(verification_payload, ensure_ascii=False, indent=2) + "\n"
    )

    if public_count != 362 or source_only_count != 128 or total_count != 490:
        raise RuntimeError(
            f"Output count mismatch: public={public_count}, source_only={source_only_count}, total={total_count}"
        )

    return manifest_entries, verification_payload


def print_summary(verification_payload: dict[str, Any]) -> None:
    internal_link_errors = sum(
        len(entry["internal_link_errors"]) for entry in verification_payload["entries"]
    )
    english_warnings = sum(
        1 for entry in verification_payload["entries"] if entry["english_paragraph_warning"]
    )
    print(
        json.dumps(
            {
                "public_count": verification_payload["public_count"],
                "source_only_count": verification_payload["source_only_count"],
                "total_count": verification_payload["total_count"],
                "internal_link_errors": internal_link_errors,
                "english_paragraph_warnings": english_warnings,
                "manifest_path": str(MANIFEST_PATH),
                "verification_report_path": str(VERIFICATION_REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> int:
    manifest_entries, verification_payload = generate_documents()
    print_summary(verification_payload)
    return 0 if manifest_entries else 1


if __name__ == "__main__":
    raise SystemExit(main())
