---
  layout: post
  title: "GBC Boot Animation 88×31 Web Button - GBC ブートアニメーション 88×31 Web ボタン"
  date: 2026-01-06T05:02:14.918Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://zakhary.dev/blog/gbc-web-button"
  source_title: "GBC Boot Animation 88×31 Web Button | Zakhary&#39;s Home"
  source_id: 46507963
  excerpt: "Game Boy Colorの起動画面を88×31のレトロWebバッジに忠実移植する方法を実践解説"
---

# GBC Boot Animation 88×31 Web Button - GBC ブートアニメーション 88×31 Web ボタン
懐かしのGame Boy Color起動画面を88×31のレトロWebバッジに“丸ごと”移植する方法

## 要約
Game Boy Colorのブートアニメーションをエミュレータでフレームごとに抜き出し、ImageMagickでトリミング・リサイズ・色置換して88×31のレトロWebボタンを作るハンズオン。

## この記事を読むべき理由
90年代的な88×31バッジは個人サイトのフッターで再流行中。オリジナルのGBC起動画面をそのまま使う技巧（エミュレータのブレークポイント、vblankの利用、ImageMagickの巧妙なパイプライン、色補間での“ゴースト”除去）は、ピクセル単位でのレトロUI再現やツールチェーン自動化の参考になる。

## 詳細解説
- コンセプト  
  起動画面（boot ROM）のアニメーションをフレームごとにキャプチャして、伝統的な灰色フレーム内の88×31バッジに収める。問題は（1）ROM由来のアニメを取り出す手順、（2）縮小や背景置換で生じるアーティファクトの除去。

- フレームの取り出し（エミュレータ × デバッガ）  
  SameBoy等のGBC対応エミュレータで起動画面を実行し、ブレークポイントで各フレームのvblank（LCD描画の垂直ブランキング）待ちを狙って止め、エミュレータのスクリーンショット機能で160×144のフレームを連番PNGで保存する。逆アセンブル済みのboot ROMでは、vblank待ちルーチン（記事では Wait_for_next_VBLANK）が呼ばれるアドレスにブレークを置くと効率的。

- GIF化（ImageMagick）  
  取得したPNG群をImageMagickでアニメ化。フレーム遅延はハードウェアカウントに基づき調整するのが正確。
  ```bash
  # 例: 取得したPNGをアニメに
  magick -delay 1.6742706299 -loop 0 *.png(n) animation.gif
  ```

- トリミング→縮小→フレーム合成  
  1) 起動画面中のロゴ領域を特定してcrop、2) 背景色を置換（白→グレー）した上で縮小、3) 88×31の中央に配置してフレーム画像を合成、という順序が重要。白背景を先にグレーに変えてから縮小しないとゴースト（フェードの白が残る影）が残る。
  ```bash
  magick animation.gif \
    -crop 127x22+16+48 +repage \
    -fill "#C0C0C0" -opaque "#FFFFFF" \
    -resize 82x \
    -gravity center -background "#C0C0C0" -extent 88x31 \
    -coalesce null: frame.png -layers composite \
    fixed.gif
  ```

- ゴースト（フェード）問題と色のリマップ  
  オリジナルはロゴが青→白へフェードしているため、背景を灰色に変えるだけだと白方向へのフェード残像が出る。対策は「フェード色列を抽出→各色の進捗に応じて灰色側へ再計算→置換」。手順は（A）各フレームを分解して色ヒストグラムを出し、フェードで使われる色群を特定、（B）色補間スクリプトで各色を新しい終了色（例 #C0C0C0）に沿って再マップ、（C）ImageMagickで色置換を適用する、という流れ。

  抽出・分析の例（フレーム分解＋ヒストグラム）:
  ```bash
  mkdir frames
  magick animation.gif frames/%03d.png
  for f in frames/*.png; do magick "$f" -format %c histogram:info: >> colors.txt; done
  ```
  色再マップは簡単なPythonでRGB補間して出力コマンド列を生成し、ImageMagickで一括置換するのが実用的。

- 法的・倫理的メモ  
  ブートROMは任天堂の所有物だが、今回のような非商用リ・クリエイションやフェアユースに類する利用は多くの作者が問題視していない。公開や配布を考える際は権利関係を再確認すること。

## 実践ポイント
- 必須ツール: SameBoy（フレーム取得）、ImageMagick（画像処理）、Aseprite等（座標・ピクセル確認）。  
- デバッグのコツ: vblank待ち関数にブレークを置くとフレーム単位で止められる。Disassemblyのラベル（例 sub_0291 → call Wait_for_next_VBLANK）を頼りにブレーク位置を決める。  
- 画像処理の順番を守る: 先に白背景を目標色で置換 → その後縮小、フレーム合成。順序を逆にすると「白フェードのゴースト」が残る。  
- カラーマッピング: フェード色群を抽出して線形補間で再マップするのが堅実。色リストが得られればImageMagickの -fill / -opaque 連打で置換可能だが、大量の色はスクリプトで自動生成すること。  
- 再利用性: 同手順をMakefileや小さなスクリプトにまとめれば、別の起動画面や別サイズのバッジにも流用しやすい。

短時間で「見栄えする」レトロバッジを作るには、このワークフローを覚えておくだけで十分。実際に試す際に欲しいコマンドやPythonスクリプトの簡易版が必要なら追加で出す。
