#!/usr/bin/env python3
"""
Generate an interactive D3.js knowledge graph for the Jeju 4·3 wiki.

Builds connections from:
1. [[wiki links]] in page body text
2. Shared meaningful tags between pages
3. Source pages that reference multiple wiki pages (co-citation)
4. Title/alias mentions in body text

Usage:
    python graph.py                    # Generate graph
    python graph.py --include-sources  # Include source pages in graph
"""

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

import yaml

WIKI_ROOT = Path(__file__).parent.parent / "content" / "wiki"
# HTML goes to quartz/static/ so it's served as-is (Quartz Assets plugin strips .html extensions)
OUTPUT_HTML = Path(__file__).parent.parent / "quartz" / "static" / "knowledge-graph.html"
OUTPUT_MD = WIKI_ROOT / "references" / "knowledge-graph.md"

TYPE_COLORS = {
    '인물': '#3b82f6',
    '사건': '#ef4444',
    '개념': '#10b981',
    '조직': '#f97316',
    '군부대': '#92400e',
    '장소': '#a855f7',
    '분석': '#14b8a6',
    '연표': '#6b7280',
    '소스': '#d97706',
    '기타': '#9ca3af',
}

# Tags that are too generic to form meaningful connections
GENERIC_TAGS = {
    '엔티티', '개념', '사건', '참조', '소스', '학술논문', '학술자료',
    '연표', '분석', '공식문서', 'bilingual', 'redirect',
}

TYPE_MAP = {
    'analysis': '분석', 'event': '사건', 'concept': '개념',
    'entity': '조직', '사건': '사건', '개념': '개념', '조직': '조직',
    '인물': '인물', '군부대': '군부대', '연표': '연표', '분석': '분석',
    '학술논문': '소스', '학술자료': '소스', '참조': '기타',
}

DIR_TYPE_DEFAULTS = {
    'entities': '조직', 'events': '사건', 'concepts': '개념',
    'timelines': '연표', 'analyses': '분석', 'sources': '소스',
    'references': '기타',
}


def parse_frontmatter(filepath: Path) -> dict:
    try:
        text = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return {}
    if not text.startswith('---'):
        return {}
    end = text.find('\n---', 3)
    if end == -1:
        return {}
    try:
        fm = yaml.safe_load(text[3:end])
        return fm if isinstance(fm, dict) else {}
    except yaml.YAMLError:
        return {}


def get_body(filepath: Path) -> str:
    try:
        text = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return ''
    if not text.startswith('---'):
        return text
    end = text.find('\n---', 3)
    return text[end + 4:] if end != -1 else text


def extract_wiki_links(text: str) -> List[str]:
    return re.findall(r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]', text)


def infer_type(fm: dict, filepath: Path) -> str:
    t = fm.get('type', '')
    if t and t in TYPE_MAP:
        return TYPE_MAP[t]
    if t:
        return t

    rel = filepath.relative_to(WIKI_ROOT)
    dir_name = rel.parts[0] if rel.parts else ''
    return DIR_TYPE_DEFAULTS.get(dir_name, '기타')


