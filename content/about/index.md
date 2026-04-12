---
title: "이 위키에 대해"
title_en: "About This Wiki"
aliases: [about, 위키소개]
tags: [메타, 위키관리]
lang: bilingual
---

## 프로젝트 소개 / Project Overview

이 위키는 제주4·3사건에 관한 이중언어(한/영) 지식 베이스입니다. [Andrej Karpathy의 LLM Wiki 아이디어](https://x.com/karpathy/status/2039805659525644595)를 바탕으로, 대규모 언어 모델(LLM)을 활용하여 다양한 1차·2차 자료를 체계적으로 정리·분석하고, 연구자들이 활용할 수 있는 마크다운 기반의 위키로 편찬하고 있습니다.

This wiki is a bilingual (Korean/English) knowledge base on the Jeju 4·3 Incident. Inspired by [Andrej Karpathy's LLM Wiki concept](https://x.com/karpathy/status/2039805659525644595), it leverages large language models to systematically organize and analyze diverse primary and secondary sources, compiling them into a markdown-based wiki accessible to researchers.

## 위키 구조 / Wiki Structure

- **[[wiki/index|위키 본문 (Wiki Entries)]]** — 제주4·3의 시기별·주제별 항목 (8개 시기 프레임)
- **[[sources/index|참고자료 요약 (Source Summaries)]]** — 보고서, 1차자료, 증언, 학술 자료의 요약
- **[[analyses/index|분석 (Analyses)]]** — 주제별 심층 분석
- **[[timelines/index|연표 (Timelines)]]** — 시간순 사건 정리

## 방법론 / Methodology

### 신뢰도 체계 / Confidence System

이 위키는 각 항목의 출처와 사실관계의 신뢰도를 체계적으로 평가합니다. 자세한 내용은 [[confidence-system|신뢰도 체계]]를 참조하십시오.

This wiki systematically evaluates the reliability of sources and factual claims for each entry. See [[confidence-system|Confidence Rating System]] for details.

### 지식 그래프 / Knowledge Graph

항목 간의 관계를 시각화하고 분석하기 위한 네트워크 구조입니다. 자세한 내용은 [[knowledge-graph|지식 그래프]]를 참조하십시오.

A network structure for visualizing and analyzing relationships between entries. See [[knowledge-graph|Knowledge Graph]] for details.

### 출처 원칙 / Source Principles

- 2003년 [[진상조사보고서]]와 2019년 [[추가진상조사보고서]]를 사실관계의 기준으로 삼음
- 언론 보도 등 추가 주장은 내용을 수록하되, 기존 정보와 다른 부분은 각주로 명시
- 사실·주장 불일치 등 논쟁이 필요한 사항은 각 입장을 모두 기록
- LLM 환각 방지를 위해 모든 서술은 출처에 근거하며, 작성 후 검증 검사 실시

## 기술 스택 / Technical Stack

[Quartz v4](https://quartz.jzhao.xyz/) 정적 사이트 생성기를 사용하며, GitHub Pages를 통해 [kb.jeju43.info](https://kb.jeju43.info)에서 서비스됩니다. 모든 콘텐츠는 마크다운으로 작성되고, [Obsidian](https://obsidian.md/)을 편집 프론트엔드로 활용합니다.

Built with the [Quartz v4](https://quartz.jzhao.xyz/) static site generator, served via GitHub Pages at [kb.jeju43.info](https://kb.jeju43.info). All content is written in markdown, with [Obsidian](https://obsidian.md/) as the editing frontend.
