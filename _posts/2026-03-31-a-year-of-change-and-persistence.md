---
layout: post
title: "A Year of Change and Persistence - 変化と粘り強さの一年"
date: 2026-03-31T21:27:04.645Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/jess/a-year-of-change-and-persistence-19cf"
source_title: "A Year of Change and Persistence - DEV Community"
source_id: 3437639
excerpt: "DEV買収を背景に、技術者向けの包摂的UI設計と次世代支援の具体策を示す必読記事"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fp6zl5vrltudjljxwf5mf.png"
---

# A Year of Change and Persistence - 変化と粘り強さの一年
変わる業界、変わらない「作る責任」 — DEV買収と包摂的UXへの招待

## 要約
DEVの共同創業者が語る買収を経た変化と、差別撤回の風潮の中で求められる「インターフェース設計」と「可視性」の重要性。個人の性自認表記やハッカソンでの次世代支援まで、技術者にとって実践的な示唆が詰まっています。

## この記事を読むべき理由
日本でもスタートアップの買収や多様性（DEI）への逆風は他人事ではありません。UI/システム設計が社会的な影響を持つ今、エンジニアやプロダクト担当が知っておくべき実践と心構えが分かります。

## 詳細解説
- 買収とリーダーシップの変化：DEVがMajor League Hacking（MLH）に買収され、創業メンバーは「権限で引っ張る」から「影響力で導く」へ役割が変化。小規模で作ってきたチーム運営が、大きな組織の中でどう継続されるかが課題です。
- DEI後退の文脈：米国では一部でDEI施策の後退が進んでおり、システム上の些細なUI（例：「Man/Woman」のラジオボタン）が無自覚な排除につながる点を指摘しています。
- インターフェース設計の責任：開発者は単に画面を作るだけでなく、人々を選別してしまう仕組みを避ける設計が求められる。具体的には「任意の代替入力（free-text）」「プリファード・プロノウンの追加」「性別入力を必須にしない」「プライバシー配慮」の実装など。
- 次世代支援の重要性：MLHのハッカソンで見た学生たちは、技術を学ぶだけでなく“この業界で生き残る術”を必要としている。統計として「女性の半数が35歳までに退職する」など、組織的支援の必要性が強調されています。

簡単な実装例（フォーム・DB設計の考え方）:
```html
<!-- HTML -->
<form>
  <label>表示名<input name="displayName" /></label>
  <label>代名詞（任意）<input name="pronouns" placeholder="she/her, they/them, prefer not to say, etc." /></label>
  <!-- 性別はオプションにする -->
  <label>性別（任意）<select name="gender">
    <option value="">選択しない</option>
    <option value="female">女性</option>
    <option value="male">男性</option>
    <option value="nonbinary">非二元</option>
  </select></label>
</form>
```
```sql
-- SQL（例: ユーザーテーブル）
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  display_name TEXT NOT NULL,
  pronouns TEXT,        -- 自由入力を許可
  gender VARCHAR(32),   -- NULL許容、固定選択にしない
  created_at TIMESTAMP DEFAULT now()
);
```

## 実践ポイント
- 自分のサービスなら：代名詞欄を任意で追加し、自由入力か広めの選択肢を用意する。性別は必須にしない。
- 個人でできること：プロフィールに代名詞を追加して「見える化」する（安全配慮は必須）。
- 組織でできること：採用・レイオフ指標を性別/属性でモニタリングし、不均衡が出たら説明責任を持つ。若手支援ハッカソンやメンタリングに関与する。
- 心構え：設計は社会に影響を与える。小さなUIの選択がある人の居場所を壊す可能性があると認識して設計すること。
