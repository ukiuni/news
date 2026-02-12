---
layout: post
title: "Warcraft III Peon Voice Notifications for Claude Code - Warcraft IIIのピオン音声通知（Claude Code用）"
date: 2026-02-12T07:08:27.882Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tonyyont/peon-ping"
source_title: "GitHub - tonyyont/peon-ping: Warcraft III Peon voice notifications for Claude Code. Stop babysitting your terminal."
source_id: 46985151
excerpt: "Claude Codeの通知をWarcraft IIIピオン音声で通知する軽量ツール"
image: "https://opengraph.githubassets.com/9a39e8c257aa9b323f445bfd43358825fb1d8f8358974df83a6b22c7192bc463/tonyyont/peon-ping"
---

# Warcraft III Peon Voice Notifications for Claude Code - Warcraft IIIのピオン音声通知（Claude Code用）
ターミナルが「Work, work!」と教えてくれる――Claude CodeのイベントをWarcraft IIIピオン音声で受け取るPeon‑Ping

## 要約
Claude Codeのフックに連携して、セッション開始やプロンプト完了などをWarcraft IIIなどの「ピオン」音声で通知する小さなツールキット。集中を切らさず、終わりや許可待ちを聴覚で把握できます。

## この記事を読むべき理由
- ターミナルの出力を監視し続ける必要がなくなり、生産性が上がる。  
- macOS／WSL2対応で日本の開発環境でも導入しやすい。  
- 軽量で設定も簡単、ミュートやサウンドパック切替も可能で遊び心もある実用ツール。

## 詳細解説
- 仕組み：peon.sh が Claude Code のフック（SessionStart、UserPromptSubmit、Stop、Notification）に登録され、イベントに対応するカテゴリの音声をランダムで再生。ターミナルタブタイトル更新やデスクトップ通知も行います。  
- 再生方法：macOSはafplay、WSL2はPowerShellのMediaPlayerを利用。  
- サウンドパック：デフォルトのOrc Peonのほか、人間、StarCraftなど複数パックを備え、セッションごとにランダム選択か固定も可能。  
- 設定ファイル：~/.claude/hooks/peon-ping/config.json で音量や通知カテゴリ、イースターエッグ発動条件、アクティブパック等を指定できます（例は下記）。  
- CLI：peon --toggle（切替）、peon --pause／--resume（ミュート切替）、peon --status、peon --pack／--packs（パック操作）。Tab補完対応。  
- 要件：macOSまたはWSL2、Claude Codeのhooksサポート、python3。サウンドファイルは元権利者の所有物でレポジトリに同梱されています（ライセンスはMITで配布ツール部分）。

インストール例:
```bash
curl -fsSL https://raw.githubusercontent.com/tonyyont/peon-ping/main/install.sh | bash
```

config.json の例:
```json
{
  "volume": 0.5,
  "categories": {
    "greeting": true,
    "acknowledge": true,
    "complete": true,
    "error": true,
    "permission": true,
    "annoyed": true
  },
  "annoyed_threshold": 3,
  "annoyed_window_seconds": 10,
  "pack_rotation": ["peon","sc_kerrigan","peasant"],
  "active_pack": "peon"
}
```

## 実践ポイント
- まず上の一行インストールを実行して即体験。  
- 会議やペア時は `peon --pause`／`peon --resume` で即ミュート。  
- 音量や通知カテゴリは config.json で調整（0.0–1.0）。  
- 好きなサウンドパックに切替えて、開発中の気分転換やチームのネタに。  
- Claude Codeのhooksが有効か確認してから導入するとトラブルが少ない。

元リポジトリ（参考）: tonyyont/peon-ping（GitHub）
