import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "제주4·3 아카이브 위키",
    pageTitleSuffix: " | 제주4·3",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "none",
    },
    locale: "ko-KR",
    baseUrl: "kb.jeju43.info",
    ignorePatterns: ["private", "templates", ".obsidian", "raw"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Noto Serif KR",
        body: "Noto Sans KR",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#faf8f5",
          lightgray: "#e8e4df",
          gray: "#a09890",
          darkgray: "#4a4540",
          dark: "#1a1816",
          secondary: "#b5291f",
          tertiary: "#8a3028",
          highlight: "rgba(181, 41, 31, 0.08)",
          textHighlight: "#b5291f22",
        },
        darkMode: {
          light: "#141210",
          lightgray: "#2e2a28",
          gray: "#6a6460",
          darkgray: "#d4d0cc",
          dark: "#ece8e4",
          secondary: "#d4594f",
          tertiary: "#e07a70",
          highlight: "rgba(212, 89, 79, 0.10)",
          textHighlight: "#d4594f22",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
