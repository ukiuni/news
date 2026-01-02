---
  layout: post
  title: "NASA's Largest Library To Permanently Close On Jan 2, Books Will Be 'Tossed Away' - NASA最大の図書館が1月2日に永久閉鎖、書籍が「廃棄」へ"
  date: 2026-01-02T11:09:07.746Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.ndtv.com/world-news/nasas-largest-library-to-permanently-close-on-jan-2-books-will-be-tossed-away-10170584"
  source_title: "NASA's Largest Library To Permanently Close On Jan 2, Books Will Be 'Tossed Away'"
  source_id: 473021215
  excerpt: "NASA最大の図書館が1月2日閉館、希少な技術資料が廃棄され研究継続に危機"
  image: "https://c.ndtvimg.com/2026-01/m0dnlhe8_nasa_625x300_01_January_26.jpg?im=FeatureCrop,algorithm=dnn,width=1200,height=738"
---

# NASA's Largest Library To Permanently Close On Jan 2, Books Will Be 'Tossed Away' - NASA最大の図書館が1月2日に永久閉鎖、書籍が「廃棄」へ
NASA図書館閉鎖が突きつける「データ保全の空白」 — エンジニアが今すぐ確認すべき4つの手順

## 要約
報道によれば、NASAの最大規模の図書館が1月2日に永久閉鎖され、所蔵物の一部が廃棄される可能性があるとされています。物理資料とテクニカルリポートの消失は、研究の再現性や長期アーカイブに大きな影響を与えます。

## この記事を読むべき理由
日本の研究者・エンジニアにとって、NASAは重要なデータ供給源であり多くの論文や設計資料が参照されています。海外機関のアーカイブ消失は、参照元が突如消えるリスクと、国際共同研究やプロジェクトのデータ管理方針を見直す必要性を教えてくれます。

## 詳細解説
- 何が問題か：NASAの図書館閉鎖は単なる本の移動ではなく、ミッションレポート、設計図、技術メモ、灰色文献（gray literature）といった「公式だが商業流通していない」重要資料の扱いに関する問題を露呈します。これらはしばしばオンラインで完全に置き換えられていないため、物理的消失は知識の断絶につながります。
- 失われやすい資産の種類：レアなミッション記録、未公開の技術仕様、複雑な図面、古いフォーマット（マイクロフィッシュ、磁気テープ）など。これらは劣化や読み取り装置の消失で二度と復元できなくなる恐れがあります。
- 技術的な対策（要点）：
  - デジタル化フォーマット：原本アーカイブ用は高解像度TIFF（非圧縮）、配信用はPDF/A＋OCR、マスターは原文スキャン＋メタデータ（METS/PREMIS/Dublin Core）。
  - 永続識別子：DOIやHandle、ARKなどで文献を恒久的に参照可能にする。
  - メタデータ＆カタログ化：MARCからJSON-LDへの変換、OAI-PMHでの公開、SRU/SRWによる検索インタフェース提供。
  - 保管と分散：OAIS準拠のアーキテクチャ、チェックサムによるfixity検証、分散レプリカ（LOCKSS/CLOCKSS、インターネットアーカイブ、学術機関リポジトリ）で単一障害点を排除。
  - 権利処理：著作権・ライセンスを整理して公開可能なものは速やかにオープン化する。非公開資料はアクセス条件を明確化。

## 実践ポイント
- 速攻でやるべきこと（個人／機関別）
  1. 参照しているNASA文献のリストを作る（DOI・URL・所蔵情報を記録）。重要資料はローカルにバックアップを保存。
  2. 所属機関図書館に連絡し、同様のリスクがないか確認。JAXAや大学図書館と共同でレプリケーションを検討する。
  3. データ管理計画（DMP）を更新し、外部リポジトリや永続識別子の利用を必須項目にする。
  4. 技術者向け：重要設計資料やプロジェクト報告書はPDF/A/TIFFで保管し、メタデータ（作成日、バージョン、参照元）を付与する。
  5. 組織的対応：希少コレクションは優先順位を決めてデジタル化資金を割り当て、国際的なアーカイブ組織へ協力を依頼する。

