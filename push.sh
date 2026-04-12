#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== git status ==="
git status --short

echo ""
echo "=== staging all changes ==="
git add -A

echo ""
echo "=== committing ==="
git commit -m "$(cat <<'EOF'
분석 페이지 제목 저널리스트 스타일 변경 + UI 개선 (언어 토글, 지식 그래프)

콘텐츠
- 분석 6건 제목 변경: 추상적 학술 제목 → 직관적 저널리스트 스타일
  책임구조분석 → 제주4·3의 지휘 체계 (The Chain of Command)
  폭력의시간 → 학살은 한 번으로 끝나지 않았다 (The Killing Did Not End Once)
  공간과기억 → 사라진 마을 122곳, 지워진 지도 (122 Villages Erased, a Map Redrawn)
  침묵의장치들 → 반세기의 침묵 (Half a Century of Silence)
  기억의정치연대기 → 50년의 침묵은 어떻게 깨졌는가 (How Fifty Years of Silence Were Broken)
  정명과화해 → 4·3 정명, 그리고 화해 (Naming 4·3, and Reconciliation)
- frontmatter title/title_en, H1(한/영), aliases, 내부 wikilink display text 일괄 갱신
- index-internal.md: Analyses 섹션 시간순 재배치
- index-internal.md: Entities/Events/Concepts → 시대별 통합 카탈로그 (8개 시기, 65건)
- 할루시네이션 수정: 조병옥(placeholder URL), 오용국(무출처 주장), 연좌제(TRC 날조·종교 역전·미검증 인용), 함병선(피해자수 불일치)

UI
- LanguageToggle 컴포넌트 신규: 한/EN 토글 버튼 (왼쪽 사이드바)
  이중언어 페이지에서 ## 한국어 / ## English 섹션을 동적 래핑 후 CSS show/hide
  언어 선택 localStorage 저장, Quartz SPA nav 이벤트 대응
  비이중언어 페이지에서는 버튼 자동 숨김
- index.md: 지식 그래프 iframe 전면 배치 (72노드 774연결)
- .gitignore: quartz/.quartz-cache/, tsconfig.tsbuildinfo 추가

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"

echo ""
echo "=== pushing ==="
git push

echo ""
echo "✅ Done."
