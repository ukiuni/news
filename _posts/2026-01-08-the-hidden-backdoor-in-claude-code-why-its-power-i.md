---
  layout: post
  title: "The Hidden Backdoor in Claude Code: Why Its Power Is Also Its Greatest Vulnerability - Claude Code に潜む裏口：強力さが招く最大の脆弱性"
  date: 2026-01-08T08:33:13.046Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.lasso.security/blog/the-hidden-backdoor-in-claude-coding-assistant"
  source_title: "Detecting Indirect Prompt Injection in Claude Code with Lasso&#x27;s Open Source Defender | Lasso Security"
  source_id: 469408015
  excerpt: "自動化フラグで裏口が有効化、プロンプト注入で全権侵害の危機—対策ツール解説"
---

# The Hidden Backdoor in Claude Code: Why Its Power Is Also Its Greatest Vulnerability - Claude Code に潜む裏口：強力さが招く最大の脆弱性
誘惑に負けるな──自動化フラグ一つで“便利”が“攻撃面”に変わる話

## 要約
Claude Code の強力な自動化機能（例：--dangerously-skip-permissions）を使うと、外部コンテンツに仕込まれた「間接的なプロンプト注入」が実行権限と結びつき、重大な侵害につながる可能性がある。Lasso のオープンソース「Prompt Injection Defender」は、ツール出力を実行前にスキャンして警告を挿入することでこのリスクを低減する。

## この記事を読むべき理由
日本の現場でも、Notion/GitHub/Slack といった外部サービス連携や自動化エージェント導入が増えています。人手を介さない高速自動化は生産性を上げますが、そのまま放置するとリポジトリやドキュメント経由でシステムに命令が入り込み、結果的に情報流出や誤操作を招きます。今すぐ理解して対策を取るべきテーマです。

## 詳細解説
- 問題の本質  
  「直接プロンプト注入」は攻撃者がAIに直接悪意ある指示を与えるケースで比較的分かりやすい。一方「間接的プロンプト注入」は、README、ウェブページ、APIレスポンス、コードコメント、チケット文面など、AIが読む“コンテンツ”に悪意ある指示を埋め込み、AIがそれをユーザー指示と誤認して実行してしまう点が悪質です。特に --dangerously-skip-permissions のように確認を外した自動化は「人間のブレーキ」を失い、成功率が飛躍的に上がります。

- 攻撃シナリオ（代表例）
  1. 毒されたリポジトリ：クローンしたライブラリ内の Markdown やコメントに命令を埋める。  
  2. 改竄されたドキュメント：外部サイトやAPIに偽の指示を追加。  
  3. MCP（Notion等）経由の侵入：コラボレーションツール内に攻撃者が書き込むことで信頼境界を突破。

- 攻撃手法のカテゴリ（Lasso の分類）
  1. Instruction Override（以前の指示を無視させる）  
  2. Role-Playing / Jailbreak（DAN 等）  
  3. Encoding / Obfuscation（Base64、ゼロ幅文字、ホモグリフ等で隠す）  
  4. Context Manipulation（偽権威やHTMLコメント、JSON内のシステムメッセージ風記載）

- 既存防御の限界  
  モデル側の耐性はあるが完璧ではなく、文脈次第で誤判定が起きやすい。量をかけた試行や巧妙なエンコーディングで突破されるリスクが残る。自動化フラグで人間チェックを外すと致命的。

- Lasso の Defender（設計と動作）  
  Claude Code の PostToolUse フックとして動作し、ファイル読み取り・ウェブフェッチ・MCP応答などツール出力を Claude が処理する前に横取りしてスキャン。50+ の正規表現パターンで検出し、検出時はコンテキストに「目立つ警告」を挿入して処理を継続する（ブロックしない）。警告には重大度（HIGH/MEDIUM/LOW）を付与。

- エンタープライズ運用  
  管理下の設定（Admin Console やファイルベース）で強制配布でき、allowManagedHooksOnly を有効にすればユーザー側のフック無効化を防げる。設定の優先順位も明確化されているため大規模組織向けに有用。

## 実践ポイント
- 原則：最小権限で運用する  
  --dangerously-skip-permissions の常時使用は避け、必要最小限に限定する。可能なら手動承認を残す。

- MCP 接続を信頼しすぎない  
  Notion/GitHub/Slack 等は信頼境界として扱い、アクセス範囲と読み取るデータを最小化する。第三者編集の履歴と権限を監査する。

- ランタイムスキャンを導入する  
  Lasso の Prompt Injection Defender のような PostToolUse スキャンを導入すると、実行前に問題の兆候を検出できる。Python/TypeScript 実装があるため導入は短時間で可能。

- 運用ルール（エンタープライズ）  
  管理者が強制配布する設定を利用して全社適用。allowManagedHooksOnly の利用でローカル回避を防ぐ。

- 継続的メンテナンス  
  検出パターンは進化するため、patterns.yaml 相当の定義を定期的に更新し、誤検知（False Positive）対応フローを整備する。

日本の開発現場では効率化の波が強いぶん、自動化フラグの“誘惑”に陥りやすいです。便利さを享受しつつ、今回紹介したようなランタイム防御と運用ルールで「自動化の安全性」を守ることが急務です。
