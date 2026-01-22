---
layout: post
title: "ZXC: another (too) fast decompressor - ZXC：さらに（速すぎる）デコーダ"
date: 2026-01-22T14:02:26.740Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/hellobertrand/zxc"
source_title: "GitHub - hellobertrand/zxc: A high-performance asymmetric lossless compression library optimized for Content Delivery. Decodes 40% faster than LZ4 on ARM64."
source_id: 420377067
excerpt: "Apple M2でLZ4比40%高速、ゲーム資産や配信を劇的に高速化するZXC"
image: "https://opengraph.githubassets.com/df99372fce640d430dca5b5310fb2171874416c499e53ef8b0e862297f33c7e4/hellobertrand/zxc"
---

# ZXC: another (too) fast decompressor - ZXC：さらに（速すぎる）デコーダ
クリックせずにはいられないタイトル: 「AppleシリコンでLZ4より40%速い圧縮フォーマット？ZXCが変える配信と組込み資産の読み込み速度」

## 要約
ZXCは「Write Once, Read Many」を前提にエンコード側で重い解析を行い、デコードを極限まで高速化した非対称ロスレス圧縮ライブラリ。Apple SiliconでLZ4比+40%のデコード性能を実証しています。

## この記事を読むべき理由
モバイルアプリやゲーム、ファームウェア配布、クラウドの高スループットサービスではデコード回数が圧縮より圧倒的に多く、読み込み遅延や帯域コストがユーザー体験と運用コストに直結します。ZXCはその「読み取り多数」の現実に最適化された実践的ソリューションです。

## 詳細解説
- 設計哲学：ZXCは圧縮（ビルド時）を犠牲にしてデコード（ランタイム）を高速化する「非対称効率」に特化。エンコーダが高度な分析でデータレイアウトを最適化し、デコーダはシンプルかつ命令パイプラインに優しい実装で高速化を実現します。
- ベンチマーク：公式ベンチでApple M2（ARM64）単体スレッドではLZ4より最大約+98%（特定設定）だが、実運用向けの標準設定ではおおむね+40%前後。クラウドARMで+20%、x86_64でも+5%程度の改善を報告。圧縮率はLZ4相当〜より良好で、Zstdより高速なデコードと良好な比率を両立する設定もあります。
- 適用領域：ゲームアセットのロード、アプリ起動時リソース、CDN配信、組込み機器やファームウェア（格納容量と起動時間が重要）に最適。
- 実装と配布：CMakeベースでビルド可能。バイナリ配布あり（macOS ARM、Linux aarch64/x86_64、Windows）。lzbenchに統合済みで独立検証が容易。
- 技術的特徴：caller-allocatedのスレッドセーフAPI、チェックサムオプション、レベル1〜5で圧縮速度/比率を選択。ビルド時に -march=native、LTO、PGOオプションが使用可能で実機向け最適化が推奨されます。

## 実践ポイント
- 使いどころ：CIで圧縮を一度だけ行い、配信先で何百万回もデコードされるデータ（ゲーム資産、アプリバンドル、静的コンテンツ）に導入するのが最も効果的。
- 検証手順：lzbenchで自分のデータセット（実際のアセット）を使ってデコードスループットと圧縮比を比較する。公式ベンチは参考値に留める。
- 導入注意：圧縮時間はZXCの方が長くなるため、ビルドパイプラインでのバッチ処理やCIタイミングと調整すること。ランタイムはクロスプラットフォームで高速だが、CPU機能に応じたランタイムディスパッチを活用する。
- すぐ試せるコマンド（例）
  - バイナリを落として実行: chmod +x zxc-* && mv zxc-* zxc
  - 圧縮: zxc -z -3 input.bin out.xc
  - 解凍: zxc -d out.xc out.bin
- 簡単なAPI例（C）
```c
#include "zxc.h"
#include <stdlib.h>
#include <string.h>

int compress_example(const void* src, size_t src_sz){
  size_t bound = zxc_compress_bound(src_sz);
  void* dst = malloc(bound);
  size_t used = zxc_compress(src, src_sz, dst, bound, ZXC_LEVEL_DEFAULT, 1);
  // used==0 -> error
  free(dst);
  return used?0:1;
}
```

導入検討時はまず自分の実データでlzbenchを回し、CI側で圧縮を組み込む運用設計を行ってください。
