---
layout: post
title: "Go Home, Windows EXE, You're Drunk - 帰れ、Windows EXE、酔ってるのか"
date: 2026-01-15T20:21:28.589Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gpfault.net/posts/drunk-exe.html"
source_title: "Go Home, Windows EXE, You're Drunk"
source_id: 425999573
excerpt: "Windows実行ファイルがWine上で直接Linuxのsyscallを叩いて動く衝撃実験"
---

# Go Home, Windows EXE, You're Drunk - 帰れ、Windows EXE、酔ってるのか
Wine上で「WindowsバイナリがLinuxのsyscallを直呼び出し」する愉快な実験

## 要約
Windows向けの実行ファイル（PE）がWine上で実行されると、なんとLinuxのsyscallを直接叩いて動作することが可能だったという冗談じみた実験結果。WinAPIを経由しない「生のsyscall」を使うと互換性問題が出るはずだが、逆向き（Windowsバイナリ→Linux syscall）は動いてしまった。

## この記事を読むべき理由
日本でもWineはレガシー業務アプリやゲーム、開発環境の移行で注目される。互換性の落とし穴やセキュリティ的な想定外の振る舞いを理解しておくことは、移行計画やトラブルシューティング、逆アセンブルの現場で役に立つ。

## 詳細解説
- syscallsとは：アプリケーションがOSにサービスを依頼する低レベルの呼び出し（ファイル操作、メモリ確保など）。LinuxとWindowsで呼び出し方や期待されるABIが異なる。
- Windowsの通常動作：アプリはWinAPI（user32/kernel32など）を呼び、これらのライブラリが内部でカーネルとやり取りする。直接syscall命令を叩くことは想定されていない（仕様的に保証されない）。
- Wineの仕組み：PEファイルをそのままプロセス空間に展開し、WinAPI相当の実装を提供してWindowsプログラムを「ネイティブプロセス」として動かす。仮想化や完全エミュレーションはしていない。
- 問題点：Windows向けに直接Windows規約のsyscallを書くプログラムはWine上でクラッシュする可能性が高い。これはWindowsのsyscall ABIをそのままLinuxで実行すると合わないため。
- 実験の肝：ならば逆に、Windowsバイナリの中からLinuxのsyscall ABI（レジスタにLinuxの呼び出し番号や引数をセットして syscall 命令）を呼ぶとどうなるか？という愉快な試み。結果、Wine上では成功した。標準出力への write（rax=1 など）や fork/execve でLinuxプロセスを起動できたが、元プロセスが不安定になるなど副作用も観察された。
- なぜ動くか（概略）：WineはプロセスをLinuxプロセスとして扱うため、CPU上の syscall 命令はカーネルに届く。バイナリがLinux向けのレジスタ約束に合わせれば、カーネルはそれを受け付ける。だから理屈上は動く。ただし実用性はほぼ無いし未保証の挙動。

短い実験コード（要点のみ、Flat Assembler風）：
```asm
; asm
mov rax, 1        ; write syscall (x86-64 Linux)
mov rdi, 1        ; stdout
mov rsi, msg      ; buf
mov rdx, len      ; len
syscall
```

## 実践ポイント
- Wineで動作確認する際は、アプリが「非公開のsyscall」に依存していないか注意する。動かない場合、まずWinAPI経由の呼び出しを疑う。
- レガシーWindowsアプリをLinuxへ移行する際は、WinAPI準拠で動作するかどうかをテスト環境（複数のWineバージョン）で確認する。
- 互換性問題のデバッグには、objdump / readelf / pefile で呼び出しを解析し、strace や Wine のデバッグログで実行時のsyscallを観察する。
- セキュリティ面：想定外のsyscallを実行できるということは攻撃面が増える可能性もある。Wineでの実行は権限分離やサンドボックス設定を検討する。
- 研究・逆アセンブルのネタには面白いが、本番用途や正式サポートを期待するのは避ける。ドキュメントに頼らない挙動は将来壊れるリスクが高い。

この実験は「動いてしまう」ことが面白いだけで、実務での利用は推奨されない。Wineや互換レイヤーの理解を深める良いデモだ。
