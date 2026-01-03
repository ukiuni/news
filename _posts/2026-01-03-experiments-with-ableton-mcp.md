---
  layout: post
  title: "Experiments with Ableton-MCP - Ableton‑MCPでの実験"
  date: 2026-01-03T22:02:06.948Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://jhurliman.org/post/804323197731373056/experiments-with-ableton-mcp-dec-2025"
  source_title: "Experiments with ableton-mcp (Dec 2025) - John Hurliman"
  source_id: 46428922
  excerpt: "LLMでAbletonを自動化し70超ツールで数日でマッシュアップを制作する実験記"
  image: "https://64.media.tumblr.com/18725cc767aab262e62859b1cbc43003/b106372ea8b9929c-ad/s1280x1920/30df9efc4f86468ae113ba294a543769fb26b703.jpg"
---

# Experiments with Ableton-MCP - Ableton‑MCPでの実験
LLMがAbletonの「秘密のボタン」を押す──70を超える自動化ツールとマッシュアップが示すDAWの次の学び方

## 要約
John Hurlimanがableton‑mcpを起点に、LLMとツール連携でAbleton Liveを自動化・拡張し、70以上のMCPツールを生成してマッシュアップを作った実験記。モデルによる逆解析で.alsファイルを書き換え、音声解析→MIDI変換などのワークフローを構築している。

## この記事を読むべき理由
- 日本のクリエイターやエンジニアが、LLMを「DAWのペアプログラマ」として使い、短期間でAbletonの学習と制作効率を劇的に高める具体例が得られるため。
- Abletonの自動化や音声→MIDI変換など、日常的な制作タスクをコードで拡張する手法は、J‑POP制作や同人音楽、Vocaloidワークフローにも応用しやすい。

## 詳細解説
- 基盤ツール
  - ableton‑mcp（ahujasid/ableton‑mcp）: MCP（Max Control Protocol）サーバを介して、ツール呼び出し可能なLLMとAbleton Liveを橋渡しするコミュニティ実装のPython API。
  - 使用モデル: 原著者はClaude Code→Opus 4.5を利用し、モデルにAbletonMCPのインストール・拡張を行わせた。現代のツール呼び出し対応LLMは、ドキュメント参照→ツール追加→テスト→反復が可能。
- 初期カバー範囲と不足点
  - 初期状態でSession Viewの基本操作（クリップ作成・編集）はカバーされたが、Arrangement View、デバイス/チェーン操作、ミキシングなど「本格DAWワークフロー」は未対応。
- 逆解析と低レイヤ操作
  - APIが露出していない機能について、モデルは.als（Ableton Live Set）ファイル形式を逆解析し、テンポ／ボリューム自動化やWarpマーカー挿入を直接注入するアプローチを取った。
- 高レベルツール例
  - vocal_to_midi(): ボーカルトラックの音声を解析し、オンセットを粗い音素カテゴリに分類して、各カテゴリをDrum RackのMIDIノートにマッピング。目的は「ボーカルからドラムを作る」ことではなく、位相・タイミングの微調整を容易にする構造化表現の獲得。
- 「聞く」能力の付与
  - モデルは自分でオーディオを再生／評価できないため、Max for Liveパッチでオン／オフできるWAVレコーダを作り、Abletonのオーディオをプログラム的に取り出す仕組みを実装。
  - 外部推論サービス（Replicate）に2つのエンドポイントを用意:
    - jhurliman/allinone-targetbpm: トラックの構造解析を返すフォークで、min_bpm/max_bpmを公開（テンポの二重カウント対策）。
    - jhurliman/music-flamingo: 音声＋プロンプトでテキスト出力を返す、音楽理論知識でファインチューニングされたモデル。
- 実際のマッシュアップ作成
  - ベーストラック（Deft & Lewis James – Octo）のテンポとキーを特定し、候補ボーカルを自動リスト化 → GloRilla – Yeah Glo! を選択。
  - 自動化と手動編集を織り交ぜ、数日で公開可能なマッシュアップを作成。アップロード→気づき→修正を繰り返し最終化。
- 成果と学び
  - ブログや動画数週間分に相当するAbletonの理解を数日で得られた。LLMを「DAWの相棒」として使うことで、学習速度と制作の自信が向上した。

## 実践ポイント
- はじめの一歩
  - ableton‑mcpリポジトリをクローンし、Ableton LiveとMax for Liveが動作する環境を準備する。Session Viewから試すとハードルが低い。
- モデルの選択とツール呼び出し
  - ツール呼び出し対応のLLM（Claude系、Opus系、あるいはOpenAIのツール呼び出し）を用意し、まずは小さなMCPツール（テンポ読み取り、クリップ複製など）を自動生成させる。
- オーディオの「可聴化」
  - Max for LiveでWAV録音パッチを作り、モデルに渡せるオーディオスナップショットを自動で作成する。これが閉ループ評価の鍵。
- 再利用可能な解析エンドポイント
  - トラック構造解析（BPM範囲、セクション検出）や音楽理論を学習したテキスト出力を返すモデルを外部に立てると、LLM側の判断精度が上がる。Replicateなど既存サービスの活用が手早い。
- 小さく反復する
  - まずは「配置・テンポ・簡単な自動化」の自動化→次に「デバイス操作」「チェーン操作」へ拡張する。.als直接編集は強力だがバックアップを必ず取る。
- 日本市場での応用と注意点
  - J‑POP制作、同人音楽、Vocaloidとの併用で制作効率アップが期待できる。ただしサンプルやボーカル素材の権利処理は日本の法規制・ガイドラインに従って行うこと。
  - 日本語ボーカルの音素カテゴリ化や歌詞理解は英語チューニング済みモデルと相性が悪い場合があるため、日本語対応モデルや追加ファインチューニングを検討する。

原著のコードやワークフローは jhurliman/ableton‑mcp/pull/1 にまとまっているため、実践する際の参考にするとよい。