def build_graph(include_sources=False):
    """Build node/edge data from wiki files."""
    pages = {}       # stem -> {title, type, confidence, tags, path, body}
    alias_map = {}   # alias_lower -> stem
    title_map = {}   # title_lower -> stem

    # 1. Load all pages
    for md in WIKI_ROOT.rglob('*.md'):
        rel = md.relative_to(WIKI_ROOT)
        dir_name = rel.parts[0] if rel.parts else ''

        if dir_name == 'sources' and not include_sources:
            continue
        if dir_name == 'references':
            continue

        fm = parse_frontmatter(md)
        title = fm.get('title', md.stem)
        if not title:
            title = md.stem

        page_type = infer_type(fm, md)
        tags = fm.get('aliases', []) if False else fm.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        tags = [str(t) for t in tags]

        confidence = fm.get('confidence', 'unknown')
        aliases = fm.get('aliases', [])
        if isinstance(aliases, str):
            aliases = [aliases]

        stem = md.stem
        pages[stem] = {
            'title': title,
            'type': page_type,
            'confidence': confidence,
            'tags': tags,
            'aliases': [str(a) for a in aliases],
            'path': str(rel),
            'stem': stem,
        }

        title_map[title.lower()] = stem
        title_map[stem.lower()] = stem
        for a in aliases:
            alias_map[str(a).lower()] = stem

    # Also load source pages for co-citation analysis (even if not displayed)
    source_links = defaultdict(set)  # source_stem -> set of linked page stems
    for md in (WIKI_ROOT / 'sources').rglob('*.md'):
        body = get_body(md)
        links = extract_wiki_links(body)
        resolved = set()
        for link in links:
            lk = link.strip().lower()
            target = alias_map.get(lk) or title_map.get(lk)
            if target and target in pages:
                resolved.add(target)
        if len(resolved) >= 2:
            source_links[md.stem] = resolved

    # 2. Build edges
    edges = Counter()  # (stem_a, stem_b) -> weight

    # Method A: Wiki links in body text
    for stem, page in pages.items():
        body = get_body(WIKI_ROOT / page['path'])
        links = extract_wiki_links(body)
        for link in links:
            lk = link.strip().lower()
            target = alias_map.get(lk) or title_map.get(lk)
            if target and target != stem and target in pages:
                edge = tuple(sorted([stem, target]))
                edges[edge] += 3  # High weight for explicit links

    # Method B: Shared meaningful tags
    tag_to_pages = defaultdict(set)
    for stem, page in pages.items():
        for tag in page['tags']:
            if tag.lower() not in GENERIC_TAGS and len(tag) > 1:
                tag_to_pages[tag].add(stem)

    for tag, tag_pages in tag_to_pages.items():
        if 2 <= len(tag_pages) <= 15:  # Skip overly broad tags
            page_list = sorted(tag_pages)
            for i in range(len(page_list)):
                for j in range(i + 1, len(page_list)):
                    edge = tuple(sorted([page_list[i], page_list[j]]))
                    edges[edge] += 1

    # Method C: Co-citation from source pages
    for src_stem, linked_pages in source_links.items():
        linked_list = sorted(linked_pages)
        for i in range(len(linked_list)):
            for j in range(i + 1, len(linked_list)):
                edge = tuple(sorted([linked_list[i], linked_list[j]]))
                edges[edge] += 2  # Medium weight for co-citation

    # Method D: Title/alias mention in body (without [[]] brackets)
    all_names = {}  # name_lower -> stem (only names ≥ 3 chars to avoid false matches)
    for stem, page in pages.items():
        if len(stem) >= 3:
            all_names[stem.lower()] = stem
        for a in page['aliases']:
            if len(str(a)) >= 3:
                all_names[str(a).lower()] = stem

    for stem, page in pages.items():
        body = get_body(WIKI_ROOT / page['path']).lower()
        for name, target_stem in all_names.items():
            if target_stem != stem and name in body:
                edge = tuple(sorted([stem, target_stem]))
                if edge not in edges:
                    edges[edge] += 1  # Low weight for implicit mention

    # Filter: only keep edges with weight ≥ 2 (at least 2 connection types)
    strong_edges = {e: w for e, w in edges.items() if w >= 2}

    return pages, strong_edges


