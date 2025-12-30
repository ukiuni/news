---
layout: post
title: One incident, onion tech debt and layoffs - postmortem to gauge metric problem - 一つのインシデント、玉ねぎのような技術的負債、そしてレイオフ - 指標の問題を測定するためのポストモーテム
date: 2025-12-29T21:29:32.155Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@IndividualSecret1/one-incident-onion-tech-debt-and-layoffs-e356610482a3"
source_title: "One incident, onion tech debt and layoffs - postmortem to gauge metric problem"
source_id: 435061290
excerpt: "Prometheusの凍結ゲージが暴いた層状技術負債とサービス崩壊の全容"
---

# One incident, onion tech debt and layoffs - postmortem to gauge metric problem - 一つのインシデント、玉ねぎのような技術的負債、そしてレイオフ - 指標の問題を測定するためのポストモーテム

## 要約
小さなPrometheusのゲージが “変わらない” ことから始まった障害対応は、例外処理の欠如→クライアント実装差→観測基盤選定→対象プロダクトの本質的問題…と層状に拡大し、最終的にサービス停止とレイオフに至った。

## この記事を読むべき理由
運用中の「値が止まる」観測データは単なるバグではなく、監視/ライブラリ/プロダクト戦略の複合問題を示唆します。日本のプロダクトチームでも起こりうる典型的な失敗パターンと、短中期で取れる具体的対策を学べます。

## 詳細解説
- 発端：トランザクション遅延を報告するカスタマーサポート。ドメインで特定した単一マイクロサービス（Python製、TRONウォレット追跡）が標的に。Grafana上の重要指標 blockchain_delay が “数日間不変” になっていた。
- 第一層（コード）：非同期ワーカーで外部API呼び出しが失敗した際に例外が捕まらず、ワーカーが死んでゲージが最後の値のまま凍結。つまりメトリクス収集自体は動いていないが値は更新されず「正常に見える」状態になった。
- 第二層（クライアントの実装差）：Prometheusのクライアント実装は言語ごとに挙動が違う。Pythonクライアントはゲージにタイムスタンプを付けるネイティブ機能が乏しく、古い値を自動で「stale（枯渇）」扱いにしにくい。PHPやGoでも実装差があるため、同じ設計でもサービスごとに挙動が異なる。
- 第三層（観測基盤の選択）：統一的な観測ライブラリ（例：OpenTelemetry）への移行を検討すればクライアント差分を吸収できるが、置換コストや移行時間が発生する。
- 第四層（ビジネス面）：対象サービスはTRON対応の機能で、規制・不正利用リスクが高い領域。プロダクト自体の利用者減少や法規制リスクと合わせ、技術的な修正だけでは根本解決にならないレベルの経営判断問題が露見。最終的にサービス停止と人員整理へ。

ポイント：観測の見える化は「値があること」を示すだけであって、「値が最新であること」を担保しない。観測設計・ライブラリ選定・運用手順・プロダクト戦略の全てが揃って初めて信頼できる。

## 実践ポイント
- まず今すぐ
  - 非同期ワーカーやバックグラウンドタスクに必ずトップレベルの例外ハンドリングを入れる（再試行・ログ・監視通知）。
  - プロセスが死んだ場合に自動で再起動する仕組み（systemd, KubernetesのRestartPolicy）を必須化する。
  - Prometheus側で stale を検出する方法を導入する（absent() アラート、recording ruleでの差分監視）。
- メトリクス設計
  - 「値が変わらない」こと自体をアラート条件にする（例：一定期間値が更新されていなければ通知）。
  - 重要な指標は「up」や「heartbeat」的な生存確認メトリクスを別途エクスポートする。
  - 可能ならばタイムスタンプ付き出力やカスタムエクスポーターで更新時刻を明示する（クライアント差分を意識して一箇所でラップする）。
- 技術選定とガバナンス
  - 共通の観測ライブラリを社内で整備し、全サービスで同じ振る舞いにする（ラッパーライブラリを1箇所で修正）。
  - OpenTelemetry等の上位抽象化の導入を検討する。ただし移行計画と検証を明確に。
- ビジネス側への提言
  - 観測から見えた不整合は単なる技術課題ではなく、利用実態・規制リスク・プロダクト戦略の再評価サインとみなす。
  - 技術チームはメトリクスの変調を経営指標に紐づけ、早期に意思決定ラインへエスカレーションする仕組みを作る。
- 例：安全なPythonワーカーの素早い修正例
```python
# python
async def update_blockchain_delay():
    while True:
        try:
            last_block_processed = await get_last_processed_block()
            current_block = await get_current_block()
            gauge.set(current_block - last_block_processed)
        except Exception:
            logger.exception("update_blockchain_delay failed")
            # 必要に応じて別の監視指標を更新する
        await asyncio.sleep(5)
```

短期対応で止められる事故は多数ありますが、観測の設計とビジネス判断の両面を無視すると、最悪プロダクト終了と人員削減という結果につながります。観測は「技術の鏡」であり、映った像をどう受け止めて行動するかがチームの寿命を決めます。
