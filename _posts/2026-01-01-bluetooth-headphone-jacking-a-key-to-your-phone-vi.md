---
  layout: post
  title: "Bluetooth Headphone Jacking: A Key to Your Phone - Bluetoothヘッドフォンジャッキング：あなたのスマホへの“鍵”"
  date: 2026-01-01T12:33:51.048Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://media.ccc.de/v/39c3-bluetooth-headphone-jacking-a-key-to-your-phone"
  source_title: "Bluetooth Headphone Jacking: A Key to Your Phone  - media.ccc.de"
  source_id: 46453204
  excerpt: "人気ブランド対応のAiroha脆弱性でイヤホンがスマホ侵害の踏み台に"
  ---

# Bluetooth Headphone Jacking: A Key to Your Phone - Bluetoothヘッドフォンジャッキング：あなたのスマホへの“鍵”
魅惑のワイヤレスが危険に変わる瞬間――あなたのイヤホンがスマホの裏口になる話

## 要約
人気のBluetoothオーディオSoC（Airoha製）に重大な脆弱性（CVE-2025-20700/20701/20702）が見つかり、ヘッドホン／イヤホン本体の完全な乗っ取りや、ペアリングしたスマホへの横展開が可能になることが示された。

## この記事を読むべき理由
国内で広く使われるSonyやJabraなどの製品にも影響例が挙がっており、日本の一般ユーザーも被害に遭い得る。ワイヤレスオーディオ普及の裏で増える「周辺機器経由の攻撃」は、個人・企業ともに無視できない新たなリスクだからだ。

## 詳細解説
- 影響箇所: AirohaのBluetoothオーディオSoCとそのSDK／リファレンス実装。TWSイヤホンで広く採用されている。
- 攻撃手法の核: 研究者が発見したカスタムプロトコル「RACE」を経由して、デバイスのフラッシュやRAMへ読み書きできる。これにより、ファームウェアの読み出し・書き換え、持続的なバックドアの埋め込みが現実的になる。
- 連鎖的な危険: 周辺機器（イヤホン）を乗っ取ることで、そのペアリング情報（Bluetooth Link Key）を盗むことができれば、攻撃者は端末に対して周辺機器を偽装して接続し、端末側の機能やデータにアクセスする可能性がある。スマホ本体の堅牢化が進む中、攻撃者はむしろ周辺機器に目を向け始めている。
- 実証と対象例: 実機（現行世代のヘッドホン）での完全侵害デモが行われ、影響が示された。例としてSony WH-1000XM5/XM6/WF-1000XM5、MarshallやBeyerdynamic、Jabraなどが挙がっている。
- 開示と対策の難しさ: サプライチェーン（SoCベンダ→ODM→ブランド）が深く入り組んでおり、パッチ配布やユーザー告知が遅れやすい点が問題として指摘されている。研究チームは影響確認用ツールも公開している（講演ページ参照）。

## 実践ポイント
- まずは確認: 使っているヘッドホン／イヤホンのメーカー発表やファームウェア更新情報をチェックする。該当モデルがリストに含まれていないか確認する。
- ファームウェアの更新: ベンダーから公式アップデートが出ている場合は速やかに適用する。
- ペアリング管理: 使わないときはペアリングを解除し、公共の場での自動接続を避ける。紛失時は端末側でペア情報を削除する。
- 最小権限の運用: 仕事端末では個人のBluetooth周辺機器を業務端末に接続させない、MDMでBluetoothポリシーを設定するなどの対策を検討する。
- 専門家向け: 研究チームが公開したツールで検査し、ファーム書き換えが必要な場合は信頼できる手順で対応する（不慣れな操作はデバイス破損や保証消失のリスクあり）。
- 企業は供給網をチェック: ブランドだけでなくSoC/ODMの出自を確認し、脆弱性対応体制をベンダーに要求する。

## 引用元
- タイトル: Bluetooth Headphone Jacking: A Key to Your Phone [video]
- URL: https://media.ccc.de/v/39c3-bluetooth-headphone-jacking-a-key-to-your-phone
