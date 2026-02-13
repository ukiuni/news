---
layout: post
title: "Nixtamal 1.0.0 released - Nixtamal 1.0.0 リリース"
date: 2026-02-13T18:06:02.092Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nixtamal.toast.al/changelog/"
source_title: "Changelog | Nixtamal"
source_id: 1246156961
excerpt: "Nixtamal 1.0.0でスキーマ安定化とFossil対応、TUI改善でNix運用が楽に。"
---

# Nixtamal 1.0.0 released - Nixtamal 1.0.0 リリース
Nix運用がもっと扱いやすくなる――スキーマ安定化とFossil対応、使いやすいTUIで現場の作業負荷を下げるNixtamal 1.0.0

## 要約
Nixtamalが1.0.0に到達し、スキーマの正式化（1.0.0化）、`nixtamal upgrade`によるスキーマ移行サポート、Fossil対応、TUIの不具合修正など運用面の改善を中心に多数の実装・修正が入っています。

## この記事を読むべき理由
NixtamalはNixベースの環境やロックファイル管理を扱うツールで、日本の開発現場でもNixやマルチVCS運用（Git＋その他）を使う場面が増えています。今回の安定化は移行コスト低減やmacOS上でのビルド安定化につながるため、Nix運用担当者やパッケージ管理を気にするエンジニアは注目すべきです。

## 詳細解説
- スキーマ安定化：バージョンが1.0.0化され、仕様の基盤が固められました。これに伴いスキーマ移行用の `nixtamal upgrade` コマンドが追加されています。
- VCSサポート拡張：Fossilのサポートを追加。Git周りも改善され、ロックファイル内のrefを正しく使ってrevを取得するようになり、タグのサポートも追加されました（以前はrevの過負荷利用があった点を解消）。
- TUI（ターミナルUI）：0.3.0-betaでTUIが導入され、1.0.0でTUIの取り扱いに関する複数のバグが修正されています。ユーザーインタラクションが改善され、操作性が向上。
- フェッチ周り：`nixtamal show`にfetch-time表示が追加。fetchを評価時（builtins.fetch*）かビルド時（pkgs.fetch*）で行う選択肢や、fetch-gitのタイポ修正など、外部リソース取得の挙動が明確化されました。
- プラットフォーム対応：macOS（Darwin）上でのNixビルド修正が含まれ、ローカルでの動作検証がしやすくなっています。
- その他：loaderの名前変更（nixpkgs→bootstrap-nixpkgs）、不要なOCaml参照の除去、サイトやドキュメント生成にNix/Nickel/Soupault等を使用。スキーマ移行には一部手動手順（旧lock.jsonやdefault.nixの削除、manifest.kdlのバージョン調整、再度 `nixtamal lock` 実行）が必要な場合があります。

## 実践ポイント
- まず `nixtamal upgrade` を試し、移行ガイドの指示に従う（必要ならバックアップを取る）。
- 自動で移行されない場合は旧ファイル（例: lock.json, default.nix）を退避して `nixtamal lock` を再実行する。
- Gitでタグ運用しているプロジェクトはロックファイルを再生成してタグ参照が正しく解決されるか確認する。
- macOSでNixを使っている場合はビルド確認を行い、問題が出たら修正ログを参照する。
- Fossilを使う組織は新サポートを試し、既存ワークフローとの互換性を検証する。

元ソース（英語）: "Nixtamal 1.0.0 released"（公式Changelog）
