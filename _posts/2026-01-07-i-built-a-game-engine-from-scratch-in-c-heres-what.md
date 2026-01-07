---
  layout: post
  title: "I Built a Game Engine from Scratch in C++ (Here's What I Learned) - C++でゲームエンジンを一から作った（学んだこと）"
  date: 2026-01-07T20:46:14.333Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://dev.to/montmont20z/building-a-game-engine-from-scratch-using-c-my-breakout-clone-journey-20d1"
  source_title: "I Built a Game Engine from Scratch in C++ (Here&#39;s What I Learned) - DEV Community"
  source_id: 3154810
  excerpt: "C++/DirectX9で自作エンジンを作り、47回のGPUクラッシュで描画・物理の本質を会得"
  image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fcpj9e8ctdi2l9m9gghq8.png"
---

# I Built a Game Engine from Scratch in C++ (Here's What I Learned) - C++でゲームエンジンを一から作った（学んだこと）
破壊力抜群の「自作ゲームエンジン」入門 — 47回GPUをクラッシュさせて見えた本質

## 要約
C++17 + DirectX9 + Win32で3ヶ月かけてBreakoutクローンを自作した体験談。低レイヤーから作ることで、レンダリング、物理、アーキテクチャ設計の本質が身についた。

## この記事を読むべき理由
UnityやUnrealを使うだけでは見えない「内部の動き」を理解すると、パフォーマンス診断や最適化、独自機能の実装が圧倒的に楽になる。日本のインディー開発者、学生、またはゲームエンジンやグラフィック周りの基礎を学びたいエンジニアに特に有益。

## 詳細解説
なぜ低レイヤーから作るのか  
- 高レイヤーツールは便利だがブラックボックスが多い。内部で何が起きるかを理解することで、なぜ描画が遅くなるのか、物理が不安定になるのかを自力で突き止められる。

今回の技術スタック（要点）
- 言語: C++17  
- グラフィクスAPI: DirectX9（学習用に最適。構成要素が明確）  
- ウィンドウ: Win32 API  
- 音声: Windows multimedia extensions  
- IDE: Visual Studio

アーキテクチャ（分離と責務）
- Game（オーケストレータ）: マネージャ群（Renderer, Input, Physics, Sound）を所有し、状態遷移を管理
- MyWindow（プラットフォーム層）: Win32イベントをラップ。描画やOS依存コードを隔離
- Renderer: Direct3Dデバイス初期化、テクスチャ管理、DrawSprite()などのAPIを提供
- InputManager: DirectInputをラップしてゲーム側には IsKeyDown("LEFT") だけを提供
- PhysicsManager: AABB と Swept AABB（トンネリング防止）、検出と解決の分離
- Stateパターン: Menu, Level, GameOver を IGameState 経由で切り替え

ゲームループ（固定タイムステップ推奨）
```cpp
// cpp
while (window.ProcessMessages()) {
    float dt = CalculateDeltaTime(); // 固定あるいは固定サブステップ
    inputManager.Update();
    currentState->Update(dt, inputManager, physicsManager, soundManager);
    renderer.BeginFrame();
    currentState->Render(renderer);
    renderer.EndFrame();
}
```

DirectX9初期化の要点（つまずきポイント）
1. Direct3DCreate9() でインターフェースを取得  
2. GetAdapterDisplayMode() でディスプレイ能力を確認  
3. D3DPRESENT_PARAMETERS を設定（バックバッファ、深度バッファ、スワップ効果）  
4. CreateDevice() でデバイス作成 — ここでパラメータ不備によりクラッシュ多発。失敗時はソフトウェア頂点処理へフォールバックする実装が実用的。
```cpp
// cpp
HRESULT hr = d3d->CreateDevice(..., D3DCREATE_HARDWARE_VERTEXPROCESSING, ..., &device);
if (FAILED(hr)) {
    // 古いGPU向けにフォールバック
    hr = d3d->CreateDevice(..., D3DCREATE_SOFTWARE_VERTEXPROCESSING, ..., &device);
}
```
5. ID3DXSprite を使って2Dスプライトをバッチ描画

レンダリングで押さえるポイント
- BeginScene / EndScene / Present の流れ
- バックバッファへ描画してから Present で画面に反映（ダブルバッファリング）
- DrawSprite 呼び出しはコストが高いのでバッチングが鍵（Breakout級なら許容範囲）

物理と当たり判定のポイント
- 単純AABB重なりチェックは高速だが高速移動物体で「トンネリング（すり抜け）」が発生する  
- 解決策は Swept AABB（移動軌道を連続的に評価）— フレーム間で交差する可能性を検出できる  
- 衝突検出と衝突解決を分ける設計が保守性を高める

設計での最大の学び：設計しないで書くと後で辛い
- 初期はすべて1つのUpdateに書いてしまい状態遷移やメニュー追加で大改修が必要になった  
- Stateパターンで各スクリーンを独立させることで拡張性が劇的に向上

チャレンジと実用的な工夫
- GPUやDirectXの失敗で多くクラッシュした → ロギング・フォールバック・小さな差分で試す  
- デバッグはVisual StudioのデバッガとGPUドライバのメッセージ、DirectXの戻り値チェックが必須  
- パフォーマンス改善はまずアルゴリズムとバッチング、次にAPIコールの削減

## 実践ポイント
- 小さく始める: Breakoutは最小限の機能で学びが多い。まずは「画面に三角形を描く」までを目標に。  
- 設計優先: 主要コンポーネント（Renderer, Input, Physics, State）を先に設計する。紙にクラス図を書くと後で楽。  
- 固定タイムステップを採用して物理の再現性を確保する（例: 60Hz または複数サブステップ）  
- トンネリング対策に Swept AABB を実装する（高速移動でも安定）  
- レンダリングはバッチングを意識。まずは ID3DXSprite でまとめて描画してから、必要なら自前のバッチへ移行する  
- Windows + Visual Studio 環境で始めるのが手っ取り早い。日本の大学や企業でのWindows開発経験が活きる場面が多い  
- 学んだことは他のAPI（Vulkan, DX12）へも応用可能：低レイヤー理解が新API学習の近道になる

最後に一言：ツールに頼るのは悪くないが、「中身を知る」ことで次の一歩が見える。47回クラッシュしても、画面に三角が出た瞬間の感動は代えがたい学習体験になる。
