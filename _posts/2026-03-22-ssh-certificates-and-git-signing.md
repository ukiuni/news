---
layout: post
title: "SSH certificates and git signing - SSH 証明書と git 署名"
date: 2026-03-22T14:46:03.680Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codon.org.uk/~mjg59/blog/p/ssh-certificates-and-git-signing/"
source_title: "SSH certificates and git signing"
source_id: 1153176793
excerpt: "SSH証明書＋TPMでgit署名の「真の作者」を強固に証明する方法"
---

# SSH certificates and git signing - SSH 証明書と git 署名
git署名が変わる：SSH証明書×TPMで「本物の作者」を証明する方法

## 要約
SSH証明書を使うと、署名付きコミットに対して「その鍵が誰に属するか」をより強く主張できる。さらに鍵をTPMやSecure Enclaveに置けば、署名が本当にハードウェア上で行われたことまで目指せる。

## この記事を読むべき理由
サプライチェーン攻撃やアカウント乗っ取りが増える中で、「誰がコミットしたか」を信頼できる仕組みは日本のプロダクト開発やOSS運用にも直結する課題だから。

## 詳細解説
- なぜSSH証明書か：OpenPGPやX.509に比べて運用がシンプルで、既存のSSH CAインフラをそのまま再利用できる。証明書にはPrincipals（ユーザ名やグループ情報）などのメタデータが含まれる。
- git側の設定：gitは古い設計で署名設定がgpg名前空間に格納されているが、SSH署名はサポートされる。署名キーは証明書ファイルを直接指すか、SSHエージェント経由で取得するコマンドを指定する形で使える。
- 検証の現状：ネイティブ検証はssh-keygenとauthorized_keys風のフォーマット（例：cert-authority）に依存するため、細かなポリシー（有効期限やグループ制約など）を表現しにくい。GitHub/GitLabはSSH証明書による「コミット信頼」の一括指定をまだサポートしていない。
- 実装例：著者は、CA公開鍵でコミット列を検証するスクリプト（OpenPGP併用オプションあり）と、TPM-backedキーをSSHエージェント経由で扱うツールを作成している。後者はgo-attestationを用い、鍵生成時にTPMアテステーション情報も収集する。
- ハードウェア保護とアテステーション：鍵をTPM/SEに閉じ込めれば盗難リスクを下げられ、アテステーションを利用すれば「その鍵が実際にハードウェアで生成された」ことを証明するルートが作れる。

## 実践ポイント
- 基本設定（例）:
```bash
git config --global gpg.format ssh
git config --global user.signingkey /path/to/your.cert.pub
# あるいはエージェント経由
git config --global gpg.ssh.defaultKeyCommand "/path/to/ssh-agent-wrapper -ca /path/to/ca.pub"
git commit -S -m "Signed commit"
```
- CIで検証する：著者の検証ツールや同等の仕組みで、マージ前にコミットがCA署名（または許可されたPGP）であることをチェックする。
- 鍵の保護：可能ならSecure Enclave（Mac）、TPM（Linux/Windows）を使い、エージェント経由で署名できる構成にする。MacはSecretive、Linuxはssh-tpm-agentや著者のツールを検討。
- 運用注意：CA公開鍵の管理・ローテーションを厳格にし、GitHub/GitLab上だけで信頼を委ねない。Web/API由来のコミットはPGP署名になることがあるため併用ポリシーを設ける。

原著：Matthew Garrett（要点を翻訳・整理）
