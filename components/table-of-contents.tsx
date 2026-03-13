"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import type { TocItem } from "@/lib/docs";
import { cn } from "@/lib/utils";

export function TableOfContents({ items }: { items: TocItem[] }) {
  const [activeId, setActiveId] = useState<string>(items[0]?.id ?? "");

  useEffect(() => {
    if (items.length === 0) {
      return;
    }

    const headings = items
      .map((item) => document.getElementById(item.id))
      .filter((value): value is HTMLElement => Boolean(value));

    if (headings.length === 0) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort(
            (left, right) =>
              (left.target as HTMLElement).offsetTop - (right.target as HTMLElement).offsetTop,
          );

        if (visible[0]) {
          setActiveId(visible[0].target.id);
        }
      },
      {
        rootMargin: "-20% 0px -65% 0px",
        threshold: [0, 1],
      },
    );

    headings.forEach((heading) => observer.observe(heading));

    return () => {
      observer.disconnect();
    };
  }, [items]);

  if (items.length === 0) {
    return null;
  }

  return (
    <div className="sticky top-24 rounded-[1.75rem] border border-border/70 bg-surface/80 p-5 backdrop-blur">
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-accent">On this page</p>
      <nav className="mt-4 space-y-1">
        {items.map((item) => (
          <Link
            key={item.id}
            href={`#${item.id}`}
            className={cn(
              "block rounded-xl px-3 py-2 text-sm transition",
              activeId === item.id
                ? "bg-accentSoft/15 text-text"
                : "text-muted hover:bg-surfaceStrong hover:text-text",
              item.depth === 3 && "pl-5",
              item.depth >= 4 && "pl-7",
            )}
          >
            {item.value}
          </Link>
        ))}
      </nav>
    </div>
  );
}
