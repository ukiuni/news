---
  layout: post
  title: "I switched from VSCode to Zed - VSCodeからZedに乗り換えた話"
  date: 2026-01-05T14:51:05.291Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://tenthousandmeters.com/blog/i-switched-from-vscode-to-zed/"
  source_title: "I switched from VSCode to Zed"
  source_id: 46498735
  excerpt: "VSCodeの重さに疲れた人向け、軽快なZed移行とPython設定の実践ガイド"
  ---

# I switched from VSCode to Zed - VSCodeからZedに乗り換えた話
Zedで戻る「快適さ」──AI機能に疲れたエンジニアが選んだ軽快な代替案

## 要約
VSCodeのAI機能や頻繁なアップデートによる挙動変化・遅延に不満を持った筆者が、Rust製の軽量IDE「Zed」に完全移行。高速で安定、ほぼそのままの操作感だが、Python周りは言語サーバー設定で少し手間が必要だった。

## この記事を読むべき理由
日本の開発現場でもVSCodeは事実上の標準です。AI統合の増加や拡張の肥大化で「以前ほど快適に感じない」人が増えています。Zedの実使用レポートと、移行時に直面する具体的な設定課題（特にPython/LSP周り）は、実務で試す価値がある情報です。

## 詳細解説
- なぜ乗り換えたか  
  - 最近のVSCodeはAI機能（Copilotなど）を前提にしたアップデートが増え、無効化のための設定が増える一方で、動作が重く・不安定になったと感じるユーザーがいる。筆者はこうした「押し付けられるAI体験」に嫌気がさし、代替を探した。  

- Zedの第一印象  
  - UI／キーバインドはVSCodeに近い（移行コスト小）。ファイル一覧パネルは無く、Cmd/Ctrl+Pでのファイル検索が推奨。デフォルト設定で高速・安定に動作し、編集のレスポンスが良い。拡張エコシステムは小さいが、筆者の用途には十分だった。  

- Pythonでの落とし穴（技術的ポイント）  
  - ZedはLSP（Language Server Protocol）ベースで動く。Python用に複数の言語サーバーをサポートするが、PylanceはMicrosoftの非OSS実装でVSCode外では使えない。ZedのデフォルトはBasedpyright（Pyright系）で、設定の既定値がプロジェクトのpyproject.toml内の[tool.pyright]を優先する点に注意。  
  - 結果として、プロジェクトに [tool.pyright] があるとBasedpyrightがより厳しいtypeCheckingMode（recommended等）で動き、意図せぬ型エラーが大量に出ることがある。対処法はpyproject.toml内で明示的に typeCheckingMode = "standard" を指定すること。  
  - さらに、別ファイルの編集で生じた診断が即時反映されない問題は、Zed側のLSP初期化オプションで "disablePullDiagnostics": true を設定することで改善する。  
  - 代替LSPとして新興の ty（ベータ）も動作良好で、将来的な選択肢として注目される。

- 欠点とビジネス的観点  
  - 拡張はまだ小規模。GitLensのような高度な差分ツール（サイドバイサイド比較）が欲しい場合は物足りない。Zedは有料プランで編集予測などを提供しており、持続性のあるビジネスモデルを採っている点は評価できる。

## 実践ポイント
- まずは小さなプロジェクトで一日試す：体感速度や安定性を確かめる。  
- VSCode設定は移行機能で取り込めるが、クリーンスタートを推奨（フォントやテーマ、autosaveは最初に合わせるだけで十分）。  
- Pythonプロジェクトでの必須設定（例）:
```json
{
  "lsp": {
    "basedpyright": {
      "initialization_options": {
        "disablePullDiagnostics": true
      },
      "settings": {
        "basedpyright.analysis": {
          "typeCheckingMode": "standard"
        }
      }
    }
  }
}
```
- pyproject.tomlを使っている場合は、[tool.pyright] に typeCheckingMode = "standard" を明示する（プロジェクト単位での一致を保つため）。  
- CIでPyrightを使っているなら、ローカルもBasedpyright／Pyrightに揃えると差異を避けられる。将来的に ty を検討するのも手。  
- チームでの移行を考えると、Git差分ツールや拡張の有無を評価してから導入判断を。

短くまとめると、Zedは「軽快さ」と「安定感」を取り戻したい開発者にとって魅力的な選択肢。特にレスポンスやクラッシュに悩んでいる人は一度試してみる価値があります。
