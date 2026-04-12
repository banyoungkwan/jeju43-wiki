---
title: "신뢰도 체계 / Confidence Rating System"
aliases: [confidence system, 신뢰도, 출처등급, source confidence]
tags: [참조, 메타데이터, 위키관리]
lang: bilingual
type: 참조
created: 2026-04-11
updated: 2026-04-11
---

# 신뢰도 체계 / Confidence Rating System

## 한국어

이 위키는 각 문서의 `confidence` 프론트매터 필드를 통해 정보의 신뢰도를 표시합니다. 이는 제주4·3이 오랫동안 비밀에 부쳐졌던 사건이라는 점, 그리고 사실관계가 출처에 따라 상이할 수 있다는 점을 반영한 체계입니다.

### 등급

| 등급 | 의미 | 기준 |
|------|------|------|
| **confirmed** | 확인됨 | [[진상조사보고서]] 또는 [[추가진상조사보고서]]에서 직접 확인 가능한 사실 |
| **well-sourced** | 다중출처 | 2개 이상의 독립적 학술 자료에서 일치하는 내용 |
| **sourced** | 출처있음 | 1개의 학술 자료 또는 공식 문서에 근거한 내용 |
| **reported** | 보도/증언 | 언론 보도, 개인 증언, 구술 기록 등에 근거한 내용 |
| **contested** | 논쟁중 | 출처 간 사실관계 또는 해석이 상충하는 내용 |
| **unverified** | 미확인 | 출처가 불명확하거나 확인이 필요한 내용 |

### 적용 원칙

1. **진상조사보고서 기준**: 2003년 진상조사보고서와 2019년 추가진상조사보고서를 사실관계의 기준으로 삼음
2. **학술 자료 우선**: 학술 논문과 공식 보고서가 언론 보도보다 높은 신뢰도를 가짐
3. **증언의 가치**: 구술 증언은 `reported` 등급이지만, 역사적으로 대체할 수 없는 가치를 지님
4. **논쟁 기록**: `contested` 등급의 경우 각 입장을 모두 기록하고 출처를 명시

### 프론트매터 사용법

```yaml
confidence: confirmed
confidence_note: "진상조사보고서 제3장에서 직접 확인"
```

---

## English

This wiki uses a `confidence` frontmatter field to indicate how well-sourced each article's content is. This system reflects the fact that the Jeju 4·3 Incident was suppressed for decades and factual claims can vary across sources.

### Ratings

| Rating | Meaning | Criteria |
|--------|---------|----------|
| **confirmed** | Confirmed | Directly verifiable in the [[진상조사보고서\|2003 Truth Report]] or [[추가진상조사보고서\|2019 Supplementary Report]] |
| **well-sourced** | Multi-sourced | Corroborated by 2+ independent academic sources |
| **sourced** | Single source | Based on 1 academic source or official document |
| **reported** | Reported/testified | Based on news reports, personal testimony, or oral history |
| **contested** | Contested | Conflicting facts or interpretations across sources |
| **unverified** | Unverified | Source unclear or verification needed |

### Principles

1. **Truth Report baseline**: The 2003 and 2019 official reports serve as the factual baseline
2. **Academic priority**: Peer-reviewed research and official reports rank above news coverage
3. **Testimony value**: Oral testimony is rated `reported` but holds irreplaceable historical value
4. **Recording disputes**: `contested` items must record all positions with cited sources

## 관련 항목 / See Also

- [[진상조사보고서]] — Primary factual baseline
- [[추가진상조사보고서]] — Supplementary factual baseline
- [[참고문헌]] — Bibliography
