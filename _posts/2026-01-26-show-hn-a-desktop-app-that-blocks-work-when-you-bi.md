---
layout: post
title: "Show HN: A desktop app that blocks work when you bite your nails - 指が口元に来たら作業を遮断するデスクトップアプリ"
date: 2026-01-26T06:47:39.799Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/cacoos/trackhands"
source_title: "GitHub - cacoos/trackhands: Detects when your fingers are near your mouth and reminds you to stop. Built with Tauri + React + MediaPipe."
source_id: 46759850
excerpt: "カメラで口元に手が触れると作業を遮断し無意識の癖を矯正するデスクトップアプリ"
image: "https://opengraph.githubassets.com/05a88b6ef4acc7eb6d4a14eb09708c9902eae08b1e32b0540fe190e150afddc2/cacoos/trackhands"
---

# Show HN: A desktop app that blocks work when you bite your nails - 指が口元に来たら作業を遮断するデスクトップアプリ
作業中のクセを“見える化”して止めさせる——カメラで口元に手が来たら注意を出すデスクトップアプリ「TrackHands」を試す理由

## 要約
TrackHandsはTauri + React + MediaPipeで作られたクロスプラットフォームアプリで、カメラで手と顔の位置を検出し、指が口元に近づくと警告や作業ブロックを行います。処理はローカルで完結し、プライバシー配慮されています。

## この記事を読むべき理由
- テレワーク増加で「無意識のクセ」が映像越しに問題化する場面が増加中。自分の習慣改善に手軽に使えるツールは実用性が高い。  
- MediaPipeやTauriなど、最近注目の技術スタックを組み合わせた実装例として学びになる。

## 詳細解説
- コア機能：MediaPipeのFace Meshで顔（口の位置）を検出、Handsで手指のランドマークを追跡。口元と指先の距離が閾値を下回ると警告オーバーレイやスクリーンショット保存を実行。  
- アーキテクチャ：フロントエンドはReact + TypeScript（Vite・Tailwind）、デスクトップ化はTauri（Rustバックエンド）で実現。状態管理はZustand。  
- プライバシー：すべてローカル処理。映像の外部送信は行わないため、社内データポリシーに抵触しにくい。  
- 設定項目：検出頻度（Slow/Medium/Fast）、カメラ解像度（Low/Medium/High）、検知時のスクリーンショット保存。  
- 動作環境：macOS 11+/Windows 10+/Linux、内蔵またはUSBカメラ。開発にはNode.js 18+, pnpm, Rust, Tauri CLIが必要。  
- ビルド／起動（開発時の例）：
```bash
# Clone と開発起動
git clone https://github.com/cacoos/trackhands.git
cd trackhands
pnpm install
pnpm tauri dev
```

## 実践ポイント
- まずはリリースからバイナリをダウンロードして試す（カメラ許可を忘れずに）。  
- 検出が不安定なら：顔に十分なライティング、カメラ解像度を上げる、検出頻度をFastに。  
- プライバシー重視の職場では「ローカル処理」をアピールして導入提案しやすい。  
- 習慣改善用途だけでなく、社内研修やヘルスケアのセルフモニタリングツールとして応用可能。  
- 開発者向け：MediaPipe + Tauri の組み合わせは他のジェスチャ検出や手元操作トリガー実装にも転用できる。興味があればリポジトリにPRを送ろう。

興味があれば、まずリリースを落として動かしてみることをおすすめします。
