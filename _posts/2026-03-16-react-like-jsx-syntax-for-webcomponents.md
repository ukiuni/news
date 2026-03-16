---
layout: post
title: "React-Like JSX Syntax for Webcomponents - Webコンポーネント向けのReact風JSX構文"
date: 2026-03-16T12:25:21.894Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://positive-intentions.com/docs/research/Tutorials/dim/dim-functional-webcomponents"
source_title: "1. Functional Web Components | positive-intentions"
source_id: 382626765
excerpt: "JSX構文でReact感覚の関数型Web ComponentsをLitで実現"
image: "https://positive-intentions.com/assets/images/dim-db2fd60925f4927c43bc58a821988ab3.png"
---

# React-Like JSX Syntax for Webcomponents - Webコンポーネント向けのReact風JSX構文
Web ComponentsをReactのフック感覚で扱う——Litを使った「関数型Webコンポーネント」入門

## 要約
Litの軽量な基盤にReact風のフック（useState、useEffectなど）を組み合わせ、クラスベースの煩雑さを避けつつ再利用可能で宣言的なWeb Componentsを実現する手法を紹介する。

## この記事を読むべき理由
Reactに馴染んだ開発者がその感覚のままブラウザ標準のWeb Componentsを使えるようになれば、軽量で互換性の高いUI部品を社内ライブラリやマイクロフロントで活用できる。国内の既存資産やSaaS製品でも採用しやすいアプローチだ。

## 詳細解説
- アイデア全体  
  LitElementをベースに「define」ユーティリティで関数型コンポーネントをラップし、props（属性）とchildrenを渡してレンダリングする。これによりクラス継承のボイラープレートを隠蔽し、関数的にUIを記述できる。

- define関数（要点）  
  - elementのattributesをオブジェクト化して関数コンポーネントに渡す。  
  - window.customElements.defineで登録するだけで使えるカスタム要素が作れる。

```javascript
import { LitElement } from "lit";

export function define({ tag, component: CustomFunctionalComponent }) {
  class CustomComponent extends LitElement {
    render() {
      const attributes = Array.from(this.attributes).reduce((acc, attr) => {
        acc[attr.name] = attr.value;
        return acc;
      }, {});
      return CustomFunctionalComponent({
        ...attributes,
        children: this.innerHTML,
        component: this,
      });
    }
  }
  window.customElements.define(tag, CustomComponent);
}
```

- useState（要点）  
  - stateはコンポーネントインスタンス上に一意のプロパティ名で保持。  
  - セッターは値関数を受け取り、更新後にcomponent.requestUpdate()で再描画を要求する。

```javascript
export function useState(initialState, component, id) {
  const propName = `state-${id}`;
  component[propName] = component[propName] ?? initialState;
  const setState = (newState) => {
    const current = component[propName];
    const value = typeof newState === "function" ? newState(current) : newState;
    component[propName] = value;
    component.requestUpdate();
  };
  return [() => component[propName], setState];
}
```

- useEffect（要点）  
  - 依存配列を比較して副作用を実行。クリーンアップ関数を保存し、component.addControllerで切断時に解放する。

```javascript
export function useEffect(effectCallback, dependencies, component, id) {
  const key = `effect-${id}`;
  const hasChanged = component[key]
    ? !dependencies.every((d, i) => d === component[key].dependencies[i])
    : true;
  if (hasChanged) {
    component[key] = { dependencies, cleanup: undefined };
    const cleanup = effectCallback();
    if (typeof cleanup === "function") component[key].cleanup = cleanup;
  }
  component.addController({
    hostDisconnected() {
      if (component[key]?.cleanup) component[key].cleanup();
    },
  });
}
```

- 利点とトレードオフ  
  - 長所: 小さく、ブラウザネイティブの利点（シャドウDOM、互換性）を活かせる。React依存が減る。  
  - 短所: フックのライフサイクル管理や複雑な状態管理は手動で注意が必要。既存のエコシステム（JSX/ビルド設定）との統合を考える必要あり。

## 実践ポイント
- まずは小さなカウンターコンポーネントでdefine/useState/useEffectを試す。  
- ViteやRollupでLitをビルドに組み込み、StorybookでUIカタログを作ると採用が進みやすい。  
- 既存Reactチームの場合、段階的に共通UIをWeb Components化して移行コストを下げる。  
- アクセシビリティ（a11y）とSSRの要件を早めに検討する（Web ComponentsはSSRが別途必要なケースあり）。  

以上を踏まえ、React風の開発感覚を保ちながらブラウザ標準の堅牢なUI部品を作る一手として試してみてほしい。
