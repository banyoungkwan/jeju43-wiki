# Jeju 4·3 Wiki Comprehensive Lint Report

**Date**: 2026-04-11
**Total Files Analyzed**: 175 markdown files
**Project Root**: `/sessions/tender-relaxed-babbage/mnt/jeju43-wiki/content`

---

## EXECUTIVE SUMMARY

| Category | Count | Severity |
|----------|-------|----------|
| Orphan Pages (no backlinks) | 68 | HIGH |
| Broken Wiki Links | 791 | CRITICAL |
| Frontmatter Issues | 55 | MEDIUM |
| Very Short Pages (<10 lines) | 6 | LOW |
| Duplicate Aliases | 21 | MEDIUM |
| Unidirectional Links (asymmetric) | 882 | MEDIUM |

---

## 1. ORPHAN PAGES (68 total)

Pages that have no incoming backlinks and appear isolated from the wiki network.

### Source Files (mostly raw/ingested materials)
Most orphans are **source reference files** in `/wiki/sources/` that link outward but receive no reciprocal links:
- `Ahn-2025-litigation` (6 outward links)
- `ChangJieun-2009-외상기억` (10 outward links)
- `Eperjesi-2019-caves` (7 outward links)
- `Eperjesi-2022-imperialism` (5 outward links)
- `Hauben-1958-peoples-republic` (5 outward links)
- `JungKim-2018-생존자자살` (5 outward links)
- `Kim-2023-economic-impact` (4 outward links)
- `Kim-2025-resistance` (5 outward links)
- `Kim-Jimin-2023-trauma` (5 outward links)
- `KimHunjoon-2009-진실위원회` (7 outward links)
- `Ko-2015-truth-seeking-compliance` (5 outward links)
- `Koh-Barclay-2007-autonomy` (5 outward links)
- `Okada-2015-nation` (4 outward links)
- `Park-2024-archives` (5 outward links)
- `UN-A-HRC-25-49-기념화과정` (9 outward links)
- `UN-A68-296-역사쓰기와교육` (8 outward links)
- `Yon-Kim-2023-red-camellia-design` (6 outward links)
- **28 additional source pages** (mostly Korean-language testimony and papers)

### Entity Pages (should have reciprocal links)
- `문형순` (14 outward links) — Links to many pages but not mentioned by them
- `조병옥` (14 outward links) — Links to many pages but not mentioned by them

### Assets and Ingested Materials
- `70주년-어둠에서빛으로` (0 links) — Raw asset with no metadata
- `AMIK-외교문서` (0 links) — Source collection with no integration
- `HWP_WB_화해와상생` (0 links) — Source file not referenced

### Analysis Pages
- `기억의정치연대기` (56 outward links!) — Highly connected analysis but not cited elsewhere

### Other Issues
- `log` — Appears to be a process log rather than content

**RECOMMENDATION**: Source files are designed to be referenced, so orphanhood is expected. However, entity pages like `문형순` and `조병옥` should have reciprocal links from pages that discuss them. Consider adding "See Also" sections to pages that discuss these individuals.

---

## 2. BROKEN WIKI LINKS (791 total)

### Critical Issue: English/Korean Page Naming Mismatch

Many broken links attempt to reference pages using English translations, but actual pages exist only in Korean or with different naming:

**Examples**:
```
Source: 3·10총파업
  [[3·1발포사건]] → Not found (Korean translation)
  [[4·3사건]] → Not found (use "Jeju 4·3 Incident" or similar)
  [[강순]] → Not found
  [[March 1 Shooting Incident (3·1발포사건)]] → Not found
  [[May 10 Election (5·10선거)]] → Not found
```

### Pattern 1: English-Only Links in Korean Pages
Many pages use English titles in brackets that don't match any existing pages:
- `[[armed uprising]]`
- `[[이승만 정부]]` (partial link)
- `[[분단]]`
- `[[제헌국회]]`
- `[[재판]]`
- `[[피해자성]]`
- `[[법적동원]]`
- `[[생존자증언]]`

