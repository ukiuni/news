---
  layout: post
  title: "Going immutable on macOS - macOSを不変にする（Nix‑Darwin を使う）"
  date: 2026-01-02T09:16:53.517Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://carette.xyz/posts/going_immutable_macos/"
  source_title: "Going immutable on macOS | A journey into a wild pointer"
  source_id: 46462719
  excerpt: "nix-darwinでmacOSを宣言的管理し、環境再現・ロールバックとGUI対処を実践的に解説"
---

# Going immutable on macOS - macOSを不変にする（Nix‑Darwin を使う）
もう「環境の崩壊」で時間を失わないための、nix-darwinによるmacOS不変化ガイド

## 要約
Homebrewなどの命令的な運用で起こる「環境の劣化（imperative rot）」を避け、Nix（nix-darwin）でシステムを宣言的・再現可能に管理する手法と実用上の落とし穴を解説する。

## この記事を読むべき理由
日本でも複数マシン・チーム開発・長期運用が当たり前になり、環境差分で潰される時間はコストになる。Nixは「設定ファイル＝システムのソースコード」にすることで再現性、ロールバック、バージョン固定を提供し、運用負荷を大幅に下げられるため知っておく価値が高い。

## 詳細解説
- 問題点（“imperative rot”）  
  Homebrewのような手動インストールは「その時点の最新」を取るため、半年後に同じコマンドを実行しても違う結果になり得る。結果として環境復元やデバッグに時間を取られる。

- Nixの考え方（関数的・不変のストア）  
  Nixは「システムは設定の純関数」であるというモデルを採用。パッケージは /nix/store にハッシュ付きで置かれ、異なるバージョンを安全に並列併存できる。過去世代（generations）へのロールバックも簡単で、flake.lock により依存をコミット単位で固定できるため「動作する時点の正確なビルド」を再現できる。

- Flakesの役割  
  flake.nix が設計図、flake.lock がタイムカプセルとして機能し、依存の正確なコミットを固定する。これにより別のマシンでも同一の環境が再現される。

- 一時的シェル（nix shell）の利便性  
  特定の言語やバージョンを一時的に試す「get-and-forget」ワークフローが可能。例: `nix shell nixpkgs#python314` で一時的に Python を利用して終了すれば痕跡は残らない。ただしコンテナ／VMほど隔離されるわけではない点に注意。

- 現実的な課題とハイブリッド運用  
  Nix（とnix-darwin）は強力だが学習コストが高い。GUIアプリは自己更新や /Applications 依存のため手直しが必要なことが多く、トランポリン実行や mkalias 等の細工が必要になる場合がある。実務では重要ツールをNixで管理し、GUIの大物はhomebrewモジュールやcaskに任せるハイブリッド運用が現実的で効果的。

- macOS特有の運用メモ  
  - darwin-rebuild を使って設定を切り替える（例: `darwin-rebuild switch --flake .`）。  
  - 生成済み世代を確認してロールバックできる：  
    ```bash
    sudo nix-env --list-generations -p /nix/var/nix/profiles/system
    ```
  - Nixの導入はDeterministic Nix Installerなどツールを使うと macOS のマルチユーザ周りの面倒を軽減できる。

## 実践ポイント
- 最初の導入
  1. Determinate Nix Installer で macOS に Nix を入れる。  
  2. flake を初期化し、home-manager と nix-darwin を組み合わせる。  
- 設定の分割とバージョン管理  
  - system.nix（OS設定）/ dev.nix（開発ツール）/ brew.nix（GUIアプリ）などに分割してモジュール化する。  
  - flake.lock を必ずコミットして「動く状態」をソース管理する。  
- ハイブリッド運用の例（nix から Homebrew の cask を管理）  
  ```nix
  homebrew = {
    enable = true;
    casks = [ "firefox" "thunderbird" "crossover" ];
  };
  ```
- 日常運用
  - 一時的な検証は `nix shell` で済ませる。  
  - 大きな変更は別 generation でテストしてから切り替える。  
- 学習のコツ
  - まずは小さな部分（シェル設定、コンパイラ）から移行して慣れる。  
  - GUIアプリや macOS 特有の振る舞いはドキュメントとコミュニティ（nix-darwin のマニュアル）を参照しつつ段階的に調整する。

