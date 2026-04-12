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
분석 제목 재변경 + Explorer 시간순 정렬 + index.md 분석 링크 6건

- 침묵의장치들: 반세기의 침묵 → 누가, 어떻게 입을 막았는가 (Who Silenced Them, and How)
- 기억의정치연대기: 50년의 침묵은 어떻게 깨졌는가 → 어둠에서 빛으로 (From Darkness to Light)
- 왼쪽 Explorer 사이드바에 분석 페이지 시간순 정렬 적용 (quartz.layout.ts sortFn 커스텀)
- 분석 6건 frontmatter에 order 필드 추가 (1-6)
- index.md 둘러보기: 분석 6건 전체 시간순 링크
- aliases에 이전 제목 보존, wikilink display text 갱신

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"

echo ""
echo "=== pushing ==="
git push

echo ""
echo "✅ Done."
