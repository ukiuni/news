---
layout: post
title: "PDF Generation in Quarkus: Practical, Performant, and Native - QuarkusでのPDF生成：実務的・高速・ネイティブ対応"
date: 2026-02-12T15:21:12.168Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.the-main-thread.com/p/howto-pdf-generation-in-quarkus"
source_title: "PDF Generation in Quarkus: Practical, Performant, and Native"
source_id: 443467554
excerpt: "QuarkusとOpenPDFで高速・ネイティブ対応の業務向けPDF生成を最短実装"
image: "https://substackcdn.com/image/fetch/$s_!xw4I!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbaba8c22-f7df-42d4-9d0e-35cabefb3788_1024x1024.png"
---

# PDF Generation in Quarkus: Practical, Performant, and Native - QuarkusでのPDF生成：実務的・高速・ネイティブ対応
Quarkus + OpenPDFで「本番で使える」PDF生成を最短で実装する方法 — 複数業務で必須なPDFをクラウドネイティブに、しかもネイティブ実行可能に。

## 要約
QuarkusとOpenPDFを組み合わせると、サーバーサイドで安全かつ高速にPDFを生成でき、ネイティブイメージ化（GraalVM）にも対応して運用コストと起動時間を抑えられます。

## この記事を読むべき理由
請求書や監査用書類、ラベルなどPDFは国内外の企業システムで不可欠です。日本の金融・保険・医療・物流システムでも「改ざん耐性」「オフラインでの配布」「ブランド保持」が求められ、Quarkus + OpenPDFはその要件を満たす実務的な選択肢です。

## 詳細解説
- なぜサーバー側でPDFを作るか  
  セキュリティ（テンプレートや署名の保護）、一貫したレイアウト、監査対応のため。フロント任せにするとフォーマットの破綻や改ざんリスクが増えます。

- 技術スタックの特徴  
  - OpenPDF：純JavaでPDF生成（LGPL）、フォント/画像/テーブル制御が可能。  
  - Quarkus：高速起動・低メモリ、開発時のホットリロード、ネイティブビルド対応。  
  - Panache（Hibernate ORM）：JPA操作を簡潔に。

- 実装の流れ（要点）
  1. プロジェクト作成（Quarkus拡張を追加）  
     quarkus-openpdf, quarkus-rest, jdbc-postgresql, hibernate-orm-panache を有効化する。
  2. エンティティ（Panache）でDBモデルを定義。例：
  ```java
  package org.acme.pdf;
  import io.quarkus.hibernate.orm.panache.PanacheEntity;
  import jakarta.persistence.Entity;

  @Entity
  public class PdfUser extends PanacheEntity {
      public String firstName;
      public String lastName;
      public String email;
  }
  ```
  3. OpenPDFでPDF生成サービスを作成（PdfWriter + Document）。バイト配列かストリームで出力。
  ```java
  @ApplicationScoped
  public class UserPdfService {
      public byte[] generateUserPdf(PdfUser user) {
          try (ByteArrayOutputStream baos = new ByteArrayOutputStream()) {
              Document doc = new Document();
              PdfWriter.getInstance(doc, baos);
              doc.open();
              doc.add(new Paragraph("User: " + user.firstName + " " + user.lastName));
              doc.close();
              return baos.toByteArray();
          } catch (Exception e) {
              throw new RuntimeException(e);
          }
      }
  }
  ```
  4. RESTエンドポイントでPDFを返却（Content-Type: application/pdf）。大きなPDFはJAX-RSのStreamingOutputでメモリ使用を抑える。
  ```java
  @GET @Path("{id}/pdf")
  @Produces("application/pdf")
  public Response getUserPdf(@PathParam("id") Long id) { ... }
  ```
  5. 画像・ロゴ・テーブルの追加、フォント埋め込みもOpenPDFで対応可能。  
  6. ネイティブビルド：quarkus-openpdfはネイティブ対応。`./mvnw clean install -Dnative` でバイナリ生成が可能。

- 運用面の注意  
  フォントの埋め込み、PDFバージョン、長期保存要件（可読性・検証性）を確認。大規模並列生成時はバックプレッシャーやキュー化を検討。

## 実践ポイント
- 小〜中規模PDFはバイト配列で問題なし。数MB以上はStreamingOutputでメモリ削減。  
- ロゴ・日本語フォントは埋め込み必須（環境依存を避ける）。TrueTypeを埋め込む。  
- テスト：PDFのバイト列からテキスト抽出して内容検証するユニットテストを用意。  
- キャッシュ：内容が固定の書類は生成結果をキャッシュして負荷を下げる。  
- CI/CD：ネイティブビルドはビルド時間とメモリ要件を考慮。コンテナ化してステージングで動作確認を行う。  
- 日本市場向け：請求書フォーマットや電帳法、業界の保存期間要件を満たすテンプレートを用意する（監査ログ、改ざん検知）。

以上を踏まえれば、Quarkus + OpenPDFは「現場で使える」PDF生成基盤を短期間で構築できます。必要なら、サンプルのQuarkusプロジェクト構成やCI設定例を用意しますか？
