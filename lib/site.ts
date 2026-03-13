export const siteConfig = {
  name: "TanStack Query 한국어 문서",
  shortName: "TanStack Query KO",
  title: "TanStack Query 한국어 문서",
  description:
    "TanStack Query 번역본 490개를 검색, 정적 생성, 라이트/다크 테마와 함께 탐색할 수 있는 한국어 문서 아카이브입니다.",
  defaultOgImage: "/opengraph-image.svg",
  locale: "ko_KR",
  language: "ko-KR",
  keywords: [
    "TanStack Query",
    "React Query",
    "한국어 문서",
    "TanStack Query 번역",
    "MDX docs",
    "프론트엔드 문서",
  ],
};

export function getSiteUrl() {
  const value = process.env.NEXT_PUBLIC_SITE_URL?.trim();
  if (!value) {
    return "https://tanstack-query-docs-ko.vercel.app";
  }

  return value.endsWith("/") ? value.slice(0, -1) : value;
}

export function withTrailingSlash(pathname: string) {
  if (pathname === "/") {
    return "/";
  }

  if (/\.[a-z0-9]+$/iu.test(pathname)) {
    return pathname;
  }

  return pathname.endsWith("/") ? pathname : `${pathname}/`;
}

export function toAbsoluteUrl(pathname: string) {
  return `${getSiteUrl()}${withTrailingSlash(pathname)}`;
}
