"use client";

import { Check, Copy } from "lucide-react";
import { useState } from "react";
import type { HTMLAttributes, ReactNode } from "react";

import { cn } from "@/lib/utils";

function collectText(node: ReactNode): string {
  if (typeof node === "string" || typeof node === "number") {
    return String(node);
  }

  if (Array.isArray(node)) {
    return node.map((child) => collectText(child)).join("");
  }

  if (node && typeof node === "object" && "props" in node) {
    return collectText((node as { props?: { children?: React.ReactNode } }).props?.children);
  }

  return "";
}

export function CodeBlock({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLPreElement>) {
  const [copied, setCopied] = useState(false);
  const source = collectText(children).trimEnd();

  async function onCopy() {
    try {
      await navigator.clipboard.writeText(source);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1400);
    } catch {
      setCopied(false);
    }
  }

  return (
    <div className="group relative">
      <button
        type="button"
        onClick={onCopy}
        className="absolute right-3 top-3 z-10 inline-flex items-center gap-1 rounded-full border border-border/70 bg-surface/90 px-2.5 py-1 text-xs text-muted opacity-0 transition group-hover:opacity-100"
        aria-label="코드 복사"
      >
        {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
        <span>{copied ? "복사됨" : "복사"}</span>
      </button>
      <pre className={cn("overflow-x-auto", className)} {...props}>
        {children}
      </pre>
    </div>
  );
}
