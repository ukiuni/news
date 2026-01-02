---
  layout: post
  title: "James Moylan, engineer behind arrow signaling which side to refuel a car, dies - ガソリン給油口の方向を示す矢印を設計したエンジニア、ジェームズ・モイルラン氏死去"
  date: 2026-01-02T05:11:57.221Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://fordauthority.com/2025/12/ford-engineer-that-designed-gas-tank-indicator-passes-away/"
  source_title: "James Moylan, engineer behind arrow signaling which side to refuel a car, dies"
  source_id: 46398235
  excerpt: "雨の経験から給油口矢印を生み出しUXを変えたジェームズ・モイルラン氏が死去"
  ---

# James Moylan, engineer behind arrow signaling which side to refuel a car, dies - ガソリン給油口の方向を示す矢印を設計したエンジニア、ジェームズ・モイルラン氏死去

雨に濡れた一瞬が生んだ「当たり前」――知らずに助かっているUXの発明者

## 要約
フォードの元エンジニア、ジェームズ・モイルラン氏（享年80）が、燃料計横の給油口方向を示す「Moylan Arrow」を考案した人物として知られる。1986年の経験から提案され、1989年ごろからフォード車に搭載され業界標準になった。

## この記事を読むべき理由
小さなUX改善が世界中の自動車ユーザーの体験をどう変えたかの好例であり、日本の自動車開発／プロダクト設計にも直結する教訓がある。設計者、UI/UX担当、組み込みソフトのエンジニアは必読。

## 詳細解説
- 発案の背景：モイルラン氏は1968年にフォード入社。1986年、会社車で給油時にポンプの反対側に駐車して雨に濡れた経験から「燃料計の近くに給油口の方向を示す矢印を付ければいい」と提案した。提案は受け入れられ、1989年ごろから採用が始まった。
- 技術的ポイント（なぜ有効か）：
  - 情報の即時提示：運転中の視線移動／認知負荷を最小化する位置に配置。アイコン一つで判断可能。
  - 汎用性：言語に依存しない視覚記号でレンタカーや外国車ユーザーにも有効。
  - 実装コストが低い：アナログ計器にもデジタルディスプレイにも容易に組み込め、ハード変更を伴わずにソフトで表示可能なケースも多い。
- 現代的拡張：
  - ソフトウェア定義車両ではインストルメントクラスタ／インフォテインメントで柔軟に表示制御が可能。
  - 車両ネットワーク（CAN/車両設定）から給油口位置フラグを取得して表示する実装が一般的。
  - EV普及に伴い、充電ポートの位置表示など同様のUX設計が重要になる。

## 実践ポイント
- 小さな摩擦を探せ：日常の「ちょっとした不便」を観察し、低コストで大きな効果が出せるUX改善を優先する。
- 実装の基本設計：給油口方向は車両設定（製造時フラグ）→ BCM/車両バス → 表示モジュール（アナログ／デジタル）という流れで実装。ソフト中心ならOTAでの修正も可能にする。
- 日本市場での配慮：右側通行（左ハンドル・右ハンドルの混在）、輸入車レンタカー、観光客向け車両などで給油口の位置は多様。明確な視覚表示は顧客満足につながる。
- アイコンの国際化：文字列よりアイコンが有効。新車・中古車のUI改良、EVの充電口方向表示への流用を検討する。

## 引用元
- タイトル: James Moylan, engineer behind arrow signaling which side to refuel a car, dies  
- URL: https://fordauthority.com/2025/12/ford-engineer-that-designed-gas-tank-indicator-passes-away/
