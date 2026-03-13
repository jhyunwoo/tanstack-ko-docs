#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

import translate_tanstack_query as ttq


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "ko"
MANIFEST_PATH = OUTPUT_ROOT / "_meta" / "translation-manifest.json"

EXACT_HEADING_MAP = {
    "Call Signature": "호출 시그니처",
    "Type Parameters": "타입 매개변수",
    "Parameters": "매개변수",
    "Returns": "반환값",
    "See": "참고",
    "Deprecated": "더 이상 사용되지 않음",
    "Type Aliases": "타입 별칭",
    "Variables": "변수",
    "Functions": "함수",
    "References": "참조",
    "Notes": "참고 사항",
}

PREFIX_HEADING_MAP = {
    "Function: ": "함수: ",
    "Type Alias: ": "타입 별칭: ",
    "Interface: ": "인터페이스: ",
    "Variable: ": "변수: ",
    "Class: ": "클래스: ",
}

GLOBAL_STRING_REPLACEMENTS = [
    ("b lob", "blob"),
    ("/ blob/", "/blob/"),
    ("정의: [패키지/", "정의 위치: [packages/"),
    ("정의: [패키지", "정의 위치: [packages"),
    ("패키지/", "packages/"),
    ("통화 서명", "호출 시그니처"),
    ("유형 매개변수", "타입 매개변수"),
    ("반품", "반환값"),
    ("기능:", "함수:"),
    ("유형 별칭", "타입 별칭"),
    ("참고자료", "참조"),
    ("반응 라우터 예", "React Router 예제"),
    ("날씬한 만들기", "create-svelte"),
    ("반응 라우터", "React Router"),
    ("반응하다", "React"),
    ("리덕스", "Redux"),
    ("아폴로 클라이언트", "Apollo Client"),
    ("아폴로", "Apollo"),
    ("스타-아폴로", "stars-apollo"),
    ("gh-아폴로", "gh-apollo"),
    ("rtk-query-비교", "rtk-query-comparison"),
    ("bpl-역사", "bpl-history"),
    ("노선변경", "라우트 변경"),
    ("약속", "Promise"),
    ("재검증하는 동안 유효하지 않음", "Stale While Revalidate"),
    ("T오류", "TError"),
    ("T데이터", "TData"),
    ("읽기 전용", "readonly"),
    ("*확장*", "*extends*"),
    ("*연장*", "*extends*"),
    ("부울", "boolean"),
]

GLOBAL_REGEX_REPLACEMENTS = [
    (re.compile(r"\(<([^>]+)>\)"), r"(\1)"),
    (re.compile(r"(?m)^(#+)\s+보다\s*$"), r"\1 참고"),
    (re.compile(r"(?m)^정의:\s+"), "정의 위치: "),
]

