---
  layout: post
  title: "identity is a physical property, not a digital permission - アイデンティティはデジタル権限ではなく物理的性質である"
  date: 2026-01-03T14:35:31.618Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/illegal-instruction-co/pbm-core"
  source_title: "GitHub - illegal-instruction-co/pbm-core: Perspective-Based Markers (PBM): a camera-readable spatial marker system based on perspective distortion, depth cues, and geometric invariants."
  source_id: 472074556
  excerpt: "製造時の微細な物理指紋をQRと暗号で結び偽造不可能な真正性を現場で検証"
  image: "https://opengraph.githubassets.com/1fac6b635ceea7b92c942176f1c9cd49cc2fbfebc38b60bc7e306ab5e7727f55/illegal-instruction-co/pbm-core"
---

# identity is a physical property, not a digital permission - アイデンティティはデジタル権限ではなく物理的性質である
印刷1枚で“偽造不可能”！？製造時に生まれる“物理的アイデンティティ”で真贋を証明するPBMの衝撃

## 要約
PBM（Perspective‑Based Markers）は、製造時に生じる微細な物理的特徴を「物理的指紋」として抽出し、それを暗号的にデジタル記録と結びつけることで、写真やコピーでは再現できない真贋検証を可能にするオープン標準の認証システムです。

## この記事を読むべき理由
日本では偽造対策、サプライチェーンの信頼性、二次流通や中古市場の真正性確認が重要です。PBMは安価な印刷や既存カメラで動作し、クラウド依存を減らせるため、日本のメーカーや小規模ブランドが現場で導入しやすい実装候補になります。

## 詳細解説
- コア思想：製品の「アイデンティティ」は後付けのデジタル許可ではなく、製造時に生まれる物理的性質（微細な凹凸、層間の深さ、パースペクティブ歪みなど）に根ざす。PBMはこれを測定してハッシュ化し、デジタル証明と結合します。
- 主要技術要素：
  - 視差（parallax）とパースペクティブ歪み、深度情報、幾何学的不変量を利用して「物理的指紋」を抽出。
  - ライブネスチェック（3D構造の検証）で写真/スクリーンによるなりすましを排除。
  - ハッシュ化＋署名で「測定された物理→JSON（デジタルパスポート）→QRコード」までを結びつけ、検証時に再測定して照合する流れ。
- ソフトウェア構成（リポジトリの実装概要）：
  - keygen.py：製品当局が使う鍵生成（private_key.pem を秘密に、public_key.pem を検証側へ配布）。
  - enroll.py：製造側が対象物をカメラで読み取り、物理指紋を抽出して署名付きJSONを出力。これをQRなどに埋める。
  - verify.py：ユーザー側がQRと物体をカメラで読み、署名検証→物理再抽出→比較を実行。「GENUINE／MISMATCH」を返す。
- 特徴：オフラインで動作可能、専有クラウド不要、家庭用プリンタとスマホカメラでホーム実験ができる点を明記している。
- 限界と注意点：カメラ性能や照明、製造ばらつきによる再現性、鍵管理（private keyの厳重な保護）、大量生産時の工程管理など運用面の配慮が必要。

## 実践ポイント
- 今すぐ試す手順（リポジトリ準拠の簡易手順）
  1. Python 3.11 仮想環境を作成：py -3.11 -m venv .venv → 有効化
  2. 依存を入れる：pip install -r pbm_mvp/requirements.txt
  3. 鍵生成：python pbm_mvp/keygen.py（private_key.pem を安全に保管）
  4. 試作トークンの登録（製造側想定）：python pbm_mvp/enroll.py → 出力JSONをQR化
  5. 検証：python pbm_mvp/verify.py（QRと物体をカメラに見せる）
- 導入検討のチェックリスト
  - 試験環境で「光源・カメラ距離・解像度」を固定して再現性を検証する。
  - プライバシーと鍵運用：private keyはHSMまたは専用管理で保護。公開鍵配布経路を確立する。
  - 小ロットでパイロット導入し、製造工程での誤差耐性を評価する（材質や印刷方式で指紋が変わる）。
  - 既存QR運用やパッケージシステムとの統合ポイントを設計する（例えば流通システムへの認証API）。
- 日本での応用候補：高級ブランド真贋、医薬品包装の正当性、地域工芸品の証明、イベント入場券の不正防止、小ロット製品の二次流通保証。

短時間でプロトタイプが作れる一方、実運用では検証精度と運用設計（鍵管理、製造許容誤差、ユーザーUX）を丁寧に詰める必要があります。PBMは「物理」から本人性を掘り起こす発想で、日本の現場でも現実的な替え手段になり得ます。
