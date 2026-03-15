---
layout: post
title: "Let your Coding Agent debug the browser session with Chrome DevTools MCP - コーディングエージェントがChrome DevToolsのセッションを直接デバッグできるようにする"
date: 2026-03-15T19:33:28.516Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://developer.chrome.com/blog/chrome-devtools-mcp-debug-your-browser-session"
source_title: "Let your Coding Agent debug your browser session with Chrome DevTools MCP &nbsp;|&nbsp; Blog &nbsp;|&nbsp; Chrome for Developers"
source_id: 47390817
excerpt: "Chrome M144のautoConnectでAIが表示中ページ（ログイン状態含む）を直接デバッグ"
image: "https://developer.chrome.com/static/blog/chrome-devtools-mcp-debug-your-browser-session/image/hero.png"
---

# Let your Coding Agent debug the browser session with Chrome DevTools MCP - コーディングエージェントがChrome DevToolsのセッションを直接デバッグできるようにする

魅力的タイトル: 実行中のブラウザをAIに任せる時代へ — Chrome DevTools MCPで「今開いているページ」をそのままデバッグさせる方法

## 要約
Chrome M144のDevTools MCPにautoConnect機能が追加され、コーディングエージェントが現在開いているブラウザセッションやDevToolsの選択中データ（Elements／Network）に直接接続してデバッグできるようになりました。

## この記事を読むべき理由
サインインが必要な不具合や手動で確認しているDevToolsの状態を、わざわざ再現せずにAIに解析・修正させられるため、開発・QA・運用の効率が大幅に上がります。日本のプロダクト現場でも、ローカル再現が難しい問題解決や自動化導入に直結します。

## 詳細解説
- 何が変わったか  
  - Chrome DevTools MCPサーバーに --autoConnect オプションを追加。起動中のChromeインスタンスにリモートデバッグ接続を要求し、既存のブラウザセッションを使ってエージェントが作業できる。ElementsパネルやNetworkパネルで選択した項目をエージェントに渡して調査させるユースケースが可能に。  

- 動作要件と安全対策  
  - 対象はChrome M144（Betaで提供中）。リモートデバッグはデフォルト無効で、ユーザーが chrome://inspect/#remote-debugging で有効化する必要がある。接続要求時はChromeが許可ダイアログを表示し、許可しない限り接続されない。また接続中は「Chrome is being controlled by automated test software」バナーが表示される。  

- 既存の接続方式は継続  
  - 従来通り、MCP専用プロファイル起動、リモートデバッグポート接続、複数インスタンスの一時プロファイル運用なども引き続き使える。

- 仕組み（簡易）  
  - MCPサーバーがリモートデバッグ接続を要求 → Chromeはユーザーに確認ダイアログを表示 → 許可後、MCPがDevToolsプロトコル経由でセッションとパネルデータにアクセス。

## 実践ポイント
1. Chromeでリモートデバッグを有効化する  
   - chrome://inspect/#remote-debugging にアクセスして有効化し、ダイアログで許可を与える。  
2. MCPサーバーを autoConnect 指定で起動する（例：gemini-cli設定）  
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--autoConnect",
        "--channel=beta"
      ]
    }
  }
}
```
   - M144が安定版になるまでは --channel=beta を指定。  
3. Chromeを起動してからMCPを動かし、接続ダイアログで「Allow」を選ぶ。接続後はDevToolsで要素／リクエストを選択してエージェントに調査を依頼。  
4. 注意点：社内機密セッションや権限のあるログイン状態での接続はポリシー確認を行うこと。

短時間で試したい場合は、ローカルの非機密ページでまず動作確認を行うと安全です。