### Pattern 2: Malformed Path-like Links
Some links include path prefixes that should not be in wiki links:
```
[[wiki/concepts/초토화작전]]  → Should be [[초토화작전]]
[[wiki/concepts/대반란전-교리]]  → Should be [[대반란전-교리]]
[[wiki/concepts/강제이동-및-수용소]]  → Should be [[강제이동-및-수용소]]
[[wiki/entities/KMAG]]  → Should be [[KMAG]]
[[wiki/entities/9연대]]  → Should be [[9연대]]
[[wiki/events/1948-1949-제주도-작전]]  → Should be [[1948-1949-제주도-작전]]
[[wiki/sources/Merrill-2006-Cheju-rebellion]]  → Should be [[Merrill-2006-Cheju-rebellion]]
```

### Pattern 3: Missing Characters/Punctuation
Some links have escaped characters or unusual punctuation:
- `[[진상조사보고서 \]]` — Extra backslash and bracket
- `[[화해와상생 (사료)]]` — Parenthetical might not match file

### Pattern 4: Link Target Not Found
These targets don't exist as pages, titles, or aliases:
```
Source: 4-3평화공원
  [[화해와상생 (사료)]] — Not found
  [[70주년-어둠에서빛으로 (사료)]] — Not found (stored with different name)

Source: 43은말한다
  [[2·28사건]] — Not found
  [[2003년 진상조사보고서]] — Not found (should be short form?)
  [[2019년 추가진상조사보고서]] — Not found
```

**AFFECTED FILES** (sample of sources with broken links):
- `3·10총파업` (10+ broken links)
- `3·1사건` (multiple broken links)
- `4-3위원회` (malformed links)
- `4-3평화공원` (missing sources)
- `43은말한다` (missing reports)
- `5·10선거` (multiple naming mismatches)
- `Ahn-2025-litigation` (4 broken links)
- `Ban-2023-victim-identification` (reference to wrong park name)
- `Birtle-2006-COIN교리` (10+ path-style broken links)

**TOTAL BROKEN LINKS BY SOURCE**:
- `Birtle-2006-COIN교리`: ~13 broken (path-style links)
- `3·10총파업`: ~10 broken (naming issues)
- `log`: ~7 broken
- `1948-1949-제주도작전`: ~7 broken
- Many others with 1-5 broken links each

---

## 3. FRONTMATTER ISSUES (55 total)

### Issue A: Unquoted YAML Values with Special Characters (44 cases)

The most common issue: YAML values containing colons, brackets, or other special characters are not quoted, which breaks YAML parsing.

**Examples**:
```yaml
title: [사료] 4·3은 말한다 — 《제민일보》 4·3취재반 연재기사 저서
# Should be:
title: "[사료] 4·3은 말한다 — 《제민일보》 4·3취재반 연재기사 저서"

title: [사료] 주한미사절단·주한미대사관 외교문서 — 제주4·3 관련
archive_url: https://archive.jeju43.info  # URL with colon!
# Should be:
archive_url: "https://archive.jeju43.info"

title: Ahn (2025) — Empowering Victimhood Through Litigation: Trials from the Jeju April 3 Uprising
# Should be quoted (contains colon and hyphens)
```

**AFFECTED FILES (sample)**:
- 43은말한다
- AMIK-외교문서
- Ahn-2025-litigation
- Ban-2023-victim-identification
- Eperjesi-2019-caves
- Eperjesi-2022-imperialism
- G2-일일정보보고
- HWP_WB_화해와상생
- KMAG-활동보고
- Kim-2025-resistance
- Kim-Jimin-2023-trauma
- Kim-Seong-nae-기억과애도
- KimHunjoon-2009-진실위원회
- Koh-Barclay-2007-autonomy
- Okada-2015-nation
- UN-A-HRC-25-49-기념화과정
- UN-A-HRC-45-45-기념화와이행기정의
- UN-A68-296-역사쓰기와교육
- jeju43-report-eng-ch2
- jeju43-report-eng-ch3
- jeju43-report-eng-ch4-5
- jeju43-report-eng-preface-ch1
- **32 additional source files with Korean titles**

### Issue B: Missing Required 'title' Field (10 cases)

