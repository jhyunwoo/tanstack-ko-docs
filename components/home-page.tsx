import { BookOpenText, FileStack, Sparkles } from "lucide-react";
import Link from "next/link";

import { SiteHeader } from "@/components/site-header";
import { getHomeData } from "@/lib/docs";

export function HomePage() {
  const home = getHomeData();

  return (
    <div className="min-h-screen">
      <SiteHeader />
      <div className="mx-auto max-w-[1280px] px-4 pb-16 pt-6 lg:px-6">
        <main className="space-y-8">
          <section className="doc-card overflow-hidden p-8 md:p-10">
            <div className="flex flex-wrap items-start justify-between gap-6">
              <div className="max-w-3xl">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-accent">Static MDX Library</p>
                <h1 className="mt-4 font-display text-4xl font-semibold tracking-tight text-text md:text-5xl">
                  TanStack Query 한국어 문서를 정적 사이트로 탐색하세요.
                </h1>
                <p className="mt-5 max-w-2xl text-base leading-7 text-muted md:text-lg">
                  번역된 490개 문서를 Next.js App Router와 MDX 기반으로 정적 생성해, 빠른 탐색과 검색,
                  라이트/다크 테마, 코드 중심 레이아웃까지 한 번에 제공합니다.
                </p>
              </div>

              <div className="rounded-[1.75rem] border border-border/70 bg-surfaceStrong/75 p-5">
                <p className="text-sm font-medium text-text">문서 규모</p>
                <div className="mt-4 grid grid-cols-3 gap-3 text-center">
                  <div className="rounded-2xl bg-surface px-4 py-3">
                    <p className="text-2xl font-semibold text-text">{home.publicCount}</p>
                    <p className="mt-1 text-xs uppercase tracking-[0.2em] text-muted">Public</p>
                  </div>
                  <div className="rounded-2xl bg-surface px-4 py-3">
                    <p className="text-2xl font-semibold text-text">{home.sourceOnlyCount}</p>
                    <p className="mt-1 text-xs uppercase tracking-[0.2em] text-muted">Source-only</p>
                  </div>
                  <div className="rounded-2xl bg-surface px-4 py-3">
                    <p className="text-2xl font-semibold text-text">{home.totalCount}</p>
                    <p className="mt-1 text-xs uppercase tracking-[0.2em] text-muted">Total</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section className="grid gap-4 md:grid-cols-3">
            {home.topSections.map((item) => (
              <div key={item.label} className="doc-card p-6">
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-accent">{item.label}</p>
                <p className="mt-4 text-3xl font-semibold text-text">{item.count}</p>
                <p className="mt-2 text-sm leading-6 text-muted">
                  {item.label === "Frameworks"
                    ? "React, Angular, Vue, Solid, Svelte, Preact 문서를 프레임워크별로 탐색할 수 있습니다."
                    : item.label === "ESLint"
                      ? "eslint-plugin-query 규칙 문서를 정리한 섹션입니다."
                      : "핵심 API와 타입 문서를 빠르게 훑을 수 있는 참조 섹션입니다."}
                </p>
              </div>
            ))}
          </section>

          <section className="space-y-4">
            <div className="flex items-center gap-3">
              <Sparkles className="h-5 w-5 text-accent" />
              <h2 className="font-display text-2xl font-semibold text-text">프레임워크별 문서</h2>
            </div>

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {home.frameworkCards.map((framework) => (
                <Link
                  key={framework.slug}
                  href={framework.href}
                  prefetch={false}
                  className="doc-card group p-6 transition hover:-translate-y-0.5 hover:border-accent/60"
                >
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="font-display text-xl font-semibold text-text">{framework.label}</p>
                      <p className="mt-1 text-sm text-muted">{framework.docCount} documents</p>
                    </div>
                    <BookOpenText className="h-5 w-5 text-accent transition group-hover:translate-x-0.5" />
                  </div>
                  <p className="mt-4 line-clamp-3 text-sm leading-6 text-muted">{framework.description}</p>
                </Link>
              ))}
            </div>
          </section>

          <section className="doc-card p-6 md:p-8">
            <div className="flex items-start gap-4">
              <FileStack className="mt-1 h-5 w-5 text-accent" />
              <div>
                <h2 className="font-display text-2xl font-semibold text-text">source-only 문서도 포함됩니다</h2>
                <p className="mt-3 text-sm leading-7 text-muted">
                  사이드바에는 노출하지 않지만, 검색 결과와 직접 경로를 통해 번역된 source-only 문서 128개에도
                  접근할 수 있습니다. 원본 추적 정보는 상단의 manifest 링크에서 바로 확인할 수 있습니다.
                </p>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}
