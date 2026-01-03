---
  layout: post
  title: "A Basic Just-In-Time Compiler (2015) - 基本的なJITコンパイラ（2015）"
  date: 2026-01-03T02:11:24.775Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://nullprogram.com/blog/2015/03/19/"
  source_title: "A Basic Just-In-Time Compiler"
  source_id: 46471712
  excerpt: "演算列をネイティブ機械語に変換し再帰式を高速化するJIT実装入門"
  ---

# A Basic Just-In-Time Compiler (2015) - 基本的なJITコンパイラ（2015）
数行の定義をそのままネイティブ機械語へ――自作JITで再帰式を一気に高速化する方法

## 要約
作者は「再帰関係（$u(n+1)=f(u(n))$）」を逐次解釈する代わりに、与えられた演算列をその場でネイティブ命令列に変換して実行する超シンプルなx86-64 JITを実装している。mmap/VirtualAlloc→機械語生成→mprotect/VirtualProtect→関数化、という流れが核心。

## この記事を読むべき理由
直感的で小さな問題を題材に「メモリ保護」「呼び出し規約」「機械語の埋め込み」といったJITの基礎技術を実践的に学べる。日本の組込み／ゲーム／高速処理や、独自言語・DSLを試したいエンジニアにとって手を動かして理解できる良い入門になる。

## 詳細解説
- 問題設定：入力は初期項と演算列（例: "+2 *3 -5"）。逐次実行だと一つずつ処理するが、JITは演算列をネイティブ命令に変換して一度に実行する。
- 実行可能メモリの確保と保護：
  - POSIXでは匿名マップ mmap(..., PROT_READ|PROT_WRITE, MAP_ANONYMOUS|MAP_PRIVATE, ...) でページ単位に確保し、コード生成後に mprotect(..., PROT_READ|PROT_EXEC) で実行可能にする。
  - Windowsでは VirtualAlloc(..., PAGE_READWRITE) → VirtualProtect(..., PAGE_EXECUTE_READ) を使う。
  - 重要点は W^X（Write XOR Execute）への対応。書き込み時と実行時でページ属性を切り替える必要がある。
- asmbuf 構造：例として1ページ分のバッファに命令列を書き込み、最終的にその先頭を関数ポインタにキャストして呼ぶ。ページサイズは sysconf(_SC_PAGESIZE) で取得すべき。
- 呼び出し規約：System V AMD64 ABI では第一引数が rdi、戻り値は rax。Windows x64 は第一引数が rcx。JITが受け取る入力レジスタだけはプラットフォームで扱いが変わる点に注意。
- 機械語生成の実務テクニック：
  - 命令バイト列を一から解読する代わりに、nasm 等でアセンブルし ndisasm でバイナリを確認して、そのバイト列をそのままバッファに埋める手法が紹介されている（手作りアセンブラ的な手法）。
  - 例：引数コピーは mov rax, rdi → バイト列 0x48 0x89 0xF8、戻りは ret → 0xC3。
  - 即値を扱うには mov rdi, imm64 のテンプレートを用意して、即値部分をリトルエンディアンで書き込む。
  - 各演算は rax に結果を保持し、操作するオペランドは事前に rdi にロードしておく（単純化のため）。
  - 加算/減算/乗算/除算のための命令バイト列を用意して順次追加（例: add rax, rdi / imul / idiv など）。除算は rdx をクリアしてから idiv を呼ぶ必要がある。
- 実行：
  - コード生成が終わったらページを PROT_EXEC にし、関数ポインタにキャストして呼ぶ。戻り値は rax に入ってくる。
- 制約と注意点：
  - この記事の実装は分岐・スタック操作・中間値保存・関数呼び出し等を扱わない極めて簡易なもの。安全性（境界チェック、SIGSEGV対応）、シグナルハンドリング、ASLRや実行権限の厳格化にも配慮が必要。
  - ネイティブコードを生成する以上、整合性とセキュリティに最新の注意を払うこと（ユーザ入力をそのままコードにするのは危険）。

参考となる最小コード片（POSIX, C）:
```c
// c
void *asmbuf_create(void){
    size_t pagesz = sysconf(_SC_PAGESIZE);
    return mmap(NULL, pagesz, PROT_READ|PROT_WRITE,
                MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
}
void asmbuf_finalize(void *buf, size_t len){
    mprotect(buf, len, PROT_READ|PROT_EXEC);
}
```

## 実践ポイント
- 最初は短い式・演算のみで試す（例: "+2 *3 -5"）。動作とバイト列を目で追える範囲が望ましい。
- nasm + ndisasm のワークフローで「ソース命令 → バイナリ」を確認してテンプレート化する。
- ページサイズはハードコードせず sysconf(_SC_PAGESIZE) を使う。Windowsは VirtualAlloc/VirtualProtect に対応させる。
- W^X を尊重して「書き込み→切り替え→実行」を必ず行う。CI やテスト環境では実行権限の制限で動かない場合があるので注意。
- 複雑化するなら LLVM / libjit を検討する。自作JITは学習や特殊ケース向けには有効だが、安全性・最適化面で成熟したツールに任せるべき場面も多い。
- 日本のプロジェクトでの応用例：ゲームのホットパス最適化、数値シミュレーションのDSL、軽量スクリプトの実行エンジンなど。小さく始めて、必要なら既存のJIT基盤へ移行するのが現実的。

短いコードと実機バイナリで「動くものを作る」体験が得られる良記事。JITの基本パーツを手で触って学びたい人に最適。