def generate_html(pages, edges):
    """Generate D3.js HTML visualization."""
    nodes = []
    node_idx = {}

    # Calculate connection counts
    conn_count = Counter()
    for (a, b), w in edges.items():
        conn_count[a] += 1
        conn_count[b] += 1

    for i, (stem, page) in enumerate(sorted(pages.items())):
        node_idx[stem] = i
        color = TYPE_COLORS.get(page['type'], TYPE_COLORS['기타'])
        size = min(30, max(8, 8 + conn_count.get(stem, 0) * 1.5))
        nodes.append({
            'id': i,
            'title': page['title'],
            'type': page['type'],
            'confidence': page['confidence'],
            'color': color,
            'size': size,
            'url': f"https://kb.jeju43.info/{stem}",
            'connections': conn_count.get(stem, 0),
        })

    links = []
    for (a, b), w in sorted(edges.items()):
        if a in node_idx and b in node_idx:
            links.append({
                'source': node_idx[a],
                'target': node_idx[b],
                'weight': min(w, 5),
            })

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    links_json = json.dumps(links, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>제주4·3 지식 그래프 | Jeju 4·3 Knowledge Graph</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:'Noto Sans KR',-apple-system,sans-serif; background:#141210; color:#eae6e2; overflow:hidden; }}
#app {{ display:flex; flex-direction:column; height:100vh; }}
header {{ background:#1c1a18; padding:16px 24px; border-bottom:1px solid #2c2a28; }}
header h1 {{ font-size:22px; font-weight:600; color:#eae6e2; }}
header .sub {{ font-size:13px; color:#6a6560; margin-top:4px; }}
#controls {{ background:#1c1a18; padding:10px 24px; border-bottom:1px solid #2c2a28; display:flex; gap:24px; flex-wrap:wrap; align-items:center; }}
#search {{ flex:0 1 280px; padding:6px 10px; background:#2c2a28; border:1px solid #44403a; border-radius:4px; color:#eae6e2; font-size:13px; }}
#search::placeholder {{ color:#6a6560; }}
.filters {{ display:flex; gap:14px; flex-wrap:wrap; align-items:center; }}
.filters label {{ display:flex; align-items:center; gap:6px; cursor:pointer; font-size:12px; color:#d0ccc8; user-select:none; }}
.filters input {{ cursor:pointer; }}
.dot {{ width:10px; height:10px; border-radius:50%; display:inline-block; }}
#graph {{ flex:1; position:relative; }}
svg {{ width:100%; height:100%; }}
.link {{ stroke-opacity:0.3; }}
.link:hover {{ stroke-opacity:0.8; }}
.node {{ cursor:pointer; stroke:#2c2a28; stroke-width:1px; }}
.node:hover {{ stroke:#eae6e2; stroke-width:2px; }}
.label {{ pointer-events:none; font-size:10px; text-anchor:middle; fill:#d0ccc8; opacity:0.8; }}
#tooltip {{ position:absolute; display:none; background:#2c2a28; color:#eae6e2; padding:10px 14px; border-radius:6px; font-size:12px; border:1px solid #44403a; pointer-events:none; z-index:100; max-width:280px; box-shadow:0 4px 12px rgba(0,0,0,0.6); }}
#tooltip .tt-title {{ font-weight:600; margin-bottom:4px; }}
#tooltip .tt-meta {{ color:#9a9590; font-size:11px; }}
#stats {{ background:#1c1a18; padding:8px 24px; border-top:1px solid #2c2a28; font-size:11px; color:#6a6560; }}
</style>
</head>
<body>
<div id="app">
  <header>
    <h1>제주4·3 지식 그래프</h1>
    <div class="sub">Jeju 4·3 Knowledge Graph — interactive visualization of {len(nodes)} pages and {len(links)} connections</div>
  </header>
  <div id="controls">
    <input type="text" id="search" placeholder="검색 / Search...">
    <div class="filters" id="filters"></div>
  </div>
  <div id="graph"></div>
  <div id="stats"></div>
</div>
<div id="tooltip"></div>
<script>
const nodes = {nodes_json};
const links = {links_json};
const types = [...new Set(nodes.map(n=>n.type))].sort();
const visible = new Set(types);
let query = '';

const el = document.getElementById('graph');
const W = el.clientWidth, H = el.clientHeight;
const svg = d3.select('#graph').append('svg');
const g = svg.append('g');

svg.call(d3.zoom().on('zoom', e => g.attr('transform', e.transform)));

const sim = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links).id(d=>d.id).distance(d=>80/Math.sqrt(d.weight||1)).strength(d=>(d.weight||1)*0.05))
  .force('charge', d3.forceManyBody().strength(-120))
  .force('center', d3.forceCenter(W/2, H/2))
  .force('collide', d3.forceCollide(d=>d.size+4));

const link = g.selectAll('line').data(links).join('line')
  .attr('class','link')
  .attr('stroke','#44403a')
  .attr('stroke-width', d=>Math.min(d.weight,4)*0.5);

const node = g.selectAll('circle').data(nodes).join('circle')
  .attr('class','node').attr('r',d=>d.size).attr('fill',d=>d.color)
  .call(d3.drag().on('start',(e,d)=>{{if(!e.active)sim.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;}})
    .on('drag',(e,d)=>{{d.fx=e.x;d.fy=e.y;}})
    .on('end',(e,d)=>{{if(!e.active)sim.alphaTarget(0);d.fx=null;d.fy=null;}}));

const label = g.selectAll('text').data(nodes).join('text')
  .attr('class','label')
  .text(d=>{{const t=d.title.split('/')[0].trim(); return t.length>12?t.slice(0,12)+'…':t;}})
  .attr('dy',d=>d.size+14);

sim.on('tick',()=>{{
  link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
  node.attr('cx',d=>d.x).attr('cy',d=>d.y);
  label.attr('x',d=>d.x).attr('y',d=>d.y);
}});

const tip = document.getElementById('tooltip');
node.on('mouseenter',(e,d)=>{{
  tip.innerHTML=`<div class="tt-title">${{d.title}}</div><div class="tt-meta">${{d.type}} · ${{d.confidence}} · ${{d.connections}} connections</div>`;
  tip.style.display='block';
}}).on('mousemove',e=>{{
  tip.style.left=(e.pageX+12)+'px'; tip.style.top=(e.pageY+12)+'px';
}}).on('mouseleave',()=>{{tip.style.display='none';}})
.on('click',(e,d)=>window.open(d.url,'_blank'));

// Filters
const fc = document.getElementById('filters');
types.forEach(t=>{{
  const lbl=document.createElement('label');
  const cb=document.createElement('input');cb.type='checkbox';cb.checked=true;
  const dot=document.createElement('span');dot.className='dot';
  dot.style.backgroundColor=nodes.find(n=>n.type===t)?.color||'#999';
  cb.onchange=e=>{{if(e.target.checked)visible.add(t);else visible.delete(t);filter();}};
  lbl.append(cb,dot,document.createTextNode(' '+t));fc.append(lbl);
}});

document.getElementById('search').addEventListener('input',e=>{{query=e.target.value.toLowerCase();filter();}});

function filter(){{
  const vis=new Set(nodes.filter(n=>visible.has(n.type)&&n.title.toLowerCase().includes(query)).map(n=>n.id));
  node.style('display',d=>vis.has(d.id)?null:'none');
  label.style('display',d=>vis.has(d.id)?null:'none');
  link.style('display',d=>vis.has(d.source.id)&&vis.has(d.target.id)?null:'none');
  const vc=vis.size, vl=links.filter(l=>vis.has(l.source.id)&&vis.has(l.target.id)).length;
  document.getElementById('stats').textContent=`${{vc}} nodes, ${{vl}} connections shown (total: ${{nodes.length}} nodes, ${{links.length}} connections)`;
}}
filter();
</script>
</body>
</html>"""
    return html, len(nodes), len(links)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--include-sources', action='store_true')
    args = parser.parse_args()

    print("Building Jeju 4·3 Knowledge Graph...")
    pages, edges = build_graph(include_sources=args.include_sources)
    print(f"  {len(pages)} pages, {len(edges)} edges")

    html, n_nodes, n_links = generate_html(pages, edges)
    OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html, encoding='utf-8')
    print(f"  HTML: {OUTPUT_HTML} ({n_nodes} nodes, {n_links} links)")

    # Update markdown stats
    md = f"""---
title: "지식 그래프 / Knowledge Graph"
aliases: [knowledge graph, 지식그래프, 네트워크 시각화]
tags: [참조, 메타데이터, 시각화]
lang: bilingual
type: 참조
created: 2026-04-11
updated: 2026-04-11
---

# 지식 그래프 / Knowledge Graph

제주4·3 위키의 인물, 사건, 개념, 조직 페이지 간의 연결을 시각화한 인터랙티브 그래프입니다. 노드를 클릭하면 해당 페이지 링크가 표시되고, 검색과 필터 기능을 사용할 수 있습니다.

An interactive visualization of connections between people, events, concepts, and organizations in the Jeju 4·3 Knowledge Base. Click nodes to see page links; use search and filters to explore.

<div style="position:relative;width:100%;padding-top:75%;margin:1em 0;border:1px solid var(--lightgray);border-radius:8px;overflow:hidden;">
<iframe src="/static/knowledge-graph.html" style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;" loading="lazy" title="제주4·3 지식 그래프"></iframe>
</div>

<p style="text-align:center;font-size:0.85em;color:var(--gray);">
<a href="/static/knowledge-graph.html" target="_blank">전체 화면으로 보기 / Open full screen ↗</a>
</p>

## 통계 / Statistics

| 항목 | 값 |
|------|-----|
| 노드 수 / Nodes | {n_nodes} |
| 연결 수 / Connections | {n_links} |
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
"""
    OUTPUT_MD.write_text(md, encoding='utf-8')
    print(f"  MD: {OUTPUT_MD}")
    print(f"\nDone! Open {OUTPUT_HTML} in a browser.")


if __name__ == '__main__':
    main()
