---
layout: post
title: "How I disabled 13 AI features in Windows 11 safely, no third-party apps needed - Windows 11でAI機能を13個安全に無効化した方法（サードパーティ不要）"
date: 2026-02-06T10:37:23.490Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.windowslatest.com/2026/02/06/how-i-disabled-13-ai-features-in-windows-11-safely-no-third-party-apps-needed/"
source_title: "How I disabled 13 AI features in Windows 11 safely, no third-party apps needed"
source_id: 408010086
excerpt: "サード不要でWindows 11のCopilot含むAI機能13個を安全に一括無効化"
image: "https://www.windowslatest.com/wp-content/uploads/2026/02/Remove-Copilot-from-Windows-11-Copilot-PC.jpg"
---

# How I disabled 13 AI features in Windows 11 safely, no third-party apps needed - Windows 11でAI機能を13個安全に無効化した方法（サードパーティ不要）
Windows 11の「Copilot」まみれな体験をリセットする——面倒なAI統合を公式機能だけで取り除く実用ガイド

## 要約
Windows 11に埋め込まれたCopilot／AI統合を、サードパーティなしで13項目まとめて無効化・削除する手順を紹介します。レジストリ、設定、グループポリシー、アプリの置き換えなどで元の軽快な環境へ戻せます。

## この記事を読むべき理由
企業／個人問わず、余計なクラウドAIやUIの雑音を嫌う日本のユーザーは多いはず。業務用マシンや低帯域環境でも安定したデスクトップ体験を取り戻すための実践的手順がまとまっています。

## 詳細解説
以下は記事で扱われている主な13項目と、要点だけを抜き出した技術的手順です。

1. Copilotアプリ本体のアンインストール  
   - 設定 > アプリ > インストール済みアプリ で「Copilot」を探してアンインストール。タスクバーのアイコンや一部統合機能が消えます。

2. 検索のCopilotロゴ／提案の除去（レジストリ）  
   - レジストリ: HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Explorer  
   - DWORD (32-bit) DisableSearchBoxSuggestions を作成し値を 1 に設定。再起動で検索の提案やCopilotロゴを抑制。

3. ファイルエクスプローラーの「AI Actions」非表示  
   - 設定 > アプリ > Actions で関連トグル（Paint, Photos, Teams, Microsoft 365 Copilot など）をオフに。将来的な更新で「AI Actions」自体が完全非表示になる仕様改善が順次提供される。

4. Edgeブラウザ内のCopilot無効化  
   - Edge 設定 > 外観 > Copilot とサイドバー関連をオフ、言語設定で「ウェブ上での文章作成にCopilotを使用」をオフ、AI innovations/ Copilot Mode もオフに。

5. Notepad内のCopilot無効化  
   - Notepad を開き、設定の「AI Features」から Copilot トグルをオフに。

6. PhotosのAI機能を回避（Photos Legacyへの置き換え）  
   - Photos アプリ設定から「Photos Legacy」を入手・インストールし、モダン版Photosをアンインストール。既存メディアは消えず、従来型のギャラリー体験に戻せます。

7. PaintのAI機能無効化（レジストリ／グループポリシー）  
   - レジストリ: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Paint  
     - DWORD DisableImageCreator, DisableGenerativeFill, DisableCocreator を作成して値を1に。  
   - または gpedit.msc: Computer Configuration > Administrative Templates > Windows Components > Paint の各「Disable …」ポリシーを有効化して無効化。※Generative erase や Remove background の一部機能は未対応。

8. OutlookのAI機能無効化  
   - Outlook 内の設定でAI/Copilot関連トグルをオフにするか、組織ポリシーで無効化。クライアント側のオプションを確認。

9. OneDriveのAI連携停止  
   - OneDrive設定からスマート編集やAI統合オプションをオフに。同期やクラウド機能は維持したままAI機能のみ無効化可能。

10. Gaming Copilotの無効化  
    - ゲームバー／ゲーム設定内のCopilot関連トグルをオフ。ゲーム中のオーバーレイや提案を停止。

11. Windows Studio Effects（Copilot+ PC向け）の無効化  
    - カメラ／プライバシー設定やStudio Effectsのトグルで無効化。ハードウェア連動機能を切ることで不要な処理を減らせます。

12. Windows Recall（履歴系機能）の無効化と削除  
    - 設定からRecallをアンインストールが推奨。環境によっては PowerShell や DISM を使ってコンポーネントを削除する方法もある（管理者権限が必要）。

13. Click to Do（Copilot+ PC向け）の無効化  
    - Copilot+固有の「Click to Do」などのポップアップ機能は該当するシステム設定やデバイス固有のオプションでオフにします。

注意点：
- レジストリやグループポリシーの変更は管理者権限と再起動が必要。誤操作を避けるため、変更前に復元ポイントを作成することを推奨。
- 一部の機能は段階的に提供されるため、OSのビルドや地域によって設定項目の有無がある。

## 実践ポイント
- まず「Copilotアプリ」をアンインストールして影響範囲を確認する。  
- 検索のノイズが気になるならレジストリの DisableSearchBoxSuggestions を適用して再起動。  
- 画像編集などはレガシーアプリ（Photos Legacy、旧Paint）に戻すことでAI統合を回避できる。  
- 企業環境ではグループポリシーで一括無効化を検討。個人は設定→アプリ→各アプリ内のAIトグルを順にオフにすると短時間でかなりクリーンになる。

以上の手順で、Windows 11の過剰なAI統合を公式手段だけで段階的に取り除き、よりシンプルで安定した作業環境に戻せます。
