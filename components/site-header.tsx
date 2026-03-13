import { Braces, Github, ScrollText } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";

import { MobileNav } from "@/components/mobile-nav";
import { SearchDialog } from "@/components/search-dialog";
import { ThemeToggle } from "@/components/theme-toggle";

export function SiteHeader({ sidebar }: { sidebar?: ReactNode }) {
  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-bg/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-[1600px] items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          {sidebar ? <MobileNav>{sidebar}</MobileNav> : null}
          <Link href="/" className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-accent text-white shadow-glow">
              <Braces className="h-5 w-5" />
            </div>
            <div>
              <p className="font-display text-[0.92rem] font-semibold tracking-[0.2em] text-accent">
                TANSTACK QUERY
              </p>
              <p className="text-sm text-muted">한국어 문서 아카이브</p>
            </div>
          </Link>
        </div>

        <div className="flex items-center gap-2">
          <SearchDialog />
          <Link
            href="/translation-manifest.json"
            className="hidden h-10 items-center gap-2 rounded-2xl border border-border/70 bg-surface/80 px-3 text-sm text-muted transition hover:border-accent/60 hover:text-text md:inline-flex"
          >
            <ScrollText className="h-4 w-4" />
            Manifest
          </Link>
          <a
            href="https://github.com/TanStack/query"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden h-10 items-center gap-2 rounded-2xl border border-border/70 bg-surface/80 px-3 text-sm text-muted transition hover:border-accent/60 hover:text-text md:inline-flex"
          >
            <Github className="h-4 w-4" />
            GitHub
          </a>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
