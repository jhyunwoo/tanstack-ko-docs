import Link from "next/link";

import type { SidebarSection, SidebarNode } from "@/lib/docs";
import { cn } from "@/lib/utils";

function nodeContainsRoute(node: SidebarNode, currentRoute: string): boolean {
  if (node.href === currentRoute) {
    return true;
  }

  return node.items?.some((child) => nodeContainsRoute(child, currentRoute)) ?? false;
}

function SidebarItem({
  node,
  currentRoute,
  depth = 0,
}: {
  node: SidebarNode;
  currentRoute: string;
  depth?: number;
}) {
  if (node.items && node.items.length > 0) {
    const isOpen = nodeContainsRoute(node, currentRoute);
    return (
      <details open={isOpen} className="group">
        <summary className="cursor-pointer list-none rounded-xl px-3 py-2 text-sm font-medium text-text transition hover:bg-surfaceStrong">
          {node.href ? (
            <Link
              href={node.href}
              prefetch={false}
              className={cn(
                "inline-flex rounded-md transition hover:text-accent",
                depth > 0 && "pl-2",
                node.href === currentRoute && "text-accent",
              )}
            >
              {node.label}
            </Link>
          ) : (
            <span className={depth > 0 ? "pl-2" : ""}>{node.label}</span>
          )}
        </summary>
        <div className="mt-1 space-y-1 border-l border-border/50 pl-3">
          {node.items.map((child) => (
            <SidebarItem key={child.key} node={child} currentRoute={currentRoute} depth={depth + 1} />
          ))}
        </div>
      </details>
    );
  }

  return (
    <Link
      href={node.href ?? "/"}
      prefetch={false}
      className={cn(
        "block rounded-xl px-3 py-2 text-sm transition",
        node.href === currentRoute
          ? "bg-accentSoft/15 text-text"
          : "text-muted hover:bg-surfaceStrong hover:text-text",
        depth > 0 && "ml-1",
      )}
    >
      {node.label}
    </Link>
  );
}

export function Sidebar({
  sections,
  currentRoute,
}: {
  sections: SidebarSection[];
  currentRoute: string;
}) {
  return (
    <nav className="space-y-6">
      {sections.map((section) => (
        <section key={section.key}>
          <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-[0.22em] text-accent">
            {section.label}
          </p>
          <div className="space-y-1">
            {section.items.map((item) => (
              <SidebarItem key={item.key} node={item} currentRoute={currentRoute} />
            ))}
          </div>
        </section>
      ))}
    </nav>
  );
}
