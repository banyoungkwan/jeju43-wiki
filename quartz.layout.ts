import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

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
    Component.Explorer(),
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
    Component.Explorer(),
  ],
  right: [],
}
