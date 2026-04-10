import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Jeju 4·3 Knowledge Base",
    pageTitleSuffix: " | Jeju 4·3",
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
          light: "#faf9f7",
          lightgray: "#e6e4e0",
          gray: "#9a9590",
          darkgray: "#44403a",
          dark: "#1c1a18",
          secondary: "#4a6577",
          tertiary: "#5a7a8f",
          highlight: "rgba(74, 101, 119, 0.08)",
          textHighlight: "#4a657722",
        },
        darkMode: {
          light: "#141210",
          lightgray: "#2c2a28",
          gray: "#6a6560",
          darkgray: "#d0ccc8",
          dark: "#eae6e2",
          secondary: "#7a9db5",
          tertiary: "#92b3c8",
          highlight: "rgba(122, 157, 181, 0.10)",
          textHighlight: "#7a9db522",
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
