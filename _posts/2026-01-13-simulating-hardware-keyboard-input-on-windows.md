---
layout: post
title: "Simulating hardware keyboard input on Windows - Windowsでハードウェアキーボード入力をシミュレートする"
date: 2026-01-13T00:59:20.022Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://autoptt.com/posts/simulating-a-real-keyboard-with-faker-input/"
source_title: "Simulating a Real Keyboard with FakerInput | AutoPTT"
source_id: 428320424
excerpt: "FakerInputで物理キーボードを偽装し、SendInput検出を回避する実装手順と運用上の落とし穴を解説"
image: "https://autoptt.com/logo.png"
---

# Simulating hardware keyboard input on Windows - Windowsでハードウェアキーボード入力をシミュレートする
ゲームやアプリに「バレない」仮想キーボードを作る――FakerInputで実現するソフトウェア発火の裏側

## 要約
SendInputでは検出・無視されることがあるため、FakerInputのようなユーザーモードHIDドライバを使うと「物理キーボード」として振る舞わせられる。実際に動かすにはデバイス列挙、正しいレポートフォーマットでのWriteFile、そして入力処理の統合まわりで注意が必要。

## この記事を読むべき理由
- ゲームや一部アプリはSendInput由来の入力を拒否するため、テスト自動化やカスタムPTT（Push-to-Talk）などで確実に動作させたい場面が日本の開発・QA現場でも増えている。  
- FakerInputの使い方と落とし穴（キーが押しっぱなしになる、フックとRawInputの競合、UIとの統合問題）を技術的に理解すれば、実用的で安全な実装ができる。

## 詳細解説
1) SendInputの検出  
- 低レベルフック（KBDLLHOOKSTRUCT.flags の LLKHF_INJECTED）やRaw Input（RAWINPUT.header.hDevice）を見れば、SendInputで合成された入力は簡単に区別できる。多くのゲームはGetAsyncKeyState等でキー状態を直接チェックするため問題にならないが、一部は合成入力を無視する。

2) FakerInputの役割  
- FakerInputはユーザーモードのHIDドライバでOSに「物理キーボード/マウス」として見せる。これによりRaw Inputやデバイスベースの識別をすり抜けられるケースがある（Sidekickという物理マイコン版と同等の考え方）。

3) デバイスに接続してキーを送る流れ  
- デバイスは CreateFile で開き、WriteFile（もしくは HidD_SetOutputReport/WriteFile での出力）でレポートを書き込む。重要な点はドライバ側が期待する「ヘッダ／サイズ」等のバイト列を正確に渡すこと。たとえばレポートを2バイトのコントロールヘッダ（REPORTID_CONTROL, レポート長）で先頭付けしてから実際のキーレポートを渡す必要があった、という実装上の注意。

簡略化した送信例（概念）:
```c
// c
// ハンドルは CreateFile で取得済みとする
uint8_t control[CONTROL_REPORT_SIZE] = {0};
control[0] = REPORTID_CONTROL;
control[1] = sizeof(FakerInputKeyboardReport);
memcpy(control + 2, &keyboard_report, sizeof(keyboard_report));
DWORD written;
WriteFile(handle, control, sizeof(control), &written, NULL);
```

4) デバイスの識別方法  
- SetupDiEnumDeviceInterfaces / SetupDiGetDeviceInterfaceDetail でインターフェースを列挙し、HidD_GetAttributes で VID/PID を確認、HidP_GetCaps で Usage/UsagePage を確認する、という手順でプログラム的に特定できる。

5) 統合時の罠（実運用で遭遇した問題）  
- “キーを押した結果が永続する” 問題：システムから見るとFakerInputは物理キーなので、PTTの状態変更と干渉してしまう。Raw Inputの hDevice を見て生成元を判別し「仮想入力として扱う」ことで回避できる。  
- Raw Input と低レベルフックの共存トラブル：別スレッド／GUIスレッドの違いでフックが動かなくなるケースや、GUIのFPSに引かれて入力処理が遅延するケースがある。結果として別プロセスでRaw Inputを処理し、IPCで本体に伝える（著者はロックフリー共有メモリリングバッファ＋イベントで高速IPCを作った）という解決に至った。

## 実践ポイント
- テストはVMや安全な環境で：キーが押しっぱなしになる等の最悪ケースに備え、すぐ切れる環境を用意する。ハンドルを閉じるとドライバが状態をリセットすることが多い。  
- デバイス列挙と識別を堅牢に：SetupDi*、HidD_GetAttributes、HidP_GetCaps を組み合わせてPID/VIDやUsageを確認する。  
- レポート形式はドライバ実装に依存：公開ヘッダがあればそれに従い、必要な先頭バイト（control/report id/length）を忘れないこと。  
- 入力処理の分離：低レベルフックやRaw InputはGUIスレッドで処理すると遅延や動作停止を招く。別スレッド／別プロセスで処理し、効率的なIPCで連携するのが安全。  
- 法的・倫理的配慮：ゲームのアンチチートや利用規約に抵触しないか事前に確認する。自動操作を悪用しない。  
- 日本の活用例：QA自動化（ゲームのキー操作テスト）、PTT系アプリの互換性確保、ハードウェアが使えない現場での検証ツール作成などに有用。

以上のポイントを押さえれば、FakerInputのようなドライバを安全に使って「より実機に近い」入力シミュレーションが可能になる。実装時はデバイス固有のレポート仕様とOSの入力経路（低レベルフック／Raw Input／GetAsyncKeyState 等）をよく理解して設計すること。
