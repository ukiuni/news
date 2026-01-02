---
  layout: post
  title: "Why users cannot create Issues directly (Ghostty) - なぜユーザーはIssueを直接作成できないのか（Ghostty）"
  date: 2026-01-02T03:11:59.817Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/ghostty-org/ghostty/issues/3558"
  source_title: "Why users cannot create Issues directly · Issue #3558 · ghostty-org/ghostty · GitHub"
  source_id: 46460319
  excerpt: "GhosttyがIssue禁止、Discussions先行で無駄報告を削減する運営法"
  image: "https://opengraph.githubassets.com/4cfd6d53bf09b6cf107374eb07cf115de75cbbc602c83f64c5358798bf44e622/ghostty-org/ghostty/issues/3558"
---

# Why users cannot create Issues directly (Ghostty) - なぜユーザーはIssueを直接作成できないのか（Ghostty）
メンテナが明かす「Issue封印」の理由と、Discussion優先ワークフローでプロジェクトが劇的に効率化する仕組み

## 要約
GhosttyはIssueを直接受け付けず、まずGitHub Discussionsでやり取りしてからメンテナが「実行可能な課題」と判断したものだけをIssueへ移すポリシーを採っています。これによりノイズを減らし、着手可能なタスクだけをIssueに残します。

## この記事を読むべき理由
OSS運営や外部貢献をする日本のエンジニアにとって、単にバグを投げるだけでは動かないOSSプロジェクトが増えています。Ghosttyの方針は、労力を節約して品質を上げる実務的な運用例なので、報告の仕方や貢献の効率化に直結する知見が得られます。

## 詳細解説
- ポリシーの中核
  - 「Issueは最終的に作業可能な状態のものだけ」：議論→確認→Issue化という流れを明確にしている。
  - 理由として、長年の運営経験から80〜90%の報告が誤解、環境依存、設定ミスなどであり、多くが単なる機能要望や不十分な情報であると観察している点を挙げている。

- メリット
  - メンテナの時間節約：Issueトラッカーに残るものは既に検証済みで、すぐ着手できる。
  - バックログの品質向上：未調査の要求や再現不能な報告で埋まらない。
  - 貢献者の心理的ハードルを下げる：議論ベースなら相談しやすい。

- 実務上の運用
  - Discussionsで仕様検討や現象の切り分けを行い、再現性や影響範囲が確定したらメンテナがIssueへ移す。
  - CONTRIBUTING.mdに手順が示されているため、従うことで無駄なやり取りを減らせる。

## 実践ポイント
すぐ使えるチェックリスト（Ghosttyや他プロジェクトへ報告する際に有効）
- まずDiscussionを作る：疑問・報告・提案はDiscussionが定位置と仮定する。
- 再現手順を明確に：最小限の再現コード、OS/バージョン、設定ファイル、ログを添付する。
- 期待値と実際の挙動を比較：スクリーンショットやログ抜粋を含める。
- 環境依存の可能性を検証：別マシンやクリーン環境での挙動を確認する。
- 要望は具体化する：仕様変更や新機能ならユースケースと設計案を添える。
- Issue化を望む場合：Discussion内で「これは再現でき、作業に値する問題です」と結論づけることでメンテナがIssueに移しやすくなる。
- プロジェクトのCONTRIBUTING.mdを必ず確認：プロジェクト固有の手順やテンプレが載っている。

## 引用元
- タイトル: Why users cannot create Issues directly (Ghostty)  
- URL: https://github.com/ghostty-org/ghostty/issues/3558
