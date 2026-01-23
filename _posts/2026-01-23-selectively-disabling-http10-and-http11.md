---
layout: post
title: "Selectively Disabling HTTP/1.0 and HTTP/1.1 - HTTP/1.0 と HTTP/1.1 の選択的無効化"
date: 2026-01-23T12:39:31.092Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://markmcb.com/web/selectively_disabling_http_1/"
source_title: "Selectively Disabling HTTP/1.0 and HTTP/1.1 - Mark McBride"
source_id: 1173735606
excerpt: "nginxでHTTP/1.xをUA別に段階的に弾き、負荷と悪質トラフィックを削減"
image: "https://markmcb.com/web/selectively_disabling_http_1/og_image.png"
---

# Selectively Disabling HTTP/1.0 and HTTP/1.1 - HTTP/1.0 と HTTP/1.1 の選択的無効化
攻めのボット対策＆通信近代化：nginxでHTTP/1.xだけ賢く弾く方法

## 要約
作者はサイトをHTTP/3化した際、アクセスの大半がHTTP/1.xでしかも悪質なトラフィックが多いことに気づき、nginxのmapを使ってHTTP/1.0/1.1をユーザエージェントに応じて選択的に遮断（426や444で応答）する設定を導入して効果を得た。

## この記事を読むべき理由
日本でもスクレイパーや脆弱性スキャン、SNSのプレビュー用ボットなどがサイト運用のノイズ・負荷源になっています。HTTP/2/3普及を踏まえ、旧来のHTTP/1.xだけを選別して弾く手法は簡単に導入でき、誤検知を監視しながら段階的に強化できる実用的な防御策です。

## 詳細解説
- 方針：リクエストのプロトコル（$server_protocol）とUser-Agent（$http_user_agent）を組み合わせ、許可リスト方式（Include）か除外リスト方式（Exclude）でHTTP/1.xを扱う。
- 技術要点：nginxのmapでグローバル変数を作り、serverブロックで条件変数に応じて426を返す。426応答は「Upgradeを要求」する標準的な応答で、最終的にログを別ファイルに分けて監査する。より厳密には不要な応答（444）で接続を無視する運用も可能。
- 代表的なmapの流れ（要点のみ）：

```nginx
# nginx
map $server_protocol $is_http1 {
  default 0;
  "HTTP/1.0" 1;
  "HTTP/1.1" 1;
}

map $http_user_agent $is_text_browser {
  default 0;
  "~*^w3m" 1;
  "~*^lynx" 1;
  "~*Googlebot" 1;
  "~*bingbot" 1;
}
map "$is_http1:$is_text_browser" $http1_and_unknown {
  default 0;
  "1:0" 1;
}
```

- serverブロックでの処理例：

```nginx
# nginx (server)
if ($http1_and_unknown) {
  return 426;
}
error_page 426 @upgrade_required;
location @upgrade_required {
  internal;
  access_log /var/log/nginx/access_426.log;
  add_header Upgrade "HTTP/2" always;
  add_header Connection "Upgrade" always;
  return 426 "Upgrade required";
}
```

- テスト例（curlでHTTP/1.1を指定）：

```bash
# bash
curl --http1.1 --user-agent "" -I https://example.com/
# -> HTTP/1.1 426
curl --http2 -I https://example.com/
# -> HTTP/2 200
```

- 運用上の注意：HTTP/1.1はまだ有効な標準で、古いクライアントや一部のプレビュー用ボット（SNSやメッセンジャー）がHTTP/1.xを使うことがある。まずは除外リスト方式（問題ありそうなUAだけ弾く）で様子を見て、426ログを確認しながら許可を追加するのが無難。

## 実践ポイント
- まずはExclude方式（疑わしいUAだけをターゲット）で導入し、/var/log/nginx/access_426.logを監視する。  
- 426ログに誤ブロックがあれば該当UAを許可リストに追加する。  
- 試験環境でcurlや実際のSNSプレビューで挙動確認を必ず行う。  
- 安全に確信が持てたら、426を444にして完全に無視する運用に移行して負荷とログを削減する。  
- 日本のサービスではモバイルアプリやレガシーAPIが残ることがあるため、影響範囲を事前に洗い出すこと。

以上が要点です。導入はシンプルですが、ログ監視と段階的な調整を忘れずに。
