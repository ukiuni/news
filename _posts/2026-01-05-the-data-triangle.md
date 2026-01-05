---
  layout: post
  title: "The Data Triangle - データ三角形（The Data Triangle）"
  date: 2026-01-05T15:55:34.401Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.benlorantfy.com/blog/the-data-triangle-and-nestjs-zod-v5"
  source_title: "The Data Triangle - Announcing nestjs-zod v5"
  source_id: 470483428
  excerpt: "Zodで単一スキーマから実行時・静的型・OpenAPIを自動生成しAPIの不整合を防ぐ方法"
  image: "https://www.benlorantfy.com/_next/static/media/data-triangle.cd54512b.png"
---

# The Data Triangle - データ三角形（The Data Triangle）
APIの「型の三位一体」を守ってバグを潰す — nestjs-zod v5で目指す設計

## 要約
「Data Triangle（データ三角形）」は、APIの run-time（実行時検証）、compile-time（静的型）、docs-time（ドキュメント） の3点を単一のソースから生成し一貫性を保証する設計原則。nestjs-zod v5はこれを実践するツールセットを提供する。

## この記事を読むべき理由
- APIの仕様と実装のズレが原因のバグを減らしたいエンジニアに必読。  
- 日本の企業やプロダクトで増える内部API／外部公開APIの信頼性向上に直結する実践的手法が学べる。

## 詳細解説
Data Triangleの3点：
- Run-time：実行時バリデーション（リクエスト／レスポンスが期待通りか）
- Compile-time：静的型（TypeScriptなどでコンパイル時に矛盾を検出）
- Docs-time：APIドキュメント（OpenAPI等）

原則：これらを別々に定義すると必ず差分（ドリフト）が生まれる。差分があるとランタイムでエラーになったり、誤った仕様を公開してしまう。解決策は「1つのソースを信頼し、他は生成する」こと。

よくある違反パターン：
- 実装から生成しないAPIドキュメント（ドキュメントが手作業で陳腐化）
- コンパイルステップがない言語（TypeScript等の静的解析がないと保証できない）
- 型定義を複数箇所に書き分ける（OpenAPI、TypeScript、バリデータのデコレータ等）

class-validator の問題例（型がバラバラになるケース）：
```ts
export class Post {
  @ApiProperty({ type: Boolean })
  @IsString()
  rating: number;
}
```
- Run-time: string（@IsString）
- Compile-time: number（rating: number）
- Docs-time: boolean（@ApiProperty）

nestjs-zod のアプローチ（単一スキーマから生成）：
```ts
import { z } from 'zod'
import { createZodDto, ZodResponse } from 'nestjs-zod'

class PostDto extends createZodDto(z.object({
  title: z.string().describe('The title of the post'),
  content: z.string().describe('The content of the post'),
  authorId: z.number().describe('The ID of the author of the post'),
})) {}

@Controller('posts')
export class PostsController {
  @Get(':id')
  @ZodResponse({ type: PostDto })
  getById(@Param('id') id: string) {
    return { title: 'Hello', content: 'World', authorId: 1 }
  }
}
```
@ZodResponse の効果：
- 実行時：レスポンスを Zod で検証して不正データを防ぐ  
- コンパイル時：TypeScript 側で型の不一致を検出できるようにする  
- ドキュメント：nestjs/swagger 等と連携して OpenAPI スキーマを生成する

その他の発展：Data Triangle を拡張して「End-to-end type safety」を目指すと、クライアント側で API 呼び出し時にコンパイルエラーを出せる（openapi-ts 等で型付きクライアントを生成、あるいは tRPC のような仕組み）。

補足：nestjs-zod v5 は Zod v4 サポートなどの改良を含むリリース。マイグレーション注意点はリリースノート／MIGRATION.md を確認すること。

## 実践ポイント
- 最初の一歩：既存プロジェクトで class-validator を使っているなら、まず新しいエンドポイントやレスポンスで Zod を試す。  
- 単一ソース化：スキーマは Zod や同等のランタイムスキーマに一本化し、型（z.infer）とドキュメント（z.toJSONSchema → OpenAPI）を自動生成する。  
- CI に型検査を組み込む：ビルドが通ったら docs と実装が一致することを前提にする。  
- 型付きクライアントを生成：openapi-ts 等でクライアントを生成してフロント／バック間の安全性を高める。  
- v5 への移行：nestjs-zod@latest を導入する場合は MIGRATION.md を確認し、Zod v4 周りの破壊的変更に注意する。

この原則を取り入れれば、APIの信頼性と開発スピードが両立でき、後の不具合対応コストを大幅に下げられる。
