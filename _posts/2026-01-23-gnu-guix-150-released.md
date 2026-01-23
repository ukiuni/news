---
layout: post
title: "GNU Guix 1.5.0 released - GNU Guix 1.5.0 リリース"
date: 2026-01-23T14:53:25.970Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://guix.gnu.org/en/blog/2026/gnu-guix-1.5.0-released/"
source_title: "GNU Guix 1.5.0 released"
source_id: 702636036
excerpt: "Guix 1.5.0公開、rootless標準化とSBOM対応でセキュリティを大幅強化。"
---

# GNU Guix 1.5.0 released - GNU Guix 1.5.0 リリース
魅力タイトル: 「使いやすさと安全性が大幅強化されたGNU Guix 1.5.0──いま試すべき理由」

## 要約
Guix 1.5.0が公開され、ルート不要デーモン（rootless）標準化、Codeberg移行・合意形成プロセスの導入、膨大なパッケージ追加やデスクトップ・サービス改善、SBOM出力やフルソース・ブートストラップの拡充など、セキュリティと再現性を重視した大規模アップデートが入った。

## この記事を読むべき理由
パッケージ管理・システム構成の再現性やセキュリティを重視する開発者・運用者、日本の組込み／EDA／HPC分野の実務者にとって、Guixの新機能はすぐ実務で役立つ選択肢とツール群を提供します。既存のLinux上に導入できるため導入ハードルも低いです。

## 詳細解説
- リリース形態と入手
  - ISO/VMイメージ、ソース/バイナリのtarballを提供。既存ユーザーは guix pull で更新可能。
- ガバナンスと開発プロセス
  - 合意ベースの決定プロセス（GCD）採用、Codebergへのリポジトリ移行、年間リリースプロセスの導入で貢献・変更が明確に。
- システム／デスクトップ面の強化
  - KDE Plasma 6.5対応、GNOME 46（Waylandデフォルト）、GNU Shepherd 1.0採用（タイムドサービス、kexec、ログ管理の改善）。
  - 約12,500の新規パッケージ追加、主要ソフトの更新（GCC 15.2、Emacs 30.2、LLVM 21、Linux-libre 6.17 など）。
- サービス・セキュリティ
  - 多数の新しいシステムサービス（Forgejo Runner、RabbitMQ、iwd、dhcpcd 等）。
  - setuid-programs → privileged-programs に変更し Linux capabilities をサポート。
  - デーモンの rootless 実行がデフォルト（非 Guix System）。AppArmor プロファイルを同梱。
  - 複数のCVEに対する修正適用。
- ビルドの再現性（フルソース・ブートストラップ）
  - Zig と Mono のフルソースブートストラップを追加。信頼の連鎖（trusting trust）問題に対処する取り組みを継続。
- CLI と配布ツールの拡張
  - guix graph に GraphML / CycloneDX 出力で SBOM 作成が可能。
  - guix shell に --nesting / --emulate-fhs、guix pack に RPM/AppImage バックエンド、guix locate 追加。
- アーキテクチャ対応
  - riscv64 用のリリース tarball、x86_64-gnu（Hurd）向け実験的サポート強化。
- コミュニティ
  - チーム制で 50 チームが言語・分野ごとに活動（Python/Rust/Zig、EDA、HPC、科学等）。
- 資金面
  - ビルドファームやインフラ維持のための募金キャンペーン継続中。

## 実践ポイント
- まず試す：既存ユーザーはターミナルで guix pull。新規は公式ダウンロードページからISOやインストーラを入手。
- rootless を試す：非 Guix System 環境ではデフォルトで有効。Guix System で有効にするなら guix-configuration に `(privileged? #f)` を設定。
- SBOM／配布：ソフトを外部に配るなら guix graph（CycloneDX）でSBOM、guix pack でAppImage/RPM化を活用。
- 開発環境：guix shell --nesting や --emulate-fhs でコンテナ内にGuix環境を持ち込みやすくなる。
- セキュリティ確認：AppArmor が必要な環境では同梱プロファイルを確認。重要な修正はリリースノートのCVE一覧を参照。
- 関わる／支援する：パッケージ追加や翻訳、インフラ支援を検討するなら Codeberg のリポジトリや募金ページへ。

元記事全文やダウンロードは公式ページ（https://guix.gnu.org/en/blog/2026/gnu-guix-1.5.0-released/）を参照してください。
