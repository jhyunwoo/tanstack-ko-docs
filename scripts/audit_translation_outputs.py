#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = REPO_ROOT / "ko"
REPORT_PATH = OUTPUT_ROOT / "_meta" / "accuracy-audit.json"


@dataclass(frozen=True)
class SuspiciousPattern:
    key: str
    description: str
    regex: re.Pattern[str]


SUSPICIOUS_PATTERNS = [
    SuspiciousPattern(
        key="react_verb_translation",
        description="React가 동사처럼 잘못 번역된 흔적",
        regex=re.compile(r"반응하다"),
    ),
    SuspiciousPattern(
        key="create_svelte_translation",
        description="create-svelte 고유명이 직역된 흔적",
        regex=re.compile(r"날씬한 만들기"),
    ),
    SuspiciousPattern(
        key="route_change_translation",
        description="Route Change가 잘못 번역된 흔적",
        regex=re.compile(r"노선변경"),
    ),
    SuspiciousPattern(
        key="call_signature_translation",
        description="Call Signature가 잘못 번역된 흔적",
        regex=re.compile(r"통화 서명"),
    ),
    SuspiciousPattern(
        key="returns_translation",
        description="Returns가 반품으로 번역된 흔적",
        regex=re.compile(r"반품"),
    ),
    SuspiciousPattern(
        key="type_parameters_translation",
        description="Type Parameters가 유형 매개변수로 번역된 흔적",
        regex=re.compile(r"유형 매개변수"),
    ),
    SuspiciousPattern(
        key="translated_query_identifiers",
        description="query/mutation 계열 식별자가 한국어로 변형된 흔적",
        regex=re.compile(
            r"무한쿼리옵션|쿼리옵션|돌연변이옵션|쿼리결과|쿼리클라이언트|쿼리오류리셋경계|"
            r"쿼리클라이언트 제공자|질의옵션|질의결과"
        ),
    ),
    SuspiciousPattern(
        key="mixed_language_identifier",
        description="식별자 일부만 한국어로 바뀐 혼합형 토큰",
        regex=re.compile(r"[가-힣]+[A-Za-z][A-Za-z0-9]*|[A-Za-z][A-Za-z0-9]*[가-힣]+"),
    ),
    SuspiciousPattern(
        key="translated_reference_heading",
        description="reference 문서 heading의 식별자가 한국어로 바뀐 흔적",
        regex=re.compile(r"^#+\s+(?:함수|인터페이스|타입 별칭|변수):\s*[가-힣][^(\n]*", re.MULTILINE),
    ),
    SuspiciousPattern(
        key="translated_is_restoring",
        description="isRestoring 계열 용어가 번역된 흔적",
        regex=re.compile(r"복원 중"),
    ),
]


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def line_excerpt(text: str, offset: int) -> str:
    line_start = text.rfind("\n", 0, offset) + 1
    line_end = text.find("\n", offset)
    if line_end == -1:
        line_end = len(text)
    return text[line_start:line_end].strip()


def scan_file(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    findings: list[dict[str, object]] = []
    for pattern in SUSPICIOUS_PATTERNS:
        for match in pattern.regex.finditer(text):
            findings.append(
                {
                    "pattern": pattern.key,
                    "description": pattern.description,
                    "line": line_number_for_offset(text, match.start()),
                    "match": match.group(0),
                    "excerpt": line_excerpt(text, match.start()),
                }
            )
    return findings


def build_report() -> dict[str, object]:
    files = markdown_files(OUTPUT_ROOT)
    matches_by_file: dict[str, list[dict[str, object]]] = {}
    summary = {
        pattern.key: {
            "description": pattern.description,
            "count": 0,
            "files": 0,
        }
        for pattern in SUSPICIOUS_PATTERNS
    }

    for path in files:
        findings = scan_file(path)
        if not findings:
            continue
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        matches_by_file[rel_path] = findings
        seen_patterns = set()
        for finding in findings:
            pattern_key = str(finding["pattern"])
            summary[pattern_key]["count"] += 1
            seen_patterns.add(pattern_key)
        for pattern_key in seen_patterns:
            summary[pattern_key]["files"] += 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "output_root": OUTPUT_ROOT.as_posix(),
        "report_path": REPORT_PATH.as_posix(),
        "file_count": len(files),
        "files_with_matches": len(matches_by_file),
        "summary_by_pattern": summary,
        "matches_by_file": matches_by_file,
    }


def main() -> None:
    if not OUTPUT_ROOT.exists():
        raise FileNotFoundError(f"Output root not found: {OUTPUT_ROOT}")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH} ({report['files_with_matches']} files with suspicious matches)")


if __name__ == "__main__":
    main()
