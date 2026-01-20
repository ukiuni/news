---
layout: post
title: "Running Claude Code dangerously (safely) - Claude Code を“危険に”走らせる（でも安全に）"
date: 2026-01-20T13:37:19.667Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.emilburzo.com/2026/01/running-claude-code-dangerously-safely/"
source_title: "Running Claude Code dangerously (safely) ::         Emil Burzo"
source_id: 46690907
excerpt: "VirtualBox＋VagrantでClaude Codeの許可省略を安全に試す手順"
---

# Running Claude Code dangerously (safely) - Claude Code を“危険に”走らせる（でも安全に）
「許可待ちゼロ」でAIに実行させる—でもホストを守るVagrantサンドボックス術

## 要約
Claude Code の --dangerously-skip-permissions を便利に使いたいが、ホスト破壊が怖い──そんなときはVirtualBox＋Vagrantで完全な仮想マシンを用意して、AIに自由に操作させつつ被害を限定する手法を紹介する。

## この記事を読むべき理由
日本の開発現場では、社内コードやローカル環境を“AIに自由に触らせる”ことに心理的・ポリシー的な抵抗がある。だが許可プロンプトを逐一許可しているとワークフローが途切れる。本稿は「効率」を保ちつつ「被害範囲を限定」する現実的な運用案を示す。

## 詳細解説
- 問題：Claude Code の --dangerously-skip-permissions を使うと、パッケージのインストールやファイル削除などを確認無しで実行してしまう。便利だがホスト側での事故リスクが高い。
- なぜ Docker は合わないか：Docker で隔離しようとすると、コンテナ内でさらに Docker を動かす（Docker-in-Docker）必要が出てきて、結局 --privileged でランタイムに近い権限を与えざるを得ない。これは「隔離の放棄」につながる。
- 提案する解：Vagrant + VirtualBox によるフルVM。ホストと異なるカーネル空間で動くためファイルシステムやプロセスの事故から隔離しやすい。ベネフィットは再現可能な設定ファイル（Vagrantfile）、簡単に破棄・再生成できる点。
- 実装要点：VM に Docker / Node / claude-code CLI を入れ、プロジェクトを共有フォルダでマウントする。作業フローはホストで vagrant up → vagrant ssh → claude-code --dangerously-skip-permissions。終わったら vagrant suspend（あるいは destroy）で簡単に状態を巻き戻せる。
- 注意点と限界：VirtualBox 7.2.4 ではアイドル時の高CPU問題などバグがあるためバージョン注意。VMescape のような攻撃やネットワーク経由のデータ漏洩は完全には防げない。共有フォルダはデフォルトで双方向なので、AIがプロジェクトファイルを壊す可能性がある（必要なら type: "rsync" で一方通行にする）。

Vagrantfile の一例（要点を簡潔化）:

```ruby
# Ruby
vm_name = File.basename(Dir.getwd)

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-24.04"
  config.vm.synced_folder ".", "/agent-workspace", type: "virtualbox"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus   = 2
    vb.gui    = false
    vb.name   = vm_name
    vb.customize ["modifyvm", :id, "--audio", "none"]
    vb.customize ["modifyvm", :id, "--usb", "off"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y docker.io nodejs npm git unzip
    npm install -g @anthropic-ai/claude-code --no-audit
    usermod -aG docker vagrant
    chown -R vagrant:vagrant /agent-workspace
  SHELL
end
```

運用イメージ：
- 初回は vagrant up 中にプロビジョニングで環境構築（数分〜数十秒）。
- プロジェクト単位で VM を用意すれば、プロジェクトごとに Claude に自由に触らせられる。
- 問題が起きたら vagrant destroy してクリーン再作成が可能。

## 実践ポイント
- まずは試験プロジェクトで試す：重要データは置かない。git 管理下なら被害は最小化できる。
- コマンド：vagrant up → vagrant ssh → claude-code --dangerously-skip-permissions
- リソース割当：4GB / 2CPU を目安。必要に応じて増減。
- 同期フォルダの扱い：双方向の共有が嫌なら type: "rsync" にしてホスト→VM の一方同期にする（戻すのは手動）。
- VirtualBox のバージョン確認：7.2.4 等で既知の不具合があるため、問題が出たら別バージョンを検討する。
- セキュリティモデルを明確に：この構成は「誤操作を防ぐ」ための隔離であり、高度な攻撃やデータ漏洩を完全に防ぐものではない。

この方法は「AIに任せて効率を上げたいがホストは守りたい」場面に実用的な折衷案を提供する。まずは小さな実験から試して、社内ポリシーや重要データの有無に応じて運用ルールを整備すると良い。