COMPARISON_STRING_REPLACEMENTS = [
    ("Apollo 클라이언트", "Apollo Client"),
    ("|React Query|SWR [_(웹사이트)_][swr]|Apollo Client [_(웹사이트)_][apollo]|RTK-Query [_(웹사이트)_][rtk-query]|React Router [_(웹사이트)_][react-router]|",
     "|React Query|SWR [_(웹사이트)_][swr]|Apollo Client [_(웹사이트)_][apollo]|RTK Query [_(웹사이트)_][rtk-query]|React Router [_(웹사이트)_][react-router]|"),
    ("|Github 레포 / 별|", "|GitHub 레포 / 별|"),
    ("|플랫폼 요구 사항|React|React|리액트, GraphQL|Redux|React|", "|플랫폼 요구 사항|React|React|React, GraphQL|Redux|React|"),
    ("|그들의 비교||", "|자체 비교 문서||"),
    ("|지원되는 Query 구문|Promise, REST, GraphQL|Promise, REST, GraphQL|GraphQL, Any(반응형 변수)|Promise, REST, GraphQL|Promise, REST, GraphQL|",
     "|지원되는 Query 문법|Promise, REST, GraphQL|Promise, REST, GraphQL|GraphQL, Any (Reactive Variables)|Promise, REST, GraphQL|Promise, REST, GraphQL|"),
    ("|지원되는 프레임워크|React|React|React + 기타|어느|React|", "|지원되는 프레임워크|React|React|React + 기타|Any|React|"),
    ("|지원되는 프레임워크|React|React|반응 + 기타|어느|React|", "|지원되는 프레임워크|React|React|React + 기타|Any|React|"),
    ("|캐싱 전략|계층적 키 -> 값|고유 키 -> 값|정규화된 스키마|고유 키 -> 값|중첩 경로 -> 값|",
     "|캐싱 전략|계층적 키 -> 값|고유 키 -> 값|정규화된 스키마|고유 키 -> 값|중첩 라우트 -> 값|"),
    ("|캐시 키 전략|JSON|JSON|GraphQL Query|JSON|경로 경로|", "|캐시 키 전략|JSON|JSON|GraphQL Query|JSON|라우트 경로|"),
    ("|캐시 변경 감지|심층 비교 키(안정적인 직렬화)|심층 비교 키(안정적인 직렬화)|심층 비교 키(불안정한 직렬화)|주요 참조 동등성(===)|라우트 변경|",
     "|캐시 변경 감지|심층 비교 키(안정적인 직렬화)|심층 비교 키(안정적인 직렬화)|심층 비교 키(불안정한 직렬화)|키 참조 동일성(===)|라우트 변경|"),
    ("|데이터 변경 감지|심층 비교 + 구조적 공유|심층 비교(`stable-hash`를 통해)|심층 비교(불안정한 직렬화)|주요 참조 동등성(===)|로더 실행|",
     "|데이터 변경 감지|심층 비교 + 구조적 공유|심층 비교 (`stable-hash` 사용)|심층 비교(불안정한 직렬화)|키 참조 동일성(===)|로더 실행|"),
    ("|데이터 메모화|전체 구조 공유|신원(===)|정규화된 정체성|신원(===)|신원(===)|",
     "|데이터 메모화|완전한 구조적 공유|동일성(===)|정규화된 동일성|동일성(===)|동일성(===)|"),
    ("|API 정의 위치|구성 요소, 외부 구성|요소|GraphQL 스키마|외부 구성|경로 트리 구성|",
     "|API 정의 위치|컴포넌트, 외부 설정|컴포넌트|GraphQL 스키마|외부 설정|라우트 트리 설정|"),
    ("|재검증하는 동안 유효하지 않음|", "|Stale While Revalidate|"),
    ("|오래된 시간 구성|", "|staleTime 설정|"),
    ("|창 포커스 다시 가져오기|", "|윈도우 포커스 시 refetch|"),
    ("|네트워크 상태 다시 가져오는 중|", "|네트워크 상태 변경 시 refetch|"),
    ("|반응 Suspense|", "|React Suspense|"),
    ("[Apollo]:", "[apollo]:"),
    ("[gh-Apollo]:", "[gh-apollo]:"),
    ("[stars-Apollo]:", "[stars-apollo]:"),
    ("[스타-Apollo]:", "[stars-apollo]:"),
    ("[React Router]:", "[react-router]:"),
    ("[![][스타-Apollo]][gh-Apollo]", "[![][stars-apollo]][gh-apollo]"),
    ("[![][bp-Apollo]][bpl-Apollo]", "[![][bp-apollo]][bpl-apollo]"),
    ("[bp-Apollo]:", "[bp-apollo]:"),
    ("[bpl-Apollo]:", "[bpl-apollo]:"),
]


def load_manifest() -> list[dict[str, object]]:
    return json.loads(MANIFEST_PATH.read_text())


def should_preserve_title(entry: dict[str, object]) -> bool:
    title_en = str(entry["title_en"])
    output_path = str(entry["output_path"])
    return ttq.should_preserve_title_english(title_en, output_path) or ttq.looks_like_technical_label(title_en)


def translated_heading_text(source_heading: str) -> str | None:
    stripped = source_heading.strip()
    wrapper_prefix = ""
    wrapper_suffix = ""
    if stripped.startswith("~~") and stripped.endswith("~~") and len(stripped) > 4:
        wrapper_prefix = "~~"
        wrapper_suffix = "~~"
        stripped = stripped[2:-2].strip()
    optional_suffix = ""
    if stripped.endswith("?"):
        optional_suffix = "?"
        stripped = stripped[:-1]
    if stripped in EXACT_HEADING_MAP:
        return wrapper_prefix + EXACT_HEADING_MAP[stripped] + optional_suffix + wrapper_suffix
    for prefix, replacement in PREFIX_HEADING_MAP.items():
        if stripped.startswith(prefix):
            return wrapper_prefix + replacement + stripped[len(prefix) :] + optional_suffix + wrapper_suffix
    if ttq.looks_like_technical_label(stripped):
        return wrapper_prefix + stripped + optional_suffix + wrapper_suffix
    return None


