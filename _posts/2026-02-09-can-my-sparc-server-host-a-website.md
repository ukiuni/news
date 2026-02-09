---
layout: post
title: "Can my SPARC server host a website? - SPARCサーバでウェブサイトはホストできるか？"
date: 2026-02-09T23:15:13.666Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rup12.net/posts/can-my-sparc-server-host-my-website/"
source_title: "Can my SPARC server host a website?"
source_id: 1322395669
excerpt: "25年前のSPARCをOpenBSDで動かしCloudflare経由で安全公開する方法"
image: "https://rup12.net//post-content/can-my-sparc-server-host-my-website/sun.jpeg"
---

# Can my SPARC server host a website? - SPARCサーバでウェブサイトはホストできるか？
古いSun Netra X1を現代的にネット公開したレトロ×セキュアな自宅ホスティングの挑戦

## 要約
25年前のSun Netra X1（SPARC）にOpenBSDを入れて静的サイトをhttpdで公開。ファン改造で静音化し、Cloudflare Tunnelを別ホスト経由で使ってポート開放ゼロで安全に公開している。

## この記事を読むべき理由
レトロハードを趣味で動かすだけでなく、実運用レベルで安全にインターネットに繋ぐ手順と工夫（OpenBSD選定、最小構成、トンネリングの回避策）は、日本のホムラボや個人運用者にそのまま使える実践知です。

## 詳細解説
- ハードウェア：Sun Netra X1（UltraSPARC IIe 500MHz、1GB ECC SDRAM、IDE HDD、ヘッドレス）。元は企業で使われていた個体を整備。騒音対策でNoctua 40mmファンに換装（Ciscoスイッチも同様）。  
- インストール：光学ドライブ/USBブート不可のためPXE＋TFTP＋NFSでOpenBSDを導入（詳細は別記事予定）。  
- OS選定：古いSolarisはインターネット公開にリスク大→セキュリティ重視でOpenBSD 7.8を採用。実メモリ使用量はOpenSSH起動後で約55MB。pkg_addでパッケージ管理可能（Rustも動いた）。  
- Webサーバ：OpenBSD純正のhttpdを使用。静的HTML/CSSのみで攻撃面を抑え、wwwユーザはchroot(/var/www)。設定例（ディレクトリ一覧無効、隠しファイルブロック）は下記。  

```conf
# httpd.conf
types { include "/usr/share/misc/mime.types" }
server "default" {
  listen on * port 80 root "/htdocs"
  directory no auto index
  location "/**/.*" { block return 404 }
}
```

- トンネリング（公開方法）：家庭内ゲートウェイでポート開放はしたくない→Cloudflare Tunnelを採用。問題はcloudflaredがSparc64で動かない点。解決策は、同一ネットワークの別マシン（Raspberry PiやProxmox上のLXC）にcloudflaredを入れ、トンネル先をNetraのHTTPに転送する構成。cloudflaredコンテナの設定例：  

```yaml
# /usr/local/etc/cloudflared/config.yaml
tunnel: sparc
credentials-file: /root/.cloudflared/<UUID>.json
ingress:
  - hostname: sparc.rup12.net
    service: http://192.168.1.248:80
  - service: http_status:404
```

Proxmoxでの導入は公式で配られているスクリプトを使うと簡単（ただしネットのスクリプトは事前に確認を）。例：

```bash
# Proxmoxホスト上で（実行前に内容を確認すること）
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/cloudflared.sh)"
```

- セキュリティ：pfでデフォルトdeny、SSHは自宅LANからのみ許可、httpはcloudflaredコンテナのIPからのみ許可。不要サービスは停止、動的コードやCGIは一切使わない（静的配信のみ）。Cloudflareトンネルは発信接続のみなので家庭ネットワークはインバウンド非公開。

## 実践ポイント
- レトロ機器を外に出すときは最新OS（またはセキュアなBSD系）を選ぶ。  
- 光学/USB非対応機はPXE/TFTPでインストールする方法を習得しておくと便利。  
- 騒音対策は小型Noctuaファン＋必要なら3Dパーツで置換。温度上昇には注意。  
- cloudflaredが動かないアーキテクチャは、同ネットワークの別ホスト（LXC/VM/RPi）でプロキシしてCloudflare Tunnelを利用。  
- 最小権限・最小サービス（static only）＋pfのdefault-denyで攻撃面を減らす。  
- まずは静的ページで試し、ログやアクセス解析を段階的に導入する。

以上を応用すれば、古いSPARCマシンでも安全に「家のサーバ」を外部公開できます — レトロ好きにも実運用者にも嬉しいハイブリッド。
