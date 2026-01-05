---
  layout: post
  title: "Setting up a public URL that flashes my office lights - オフィスのライトを点滅させる公開URLの作り方"
  date: 2026-01-05T20:38:52.786Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://dev.to/peter/setting-up-a-public-url-that-flashes-my-office-lights-218i"
  source_title: "Setting up a public URL that flashes my office lights - DEV Community"
  source_id: 3150931
  excerpt: "TailscaleとVPSで安全にWebhook公開し、ワンクリックでライトを赤点滅"
  image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fa914ct1o2npckkdwhobm.png"
---

# Setting up a public URL that flashes my office lights - オフィスのライトを点滅させる公開URLの作り方
ワンクリックでオフィスのライトを「赤く点滅」させる公開エンドポイントを、安全に作る手順と注意点

## 要約
Raspberry Pi上のHome Assistantをローカルに残しつつ、DigitalOcean等の小さなVPSを公開受け口にしてTailscaleで安全に接続し、認証付きWebhookからライトを点滅させる仕組みを構築する手法を紹介する。

## この記事を読むべき理由
在宅勤務や分散チームで「目に見える通知」が欲しい場面は増えている。直接Home Assistantを公開せず、VPNと短期トークンで安全に外部トリガーを受けられる実用的なアーキテクチャは、日本のスタートアップや個人開発者にもすぐ応用できる。

## 詳細解説
アーキテクチャ（簡潔）
- クラウド（VPS, 公開URL）→ nginx → Flask webhook（認証）→ Tailscale → Raspberry Pi → Home Assistant API → ライト操作

主要ポイント
- なぜTailscale: 自宅ネットワークを直接ポート開放せず、100.x.x.xのプライベートIPで安全に疎通できるため。VPNのメッシュでルーティングが簡単。
- VPSの役割: HTTPS終端と認証付きWebhookを受ける公開受け口。短いJSONトークンでユーザー管理し、侵害時は即削除可能。
- ライト制御スクリプト: 点滅前に現在の状態（on/off、brightness、色モードやxy_color）を取得して保存し、赤で点滅させた後に元の状態へ復帰させる必要がある。色モードの違い（RGB vs XY）を考慮しないと復帰に失敗する。
- 実装上の注意: GETは意図せず実行される可能性があるため状態変更にはPOSTを利用。HTTPS、トークンの取り扱い、レート制限、ログ記録で安全性を高める。

使われる技術スタック（例）
- Home Assistant（Raspberry Pi）
- Tailscale（Pi と VPS 両方にインストール）
- VPS（例: DigitalOcean droplet）で nginx + Flask
- SSH鍵を使ったPiへのリモートコマンド実行
- systemdでサービス化して永続化

自動化補助
- 設定を短時間でまとめるために、SSHでのコマンド投入やスクリプト生成を自動化ツール（例: Claude等）で補助するケースもある。

## 実践ポイント
- 必要なもの
  - Home Assistant稼働のRaspberry Pi
  - 小額VPS（公開受け口）
  - Tailscaleアカウント（PiとVPSにインストール）
  - SSH鍵と最小限のスクリプト / Flaskアプリ

- 手順（概略）
  1. PiとVPSにTailscaleを導入し互いに疎通確認する。
  2. VPS上でnginxをHTTPS終端に設定し、Flaskアプリをリバースプロキシで公開する。
  3. トークン管理用JSONを用意し、WebhookはPOSTでトークン検証する。
  4. VPSからTailscale経由でPiにSSH接続できるように公開鍵を配置する。
  5. Pi上で点滅スクリプトを用意：事前に状態を取得→赤で点滅→元の状態へ復帰。色情報（xy_color等）も保存する。
  6. systemdでサービス化し、ログとレート制限を追加する。

- 最低限の実装例（イメージ）
```bash
# bash - 点滅の流れ（要環境に合わせて調整）
STATE=$(curl -s -H "Authorization: Bearer $HA_TOKEN" http://localhost:8123/api/states/light.office)
BRIGHT=$(echo "$STATE" | jq -r '.attributes.brightness // 255')
XY_X=$(echo "$STATE" | jq -r '.attributes.xy_color[0] // empty')
XY_Y=$(echo "$STATE" | jq -r '.attributes.xy_color[1] // empty')

# 赤で点灯
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -d '{"entity_id":"light.office","rgb_color":[255,0,0],"brightness":255}' http://localhost:8123/api/services/light/turn_on
sleep 1

# 元に戻す（XY情報があれば優先）
if [ -n "$XY_X" ]; then
  curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -d "{\"entity_id\":\"light.office\",\"brightness\":$BRIGHT,\"xy_color\":[$XY_X,$XY_Y]}" http://localhost:8123/api/services/light/turn_on
else
  curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -d "{\"entity_id\":\"light.office\",\"brightness\":$BRIGHT}" http://localhost:8123/api/services/light/turn_on
fi
```

```python
# python - Webhookの概念（Flask）
from flask import Flask, request, jsonify
app = Flask(__name__)
TOKENS = {"alice-token-123": {"name": "Alice"}}

@app.route('/flash-office', methods=['POST'])
def flash():
    token = request.form.get('auth_token') or request.json.get('auth_token')
    if not token or token not in TOKENS:
        return jsonify({"error":"invalid token"}), 403
    # SSH経由でPi上のスクリプトを実行（例: subprocessでsshコマンド）
    return jsonify({"status":"flashed","user":TOKENS[token]["name"]})
```

- セキュリティ＆運用のヒント
  - 公開URLは必ずHTTPSにする（Cloudflare等の利用も有効）。
  - POSTを採用し、Content-TypeやCSRFを考慮する。
  - トークンはユーザー単位で発行・削除可能にし、可能なら短期トークンや署名付きURLを検討。
  - レート制限とログを導入して濫用を防止。
  - 会社で使う場合はSlack連携に認証フローや利用規約の周知を。

日本の読者への一言
- オフィスの「視覚的通知」はリモート中心の働き方で意外に有効。Tailscale経由で自宅・オフィスのIoTを安全に公開する手法は、個人ユースだけでなく小さなオフィスの運用改善にも使える。まずはローカルでスクリプトとAPIのやり取りを確認してから公開層の構築に進むと安全で確実。
