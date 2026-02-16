---
layout: post
title: "I Sold Out for $20 a Month and All I Got Was This Perfectly Generated Terraform - 月20ドルで“降参”したら手に入ったのは完璧に生成されたTerraformだった"
date: 2026-02-16T16:27:40.408Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://matduggan.com/i-sold-out-for-200-a-month-and-all-i-got-was-this-perfectly-generated-terraform/"
source_title: "matduggan.com"
source_id: 891825315
excerpt: "月20ドルでAIに任せたら完璧なTerraformが手に入り、倫理と品質の葛藤が浮上する実話"
image: "https://matduggan.com/content/images/2024/01/favicon.ico"
---

# I Sold Out for $20 a Month and All I Got Was This Perfectly Generated Terraform - 月20ドルで“降参”したら手に入ったのは完璧に生成されたTerraformだった
月20ドルのAIサブスクで「面倒なInfra作業」を丸投げしたら、仕事も倫理観も揺らいだ話

## 要約
著者はClaude CodeというLLMを試した結果、TerraformやGitHub Actionsなどの煩雑な作業を驚くほど正確に自動生成できることを発見したが、同時に著作権やコード品質、職業倫理といった問題に直面する。

## この記事を読むべき理由
- 初心者でも分かる形で、LLMがインフラ作業（Terraform・k8s YAML・CIなど）をどう変えるか学べる  
- 実務で使う際の落とし穴（品質・セキュリティ・ライセンス）を押さえられるため、日本の現場でも即役立つ

## 詳細解説
- 何が起きたか：著者は月額20ドルのサブスクでClaude Codeを利用。手作業で時間を食っていたDNSレコードのimportやプロバイダ設定、GitHub Action作成などをAIに任せたところ、出力がほぼ期待通りになり「レビューしてマージするだけ」で済んだ。  
- 効率の勝利：繰り返し作業や設定ミスを減らし、エンジニアは実装ではなくレビューや設計へ集中できる。短期的な生産性は明確に向上する。  
- 倫理と法的問題：一方で、LLMの学習データにはウェブ上の著作物やコードが大量に含まれている可能性があり、著作権や貢献者への対価未支払といった論点が残る。  
- 品質の議論：「短期的には動けば良い」と割り切る開発者もいれば、将来の保守性や美しい設計を重視する開発者もいる。LLMは両者にとって利点だが、どちらの価値観を優先するかで利用の是非が分かれる。  
- 仕事市場への影響：LLMを使いこなす人は同じ時間でより多くのアウトプットを出せるため、競争優位になる可能性が高い。

## 実践ポイント
- まずは試す：小さなタスク（Terraformのリソース生成、簡単なGitHub Action、k8sマニフェスト）からAIに任せてみる。  
- レビュー前提で運用：自動生成コードは「素案」として扱い、必ず人間がレビューしてからマージする。  
- セキュリティと設定チェック：シークレットやリージョン・プロバイダのバージョン固定、不要な権限付与がないか点検する。  
- ライセンス／著作権の確認：企業利用前に法務やポリシー部門と整合を取る。学習元の問題を放置しない。  
- 技術的負債対策：重要な箇所はテストやドキュメント、設計レビューを追加して将来の保守性を担保する。

短期的な生産性と長期的な職業倫理・品質のバランスを意識すれば、LLMは「道具」として有効に使える。日本の現場でもまずは小さく試し、ガードレールを設ける運用が現実的です。
