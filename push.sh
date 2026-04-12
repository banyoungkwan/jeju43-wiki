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
feat: 시대별 폴더 재구조화 + Explorer 이중언어 토글 + 딘-하지 지휘체계 오류 수정

구조 재편:
- entities/events/concepts → 8개 시대별 폴더 (기억의정치연대기 프레임워크 기반)
- 각 시대 폴더 + analyses 폴더에 index.md 생성 (한/영 제목)
- index.md, index-internal.md 경로 전체 갱신 (86건)

Explorer 이중언어:
- ContentIndex→fileTrie→Explorer 파이프라인에 title_en 추가
- data-lang MutationObserver로 Explorer 사이드바 실시간 언어 전환
- 76개 파일 title/title_en 분리 완료

사실관계 수정 (딘-하지 지휘체계):
- 딘.md: 딘→하지 협의 서술을 하지→딘→브라운 정확한 상하관계로 수정
- 함병선.md: 동일 오류 수정
- 진상조사보고서.md: 원문 보존하되 지휘체계 각주 추가

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"

echo ""
echo "=== pushing ==="
git push

echo ""
echo "✅ Done."
