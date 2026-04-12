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
fix: Explorer 시대 폴더 정렬 — slugSegment 기준으로 숫자순 정렬

폴더 정렬 시 displayName(한글 제목) 대신 slugSegment(1-해방과미군정 등)를
사용하여 시대순 정렬 보장. 파일은 기존대로 displayName(제목)으로 정렬.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"

echo ""
echo "=== pushing ==="
git push

echo ""
echo "✅ Done."
