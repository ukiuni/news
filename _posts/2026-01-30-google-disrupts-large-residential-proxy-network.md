---
layout: post
title: "Google Disrupts Large Residential Proxy Network - 世界最大級の「住宅プロキシ」ネットワークを切断"
date: 2026-01-30T13:58:00.414Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cloud.google.com/blog/topics/threat-intelligence/disrupting-largest-residential-proxy-network"
source_title: "Disrupting the World&#39;s Largest Residential Proxy Network | Google Cloud Blog"
source_id: 1152318783
excerpt: "Googleが数百万台規模の住宅プロキシ網を壊滅、あなたの端末も踏み台に？"
image: "https://storage.googleapis.com/gweb-cloudblog-publish/images/03_ThreatIntelligenceWebsiteBannerIdeas_BA.max-2600x2600.png"
---

# Google Disrupts Large Residential Proxy Network - 世界最大級の「住宅プロキシ」ネットワークを切断
あなたのスマホが踏み台に？数百万台を売る“住宅プロキシ”網をGoogleが壊滅へ

## 要約
Google Threat Intelligence Group は、IPIDEA と呼ばれる世界最大級の住宅プロキシネットワークを標的にし、ドメイン差し止めや脅威インテリの共有、Play Protect を通したアプリ除去などで、数百万台分の利用可能デバイスを減らす措置を実施しました。

## この記事を読むべき理由
住宅プロキシは一般消費者の端末を第三者のトラフィック中継に使い、ボットネット・スパイ活動・不正ログインの隠れ蓑になります。日本でもスマホやIoTが標的になり得るため、開発者・セキュリティ担当・一般利用者いずれにも重要な警鐘です。

## 詳細解説
- 住宅プロキシとは：ISP が割り当てる家庭や小規模事業者のIPを経由させるプロキシ。攻撃者は実際のユーザーIPを使うことで追跡やブロックを難しくする。  
- IPIDEA の仕組み：開発者向けに配布される SDK（Castar/ Earn/ Hex/ Packet など）をアプリへ埋め込み、端末を「出口ノード（exit node）」として登録することで巨大なプロキシプールを形成する。ユーザーは知らずに参加する場合が多い。  
- コマンド＆コントロール（C2）：二層構成で、Tier One（ドメイン経由で設定とTier Twoノード情報を取得）→ Tier Two（IP:port で定期ポーリングし、プロキシタスクを受ける）。解析では約7,400台のTier Twoノードが確認され、世界中でスケールしていた。  
- 悪用例：ボットネット（BadBox2.0 等）、スパイ活動、SaaS 侵害、パスワードスプレーなど多数の脅威グループがこれを利用。端末所有者には不正活動の踏み台にされるだけでなく、自身のネットワークが露出するリスクがある。  
- Google の対策：法的差し止め、SDK とプロキシソフトの検出情報共有、Google Play Protect による自動警告／削除と新規インストール阻止。結果としてIPIDEAの運用と拡大能力が大幅に低下したと報告されている。  
- 関連ブランド例（調査で関連が指摘されたもの）：360 Proxy、922 Proxy、ABC Proxy、Cherry Proxy、Door VPN、Galleon VPN、Ipidea、Luna Proxy、PIA S5 Proxy、Radish VPN、Tab Proxy 等。

## 実践ポイント
- 一般ユーザー
  - 不要なアプリや提供元不明のVPNアプリは削除。未知の権限（ネットワーク中継権限など）に注意。  
  - Android は Play Protect を有効にし、OS・アプリを最新に保つ。サイドロードは最小限に。  
  - 家庭内ネットワークで不審な挙動（回線負荷、未知のポートアクセス）があれば再起動・初期化やルータログ確認を検討。
- 開発者／アプリ運営者
  - 外部SDKや広告SDKを導入する前にソース／挙動を精査。ライブラリの出所とビジネスモデルを確認。  
  - ネットワークの出口監視・Egress フィルタリング、通信先のホワイトリスト化を行う。  
  - モバイルアプリの権限最小化と透明なユーザー説明を実施。マネタイズ手法が「帯域提供」を謳う場合は要警戒。  
- 企業セキュリティ担当
  - 社内デバイスのインベントリとインストールアプリの監視を強化。エンドポイント検出でC2通信の兆候（定期ポーリング、未知IP:portへの接続）を探す。  
  - MDM/EMM を使って信頼できないアプリをブロックし、フローの可視化を導入する。  
- 報告：疑わしいアプリやドメインを見つけたらベンダーやプロバイダに通報することで同様の対策を促進可能。

短く言えば、「知らぬ間にあなたの端末が他人の攻撃の踏み台になっている」可能性があり、最低限のアプリ管理とネットワーク監視で被害予防が可能です。
