#!/usr/bin/env python3
"""
Jeju 4·3 Wiki CLI Search Tool

A lightweight search engine for the wiki content, designed for both
human CLI use and LLM tool integration (per Karpathy LLM wiki pattern).

Usage:
    python search.py "초토화"                    # Basic content search
    python search.py --field confidence confirmed  # Metadata search
    python search.py --field type 인물             # Find all people
    python search.py --tag 국가폭력               # Tag search
    python search.py --orphans                    # Find orphan pages
    python search.py --stats                      # Wiki statistics
"""

import argparse
import os
import re
import sys
import yaml
from collections import Counter, defaultdict
from pathlib import Path

WIKI_ROOT = Path(__file__).parent.parent / "content"


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}

    if not text.startswith("---"):
        return {}

    end = text.find("\n---", 3)
    if end == -1:
        return {}

    try:
        fm = yaml.safe_load(text[3:end])
        return fm if isinstance(fm, dict) else {}
    except yaml.YAMLError:
        return {}


def get_body(filepath: Path) -> str:
    """Get markdown body (after frontmatter)."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

    if not text.startswith("---"):
        return text

    end = text.find("\n---", 3)
    if end == -1:
        return text

    return text[end + 4:]


def find_wiki_links(text: str) -> list[str]:
    """Extract [[wiki links]] from text."""
    return re.findall(r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]', text)


def all_pages() -> list[Path]:
    """List all markdown files in the wiki."""
    return sorted(WIKI_ROOT.rglob("*.md"))


def content_search(query: str, case_sensitive: bool = False):
    """Search page titles, aliases, and body content."""
    results = []
    flags = 0 if case_sensitive else re.IGNORECASE

    for page in all_pages():
        fm = parse_frontmatter(page)
        body = get_body(page)
        rel = page.relative_to(WIKI_ROOT)

        title = fm.get("title", "")
        aliases = fm.get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]

        # Score: title match > alias match > body match
        score = 0
        matches = []

        if re.search(query, str(title), flags):
            score += 10
            matches.append(f"title: {title}")

        for alias in aliases:
            if re.search(query, str(alias), flags):
                score += 5
                matches.append(f"alias: {alias}")
                break

        body_matches = list(re.finditer(query, body, flags))
        if body_matches:
            score += len(body_matches)
            # Show first match in context
            m = body_matches[0]
            start = max(0, m.start() - 40)
            end = min(len(body), m.end() + 40)
            snippet = body[start:end].replace("\n", " ").strip()
            matches.append(f"body ({len(body_matches)}x): ...{snippet}...")

        if score > 0:
            results.append({
                "path": str(rel),
                "title": title,
                "score": score,
                "confidence": fm.get("confidence", ""),
                "matches": matches,
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def field_search(field: str, value: str):
    """Search by frontmatter field value."""
    results = []
    for page in all_pages():
        fm = parse_frontmatter(page)
        rel = page.relative_to(WIKI_ROOT)

        fval = fm.get(field, "")
        if isinstance(fval, list):
            if any(value.lower() in str(v).lower() for v in fval):
                results.append({"path": str(rel), "title": fm.get("title", ""), field: fval})
        elif value.lower() in str(fval).lower():
            results.append({"path": str(rel), "title": fm.get("title", ""), field: fval})

    return results


def tag_search(tag: str):
    """Find pages with a specific tag."""
    return field_search("tags", tag)


def find_orphans():
    """Find pages with no incoming links."""
    # Build link graph
    incoming = defaultdict(set)
    all_titles = {}

    for page in all_pages():
        fm = parse_frontmatter(page)
        rel = str(page.relative_to(WIKI_ROOT))
        name = page.stem
        title = fm.get("title", name)
        all_titles[name.lower()] = rel

        # Register aliases
        aliases = fm.get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]
        for alias in aliases:
            all_titles[str(alias).lower()] = rel

    for page in all_pages():
        body = get_body(page)
        source = str(page.relative_to(WIKI_ROOT))
        links = find_wiki_links(body)

        for link in links:
            target = link.strip().lower()
            if target in all_titles:
                target_path = all_titles[target]
                if target_path != source:
                    incoming[target_path].add(source)

    orphans = []
    for page in all_pages():
        rel = str(page.relative_to(WIKI_ROOT))
        if rel not in incoming or len(incoming[rel]) == 0:
            fm = parse_frontmatter(page)
            orphans.append({
                "path": rel,
                "title": fm.get("title", ""),
                "outgoing_links": len(find_wiki_links(get_body(page))),
            })

    return orphans


def wiki_stats():
    """Generate wiki statistics."""
    pages = all_pages()
    by_dir = Counter()
    by_confidence = Counter()
    by_lang = Counter()
    total_words = 0
    total_links = 0

    for page in pages:
        fm = parse_frontmatter(page)
        body = get_body(page)
        rel = page.relative_to(WIKI_ROOT)

        # Directory
        parts = rel.parts
        if len(parts) > 1:
            by_dir[parts[0] + "/" + parts[1]] += 1
        else:
            by_dir[str(rel)] += 1

        # Confidence
        conf = fm.get("confidence", "none")
        by_confidence[conf] += 1

        # Language
        lang = fm.get("lang", "unknown")
        by_lang[lang] += 1

        # Word count (rough)
        total_words += len(body.split())

        # Link count
        total_links += len(find_wiki_links(body))

    return {
        "total_pages": len(pages),
        "total_words": total_words,
        "total_wiki_links": total_links,
        "by_directory": dict(by_dir.most_common()),
        "by_confidence": dict(by_confidence.most_common()),
        "by_language": dict(by_lang.most_common()),
    }


def main():
    parser = argparse.ArgumentParser(description="Jeju 4·3 Wiki Search Tool")
    parser.add_argument("query", nargs="?", help="Search query (regex supported)")
    parser.add_argument("--field", nargs=2, metavar=("FIELD", "VALUE"),
                        help="Search by frontmatter field")
    parser.add_argument("--tag", help="Search by tag")
    parser.add_argument("--orphans", action="store_true", help="Find orphan pages")
    parser.add_argument("--stats", action="store_true", help="Wiki statistics")
    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if args.stats:
        stats = wiki_stats()
        if args.json:
            import json
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print(f"📊 Wiki Statistics")
            print(f"   Pages: {stats['total_pages']}")
            print(f"   Words: {stats['total_words']:,}")
            print(f"   Wiki links: {stats['total_wiki_links']:,}")
            print(f"\n📁 By directory:")
            for d, c in stats["by_directory"].items():
                print(f"   {d}: {c}")
            print(f"\n🔒 By confidence:")
            for conf, c in stats["by_confidence"].items():
                print(f"   {conf}: {c}")
        return

    if args.orphans:
        orphans = find_orphans()
        if args.json:
            import json
            print(json.dumps(orphans, ensure_ascii=False, indent=2))
        else:
            print(f"🔗 Orphan pages ({len(orphans)} total):\n")
            for o in orphans[:args.limit]:
                print(f"  {o['path']}")
                print(f"    {o['title']} (→ {o['outgoing_links']} outward links)")
        return

    if args.field:
        results = field_search(args.field[0], args.field[1])
    elif args.tag:
        results = tag_search(args.tag)
    elif args.query:
        results = content_search(args.query)
    else:
        parser.print_help()
        return

    if args.json:
        import json
        print(json.dumps(results[:args.limit], ensure_ascii=False, indent=2))
    else:
        print(f"🔍 {len(results)} results" + (f" (showing top {args.limit})" if len(results) > args.limit else "") + ":\n")
        for r in results[:args.limit]:
            conf = f" [{r.get('confidence', '')}]" if r.get('confidence') else ""
            print(f"  📄 {r.get('title', '?')}{conf}")
            print(f"     {r['path']}")
            for m in r.get("matches", []):
                print(f"     ↳ {m}")
            print()


if __name__ == "__main__":
    main()
