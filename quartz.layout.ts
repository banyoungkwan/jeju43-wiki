import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// Explorer sortFn — analysisOrder must be INSIDE the function
// because Quartz serializes sortFn to an inline script at runtime
const explorerSortFn = (a: any, b: any) => {
  // Analysis pages: fixed chronological order
  const analysisOrder: Record<string, number> = {
    "책임구조분석": 1,
    "폭력의시간": 2,
    "공간과기억": 3,
    "침묵의장치들": 4,
    "기억의정치연대기": 5,
    "정명과화해": 6,
  }

  const aSlug = a.slugSegment ?? ""
  const bSlug = b.slugSegment ?? ""
  const aOrder = analysisOrder[aSlug]
  const bOrder = analysisOrder[bSlug]
  if (aOrder !== undefined && bOrder !== undefined) return aOrder - bOrder

  // Files: index first, then sort by publication year (ascending)
  // File naming convention: {author}_{year}_{title}.md
  if (!a.isFolder && !b.isFolder) {
    // Both are files — check for index first
    const aIsIndex = aSlug === "index"
    const bIsIndex = bSlug === "index"
    if (aIsIndex && !bIsIndex) return -1
    if (!aIsIndex && bIsIndex) return 1

    // Extract year from slugSegment: pattern {author}_{year}_{title}
    const yearPattern = /_(1[89]\d{2}|20\d{2})_/
    const aYearMatch = aSlug.match(yearPattern)
    const bYearMatch = bSlug.match(yearPattern)
    const aYear = aYearMatch ? parseInt(aYearMatch[1]) : 0
    const bYear = bYearMatch ? parseInt(bYearMatch[1]) : 0

    // If both have years, sort by year ascending; then by name within same year
    if (aYear > 0 && bYear > 0) {
      if (aYear !== bYear) return aYear - bYear
      // Same year: sort by displayName
      return (a.displayName ?? aSlug).localeCompare(b.displayName ?? bSlug, undefined, {
        numeric: true,
        sensitivity: "base",
      })
    }
    // If only one has year, files with year come after index but order normally
    if (aYear > 0 && bYear === 0) return 1
    if (aYear === 0 && bYear > 0) return -1

    // Fallback: alphabetical by displayName
    return (a.displayName ?? aSlug).localeCompare(b.displayName ?? bSlug, undefined, {
      numeric: true,
      sensitivity: "base",
    })
  }

  if (a.isFolder && b.isFolder) {
    // Both folders: sort by slugSegment for numeric prefix ordering
    return aSlug.localeCompare(bSlug, undefined, {
      numeric: true,
      sensitivity: "base",
    })
  }
  return a.isFolder ? -1 : 1
}

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      "제주4·3 포털": "https://jeju43.info",
      "미국자료 아카이브": "https://archive.jeju43.info",
      "뉴스 아카이브": "https://news.jeju43.info",
      GitHub: "https://github.com/banyoungkwan/jeju43-wiki",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
        { Component: Component.LanguageToggle() },
      ],
    }),
    Component.Explorer({
      sortFn: explorerSortFn,
      mapFn: (node: any) => {
        // Shorten long display names for sidebar readability
        if (!node.isFolder && node.displayName && node.displayName.length > 32) {
          node.displayName = node.displayName.substring(0, 30) + "…"
        }
      },
    }),
  ],
  right: [
    Component.Graph({
      localGraph: {
        depth: 2,
        linkDistance: 40,
        fontSize: 0.5,
        repelForce: 0.6,
        centerForce: 0.5,
        opacityScale: 2,
        removeTags: [],
        showTags: false,
      },
      globalGraph: {
        depth: -1,
        linkDistance: 40,
        fontSize: 0.5,
        repelForce: 0.1,
        centerForce: 0.5,
        opacityScale: 2,
        removeTags: [],
        showTags: false,
      },
    }),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer({
      sortFn: explorerSortFn,
      mapFn: (node: any) => {
        if (!node.isFolder && node.displayName && node.displayName.length > 32) {
          node.displayName = node.displayName.substring(0, 30) + "…"
        }
      },
    }),
  ],
  right: [],
}
