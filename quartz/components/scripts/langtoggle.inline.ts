// 초기 언어 설정 — DOM 로드 전에 적용해 FOUC 방지
const STORAGE_KEY = "jeju43-lang"
const savedLang = localStorage.getItem(STORAGE_KEY) ?? "ko"
document.documentElement.setAttribute("data-lang", savedLang)

// 버튼 시각 상태 업데이트
const updateButtonState = (lang: string) => {
  const btn = document.querySelector<HTMLButtonElement>(".lang-toggle")
  if (!btn) return
  const koLabel = btn.querySelector<HTMLElement>(".lang-ko")
  const enLabel = btn.querySelector<HTMLElement>(".lang-en")
  if (koLabel) koLabel.style.opacity = lang === "ko" ? "1" : "0.35"
  if (enLabel) enLabel.style.opacity = lang === "en" ? "1" : "0.35"
}

document.addEventListener("nav", () => {
  const applyLang = (lang: string) => {
    document.documentElement.setAttribute("data-lang", lang)
    localStorage.setItem(STORAGE_KEY, lang)
    updateButtonState(lang)
  }

  // 양언어 페이지 여부 감지 및 섹션 래핑
  const setupSections = (): boolean => {
    const article = document.querySelector("article")
    if (!article) return false

    // 이미 래핑된 경우 스킵
    if (article.querySelector(".lang-section")) return true

    const h2s = Array.from(article.querySelectorAll("h2"))
    const koH2 = h2s.find((h) => h.textContent?.trim() === "한국어")
    const enH2 = h2s.find((h) => h.textContent?.trim() === "English")

    if (!koH2 || !enH2) return false // 이중언어 페이지 아님

    // 한국어 섹션 래핑: koH2부터 enH2 직전까지
    const koWrapper = document.createElement("div")
    koWrapper.className = "lang-section lang-ko"
    koH2.parentNode!.insertBefore(koWrapper, koH2)

    let node: ChildNode | null = koH2
    while (node && node !== enH2) {
      const next: ChildNode | null = node.nextSibling
      koWrapper.appendChild(node)
      node = next
    }

    // English 섹션 래핑: enH2부터 끝까지
    const enWrapper = document.createElement("div")
    enWrapper.className = "lang-section lang-en"
    enH2.parentNode!.insertBefore(enWrapper, enH2)

    let enNode: ChildNode | null = enH2
    while (enNode) {
      const next: ChildNode | null = enNode.nextSibling
      enWrapper.appendChild(enNode)
      enNode = next
    }

    return true
  }

  const isBilingual = setupSections()

  // 이중언어 페이지에만 토글 버튼 표시
  const btn = document.querySelector<HTMLButtonElement>(".lang-toggle")
  if (btn) {
    btn.classList.toggle("hidden", !isBilingual)
  }

  // 현재 저장된 언어 적용
  const currentLang = localStorage.getItem(STORAGE_KEY) ?? "ko"
  applyLang(currentLang)

  // 클릭 이벤트
  const handleToggle = () => {
    const current = document.documentElement.getAttribute("data-lang") ?? "ko"
    applyLang(current === "ko" ? "en" : "ko")
  }

  const toggleBtn = document.querySelector(".lang-toggle")
  toggleBtn?.addEventListener("click", handleToggle)
  window.addCleanup(() => toggleBtn?.removeEventListener("click", handleToggle))
})