These files have empty or missing titles:
- `70주년-어둠에서빛으로` (raw asset)
- `ChapterIII_Jeju43Report_ENG` (ingested chapter)
- `ChapterII_Jeju43Report_ENG` (ingested chapter)
- `ChapterIV_V_Appendices_Jeju43Report_ENG` (ingested appendices)
- `GLOSSARY` (reference)
- `log` (process log)
- `PrefaceChapterI_Jeju43Report_ENG` (ingested chapter)

---

## 4. VERY SHORT PAGES (6 total)

Pages with minimal content (< 10 lines excluding frontmatter):

| Page | Lines | Path |
|------|-------|------|
| jeju43-report-eng-ch2 | 1 | `/wiki/sources/jeju43-report-eng-ch2.md` |
| jeju43-report-eng-ch3 | 1 | `/wiki/sources/jeju43-report-eng-ch3.md` |
| jeju43-report-eng-ch4-5 | 1 | `/wiki/sources/jeju43-report-eng-ch4-5.md` |
| jeju43-report-eng-preface-ch1 | 1 | `/wiki/sources/jeju43-report-eng-preface-ch1.md` |
| 김용철-2009-경비대협상 | 1 | `/wiki/sources/김용철-2009-경비대협상.md` |
| HWP_WB_화해와상생 | 5 | `/wiki/sources/HWP_WB_화해와상생.md` |

**Note**: These appear to be skeleton files awaiting content population. The English report chapters likely need their full text ingested.

---

## 5. DUPLICATE ALIASES (21 total)

Multiple pages share the same alias, which breaks the uniqueness guarantee:

```
'2021 증언채록': 
  - 김창후-2021-증언채록
  - 김수열-2021-증언채록

'Eperjesi': 
  - Eperjesi-2019-caves
  - Eperjesi-2022-imperialism

'KMAG': 
  - 박동찬-2011-KMAG
  - KMAG-활동보고
  - KMAG

'Kim': 
  - Kim-2023-economic-impact
  - Yon-Kim-2023-red-camellia-design
  - Kim-2025-resistance

'PMAG': 
  - KMAG-활동보고
  - KMAG

'PTSD': 
  - JungKim-2018-생존자자살
  - 현명호-2011-분노와한용서

'USAMGIK': 
  - Kim-2025-resistance
  - USAMGIK

'Zainichi Jeju': 
  - 재일제주인디아스포라
  - 재일제주인

'Zainichi Korean': 
  - 재일제주인디아스포라
  - Koh-Barclay-2007-autonomy

'preventive detention': 
  - 예비검속
  - 강성현-2014-예비검속

'국가폭력': 
  - 박성호-2023-국가폭력-계엄
  - 허선주-송은경-2020-민족주의국가폭력

'국제점령법': 
  - 이춘선-2017-미군정국제법
  - 안준형-2018-미군정국제법성격

'군사고문단': 
  - 박동찬-2011-KMAG
  - KMAG-활동보고
  - KMAG

'미군정': 
  - 이춘선-2017-미군정국제법
  - 박동찬-2011-KMAG
  - 안준형-2018-미군정국제법성격
  - USAMGIK

'양정심': 
  - 양정심-2017-3ㆍ1기념대회
  - 양정심-기억투쟁과전쟁범죄

'언론담론': 
  - 강창일-2003-언론사적의미
  - 이관열-2003-보도의언론사적의미

'재일동포': 
  - 재일제주인디아스포라
  - 재일제주인

'재일제주인': 
  - 재일제주인디아스포라
  - 문경수-재일디아스포라
  - 무라카미나오코-지영임-2007-재일제주인

'제민일보': 
  - 제민일보-기획3-4ㆍ3은말한다
  - 정용복-최명원-2025-저널리즘기억

'집단기억': 
  - 정근식-기억과다크투어리즘
  - 권귀숙-2001-사회적기억

'한국전쟁': 
  - 박동찬-2011-KMAG
  - 메릴-2004-한국전쟁기원
```

**RECOMMENDATION**: Use more specific aliases (e.g., 'KMAG-Report', 'KMAG-Activities', 'KMAG-Entity' instead of all using 'KMAG').

