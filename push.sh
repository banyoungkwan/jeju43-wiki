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
refactor: sources 4분류 재정리 + 파일 병합 + 크로스링크

- sources/를 보고서·1차자료·증언·학술 4개 하위폴더로 재구조화
- references/ 폴더를 sources/로 통합, 삭제
- 재일제주인디아스포라.md → 재일제주인.md로 병합
- jeju43-followup-eng → 추가진상조사보고서 English Section 통합
- HWP_WB_화해와상생 → 화해와상생.md로 통합 (English academic summary 추가)
- 영문 redirect 4개 파일 삭제 (jeju43-report-eng-*)
- 3·1사건 ↔ 3·10총파업 상호 크로스링크 추가
- 3·1사건 aliases에 3·1발포사건, March 1 Shooting Incident 추가
- 각 하위폴더 index.md 생성 (가나다/ABC순 정렬)
- index-internal.md 전면 갱신

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"

echo ""
echo "=== pushing ==="
git push

echo ""
echo "✅ Done."
