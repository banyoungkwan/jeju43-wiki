// @ts-ignore
import langToggleScript from "./scripts/langtoggle.inline"
import styles from "./styles/langtoggle.scss"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const LanguageToggle: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
  return (
    <button class={classNames(displayClass, "lang-toggle")} aria-label="언어 전환 / Toggle language">
      <span class="lang-ko">한</span>
      <span class="divider">/</span>
      <span class="lang-en">EN</span>
    </button>
  )
}

LanguageToggle.beforeDOMLoaded = langToggleScript
LanguageToggle.css = styles

export default (() => LanguageToggle) satisfies QuartzComponentConstructor
