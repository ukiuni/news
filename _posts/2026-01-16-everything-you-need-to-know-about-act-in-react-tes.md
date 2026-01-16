---
layout: post
title: "Everything you need to know about act() in React tests - Reactテストのact()完全ガイド"
date: 2026-01-16T05:52:48.488Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://howtotestfrontend.com/resources/react-act-function-everything-you-need-to-know"
source_title: "Absolutely everything you need to know about act() in React tests | How To Test Frontend"
source_id: 46576261
excerpt: "Reactテストのact()を実践的に解説し、警告を防ぎ非同期更新を確実に検証する方法を紹介"
---

# Everything you need to know about act() in React tests - Reactテストのact()完全ガイド
クリックせずにはいられない！「テストでのact()」を一発で理解して、無駄な失敗を減らす実践ガイド

## 要約
Reactテストでのact()は、コンポーネントの状態更新や副作用がテスト内で確実に反映されるようにするための必須ツール。多くはTesting LibraryのAPIで自動処理されるが、手動トリガーやフックテスト、タイマーや非同期処理では明示的に使うべき場面がある。

## この記事を読むべき理由
日本のフロントエンド開発現場でもReact＋Testing Library／Jest／Vitestの組み合わせは一般的。CIやローカルで「update was not wrapped in act(...)」の警告を見て途方に暮れる人が多いはず。原因と対処、ベストプラクティスを短く整理します。

## 詳細解説
- act()の目的：テストで発生するReactの状態更新や副作用を「フラッシュ（同期処理）」して、古い状態に対する誤ったアサーションを防ぐ。
- どのact()を使うか：基本は @testing-library/react からimportするのが安全（テスト環境設定や互換性ラッパーが入っているため）。
  ```javascript
  import { act } from '@testing-library/react';
  ```
- いつ必要か（代表例）：
  - renderHookでフックを直接操作する時（renderHook の result.current を更新する場合）
  - DOM要素の click() を直接呼ぶなど、userEvent を使わずにイベントを発火した時
  - setTimeout／setInterval やフェイクタイマーを使った非同期の状態更新
  - Promiseの解決で状態が変わる非同期処理
- いつ不要か：
  - userEvent.click / screen.findBy... / waitFor など、Testing LibraryのAPIは内部でact()を扱っているため通常は自前でwrapしなくて良い
- sync vs async：ほとんどの場合は await act(async () => { ... }) を使うのが無難。非同期境界を跨ぐ更新を確実に捕まえられる。
- デバッグのヒント：テスト出力の "update was not wrapped..." 警告は無視厳禁。まずは findBy / waitFor に置き換えられないか検討し、どうしてもだめならactで囲む。

例：フェイクタイマーでの失敗とactでの解決
```javascript
// JavaScript
vi.useFakeTimers();
test('auto increment', async () => {
  render(<AutoCounter />);
  const h = screen.getByRole('heading');
  expect(h).toHaveTextContent('Count: 0');

  await act(async () => {
    vi.advanceTimersByTime(10);
  });

  expect(h).toHaveTextContent('Count: 1');
});
```

フックのテスト例（renderHook）
```javascript
// JavaScript
const { result } = renderHook(useCounter);
await act(async () => {
  result.current.increment();
});
expect(result.current.value).toBe(1);
```

## 実践ポイント
- まずは await screen.findBy... / await waitFor(...) を試す。多くのケースでact()不要になる。
- 手動イベント発火（element.click()）や renderHook 操作では act() を使う。特に非同期処理が絡むなら await act(async () => { ... }) を使う。
- 常に @testing-library/react の act をインポートしておく（互換性と環境設定のため）。
- CIでの警告は見逃さない。ローカルのターミナル（VS Codeの統合ターミナル／テストパネル）で出るならまず原因箇所を特定して対応。
- userEvent を優先：可能なら userEvent や findBy 系で書き換えて、テストの読みやすさと安定性を高める。

短くまとめると：act()は「最後の手段」ではなく「正しく使うべき道具」。まずはRTLの高レベルAPIで済ませ、必要な場面で async act(...) を使えばテストの信頼性がぐっと上がります。
