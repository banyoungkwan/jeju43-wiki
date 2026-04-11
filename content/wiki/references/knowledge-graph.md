---
title: "지식 그래프 / Knowledge Graph"
aliases: [knowledge graph, 지식그래프, 네트워크 시각화]
tags: [참조, 메타데이터, 시각화]
lang: bilingual
type: 참조
created: 2026-04-11
updated: 2026-04-11
---

# 지식 그래프 / Knowledge Graph

제주4·3 위키의 인물, 사건, 개념, 조직 페이지 간의 연결을 시각화한 인터랙티브 그래프입니다.

An interactive visualization of connections between people, events, concepts, and organizations in the Jeju 4·3 Knowledge Base.

[**→ 그래프 보기 / View Graph**](./knowledge-graph.html)

## 통계 / Statistics

| 항목 | 값 |
|------|-----|
| 노드 수 / Nodes | 67 |
| 연결 수 / Connections | 589 |
| 생성일 / Generated | 2026-04-11 |

## 연결 방식 / Connection Methods

이 그래프는 4가지 방식으로 페이지 간 연결을 탐지합니다:

1. **위키 링크**: `[[페이지]]` 형태의 명시적 링크 (가중치 3)
2. **공유 태그**: 의미있는 태그를 공유하는 페이지 (가중치 1)
3. **공동인용**: 같은 소스 문서에서 함께 언급되는 페이지 (가중치 2)
4. **텍스트 언급**: 본문에서 다른 페이지의 제목/별칭이 언급되는 경우 (가중치 1)

가중치 2 이상의 연결만 표시됩니다.

## 사용법 / Usage

```bash
cd jeju43-wiki
python3 tools/graph.py              # 기본 (소스 제외)
python3 tools/graph.py --include-sources  # 소스 포함
```

## 관련 항목 / See Also

- [[참고문헌]] — Bibliography
- [[confidence-system]] — Confidence rating system
