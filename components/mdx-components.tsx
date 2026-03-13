/* eslint-disable @next/next/no-img-element */

import type { ComponentPropsWithoutRef } from "react";
import Link from "next/link";

import { CodeBlock } from "@/components/code-block";
import { cn } from "@/lib/utils";

function SmartAnchor({
  href = "",
  className,
  ...props
}: ComponentPropsWithoutRef<"a">) {
  if (href.startsWith("/")) {
    return <Link href={href} prefetch={false} className={className} {...props} />;
  }

  if (href.startsWith("#")) {
    return <a href={href} className={className} {...props} />;
  }

  return <a href={href} className={className} target="_blank" rel="noopener noreferrer" {...props} />;
}

function ResponsiveImage({ className, alt = "", ...props }: ComponentPropsWithoutRef<"img">) {
  return (
    <img
      alt={alt}
      decoding="async"
      loading="lazy"
      referrerPolicy="no-referrer"
      className={cn("h-auto max-w-full rounded-2xl border border-border/60", className)}
      {...props}
    />
  );
}

function ResponsiveTable({ className, ...props }: ComponentPropsWithoutRef<"table">) {
  return (
    <div className="my-6 overflow-x-auto rounded-2xl border border-border/70 bg-surfaceStrong/60">
      <table className={cn("w-full border-collapse text-sm", className)} {...props} />
    </div>
  );
}

export const mdxComponents = {
  a: SmartAnchor,
  img: ResponsiveImage,
  pre: CodeBlock,
  table: ResponsiveTable,
  code: ({ className, ...props }: ComponentPropsWithoutRef<"code">) => (
    <code
      className={cn(
        "rounded-md bg-surfaceStrong/80 px-1.5 py-0.5 font-medium text-[0.95em] text-text",
        className,
      )}
      {...props}
    />
  ),
};
