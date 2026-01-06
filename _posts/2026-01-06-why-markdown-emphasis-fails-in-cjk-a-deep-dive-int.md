---
  layout: post
  title: "Why Markdown emphasis fails in CJK: A deep dive into CommonMark's delimiter rules - CJK環境でMarkdown強調が崩れる理由：CommonMark区切りルールの深掘り"
  date: 2026-01-06T05:03:59.738Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://hackers.pub/@yurume/019b912a-cc3b-7e45-9227-d08f0d1eafe8"
  source_title: "유루메 Yurume: As Markdown has become the standard for LLM outputs, we are now forced to witness a common and unsightly mess where Markdown emphasis markers (**) remain unrendered and exposed, as seen in the image. This is a chronic issue with the CommonMark specification---one that I once reported about ten years ago---but it has been left neglected without any solution to this day.  The technical details of the problem are as follows: In an effort to limit parsing complexity during the standardization process, CommonMark introduced the concept of &quot;delimiter runs.&quot; These runs are assigned properties of being &quot;left-flanking&quot; or &quot;right-flanking&quot; (or both, or neither) depending on their position. According to these rules, a bolded segment must start with a left-flanking delimiter run and end with a right-flanking one. The crucial point is that whether a run is left- or right-flanking is determined solely by the immediate surrounding characters, without any consideration of the broader context. For instance, a left-flanking delimiter must be in the form of **&lt;ordinary character>, &lt;whitespace>**&lt;punctuation>, or &lt;punctuation>**&lt;punctuation>. (Here, &quot;ordinary character&quot; refers to any character that is not whitespace or punctuation.) The first case is presumably intended to allow markers embedded within a word, like **마크다운**은, while the latter cases are meant to provide limited support for markers placed before punctuation, such as in 이 **&quot;마크다운&quot;** 형식은. The rules for right-flanking are identical, just in the opposite direction.  However, when you try to parse a string like **마크다운(Markdown)**은 using these rules, it fails because the closing ** is preceded by punctuation (a parenthesis) and it must be followed by whitespace or another punctuation mark to be considered right-flanking. Since it is followed by an ordinary letter (은), it is not recognized as right-flanking and thus fails to close the emphasis.  As explained in the CommonMark spec, the original intent of this rule was to support nested emphasis, like **this **way** of nesting**. Since users typically don't insert spaces inside emphasis markers (e.g., **word **), the spec attempts to resolve ambiguity by declaring that markers adjacent to whitespace can only function in a specific direction. However, in CJK (Chinese, Japanese, Korean) environments, either spaces are completly absent or (as in Korean) punctuations are commonly used within a word. Consequently, there are clear limits to inferring whether a delimiter is left or right-flanking based on these rules. Even if we were to allow &lt;ordinary character>**&lt;punctuation> to be interpreted as left-flanking to accommodate cases like **마크다운(Markdown)**은, how would we handle something like このような**[状況](...)は**?  In my view, the utility of nested emphasis is marginal at best, while the frustration it causes in CJK environments is significant. Furthermore, because LLMs generate Markdown based on how people would actually use it---rather than strictly following the design intent of CommonMark---this latent inconvenience that users have long felt is now being brought directly to the surface."
  source_id: 1462598581
  excerpt: "CJK環境で**が露出するCommonMarkの誤判定原因と即効回避策を解説"
  ---

# Why Markdown emphasis fails in CJK: A deep dive into CommonMark's delimiter rules - CJK環境でMarkdown強調が崩れる理由：CommonMark区切りルールの深掘り
LLMの標準出力で露呈した「**がそのまま表示される」問題──CJK（中日韓）環境でMarkdown強調が壊れる原因と、現場で取れる対処法

## 要約
CommonMarkの「delimiter run（連続区切り）」ルールは、区切り文字が左寄り／右寄りかを周囲数文字だけで決めるため、スペースが省略されるCJK環境や語中に句読点が入る韓国語で誤判定が起き、`**太字**`が閉じられず生の`**`が露出する。

## この記事を読むべき理由
LLMやドキュメント生成ツールがMarkdown出力を標準化する今、この問題は単なる表示崩れではなくUXと可読性に直結する。日本のエンジニアやコンテンツ制作者は、原因を理解して短期／中期の現場対策と長期的なパーサ改善案を知っておくべきだ。

## 詳細解説
- 背景：CommonMarkはパースの複雑さを抑えるため「delimiter run」を導入。区切り（`*`や`_`）が「左フランク（left-flanking）」「右フランク（right-flanking）」かを、その直前・直後の文字カテゴリ（空白／句読点／普通文字）だけで判断する。
- 仕様の狙い：空白を内側に入れたネスト（例：`**this **way** of nesting**`）のあいまいさを回避するため、空白隣接の区切りは一方向にしか動作しないと明示した。
- CJKでの問題点：
  - 日本語・中国語では語間に空白がないため「普通文字か空白か」の判定が有効に機能しない。
  - 韓国語などでは括弧や引用符が語中に使われる例が多く、閉じの`**`の前に句読点（`(` など）があると「右フランク」と判定されず閉じられない。
  - 具体例：`**マークダウン(Markdown)**は` は、閉じの`**`が直前に句読点を持つため右フランク判定を満たさず強調が閉じられない。逆に `このような**[状況](...)は**` のような混合ケースはどちらに寄せるか曖昧。
- 設計上のトレードオフ：ネスト強調を完全にサポートする設計意図と、CJKでの実用性が相反している。LLMが人間らしい書き方でMarkdownを生成することで、この潜在的不便が顕在化している。

## 実践ポイント
- 即効の回避策（出力側）：
  - 強調にHTMLタグを使う：`<strong>マークダウン(Markdown)</strong>は` — パーサに依存しない安定表示。
  - 区切りの前後にゼロ幅スペース（U+200B）を入れる：`**マークダウン(U+200B(Markdown)）**`（表示上は目立たないがパーサ挙動を変える）。ただし検索やコピーで差異が出る。
  - 明示的にスペースを入れる：`**マークダウン (Markdown)** は`（意図しない空白が増える点で可読性に影響）。
  - エスケープ：句読点や`*`をバックスラッシュで逃がす。ただし多用は面倒。
- ツール／パーサ側の対処（推奨順）：
  - MarkdownライブラリにCJK-awareな文字カテゴリ判定を入れる（Unicodeの分類／East Asian Widthを参照）。これなら「CJKの文字は普通文字扱い」で誤判定を減らせる。
  - オプションで「nested-emphasisを抑制する」モードを用意する：ネストの利得が小さいなら、CJK向けにより寛容なフランキング判定に切り替え可能にする。
  - CommonMark拡張として議論：コミュニティでの仕様追加を通じて一貫した解決を目指す（互換性問題と議論のコストあり）。
- 実務での勧め：
  - LLMにMarkdownを出力させる場合はテンプレートでHTML強調を使わせる、あるいは出力後にポストプロセスで上記のゼロ幅空白挿入やHTML化を行う。
  - ドキュメント生成パイプラインで使用するMarkdownライブラリの挙動をテストケース（CJK特有の例）でカバーし、レンダリング確認を自動化する。

まとめ：CommonMarkの設計選択がCJK環境で不都合を生み、LLMの普及で顕在化している。即効策としてはHTML強調やゼロ幅空白の利用、根本解決はパーサのCJK対応（仕様／実装の改善）にある。日本の現場ではまず生成側・パース側のどちらで解決するか決めて、小さな回避策を運用に組み込むのが現実的。
