---
  layout: post
  title: "Determining Current Arm Cortex-M Security State with GDB - Arm Cortex‑M の現在のセキュリティ状態を GDB で判定する方法"
  date: 2026-01-04T00:20:13.507Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://danielmangum.com/posts/arm-cortex-m-security-state-gdb/"
  source_title: "Determining Current Arm Cortex-M Security State with GDB · Daniel Mangum"
  source_id: 46414683
  excerpt: "GDBで数レジスタを見比べるだけでCortex‑MのTrustZone状態を即判定"
  image: "https://danielmangum.com/images/twitter-card.png"
---

# Determining Current Arm Cortex-M Security State with GDB - Arm Cortex‑M の現在のセキュリティ状態を GDB で判定する方法
思わずデバッグしたくなる！GDBで数秒で分かる、Cortex‑M TrustZone（Armv8‑M）現在状態の見極め方

## 要約
Armv8‑M（Cortex‑M33 など）の TrustZone 実装では、スタックポインタが Secure / Non‑Secure のどちらの領域を使っているかで現在のセキュリティ状態を推定できます。GDBから数個のレジスタを一度に表示するだけで「今SecureかNon‑Secureか」が簡単に分かります。

## この記事を読むべき理由
日本の組込み／IoT 開発では、セキュアブートや分離された実行環境（TrustZone）を使うケースが増えています。ファームウェアの動作確認やデバッグで「いまプロセッサがどちらのセキュリティ状態で動いているか」を即座に判定できると、原因切り分けや動作確認が劇的に速くなります。

## 詳細解説
- 背景：
  - Armv8‑M のセキュリティ拡張（CMSE / TrustZone）ではメモリを Secure / Non‑Secure に分割し、コアはそれぞれの領域で「Secure状態」「Non‑Secure状態」を持ちます。
  - スタックポインタ（SP / R13）は実行モード（Handler/Thread）と CONTROL.SPSEL の値によって MSP（Main SP）か PSP（Process SP）を参照します。TrustZone が有効な場合、それぞれに Secure / Non‑Secure のバリアントが存在します（例：MSP_S / MSP_NS, PSP_S / PSP_NS）。

- 判定の考え方：
  - 現在の SP 値がどの MSP/PSP（Secure／Non‑Secure）と一致するかを比較すれば、現在のセキュリティ状態を推測できます。
  - GDBで該当レジスタを一括表示し、SP が MSP_S/PSP_S のどちらかと一致すれば Secure、MSP_NS/PSP_NS と一致すれば Non‑Secure と判断します。

- 実際の GDB 操作（要点）：
  - 対象レジスタを一度に表示するコマンド例：
```bash
# 表示対象：SP, PSP_NS, MSP_NS, PSP_S, MSP_S
i r sp psp_ns msp_ns psp_s msp_s
```
  - CONTROL.SPSEL を確認するには CONTROL レジスタの 2 ビット目をマスクして見る：
```bash
# CONTROL.SPSEL が 1 ならスレッドモードで PSP を使用中
print $control & 0x2
```
  - SP と各 MSP/PSP のどれが一致するかを見れば、現在が Secure か Non‑Secure かが分かります。

- 注意点：
  - 実行モード（Handler/Thread）や RTOS の設定によって MSP/PSP の割り当てが変わります。特に割り込みハンドラでは常に MSP が選ばれます。
  - ベクタテーブルやOSのスタック配置により値がゼロや特殊なアドレスになるケースもあるため、単純に「0かどうか」での判定は避け、比較で確認してください。

## 実践ポイント
- すぐ試せるワークフロー（デバッグ時）：
  1. GDBでターゲットに接続して停止（reset や break main 等）。
  2. 次のコマンドを実行して SP および MSP/PSP の各バリアントを表示：
```bash
i r sp psp_ns msp_ns psp_s msp_s
```
  3. SP の値がどれと一致するかを確認して Secure / Non‑Secure を判定。
  4. 必要なら CONTROL.SPSEL を確認：
```bash
print $control & 0x2
```
- 日本での応用例：
  - IoT デバイスや工場制御のファームウェアで、Secure 側／Non‑Secure 側の切り替えやブートフロー確認に有効。
  - Zephyr 等の RTOS を使っているプロジェクトでは、Threadモードでの PSP 使用状況と合わせてチェックすると誤動作の原因追跡が捗る。
- 補足：さらに確実に状態を把握したい場合は、PSA/TrustZone の文書で Secure attribution（メモリ領域の割当）やベクタテーブルの配置も合わせて確認してください。

この方法は「素早く現在のセキュリティ状態だけを把握したい」ときにとても便利です。現場でのデバッグ時間を減らす小技として覚えておくと役立ちます。
