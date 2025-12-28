---
layout: post
title: "Can I throw a C++ exception from a structured exception?"
date: 2025-12-28T16:19:01.968Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devblogs.microsoft.com/oldnewthing/20170728-00/?p=96706"
source_title: "Can I throw a C++ exception from a structured exception?"
source_id: 436091837
excerpt: "SEHをC++例外に変換する安易なトリックが最適化崩壊と未定義動作を招く理由"
---

# SEHをC++例外に変換しても「タダ得」にはならない理由 — /EHaなしでの罠

## 要約
構造化例外（SEH）をUncaughtフィルタやトランスレータでC++例外に変換するトリックは一見魅力的だが、コンパイラの最適化や未定義動作を招き、正しく動作する保証がない。

## この記事を読むべき理由
Windowsネイティブ開発（ゲーム、ドライバ周り、低レイヤのサービス）でアクセス違反や割り算ゼロなどのOS発生例外を扱う場面は多い。パフォーマンスを落とさずにそれらをC++例外として扱いたいと考える開発者にとって、安易な「フィルタでthrow」トリックは危険であり、その理由を短く理解しておくべきだからです。

## 詳細解説
問題のトリックはこうです：SetUnhandledExceptionFilterなどでSEHハンドラを登録し、そこでstd::exceptionをthrowしてC++のtry/catchで捕まえようとする。コード例（要旨）:

```cpp
// cpp
LONG WINAPI CleverConversion(EXCEPTION_POINTERS* ExceptionInfo) {
    // SEH 情報を元にメッセージを作成して
    throw std::exception(message.c_str());
}
int sample_function(int* p) {
    try {
        printf("About to dereference %p\n", p); // ← printf があると"幸運"に動く場合がある
        return *p;
    } catch (std::exception& e) {
        Log(e.what());
    }
    return 0;
}
```

なぜ不安定になるのか、要点は2つです。

1. コンパイラ最適化と例外モデルの関係  
   - MSVCの/EHa（asynchronous+sync例外サポート）を有効にすると、コンパイラは「任意のメモリアクセスや算術でSEHが発生する可能性がある」と見なし、局所変数をメモリに安定して保存するなどの制約を課す。これが最適化低下の主因です。  
   - /EHaを付けない（デフォルトの/EHsc等）場合、コンパイラは「そのブロック内でC++例外が発生しない」と判断できればtry/catchを最適化で消すことがある。上の例でprintfがあるとprintfが noexcept でないためtryが残り「偶然」捕まるが、printfが無ければtryが消えてcatchで捕まらない。

2. 未定義動作の危険性  
   - /EHaを付けずにSEHをC++例外へ“強引に”変換すると、例外発生時にオブジェクトの状態が不安定（未初期化のままデストラクタが走る等）である可能性が高く、未定義動作を引き起こす。元記事のReminder例（フィールドの初期化を遅延する最適化）が良い例です。  
   - つまり「フィルタでthrowしておけばOK」という考えは、コンパイラの理解と実行時状態を裏切るため危険です。

補足：構造化例外を安全にC++例外へ橋渡しする公式手段としては、ランタイムが提供するシリアライズ済みのトランスレーター等を検討する（ただし挙動は例外モデルやプラットフォーム依存）。Uncaughtフィルタ内で無理にthrowするのは避けるべきです。

## 実践ポイント
- SEHをC++のtry/catchで確実に扱いたければ、明示的に/EHaでビルドする（副作用・最適化低下を理解した上で）。  
- 「遅延初期化やレジスタ管理」の最適化が動かなくなる点を考慮し、パフォーマンス影響を測る。  
- SetUnhandledExceptionFilterでのthrowは未定義動作を招く可能性があるため避ける。代替手段（例：専用のSEHハンドリング、プロセス境界での復旧、明示的なエラーパス）を検討する。  
- ライブラリやAPIが noexcept かどうかでtry/catchの残存が変わるため、例外設計（どこでthrow可能か）を明確にする。  
- 日本のプロダクトで高信頼性やセキュリティが要求される場合、OS例外をC++例外に無理に変換するのは避け、設計で扱う（ログ/再起動/サンドボックス化など）方が安全。

## 引用元
- タイトル: Can I throw a C++ exception from a structured exception?  
- URL: https://devblogs.microsoft.com/oldnewthing/20170728-00/?p=96706
