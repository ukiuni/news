---
  layout: post
  title: "How Twitch tamed a million lines of TypeScript - Twitchが100万行のTypeScriptを制した方法"
  date: 2026-01-05T19:23:23.515Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.joshribakoff.com/blog/lint-snapshots/"
  source_title: "How Twitch Tamed a Million Lines of TypeScript - Josh Ribakoff"
  source_id: 46496718
  excerpt: "ESLintスナップショットで例外を見える化し規約劣化を防いだTwitch流運用"
  ---

# How Twitch tamed a million lines of TypeScript - Twitchが100万行のTypeScriptを制した方法
「例外を見える化して守る」Twitch流：大規模TypeScriptコードベースのための実践的ルール運用

## 要約
Twitchは、ESLintの「無効化コメント（// eslint-disable）」や一時的な例外が目に見えなくなることで規約が崩れていく課題に対して、ルール違反をレポートとしてスナップショット化し、CODEOWNERSでコアチームに所有させる運用で可視化とレビューを実現した。

## この記事を読むべき理由
大規模リポジトリや多数の開発者が関わるプロジェクトでは、ローカルな一時逃げやコピペで例外が累積し、規約が徐々に劣化する――日本の大企業や急拡大するスタートアップでも直面しやすい問題であり、Twitchのアプローチは「阻害しない」「見える化する」現実的な解法を示す。

## 詳細解説
課題認識
- 多人数で同じモノリスを触ると、以下が増える：エディタ自動挿入の `// eslint-disable`、コピーしたコードの例外持ち越し、リファクタでのルール意図の喪失、短期対応で型ガードやテストを外すこと。これらは悪意ではなく「見えない例外の蓄積」による。

仕組み（ポイント）
1. ESLintを「インライン設定を無視する」モードで実行する  
   - 例：`eslint --no-inline-config` に相当する実行で、全ての `eslint-disable` を無かったことにする。
2. その結果（ルール違反リスト）をリポジトリルートにスナップショットとして保存する（ファイル名例: `lint-snapshot.txt`）。  
3. スナップショットから行番号を削り、キーは「ファイルパス + ルール名」のみとする（これにより行追加や削除で差分ノイズを抑制）。  
4. そのスナップショットをCODEOWNERSでコアチームに割り当て、スナップショットの差分をPRに乗せてレビューさせる。

効果
- 例外の追加・移動があるとスナップショットが差分になり、コアチームのレビューが自動的に入る。  
- その場で作者が「なぜ例外が必要か」を説明でき、コアチームはルールのスコープ調整・一時許可・ルール維持を判断できる。  
- 開発を止めずに、例外を「黙認」ではなく「合意された例外」にすることで規約の劣化を防ぐ。

運用上の注意
- スナップショットはメンテナンスコストがある（誤検知・ノイズ対策）。  
- CI連携や自動変換（JSON→簡潔なファイル+ルール行に正規化するスクリプト）を用意すると良い。  
- CODEOWNERSレビュー負荷を分散するため、ルール単位やディレクトリ単位で所有者を細かく設定することも検討する。

## 実践ポイント
- 最小実装案（手順）
  1. ローカル／CIで ESLint を `--no-inline-config` 相当で実行して結果を JSON 出力する。  
  2. JSON をパースして「file path + ruleId」の一覧を作り、行番号を落として `lint-snapshot.txt` を生成する。  
  3. `lint-snapshot.txt` をリポジトリにコミットし、CODEOWNERSでコアチームを指定する。  
  4. CIでスナップショットの差分がある場合はその差分を PR に表示し、CODEOWNERS によるレビューを必須化する。

- 実行コマンド（例）
```bash
# 例: ESLint を行番号無視で JSON 出力（ESLint のオプションは環境に合わせて）
eslint 'src/**/*.{ts,tsx}' --no-inline-config -f json -o eslint-output.json
# JSON をパースして file+rule の簡易スナップショットを作成（jq 等で整形）
cat eslint-output.json | jq -r '.[] | .filePath as $f | .messages[] | "\($f) \(.ruleId)"' | sort -u > lint-snapshot.txt
```

- 運用ルール
  - スナップショット更新はPRに差分を残す（所有者レビューを必須に）。  
  - 既存の例外が必要なら、PRで理由を明記し、期限付きの許可や別ルール化などの合意を取る。  
  - 定期的にスナップショットを見直し、実使用に基づいてルールを進化させる。

Twitchの本質的な学びは「規約違反を叱ること」ではなく「例外を見える化して対話の対象にする」こと。日本の現場でも、同じ考え方を導入すれば規模が巨大になる前に健全なルール運用が可能になる。
