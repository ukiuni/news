---
  layout: post
  title: "c-from-scratch: Learn to build safety-critical systems in C - Cを一から学ぶ：安全重要システムをCで作る"
  date: 2026-01-07T11:41:58.042Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/williamofai/c-from-scratch"
  source_title: "GitHub - williamofai/c-from-scratch: Learn to build safety-critical systems in C. Prove first, code second."
  source_id: 1538942350
  excerpt: "この記事の詳細をチェック"
  image: "https://opengraph.githubassets.com/4a416d4dbad0436d4e34b927ba65a38494f60f39082bd64613d7bcd26c28817a/williamofai/c-from-scratch"
---

# c-from-scratch: Learn to build safety-critical systems in C - Cを一から学ぶ：安全重要システムをCで作る

「証明してから書く」――数学的に正しいCコードを目指すエンジニアのための実践コース

## 要約
本リポジトリは「Prove first, code second」を掲げ、問題定義→数学モデル→証明→構造体設計→実装という手順で、安全重要（safety-critical）システムをCで構築する教育プロジェクトです。Pulse（生存確認）とBaseline（統計的正常性検出）のモジュールを通じ、$O(1)$メモリで動作する有限状態機械を数学的に保証します。

## この記事を読むべき理由
日本は組込み、車載、産業制御など安全性が重視される分野が多く、形式的手法や証明主導の開発は今後さらに必要になります。本プロジェクトは「小さく証明できるコンポーネント」を作る実践的な手引きであり、ISO 26262 / IEC 61508 等の要求を意識するエンジニアに直接役立ちます。

## 詳細解説
- アプローチの核：「コードを書く前に証明する」。問題を厳密に定義し、数学モデルを作り、性質（安全性、ラiveness等）を証明してからそれを表現する構造体を設計し、最後にCへ写像する流れです。
- モジュール構成  
  - Pulse（Module 1）: プロセスが時間軸で存在するかを判定する小さな状態機械。クロックのラップやフォールトを扱い、Soundness, Liveness, Stability といった契約を証明。実装は約200行のCで、依存は標準ライブラリのみ。  
  - Baseline（Module 2）: スカラー時系列の統計的正常性検出器。指数移動平均（EMA）ベースで$O(1)$メモリ、決定論的な有限状態機械。収束性・感度・安定性・スパイク耐性などを契約で定義し、18個の契約・不変条件テストを備える。  
  - 予定されるComposition（Module 3）: Pulse と Baseline を組合せてタイミング異常検出へ。数学的に証明された信号連鎖を想定し、各モジュールは閉じていて全域的（total）、有界（$O(1)$）、決定論的です。  
  - 信号の流れは次のように表現できます:  
    $$\text{event}_t \to \text{Pulse} \to \Delta t \to \text{Baseline} \to \text{deviation}$$
- 設計原則: 各モジュールは「Closed（内部状態は直前の状態＋入力のみ依存）」「Total（常に有効な結果を返す）」「Bounded（メモリ/計算は$O(1)$）」「Deterministic（同一入力で同一出力）」「Contract-defined（振る舞いは契約で明確化）」を満たすよう設計されています。
- 実装・テスト: 各モジュールに対してmakeによるビルド、demo実行、テストが用意されています（例は後述）。

## 実践ポイント
- まずPulseから始める：基礎的概念（ラップアラウンド、タイムアウト、フォールト耐性）を学べます。ローカルで試すコマンド例:
```bash
# bash
cd projects/pulse
make
make demo
make test
```
- 契約駆動で設計する癖をつける：仕様を「期待する振る舞い（contract）」として書き出し、それを満たすデータ構造を先に設計する。これにより誤りの根本原因を減らせます。
- 小さな証明を積み重ねる：全体を一度に証明しようとせず、閉じたモジュールごとに性質を示す。組成の際は各モジュールの契約が合致することを確認する。
- リソース制約設計を重視する：組込みや車載ではメモリ・CPUが限られるため、$O(1)$設計は実務で即役立ちます。性能と証明の両立を意識する。
- 日本市場での応用例：車載ソフトウェアのヘルスモニタ、工場ラインの異常検出、IoTデバイスの自己診断ロジックなどに直接適用可能。規格対応のための形式手法導入の足掛かりにもなる。

短時間で「証明主導の設計」手法を体験したいエンジニアは、まずPulseモジュールを動かしてREADMEとPHILOSOPHYを読み、実装とテスト、そして証明の対応関係を追うことをおすすめします。
