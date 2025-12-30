---
layout: "post"
title: "Let's make a game! 368: Team names - ゲームを作ろう！ 368：チーム名"
date: "2025-12-29T16:28:16.289Z"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://www.youtube.com/watch?v=97QED2aoO_A"
source_title: "368: Team names (Twine Sugarcube) - YouTube"
source_id: "435312438"
excerpt: "Twine（SugarCube）で短時間に安全なチーム名機能を実装する実践ガイド"
---

# Let's make a game! 368: Team names - ゲームを作ろう！ 368：チーム名

## 要約
Twine（SugarCube）で「チーム名」を扱う際の基本設計と実装パターンを、変数設計・表示ループ・入力・検証・永続化・UX改善の観点から簡潔に解説する。

## この記事を読むべき理由
インタラクティブ作品やローカルマルチチーム式のゲームで、プレイヤーが自由にチーム名を設定・変更できる機能は必須。日本のゲーム開発者やノベル作者が短時間で安全かつ扱いやすい実装を作るための実践知を得られる。

## 詳細解説
1) 変数設計（State.variablesを使う）
- プレイヤーが編集するデータは必ずState.variables（$で参照）に置く。これでセーブ/ロードや名前の永続化が自動的に機能する。
- 配列またはオブジェクトで管理すると拡張しやすい（例：チーム名＋色＋スコア）。

例（Story JavaScript / 初期化）:
```javascript
// javascript
if (!State.variables.teams) {
  State.variables.teams = [
    { name: "赤チーム", color: "#d9534f", score: 0 },
    { name: "青チーム", color: "#337ab7", score: 0 }
  ];
}
```

2) 表示とループ
- SugarCubeのテンプレートマクロや単純なforループで一覧表示。各要素を<<for>> / <<print>>等で描画して、動的に変化するUIを作る。

擬似マークアップ例（パッセージ内）:
```html
<!-- html -->
<ul>
<<for _i range(0, State.variables.teams.length - 1)>>
  <li style="color: <<print State.variables.teams[_i].color>>;">
    <<print State.variables.teams[_i].name>>
  </li>
<</for>>
</ul>
```

3) 入力と編集
- プレイヤー入力はSugarCubeの入力マクロ（環境により<<textbox>>等）か、HTMLの<input>を使い、変更をState.variablesに反映する。
- 変更後は必要に応じて表示を再レンダリングする（SugarCubeの<<replace>>や簡単なパッセージ遷移で反映）。

簡単な保存処理の考え方（擬似コード）:
```javascript
// javascript
function saveTeamName(index, newName) {
  State.variables.teams[index].name = newName;
  // 必要ならEngine.play(currentPassage)で再描画
}
```

4) バリデーションと衝突回避
- 空文字チェック、長さ制限、禁止文字（絵文字や制御文字）や他チームとの重複チェックを行う。
- プレイヤーが同名にしたくない場合は自動的にサフィックスを付けるか、エラーメッセージで入力を拒否する。

例（重複チェックのロジック）:
```javascript
// javascript
function isDuplicateName(name) {
  return State.variables.teams.some(t => t.name === name);
}
```

5) UXと実装上の注意
- モバイル表示を意識して入力欄は広めに、フォントは可読性重視（日本語対応）。
- 名前変更は即時反映でも良いが、確認ダイアログや取り消し（undo）を用意すると安心。
- セーブ互換性：構造をあとで変える場合はマイグレーションコード（古いバージョンのStateを検出して変換）を入れる。

## 実践ポイント
- 最低限、State.variables.teams = [] を初期化しておく。これだけでセーブ/ロードが効く。
- 編集UIは「一覧表示」「編集ボタン」「確認」の3要素を揃えておくと混乱が減る。
- 名前の正規化（前後の空白除去、最大長切り詰め）を必ず入れる。
- 日本語環境ではフォントと文字数制限を厳しめに設定する（全角文字での見切れ対策）。
- 将来の拡張（色・アイコン・スコア）を見越して、チームをオブジェクトで定義する設計を採る。

以上を踏まえれば、Twine（SugarCube）で堅牢かつ使いやすい「チーム名」機能を短時間で実装できます。必要なら、具体的なテンプレート（編集フォーム＋バリデーション＋描画）をサンプルコード付きで出します。どのレベルのサンプルが欲しいですか？
