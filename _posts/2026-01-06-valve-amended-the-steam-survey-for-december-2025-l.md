---
  layout: post
  title: "Valve amended the Steam survey for December 2025 - Linux actually hit another all-time high - Valveが2025年12月のSteam調査を修正 — Linuxが再び過去最高を更新"
  date: 2026-01-06T15:48:32.529Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.gamingonlinux.com/2026/01/valve-amended-the-steam-survey-for-december-2025-linux-actually-hit-another-all-time-high/"
  source_title: "Valve amended the Steam survey for December 2025 - Linux actually hit another all-time high | GamingOnLinux"
  source_id: 469663482
  excerpt: "Steam調査修正でLinuxが3.58%に上昇、DeckとFlatpakが後押し"
  image: "https://www.gamingonlinux.com/uploads/tagline_gallery/steamos-2025.jpg"
---

# Valve amended the Steam survey for December 2025 - Linux actually hit another all-time high - Valveが2025年12月のSteam調査を修正 — Linuxが再び過去最高を更新
Steam調査の修正で見えた“Linuxの追い風”：Steam DeckとFlatpakランタイムの影響が浮き彫りに

## 要約
Valveが2025年12月のSteamハードウェア＆ソフトウェア調査を修正し、Linuxのシェアが当初報告の$3.19\%$から$3.58\%$に上方修正された。SteamOSやFlatpak関連ランタイムの存在感が特に目立つ結果になっている。

## この記事を読むべき理由
日本のゲーム開発者・パブリッシャー、そしてLinux／Steam Deckユーザーにとって、プラットフォームの実勢を把握することは配信戦略や互換性テストの優先順位決定に直結する。Desktop向けだけでなく、Steam DeckやFlatpak対応を視野に入れる価値が高まっているからだ。

## 詳細解説
- 修正後のグローバル比率（2025年12月）
  - Windows: $94.23\%$
  - Linux: $3.58\%$（初出は$3.19\%$）
  - macOS: $2.18\%$

- Linux内で検出された主なディストリビューション（抜粋、順位とシェア）
  - SteamOS Holo 64-bit: $26.32\%$
  - Arch Linux 64-bit: $9.54\%$
  - Linux Mint 22.2 64-bit: $7.85\%$
  - CachyOS 64-bit: $7.20\%$
  - Freedesktop SDK 25.08（Flatpakランタイム）64-bit: $6.29\%$
  - Ubuntu Core 24 64-bit: 目立つ新顔（増分あり）
- 注目点
  - Steam Deck寄与：ValveはLinux環境で「AMD Custom GPU 0405」（Steam Deck）を$13.37\%$として報告しており、Deckの存在がLinux比率を押し上げている。
  - Flatpakランタイム（Freedesktop SDK）が上位に入っている点は、ゲーム配布やランタイム依存の観点で無視できないシグナル。
  - 当月は最初の公開値に誤差（言語や表示順など）や欠落があり、Valveがデータを修正した経緯がある。統計の出し方・表記にまだ改善余地がある。

## 実践ポイント
- テスト優先度の見直し：自社タイトルのプレイヤーベースや目標地域を踏まえ、Steam Deckでの動作確認と最適化（コントローラUI、解像度・パフォーマンス調整）を検討する。
- 配布手法の最適化：Flatpak／Freedesktop SDKの存在感を受け、Linux向けの配布を考えるならランタイム依存を明確にし、Flatpak対応を検討すると導入障壁を下げられる。
- CI／QA環境の多様化：Arch、Ubuntu派生、SteamOSなど複数ディストリをテスト対象に加え、特にSteam Deck上での自動化テストを整備する。
- 日本市場向けの判断：日本ではWindows優勢は続くが、Steam Deckやインディー市場を狙うならLinux対応は差別化になる。ローカライズやサポート体制も含めコスト対効果を検討する価値がある。

短く言えば、今回の修正は「Linux勢力の底上げ」と「Steam Deck／Flatpakが現場に与える影響」を再確認させるものだ。次のアップデートやValve側の表記改善にも注意しつつ、自社のテスト／配布戦略を見直す好機といえる。
