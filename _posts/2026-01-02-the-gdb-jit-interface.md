---
  layout: post
  title: "The GDB JIT interface - GDB の JIT インターフェース"
  date: 2026-01-02T02:16:00.888Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://bernsteinbear.com/blog/gdb-jit/"
  source_title: "The GDB JIT interface | Max Bernstein"
  source_id: 1229759105
  excerpt: "GDBでJITを可視化する実践ガイド：perfmapとカスタムリーダの比較"
  image: "https://bernsteinbear.com/favicon.ico"
---

# The GDB JIT interface - GDB の JIT インターフェース
GDBでJITコードを「普通に」デバッグするための現実的ガイド — 実装の選択肢と落とし穴

## 要約
GDBは通常コンパイラが埋め込むDWARF情報で高機能なデバッグ表示を行うが、JITで生成されたコードはそのままでは「???」だらけになる。GDBは古いDWARFベースの登録APIと、任意フォーマットのデバッグリーダを読み込む新しいインターフェースの二択を提供している。

## この記事を読むべき理由
JITを使うランタイム（JSエンジン、VM、ゲームや高速トレースを行うライブラリなど）を開発・運用する日本のエンジニアにとって、GDBでJITコードを正しく表示／スタックトレースを得る知識は、デバッグ生産性と運用観測性を大きく改善するため必須。

## 詳細解説
- 既存の仕組み（古いインターフェース）
  - GDBはプロセス側に特定のシンボルを期待する：関数名 `__jit_debug_register_code` とグローバル変数 `__jit_debug_descriptor`。これらを使って「メモリ上で生成したELF/Mach-O+DWARF相当のシンボルファイル」をGDBに通知する。  
  - 流れ：JITで関数を生成 → その関数情報を短いオブジェクト（symfile）としてメモリ上に作る → `jit_code_entry` を linked list に追加 → `__jit_debug_register_code()` を呼ぶ → GDBがブレークして新しいシンボルを読み取る。  
  - ために多くのプロジェクト（V8やMonoなど）がオブジェクト生成ロジックを内蔵している。
- 新しいインターフェース（カスタムデバッグリーダ）
  - DWARFを作らず、独自のバイナリ形式でデバッグ情報を書き、GDBに読み手(shared object)をロードさせる。読み手は以下のようなAPIを実装する必要がある（抜粋）:

  ```c
  extern struct gdb_reader_funcs *gdb_init_reader(void);
  struct gdb_reader_funcs {
    int reader_version;
    void *priv_data;
    gdb_read_debug_info *read;
    gdb_unwind_frame *unwind;
    gdb_get_frame_id *get_frame_id;
    gdb_destroy_reader *destroy;
  };
  ```

  - read が主要部分で、アドレス範囲を関数名や行番号へマッピングする責務を持つ。多くの実装は unwind / get_frame_id を簡易にしている。
- perf map を流用する発想
  - /tmp/perf-... の perf map はアドレス→名前を吐く既存インターフェースなので、GDB側にパーサを作るか、カスタムリーダで perf map を読むことで比較的簡単な「最低限のシンボル情報」を得られる。ただしソース行や埋め込みソース表示は期待できない。
- 実装上の注意点
  - リンクリスト実装はヘッドしか持たないためエントリ数により $O(n^2)$ の操作になる可能性がある（V8の指摘）。  
  - GCとの兼ね合い：GDBはシンボル内のコードポインタが不変であることを期待するため、JITが移動GCを使う場合は移動を停止するか、登録・登録解除を厳密に行う必要がある。ARTのように定期的にデッドエントリを掃除する運用もある。

## 実践ポイント
- まず簡単に：perf map の出力を作り、GDB用に簡易リーダを作ることで最小限の可観測性を素早く確保する。  
- きちんとやるなら：カスタムリーダ（gdb_reader_funcs）を実装して行番号やアンワインド処理を提供する。unwind を実装すればより正確なスタック表示が可能。  
- GC対策：コードポインタが安定する仕組み（移動GCの停止、もしくは登録解除の確実化）を設計する。  
- 性能対策：登録データ構造が単純な linked list だとスケールしない（$O(n^2)$）。多数の小オブジェクトを登録する場合はバッチ化や再パッキング（V8 の RepackEntries 的な工夫）を検討する。  
- テスト：JIT生成直後に `__jit_debug_register_code` を呼んだり、カスタムリーダを GDB の共有オブジェクトとしてロードしてブレーク時の表示を確認する。  

