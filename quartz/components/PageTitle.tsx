import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"
import { i18n } from "../i18n"

const PageTitle: QuartzComponent = ({ fileData, cfg, displayClass }: QuartzComponentProps) => {
  const title = cfg?.pageTitle ?? i18n(cfg.locale).propertyDefaults.title
  const baseDir = pathToRoot(fileData.slug!)
  return (
    <h2 class={classNames(displayClass, "page-title")}>
      <a href={baseDir}>
        <img class="page-logo" src={`${baseDir}/static/logo.svg`} alt="제주4·3" width="30" height="30" />
        <span class="page-title-text">{title}</span>
      </a>
    </h2>
  )
}

PageTitle.css = `
.page-title {
  font-size: 1.75rem;
  margin: 0;
  font-family: var(--titleFont);
}
.page-title a {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.page-logo {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  flex-shrink: 0;
}
.page-title-text {
  line-height: 1.2;
}
`

export default (() => PageTitle) satisfies QuartzComponentConstructor
