"use client";

import { FileSearch, Search } from "lucide-react";
import Link from "next/link";
import { useDeferredValue, useEffect, useMemo, useRef, useState } from "react";

import { cn } from "@/lib/utils";

type SearchEntry = {
  title: string;
  route: string;
  section: string;
  excerpt: string;
  headings: string[];
  sourceOnly: boolean;
};

function normalize(value: string) {
  return value.toLowerCase().replace(/\s+/gu, " ").trim();
}

export function SearchDialog({ className }: { className?: string }) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [items, setItems] = useState<SearchEntry[]>([]);
  const [loaded, setLoaded] = useState(false);
  const deferredQuery = useDeferredValue(query);

  useEffect(() => {
    if (!open || loaded) {
      return;
    }

    let cancelled = false;

    fetch("/search-index.json")
      .then((response) => response.json())
      .then((data) => {
        if (!cancelled) {
          setItems(data as SearchEntry[]);
          setLoaded(true);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setItems([]);
          setLoaded(true);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [loaded, open]);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      const target = event.target as HTMLElement | null;
      const isEditable =
        target?.tagName === "INPUT" ||
        target?.tagName === "TEXTAREA" ||
        target?.isContentEditable;

      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setOpen((value) => !value);
      }

      if (!isEditable && event.key === "/") {
        event.preventDefault();
        setOpen(true);
      }

      if (event.key === "Escape") {
        setOpen(false);
      }
    }

    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
    };
  }, []);

  useEffect(() => {
    if (!open) {
      return;
    }

    const timer = window.setTimeout(() => {
      inputRef.current?.focus();
    }, 30);

    return () => {
      window.clearTimeout(timer);
    };
  }, [open]);

  const results = useMemo(() => {
    const normalized = normalize(deferredQuery);
    if (!normalized) {
      return items.slice(0, 12);
    }

    return items
      .filter((item) => {
        const haystack = normalize(
          [item.title, item.section, item.route, item.excerpt, item.headings.join(" ")].join(" "),
        );
        return haystack.includes(normalized);
      })
      .slice(0, 24);
  }, [deferredQuery, items]);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className={cn(
          "inline-flex h-10 items-center gap-2 rounded-2xl border border-border/70 bg-surface/80 px-3 text-sm text-muted transition hover:border-accent/60 hover:text-text",
          className,
        )}
      >
        <Search className="h-4 w-4" />
        <span className="hidden sm:inline">문서 검색</span>
        <span className="hidden rounded-full border border-border/70 px-2 py-0.5 text-[11px] sm:inline">
          / or Cmd+K
        </span>
      </button>

      {open ? (
        <div className="fixed inset-0 z-50 flex items-start justify-center bg-slate-950/45 px-4 py-8 backdrop-blur-sm">
          <div className="w-full max-w-3xl overflow-hidden rounded-[2rem] border border-border/70 bg-surface shadow-2xl">
            <div className="flex items-center gap-3 border-b border-border/70 px-5 py-4">
              <Search className="h-5 w-5 text-accent" />
              <input
                ref={inputRef}
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                className="w-full bg-transparent text-base text-text outline-none placeholder:text-muted"
                placeholder="제목, 경로, 본문, 헤딩으로 검색"
              />
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="rounded-full border border-border/70 px-3 py-1 text-xs text-muted"
              >
                ESC
              </button>
            </div>

            <div className="max-h-[70vh] overflow-y-auto p-3">
              {results.length > 0 ? (
                <div className="space-y-2">
                  {results.map((item) => (
                    <Link
                      key={item.route}
                      href={item.route}
                      prefetch={false}
                      className="block rounded-2xl border border-transparent bg-surfaceStrong/70 px-4 py-3 transition hover:border-accent/50 hover:bg-accentSoft/10"
                    >
                      <div className="mb-1 flex flex-wrap items-center gap-2">
                        <span className="font-medium text-text">{item.title}</span>
                        {item.sourceOnly ? (
                          <span className="rounded-full border border-border/70 px-2 py-0.5 text-[11px] text-muted">
                            source-only
                          </span>
                        ) : null}
                      </div>
                      <p className="text-xs font-medium uppercase tracking-[0.18em] text-accent">
                        {item.section}
                      </p>
                      {item.excerpt ? <p className="mt-2 line-clamp-2 text-sm text-muted">{item.excerpt}</p> : null}
                      <p className="mt-2 text-xs text-muted">{item.route}</p>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center gap-3 px-6 py-14 text-center">
                  <FileSearch className="h-8 w-8 text-accent" />
                  <div>
                    <p className="font-medium text-text">일치하는 문서를 찾지 못했습니다.</p>
                    <p className="mt-1 text-sm text-muted">검색어를 조금 더 짧게 쓰거나 API 이름으로 찾아보세요.</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
