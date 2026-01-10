---
layout: post
title: "Show HN: Miditui – a terminal app/UI for MIDI composing, mixing, and playback - Miditui — ターミナルで作曲・ミキシング・再生ができるMIDIアプリ"
date: 2026-01-10T06:27:04.025Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/minimaxir/miditui"
source_title: "GitHub - minimaxir/miditui: An interactive terminal app/UI for MIDI composing, mixing, and playback—written in Rust"
source_id: 46543359
excerpt: "ターミナルで動く軽量DAW midituiでMIDIを素早く作曲・書出し"
image: "https://opengraph.githubassets.com/d15a1935ae4c65d97d425f035d2a497c45fccb2360ae12fc5646262590d2b0dd/minimaxir/miditui"
---

# Show HN: Miditui – a terminal app/UI for MIDI composing, mixing, and playback - Miditui — ターミナルで作曲・ミキシング・再生ができるMIDIアプリ
魅力的なタイトル: ターミナルで即席DAW。キーボードだけで作曲〜書き出しまでできる「miditui」を試してみよう

## 要約
midituiはRustで書かれたターミナル上のインタラクティブなMIDI作曲・ミキシング・再生アプリ。ピアノロール、リアルタイム入力、トラックごとのミュート/ソロやWAV書き出しまで備える“軽量DAW”です。

## この記事を読むべき理由
- 開発者やDTM初心者が開発環境から離れずに音楽制作を始められる点は、日本のエンジニアやインディー音楽制作者にとって魅力的です。  
- GUIに頼らないツールは低スペック環境やリモート開発、教育現場でも使いやすく、音楽×技術の学び直しに最適です。

## 詳細解説
midituiの要点（技術的特徴と実装面のポイント）を簡潔にまとめます。

- UIと入力
  - フルターミナルのマウス対応（クリック、ドラッグ、スクロール、右クリックなど）があり、ピアノロール上で直感的に編集可能。  
  - InsertモードではQWERTYキー（Z–M／Q–I行による2オクターブ配置）でリアルタイムに音を鳴らしながら入力できます。  
  - ただし、ターミナルごとの差異でキーリリース検知は不安定なため「キーを押し続けて音を伸ばす」挙動はサポートが限定的です。

- 音声処理
  - rustysynthを利用した低レイテンシ再生（44.1kHz）。リアルタイムの打鍵入力に対しても遅延が少ない設計。  
  - 実行にはSoundFont（.sf2）が必要。軽量〜高品質のSoundFont（例：TimGM6mb, GeneralUser GS）が推奨されています。

- トラックと編集機能
  - 無制限のMIDIトラック、トラックごとのミュート/ソロ、音量・パン制御、自動MIDIチャンネル割当。  
  - タイムライン（プロジェクトビュー）で全トラックのノートを俯瞰でき、時間ルーラーをクリックしてシーク可能。  
  - 自動保存機能（専用の.oxm形式でメタ情報付き保存）とUndo/Redoをサポート。

- 入出力
  - MIDI/JSONのインポート・エクスポート、WAVへの書き出し。例：制作をMIDIで出力して別ソフトで仕上げる、などが容易。

- 開発・配布
  - Rust製で、バイナリ配布（各プラットフォームのRelease）またはcargo installで導入可能。  
  - 開発にはAIコーディングアシスタント（Claude Opus 4.5）を活用したという開発ノートが公開されています。

## 実践ポイント
すぐ試すための最短手順と運用上のコツ。

1. バイナリかcargoで導入（例：Linux x64の一例）
```bash
# Linux x64（リリースバイナリをダウンロード＆展開）
curl -sL https://github.com/minimaxir/miditui/releases/latest/download/miditui-linux.tar.gz | tar xz

# Rustがある場合は
cargo install miditui
```

2. SoundFontを用意する
- 小さめなら TimGM6mb.sf2、より多彩な音色なら GeneralUser GS を入手しておく。初回起動時にパスを聞かれ、保存されます。

3. 基本操作（覚えておくと便利）
- Space：再生／停止、i：Insertモード、Enterやダブルクリックでノート追加、g：ビュー切替、Ctrl+S：保存、e：WAV書き出し、?：アプリ内ヘルプ、Ctrl+Z：Undo、Ctrl+O：ファイルを開く

4. 使いどころの提案（日本向け）
- 学校やハッカソンでの音楽×コードの導入教材に最適。GUI配備が難しい教育PCでも動作可能。  
- インディーゲーム開発でプロトタイプBGMを素早く作る、ターミナル作業の合間にメロディ・アイデアを試す用途にも便利。  
- ライブコーディングやデモ動画作成時、ターミナルUIの見た目を活かした表現ができる。

5. 注意点
- 端末によってマウス水平スクロールなどの挙動が異なるので、Ghosttyなど推奨端末を検討。  
- 長い音の伸ばし（キーを押し続ける入力）は期待通り動かない場合があります。必要ならMIDIをエクスポートして別ツールで微調整を。

まとめ：もし「コードを書きながらアイデアをサッと音にしたい」「軽量な環境で音楽制作を試したい」と思うなら、midituiは今すぐ触って損はないツールです。GitHubのReleaseからバイナリを落として、SoundFontを用意して、まず数分で遊んでみてください。
