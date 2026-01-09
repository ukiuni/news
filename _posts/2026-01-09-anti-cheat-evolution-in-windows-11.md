---
layout: post
title: "Anti-cheat evolution in Windows 11 - Windows 11におけるアンチチートの進化"
date: 2026-01-09T03:54:32.893Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.andrea-allievi.com/blog/new-year-post-anti-cheat-evolution-in-windows-11/"
source_title: "New Year post: Anti-cheat evolution in Windows 11 &#8211; AaLl86 Security"
source_id: 46480664
excerpt: "TPMとセキュアカーネルで実行時ドライバを証明しゲームの不正を検出する技術"
---

# Anti-cheat evolution in Windows 11 - Windows 11におけるアンチチートの進化
チートをハードウェアで封じる――Windows 11の「証明できる」アンチチートが示す未来

## 要約
Windows 11に導入された「attestable（証明可能な）ドライバレポート」は、TPMとSecure Kernelを使って実行時のカーネルモジュール情報を署名付きで提供し、ゲームサーバー側でクライアント環境の改ざんを検証できる仕組みです。これによりソフトウェア的な改変だけでなく、悪意あるカーネルモジュールや一時的にロードされた不正ドライバも検出しやすくなります。

## この記事を読むべき理由
- 日本のPCゲーム市場やeスポーツ運営は不正対策の強化が重要で、サーバ側で信頼できるクライアント状態を確認できる技術は即戦力になります。  
- Windows 11ではTPM 2.0が要件であり、既存のハードウェア基盤を利用した新しい防御手法が現実味を帯びています。  
- アンチチート実装や運用（サーバ検証・ブラックリスト運用）を検討するエンジニア、セキュリティ担当者に有益です。

## 詳細解説
- TPMの役割（簡潔）
  - TPMはプラットフォームの測定値（PCR）を安全に蓄積・署名できる「ルート・オブ・トラスト」です。Extend操作で測定値を連鎖的に更新し、最終的なPCRはTPMのQuote（AIKで署名）で外部に証明できます。EKは製造時の固有鍵で、AIKの正当性を間接的に担保します。
- システム整合性と鍵の「シール」
  - TPMは特定のPCR状態でのみアンシール（復号）できる鍵を作れるため、ブート時の設定やSecure Kernelの有無などが期待値と異なれば鍵は復号されません。これが遠隔側での環境検証に使われます。
- チート手口の要点
  - ソフトウェアからゲームメモリを直接書き換える方法と、悪意あるDMAを行う外付け機器（偽装PCIeなど）を使う方法が主流。後者はIOMMUで部分的に防げるが、パフォーマンスや実装上の制約で完全防御は難しいことがあります。
- Attestable driver report（実行時証明レポート）
  - Windows Insider／25H2の更新で、HVCI（Hypervisor-protected Code Integrity）有効時にユーザモードから呼べるAPIが登場しました。例（SDK定義の抜粋）：
  ```c
  #define RUNTIME_REPORT_PACKAGE_VERSION_CURRENT (1)
  typedef enum _RUNTIME_REPORT_TYPE { RuntimeReportTypeDriver = 0, RuntimeReportTypeCodeIntegrity = 1 } RUNTIME_REPORT_TYPE;
  BOOL GetRuntimeAttestationReport(UCHAR* Nonce, UINT16 PackageVersion, UINT64 ReportTypesBitmap, _Out_ PVOID ReportBuffer, _Inout_ PUINT32 ReportBufferSize);
  ```
  - 呼び出すとSecure Kernel（HVCI下）が QUERY_RUNTIME_ATTESTATION_REPORT を通じて署名されたレポートを生成します。レポートはカーネルモジュール（ロード済み／一時的にロードされたもの含む）を列挙し、各モジュールのSHA256、署名の葉証明書ハッシュ（SHA1）、OEM名、ロード回数やフラグなどを含みます。
- サーバ側での遠隔証明フロー（簡易）
  1. クライアントからTPM Quote、TCGログ、ドライバレポートを受け取る。  
  2. サーバはTCGログの記録を再現してPCRを計算し、TPM QuoteのPCR値と一致することを確認。  
  3. AIK/EKの信頼性を検証し、Secure Kernel署名とTCGログ内の測定値が整合するか確認。  
  4. ドライバレポート内の各モジュールハッシュとブラックリストや許可リストを照合。必要ならロード済みかつ既知の悪性ドライバがあれば切断。  
  5. 任意間隔で再取得して継続的に監視（TPMのQuoteが変わらなければTCGログは毎回不要）。
- セキュリティ上の抑えどころ
  - HVCI有効下では、カーネル領域はHypervisorのステージ2マッピング（NXなど）で保護され、任意の実行コードをNTカーネルに直接挿入することは困難になります。  
  - ただし完全無敵ではなく、TPM/Plutonが物理的に改ざんされたり、Secure Kernel自体に脆弱性があれば攻撃は可能です。PlutonのようにSoCに統合された実装は改ざん耐性を高めます。

## 実践ポイント
- ゲーム開発者／サーバ運営者向け
  - サーバ側で「TPM Quote + TCGログ + ドライバレポート」を組み合わせた遠隔証明フローを組み込み、ハンドシェイクで検証を必須化する。  
  - ドライバハッシュ、葉証明書ハッシュ、OEM文字列などを元にブラックリスト／ホワイトリスト運用を作る。短い再検証間隔で継続的に確認すること。  
- システム管理者／エンドユーザ向け
  - HVCI（Core Isolation）とSecure Boot、IOMMUの有効化を推奨。Windows 11とTPM 2.0はこのモデルを実用化する基盤です。  
  - プライバシー配慮：レポートにはシステムの詳細情報が含まれるため、導入前に利用規約／同意プロセスを用意すること。  
- 実装／検証
  - まずはWindows Insider SDKで GetRuntimeAttestationReport を試験的に動かし、TCGログ取得／TPM Quoteの検証スクリプトを作る。日本で流通するハード（Pluton搭載機など）でも動作確認を行うこと。  
- 注意点
  - 完全な防御ではないため多層防御を維持する（ネットワーク側の不正検知、ランタイム監視、ユーザ行動監視など）。

この記事は、TPMとSecure Kernelを組み合わせた「実行時証明」により、従来のアンチチートが苦手としてきた一時的なカーネル改変や悪意のあるドライバによる不正をより確実に検出する方向性を示しています。日本のゲーム/セキュリティ関係者は早めに検証環境を作り、運用ルールとプライバシー対応を整備しておくと良いでしょう。
