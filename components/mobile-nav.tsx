"use client";

import { PanelLeftClose, PanelLeftOpen } from "lucide-react";
import type { ReactNode } from "react";
import { useState } from "react";

import { cn } from "@/lib/utils";

export function MobileNav({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className={cn(
          "inline-flex h-10 w-10 items-center justify-center rounded-2xl border border-border/70 bg-surface/80 text-muted transition hover:border-accent/60 hover:text-text lg:hidden",
          className,
        )}
        aria-label={open ? "메뉴 닫기" : "메뉴 열기"}
      >
        {open ? <PanelLeftClose className="h-4 w-4" /> : <PanelLeftOpen className="h-4 w-4" />}
      </button>

      {open ? (
        <div className="fixed inset-0 z-50 bg-slate-950/40 backdrop-blur-sm lg:hidden">
          <div className="absolute left-0 top-0 h-full w-[min(22rem,92vw)] border-r border-border/70 bg-surface p-4 shadow-2xl">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-accent">Navigation</p>
                <p className="text-sm text-muted">TanStack Query 한국어 문서</p>
              </div>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="inline-flex h-10 w-10 items-center justify-center rounded-2xl border border-border/70 bg-surfaceStrong text-muted"
                aria-label="메뉴 닫기"
              >
                <PanelLeftClose className="h-4 w-4" />
              </button>
            </div>
            <div className="h-[calc(100%-4rem)] overflow-y-auto pr-1">{children}</div>
          </div>
        </div>
      ) : null}
    </>
  );
}
