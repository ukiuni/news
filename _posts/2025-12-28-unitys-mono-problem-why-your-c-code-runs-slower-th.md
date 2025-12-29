---
layout: post
title: 'Unity''s Mono problem: Why your C# code runs slower than it should'
date: 2025-12-28 23:16:41.940000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://marekfiser.com/blog/mono-vs-dot-net-in-unity/
source_title: 'Unity''s Mono problem: Why your C# code runs slower than it should
  | Marek''s blog'
source_id: 46414819
excerpt: UnityのMonoは最新.NETより数倍遅く、移行やロジック分離で劇的に改善可能
---
# Unityの「見えない負荷」を暴く：Monoが遅い本当の理由と今すぐできる対策

## 要約
Unityのランタイムで動くC#は、最新の.NETランタイム（CoreCLR/.NET 10など）と比べて大幅に遅いことが実測で示されている。起動やシミュレーションで2–3倍、特定ケースでは最大15倍の差が出ることもある。

## この記事を読むべき理由
日本のゲームスタジオやUnityで重いロジックを書くエンジニアにとって、ランタイム性能差は開発速度・デバッグ効率・コストに直結する。CoreCLR導入の有無や対処法を知ることで、短期的な生産性改善と長期的なアーキテクチャ準備が可能になる。

## 詳細解説
- 問題の本質  
  Unityは長年Monoランタイムを採用してきたが、Microsoftが.NET Core/.NET（CoreCLR）を積極的に進化させた結果、JIT最適化・コンパイラ最適化・ランタイムAPIが大幅に改善された。Monoはこれら最適化の多くを取り込めておらず、特にJITによるコード生成能力で大きく遅れを取っている。

- 実測ベンチマーク（抜粋）  
  - Unity Editor（Debug）: 100秒  
  - .NET unit test（Debug）: 38秒  
  - Unity standalone（Mono, Release）: 30秒  
  - .NET standalone（Release）: 12秒  
  以上より、一般的な期待値として1.5–3×の高速化が見込め、特殊ケースでは最大で15×という極端な差も観測されている。

- 技術的原因の例  
  - インライン化の失敗やループ不変式のホイスティングがMonoではされず、レジスタを使わずメモリを多用するコード生成になる。  
  - 小さな値型（struct）を扱う際、Monoはフィールドをメモリに保存して読み書きする一方、最新のJITはスカラー化してレジスタで処理する。  
  - 新しいランタイムではSpan<T>やSIMD、ハードウェア・イントリンシックなどの最適化パスが使えるが、Monoではこれらが十分に活かせない。  
  - Unity独自の対策としてBurstコンパイラやIL2CPPがあるが、Burstはサポート対象が制限され、IL2CPPは別ルートでAOTを行うためCoreCLRが解決する問題とは扱いが異なる。

- Unityのロードマップと影響  
  UnityはCoreCLR移行を進めているが、記事時点ではプロダクション導入はまだ先（6.xへの計画はあるが時期未定）。CoreCLRが実用化されれば、ランタイム性能の改善だけでなく編集/イテレーション速度、GC挙動、AOT選択肢の幅が広がる。

## 実践ポイント
- まず「分離可能なロジック」を切り出す  
  シミュレーションやビジネスロジックをUnity依存から切り離し、通常の.NETランタイムでユニットテストを回すことで、デバッグ/プロファイルが数倍速くなる。起動待ち・ドメインリロードを回避できる。

- ホットパスの計測と小さな値型の見直し  
  プロファイラでホットループを特定し、structの使い方や演算のインライン化が効くか確認する。Monoでの非効率が疑われる部分は、シンプルなクラス/プリミティブに置き換えて影響を測る。

- Burst／IL2CPPを賢く使う  
  Burstは効果的だが制約があるため、使える処理に限定して導入する。モバイル/iOS向けはIL2CPP/AOTが必須なので、その最適化フローを整備する。

- 新しいAPIに備える設計  
  Span<T>やSIMDを利用できる設計にコードベースを段階的に対応させておくと、CoreCLR導入時に速やかに恩恵を受けられる。

- 開発プロセスの改善  
  小さな単位でのロジックテスト、CIでのネイティブ/.NETベンチ、プロファイル自動化を導入して、ランタイム差による「見えない税」を早期に発見する。

