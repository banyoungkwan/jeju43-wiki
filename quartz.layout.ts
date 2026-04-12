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

  if ((!a.isFolder && !b.isFolder) || (a.isFolder && b.isFolder)) {
    // For folders: use slugSegment so numeric prefixes (1-, 2-, ...) sort correctly
    // For files: use displayName (title)
    const aKey = a.isFolder ? aSlug : a.displayName
    const bKey = b.isFolder ? bSlug : b.displayName
    return aKey.localeCompare(bKey, undefined, {
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
    Component.Explorer({ sortFn: explorerSortFn }),
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
    Component.Explorer({ sortFn: explorerSortFn }),
  ],
  right: [],
}
