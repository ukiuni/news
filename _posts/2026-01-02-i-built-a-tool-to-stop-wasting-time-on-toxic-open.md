---
  layout: post
  title: "I Built a Tool to Stop Wasting Time on Toxic Open Source Projects - 有害なOSSに時間を浪費しないツールを作った"
  date: 2026-01-02T12:02:21.414Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://dev.to/elsad_humbetli_0971c995ce/i-built-a-tool-to-stop-wasting-time-on-toxic-open-source-projects-5h12"
  source_title: "I Built a Tool to Stop Wasting Time on Toxic Open Source Projects - DEV Community"
  source_id: 3132617
  excerpt: "OSS貢献前に時間泥棒プロジェクトを数値化とLLM補正で見抜く無料ツールの作り方"
  image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fa0trpwer0c3aa6bxywvd.png"
---

# I Built a Tool to Stop Wasting Time on Toxic Open Source Projects - 有害なOSSに時間を浪費しないツールを作った
オープンソース「当たり外れ」を見抜く──時間を奪うプロジェクトを避けるための実践ガイド

## 要約
GitHubリポジトリの「健全度」を数値化し、言語モデルで文脈を補正することで、貢献前に無駄な労力を避けられるツール（repo-health）を作ったという話。活動指標・PRやIssueの挙動・ファイル構造と問題の紐付けを組み合わせて判断する。

## この記事を読むべき理由
日本のエンジニアや学生でも、見た目は活発でも「貢献しても反応がない」「Botばかり」などで時間を浪費する経験があるはず。プロジェクト選定の体系化は効率的な学習・査読・採用候補の見極めに直結するため、具体的手法を知る価値が高い。

## 詳細解説
主な要素と技術スタック
- フロント: Next.js 16、React 19、Chakra UI  
- バックエンド: tRPC、Octokit（GitHub API）、Zod  
- データ: MySQL（Prisma）、Redis

スコアリング（0-100）
- 基本はCHAOSS的指標を参考に設計した重み付き平均。
$$Score = 0.3\times Activity + 0.25\times Maintenance + 0.2\times Community + 0.25\times Docs$$
  - Activity (30%): コミット頻度、最新更新日、作者の多様性  
  - Maintenance (25%): Issue応答時間、未解決比率、リポジトリ年齢  
  - Community (20%): Stars・Forksの対数スケール  
  - Docs (25%): README / LICENSE / CONTRIBUTING の有無

言語モデルによる補正
- 定量指標だけでは「完成してて安定＝活動が少ない」プロジェクトを誤分類するため、READMEやファイル構造をLLMに与え、スコアを最大±20点で調整する。MVPではコストと速度の観点からGPT-4 Miniを採用。

PR / Issue の深掘り
- PRメトリクス: 平均マージ時間、Botによる自動レビューの頻度、新規貢献者の定着率を可視化。Sankey図で貢献フローを示すことで「初回→継続」しているかを把握。
- 並列取得: Open/Closed PR やテンプレチェックは Promise.all で同時に取る例で高速化。
```javascript
// javascript
const [openPRs, closedPRs, template] = await Promise.all([
  fetchPRs(octokit, { owner, repo, state: "open" }),
  fetchPRs(octokit, { owner, repo, state: "closed" }),
  checkPRTemplate(octokit, { owner, repo }),
]);
```
- Issue解析: 平均クローズ時間（中央値も併用）、直近48時間で活発な「Hot Issues」、古くて影響度の高い「Hidden Gems」、難易度推定の「Crackability Score」。

プロジェクト構成の案内
- GitHubのツリーを再帰取得し、LLMに「エントリポイント」「主要ファイル」「機能別フォルダ」を解説させることで初学者が迷わず着手できるようにする。
```typescript
// typescript: issue内のファイルパス抽出（例）
const FILE_PATTERN = /[\w\-\/\.]+\.(ts|tsx|js|jsx|py|go|rs|java|cpp|c)/gi;
function extractFilePaths(text: string): string[] {
  return [...new Set(text.match(FILE_PATTERN) || [])];
}
```

検知して切り捨てた機能
- 秘密情報検出（Gitleaks風のregex＋ランダム文字列検知）は技術的に面白かったが、コミュニティ健全度というコア目的から外れるためMVPからは削除。

その他の挙動検出
- 大量削除（churn）や短時間大量コミットなどの疑わしいパターンを統計で検出し、スパム的な活動を可視化。

## 実践ポイント
- まず見るべきは「マージまでの平均時間」と「最近のIssue応答速度」。短ければ貢献のリターンは高い。  
- READMEとCONTRIBUTINGが整っているかで精神的コストが大きく変わる。存在なし＝高確率で時間を取られる。  
- 「活動が少ない＝死んでいる」ではない。ライブラリやユーティリティは安定稼働のためあえて更新が少ない場合がある。READMEやファイル構造を確認して判断を補完する。  
- 初回貢献は「Hidden Gems（古いが影響が大きいIssue）」や Crackability が低いチケットを狙うと成功率が高い。  
- チームでOSS貢献を勧めるなら、リポジトリ選定に今回のようなスコア基準を導入すると新人の学習効率が上がる。

