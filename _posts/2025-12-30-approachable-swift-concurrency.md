---
layout: post
title: "Approachable Swift Concurrency - 理解しやすい Swift の並行処理"
date: 2025-12-30T14:39:17.390Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://fuckingapproachableswiftconcurrency.com/en/"
source_title: "Approachable Swift Concurrency"
source_id: 46432916
excerpt: "async/await・Actors・SendableでSwift並行処理を短時間で安全に習得"
---

# Approachable Swift Concurrency - 理解しやすい Swift の並行処理
Swiftの非同期処理がやっと分かる！async/await・Tasks・Actors・Sendableを短時間で理解するための実践ガイド

## 要約
Swift Concurrencyは「いつ止まるか（await）」と「誰がデータに触れるか（隔離）」を明確にし、async/awaitで可読性を上げつつ、ActorsとSendableでデータ競合をコンパイル時に防ぐ仕組みを提供する。

## この記事を読むべき理由
iOS/Swiftの現場では非同期I/Oや並列処理が増え、UIフリーズやデータレースのリスクが高まっています。日本のアプリ／サーバー開発でも、安全かつ効率的に並行処理を書くための基本と落とし穴を短時間で押さえられます。

## 詳細解説
- async/await（待機の表現）  
  非同期処理をコールバックではなく逐次的に書ける構文。`async`関数は途中で「止まり（suspend）」、`await`で再開される。例：
  ```swift
  func fetchUser(id: Int) async throws -> User {
      let url = URL(string: "https://api.example.com/users/\(id)")!
      let (data, _) = try await URLSession.shared.data(from: url)
      return try JSONDecoder().decode(User.self, from: data)
  }
  // 呼び出し側
  let user = try await fetchUser(id: 123)
  ```

- 並列実行の簡単な書き方：`async let` と `TaskGroup`  
  複数I/Oを同時に開始して後で結果を集める：
  ```swift
  func loadProfile() async throws -> Profile {
      async let avatar = fetchImage("avatar.jpg")
      async let banner = fetchImage("banner.jpg")
      async let bio = fetchBio()
      return Profile(
          avatar: try await avatar,
          banner: try await banner,
          bio: try await bio
      )
  }
  ```
  多数の並列タスクを管理するときは`withThrowingTaskGroup`で構造化並行性を使う（キャンセル伝播やエラー伝搬が自動的に扱われる）。

- Tasks（開始・キャンセル・背景実行）  
  UIイベントから非同期処理を起動するには`Task { ... }`やSwiftUIの`.task`修飾子を使う。`.task(id:)`で依存ID変化時の再実行も可能。

- Isolation（隔離）とActors  
  従来の「どのスレッドで実行されるか」ではなく「誰がそのデータにアクセスできるか」を宣言する。主要な隔離ドメイン：
  1. @MainActor — UI操作やViewModelに適用。主にメインスレッド相当。  
  2. actor — 自分の可変状態を単独で保護する隔離単位。外部から呼ぶときは`await`が必要。  
  3. nonisolated — 隔離を放棄するメソッド。隔離された状態にはアクセスできない。

  例：
  ```swift
  @MainActor class ViewModel {
      var items: [Item] = []
  }

  actor BankAccount {
      var balance: Double = 0
      func deposit(_ amount: Double) { balance += amount }
  }
  ```

- Sendable（値の安全な受け渡し）  
  異なる隔離ドメイン間で値を渡すとき、型が安全に共有できるかをコンパイラがチェックするのが`Sendable`。値型や不変データは自動でSendable。mutableなクラスは原則不可。スレッド安全性を自前で担保しているなら`@unchecked Sendable`でコンパイラを説得できるが、誤るとデータレースを招く。

- Approachable Concurrency（Xcode設定）  
  Xcode 26以降のデフォルト設定では：
  - SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor（デフォルトでMainActor隔離）
  - SWIFT_APPROACHABLE_CONCURRENCY = YES（nonisolated asyncが呼び出し側のアクター上に留まる）  
  これにより、多くのコードでSendableの注釈が不要になり、既存コードの摩擦が減る。CPU負荷の高い処理は`@concurrent`で明示的にオフロードする。

- よくある落とし穴
  - mutableなクラスを隔離を跨いで渡すとデータレースが起きる  
  - `@unchecked Sendable`は最後の手段（責任は開発者）  
  - CPUバウンド処理をMainActor上で走らせるとUIが固まる（適切に`@concurrent`や専用キューへ）

## 実践ポイント
- まずViewModelやUI操作周りは@MainActorで保護する。パフォーマンス問題が出たらプロファイルして最適化する。  
- 複数I/Oは`async let`で簡潔に並列化、複雑な並列ワークは`TaskGroup`で構造化する。  
- UIイベントからの非同期開始は`Task {}`またはSwiftUIの`.task`を使う。`.task(id:)`で依存関係に応じた再取得を自動化。  
- 型を設計する際は値型（struct）で不変にするか、mutableなクラスにはスレッド安全な実装を施す（それでも`@unchecked Sendable`は注意して使う）。  
- Xcode 26の新規プロジェクト設定（SWIFT_DEFAULT_ACTOR_ISOLATION / SWIFT_APPROACHABLE_CONCURRENCY）を理解し、チームでポリシーを決める。  
- CPU重めの処理は`@concurrent`や専用のバックグラウンドTaskで実行してUIスレッドを守る。  
- 単体テスト／並行シナリオのテストでキャンセルやデータ競合を検証する習慣をつける。