@lru_cache(maxsize=None)
def source_headings_for(entry_key: str) -> list[str]:
    entries = load_manifest()
    entry = next(item for item in entries if item["output_path"] == entry_key)
    source_path = entry.get("source_path")
    if not isinstance(source_path, str) or not source_path:
        return []
    source_kind = str(entry["source_kind"])
    if source_kind == "rendered-page-fallback":
        return []
    resolved = ttq.resolve_document(source_path, source_kind, str(entry["title_en"]), list(entry.get("notes") or []))
    return [match.group(2).strip() for match in re.finditer(r"^(#{1,6})\s+(.+?)\s*$", resolved.final_body, re.MULTILINE)]


def rewrite_headings_from_source(text: str, output_path: str) -> str:
    source_headings = source_headings_for(output_path)
    if not source_headings:
        return text
    updated_lines: list[str] = []
    heading_index = 0
    for line in text.splitlines(keepends=True):
        match = re.match(r"^(#{1,6})\s+(.+?)(\r?\n)?$", line)
        if not match:
            updated_lines.append(line)
            continue
        hashes, _current, newline = match.groups()
        desired = None
        if heading_index < len(source_headings):
            desired = translated_heading_text(source_headings[heading_index])
        heading_index += 1
        if desired is None:
            updated_lines.append(line)
            continue
        updated_lines.append(f"{hashes} {desired}{newline or ''}")
    return "".join(updated_lines)


def resolve_internal_target(current_output_path: str, destination: str) -> str | None:
    base, _suffix = ttq.split_suffix(destination)
    if not base or base.startswith("#") or base.startswith("http://") or base.startswith("https://"):
        return None
    target = ((OUTPUT_ROOT / current_output_path).parent / base).resolve()
    try:
        return target.relative_to(OUTPUT_ROOT.resolve()).as_posix()
    except ValueError:
        return None


def rewrite_internal_link_labels(text: str, output_path: str, preserved_titles: dict[str, str]) -> str:
    def replace_link(match: re.Match[str]) -> str:
        bang, label, destination = match.groups()
        if bang == "!" or not label or "][" in label:
            return match.group(0)
        target_output = resolve_internal_target(output_path, destination)
        if target_output is None:
            return match.group(0)
        desired = preserved_titles.get(target_output)
        if not desired:
            return match.group(0)
        return f"{bang}[{desired}]({destination})"

    return ttq.MARKDOWN_LINK_RE.sub(replace_link, text)


def apply_global_fixes(text: str) -> str:
    updated = text
    for old, new in GLOBAL_STRING_REPLACEMENTS:
        updated = updated.replace(old, new)
    for pattern, replacement in GLOBAL_REGEX_REPLACEMENTS:
        updated = pattern.sub(replacement, updated)
    return updated


def apply_special_case_fixes(text: str, output_path: str) -> str:
    if output_path == "framework/react/comparison.md":
        updated = text
        for old, new in COMPARISON_STRING_REPLACEMENTS:
            updated = updated.replace(old, new)
        return updated
    return text


def main() -> int:
    entries = load_manifest()
    preserved_titles = {
        str(entry["output_path"]): str(entry["title_en"])
        for entry in entries
        if should_preserve_title(entry)
    }

    changed_files = 0
    for entry in entries:
        output_path = str(entry["output_path"])
        file_path = OUTPUT_ROOT / output_path
        original = file_path.read_text()
        updated = apply_global_fixes(original)
        updated = rewrite_headings_from_source(updated, output_path)
        updated = rewrite_internal_link_labels(updated, output_path, preserved_titles)
        updated = apply_special_case_fixes(updated, output_path)
        if updated != original:
            file_path.write_text(updated)
            changed_files += 1

    print(json.dumps({"changed_files": changed_files}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
