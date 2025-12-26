---
layout: post
title: "What are you doing this weekend?"
date: 2025-12-26T10:27:14.099Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lobste.rs/s/yswcyu"
source_title: "What are you doing this weekend?"
source_id: 720990974
excerpt: "Bandcampの曲メタをMPRIS経由で正確に流しscrobbleする拡張の作成と公開法"
---

# 週末で仕上げたい：Bandcampの曲情報をMPRISに流すFirefox拡張の作り方と公開まで

## 要約
Firefox拡張でBandcamp再生時の曲メタデータを正確にMPRISへ流し、mpris-scrobblerでlast.fmやListenBrainzへ送る手法と、拡張公開までの実務ポイントを整理する。

## この記事を読むべき理由
Linuxデスクトップで音楽を聴きながら再生情報を一元管理したい開発者・オーディオ好き向け。Bandcampはインディーズ中心でメタデータが欠けがちなので、正確に拾ってMPRIS経由でスコブルする価値が高い。

## 詳細解説
背景
- MPRIS：Linuxのデスクトップでメディアプレイヤーが公開するD-Bus API。mpris-scrobblerはそれを監視してscrobbleする。
- 問題点：ブラウザ（Bandcamp）のページ上で曲情報はあるが、MPRISに適切に出力されないことがある。これを補うのがブラウザ拡張。

実装アプローチ（代表的な2通り）
1. Media Session APIを使う（簡潔でブラウザ内完結）
   - content scriptでBandcampのDOM/ページJSからartist/title/album/coverを抽出。
   - navigator.mediaSession.metadata にセットすれば、ブラウザがOSや一部のミドルウェアへ伝播する場合がある。
   - ただしFirefoxや環境によってはMedia Sessionの情報がMPRISに橋渡しされない場合がある。

例（content script, JavaScript）:
```javascript
// javascript
(async () => {
  const metadata = {
    title: document.querySelector('.trackTitle')?.textContent?.trim() || 'Unknown',
    artist: document.querySelector('.artist')?.textContent?.trim() || 'Unknown',
    album: document.querySelector('.albumTitle')?.textContent?.trim() || '',
    artwork: [{ src: document.querySelector('.tralbumArt img')?.src || '' }]
  };
  if ('mediaSession' in navigator) {
    navigator.mediaSession.metadata = new MediaMetadata({
      title: metadata.title,
      artist: metadata.artist,
      album: metadata.album,
      artwork: metadata.artwork
    });
  }
})();
```

2. Native Messaging + 独自のMPRISプロバイダ（確実にMPRISへ流す）
   - 拡張はcontent scriptでメタデータを収集し、browser.runtime.sendNativeMessageでネイティブホストへ送る。
   - ネイティブホスト側でD-BusにMPRISインターフェースを公開する（Python/Nodeで可能）。
   - 注意：ネイティブホストのインストールはAMO経由ではできないため、Deb/RPMやインストーラで配布する必要がある。

ネイティブホスト用マニフェスト例:
```json
{
  "name": "com.example.bandcamp_mpris",
  "description": "Bandcamp → MPRIS bridge",
  "path": "/usr/bin/bandcamp-mpris-host",
  "type": "stdio",
  "allowed_extensions": ["your-extension-id@example.com"]
}
```

公開・配布
- Firefox拡張（WebExtension）はaddons.mozilla.org (AMO) へ提出可能。開発者アカウント作成、ポリシー順守、署名が必要。
- web-extツールでローカル検証とAMOへの署名/アップロードができる。
- ネイティブホストを使う場合は、拡張本体はAMOに置きつつ、ネイティブホストは別途OSパッケージで配布するのが現実的。

## 実践ポイント
- まずcontent scriptだけでMedia Sessionに流せるか試す（手間が少ない）。
- Bandcampは動的ロードが多いのでMutationObserverで要素変化を監視する。
- カバー画像は適切なサイズでキャッシュ・提供（mpris-scrobblerが要求する場合あり）。
- native messagingを用いる場合、インストーラ（deb/rpm/PKG）を用意してユーザーが簡単にネイティブホストを入れられるようにする。
- AMO提出前に権限は最小限にし、プライバシーポリシーや許可理由を明確に記載する。
- 日本市場向け：Bandcampは日本のインディーズアーティストも活用しているため、コミュニティ向けツールとして支持を得やすい。Linuxユーザーの多い技術コミュニティで配布すると良い。

## 引用元
- タイトル: What are you doing this weekend?
- URL: https://lobste.rs/s/yswcyu