---

## 6. CROSS-REFERENCE ASYMMETRY (882 unidirectional links - first 20 shown)

When page A links to page B, users expect B to link back (at minimum in a "See Also" or "Referenced by" section).

**Sample unidirectional links**:
```
2연대 → 국가폭력 (not reciprocated)
2연대 → 국가폭력 (duplicate)
2연대 → 서북청년회 (not reciprocated)
2연대 → 서북청년회 (duplicate)
2연대 → 예비검속 (not reciprocated)
3·10총파업 → USAMGIK (not reciprocated, appears 3 times)
3·10총파업 → 국가폭력 (not reciprocated)
3·10총파업 → 남조선노동당 (not reciprocated)
3·10총파업 → 서북청년회 (not reciprocated)
3·10총파업 → 진상규명운동 (not reciprocated)
3·1사건 → 서북청년회 (not reciprocated, appears 3 times)
3·1사건 → 진상조사보고서 (not reciprocated)
3·1사건 → 평화협상 (not reciprocated)
4-3평화공원 → 4-3위원회 (not reciprocated)
4-3평화공원 → 4-3위원회 (duplicate)
4-3평화공원 → 국가폭력 (not reciprocated)
```

This is not necessarily a problem (some references are intentionally one-way), but it's worth auditing key entity pages to ensure they have appropriate reciprocal references.

---

## RECOMMENDATIONS

### Priority 1: Fix Broken Links (CRITICAL)

1. **Fix path-style links** in files like `Birtle-2006-COIN교리`:
   - Replace `[[wiki/concepts/초토화작전]]` with `[[초토화작전]]`
   - Replace `[[wiki/entities/KMAG]]` with `[[KMAG]]`
   - Etc. (affects ~50+ links)

2. **Fix naming mismatches**:
   - Standardize English/Korean link naming (pages should have bilingual aliases if used in both languages)
   - Create missing target pages or add as aliases to existing pages
   - Examples: `[[4·3사건]]` should link to main Jeju 4·3 page

3. **Create missing reference pages**:
   - `2·28사건`, `2003년 진상조사보고서`, `2019년 추가진상조사보고서`
   - `민주주의민족전선`
   - Other frequently referenced but missing pages

### Priority 2: Fix Frontmatter (MEDIUM)

1. **Quote all special values** in YAML:
   ```yaml
   title: "[사료] 4·3은 말한다 — 《제민일보》 4·3취재반 연재기사 저서"
   archive_url: "https://archive.jeju43.info"
   ```

2. **Add missing titles** to:
   - Ingested report chapters (add actual chapter content or summaries)
   - `log.md` (clarify purpose or integrate into workflow)
   - Raw assets

### Priority 3: Populate Stub Pages (MEDIUM)

- Fill in the 6 stub pages with actual content
- Particularly the 4 English report chapter pages

### Priority 4: Rationalize Aliases (MEDIUM)

- Make aliases more specific to avoid collisions
- Examples: `KMAG` → `KMAG (organization)`, `KMAG-Report`, `KMAG-Activities`
- Combine overly broad aliases like `Kim` (used for 3 different people)

### Priority 5: Add Reciprocal Links (LOW)

- Review entity pages (`문형순`, `조병옥`, etc.) and add "Referenced in" or "See Also" sections
- This improves navigation and wiki coherence

### Priority 6: Encoding Issue

- Fix encoding error in `/content/CLAUDE.md`: `'utf-8' codec can't decode byte 0xed`

---

## AFFECTED FILES REFERENCE

### High Priority (Fix Immediately):
- `Birtle-2006-COIN교리` (13 broken path-style links)
- All files with unquoted YAML special chars (44 files)
- Files with missing titles (10 files)
- Short stub pages (6 files)

### Medium Priority:
- All source files with broken links to non-existent pages (~20+ files)
- Files with duplicate aliases (21 files sharing aliases)

### Files to Review for Reciprocal Links:
- `문형순` (14 outward links, 0 incoming)
- `조병옥` (14 outward links, 0 incoming)
- Entity pages in general

