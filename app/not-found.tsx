import Link from "next/link";

import { SiteHeader } from "@/components/site-header";

export default function NotFound() {
  return (
    <div className="min-h-screen">
      <SiteHeader />
      <main className="mx-auto flex max-w-3xl flex-col items-center px-4 py-24 text-center sm:px-6">
        <div className="doc-card w-full p-10">
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-accent">404</p>
          <h1 className="mt-4 font-display text-4xl font-semibold text-text">문서를 찾을 수 없습니다.</h1>
          <p className="mt-4 text-base text-muted">
            경로가 잘못되었거나 아직 사이트에 포함되지 않은 문서일 수 있습니다.
          </p>
          <div className="mt-8 flex items-center justify-center gap-3">
            <Link
              href="/"
              className="rounded-2xl bg-accent px-5 py-3 text-sm font-medium text-white transition hover:opacity-90"
            >
              홈으로 이동
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
