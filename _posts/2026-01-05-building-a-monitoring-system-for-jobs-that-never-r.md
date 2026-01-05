---
  layout: post
  title: "Building a Monitoring System for Jobs That Never Ran - 「走らなかったジョブ」を検出する監視システムの作り方"
  date: 2026-01-05T06:11:48.387Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.vincentlakatos.com/blog/building-a-monitoring-system-that-catches-silent-failures/"
  source_title: "Building A Monitoring System That Catches Silent Failures - Vincent Lakatos"
  source_id: 470749689
  excerpt: "アラートが来ない走らなかったジョブを自動検出し、運用事故を未然に防ぐ監視設計ガイド"
  image: "https://www.vincentlakatos.com/wp-content/uploads/2025/12/connected-network-5068978-1-scaled.jpg"
---

# Building a Monitoring System for Jobs That Never Ran - 「走らなかったジョブ」を検出する監視システムの作り方
見えない停止を掴め — アラートが来ない“静かな失敗”を確実に見つける監視設計

## 要約
ジョブが「実行されなかった」ことを検出するには、発生した事象だけでなく「起きるべき事象」をシステム側で持つ必要がある。本記事は、そのための設計（期待値管理、ポーリング、猶予ウィンドウ、通知設計）を実務目線で解説する。

## この記事を読むべき理由
- 月曜に「金曜からデータが来ていない」と気づく不要な事故を減らせる。  
- Cronベースのスケジュール運用が多い日本企業（バッチ処理、ETL、帳票バッチなど）に直結する実践的解法が得られる。  
- 自前実装の判断材料（コスト、柔軟性、運用負荷）を持てる。

## 詳細解説
問題点
- 多くの監視は「成功/失敗」の二値だが、ジョブがそもそも報告を送らないケース（ミスド）は検出が難しい。原因は再起動・更新・スケジューラの例外など多岐。

三つの結果
- Success：ジョブが実行され成功を報告  
- Failure：ジョブが実行され失敗を報告  
- Missed：ジョブが報告しなかった（監視側が検出）

アーキテクチャ（主要コンポーネント）
1. Database：スケジュール（期待）と観測（ping履歴）を永続化。  
2. UI：監視定義、履歴、メトリクス表示（例ではBlazor）。  
3. Ping API：ジョブがPOSTで通知する単一エンドポイント（統合点を最小化）。  
4. Polling Service：1分周期で各モニタを評価し、欠報を検出して通知をキューイング。  
5. Reporting Service：定期レポートや ad‑hoc クエリ（「過去7日で欠報のあるモニタ」等）。  
6. Notification Service：メール／SMS／Webhook等を拡張可能に実装。

Ping API（最小統合）
- 例：POST /ping/{monitorId}/{outcome}（outcome は success/failure）
- 任意のJSONボディでログやメタデータを添付可能（デバッグ履歴として有用）。

例（C#での最小な通知呼び出し）:
```csharp
public async Task RunJobAsync()
{
    try
    {
        await ProcessDataAsync();
        await _httpClient.PostAsync($"https://monitor.example/ping/{_monitorId}/success", null);
    }
    catch
    {
        await _httpClient.PostAsync($"https://monitor.example/ping/{_monitorId}/failure", null);
        throw;
    }
}
```

期待時刻の決定（Cron）
- 各モニタに cron 式を保持し、ポーリング時に「最後に期待される実行時刻」を計算する。
- .NETなら NCrontab 等で次発生時刻を算出して比較する。

猶予（Grace）と「前後の許容」
- 実行タイミングは微妙に前後するため、単一方向の猶予では誤検出が起こる。解決策は GraceRange（Before/After/Both）の導入で、期待時刻の前後どちらを許容するかを選べるようにする。

GraceRange の例（抜粋）:
```csharp
public enum GraceRange { Before, After, Both }
```

スケール対策
- まとめて（バッチ）クエリを投げ、メモリ内でグループ化する（モニタごとに個別クエリを投げない）。  
- grace window が閉じていないモニタはスキップする。  
- 適切な DB インデックス設計を忘れない。

通知の柔軟性
- Outcome ごとに通知ルールを持ち、送信先／チャネルをプラグイン可能に設計（Email、SMS、Webhook、Slack/Teams 等の拡張が容易）。  
- 重要なジョブだけ成功通知を出す等の細かい制御ができると運用が楽になる。

Build vs Buy の判断
- 外部サービス（healthchecks.io、cronitor.io 等）は手軽だが、250+ モニタや細かな通知ルール、既存スタック統一の要件があるとコストや運用面で自前の利点が出る。運用体制とTCOを比較して決定する。

## 実践ポイント
- まずは最小構成で PoC：Ping API（匿名POST）、DBテーブル（monitors/pings）、簡易ポーラー。  
- Cron式から「最後の期待時刻」を確実に計算できるライブラリを採用する（言語依存）。  
- GraceRange を導入して「前後許容」をユーザーに選ばせる（誤検出を減らす）。  
- ポーリングはバッチ処理とインデックス最適化でスケールさせる。  
- 通知はプラガブルに：まずはメールとWebhook、将来的に Slack/Teams を追加。  
- Build vs Buy は「運用コスト×必要な柔軟性」で判断。モニタ数が多く、独自ルーティングやログ添付が必須なら自前のメリットが大きい。  
- 日本の現場では、バッチ文化（深夜バッチ、ETL、受注連携）が強いため、欠報検出は即座に事業インパクトに直結する。まずは重点ジョブ（上位KPIに影響するもの）から監視を始めると効果が出やすい。

以上を踏まえれば、「走らなかったジョブ」を見逃さない監視基盤を比較的短期間で構築できます。必要なら、簡易アーキテクチャ図やDBスキーマ、具体的なクエリ最適化案も提示します。どれが見たいですか？
