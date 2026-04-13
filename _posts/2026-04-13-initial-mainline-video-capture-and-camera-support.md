---
layout: post
title: "Initial mainline video capture and camera support for Rockchip RK3588 - Rockchip RK3588向けメインライン動画キャプチャ＆カメラサポートの初期追加"
date: 2026-04-13T15:39:15.795Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.collabora.com/news-and-blog/news-and-events/mainline-video-capture-and-camera-support-for-rockchip-rk3588.html"
source_title: "Mainline video capture and camera support for Rockchip RK3588"
source_id: 47751621
excerpt: "RK3588の動画キャプチャがメインライン化に前進、ISP対応とlibcamera連携の今後が要注目"
image: "https://www.collabora.com/assets/images/blog/Collabora-MainlineVideoCapture-3588.jpg"
---

# Initial mainline video capture and camera support for Rockchip RK3588 - Rockchip RK3588向けメインライン動画キャプチャ＆カメラサポートの初期追加
驚くほど速く進む！RK3588のカメラ/ISPがついにメインラインLinuxで動き始めた理由と、あなたの開発に与えるインパクト

## 要約
Collaboraらの数年にわたる作業で、Rockchip RK3588の動画キャプチャ周り（VICAP／MIPI CSI-2）に関する主要ドライバがメインライン化に向け前進。ISP本体の完全対応（rkisp2）とlibcamera連携が今後の焦点です。

## この記事を読むべき理由
RK3588は高性能SoCで国内の組込み機器や産業用カメラ採用が進む可能性が高く、メインラインLinux対応は保守性・セキュリティ・規制対応（例：ベンダーカーネル依存回避）で重要だからです。

## 詳細解説
- 背景：RK35世代はVICAP（ビデオキャプチャ）やISPといった専用ハードを積み、マルチカメラや高解像度処理が可能。ただしこれらはハード文書不足や複雑さゆえにメインライン化が遅れがち。
- 取り組み：Collaboraは2022年以降でrkcif系ドライバの大規模リファクタを支援。PX30/VIPやRK3568の基本キャプチャドライバは既に受け入れられ（2025年秋頃の節目）、RK3588向け拡張パッチもレビュー中。
- MIPI CSI-2受信側ドライバもメインラインに入った（2026年初頭）。これによりカメラ入力の基礎が整備。
- 未解決事項：ISP本体のメインラインドライバが不足。Rockchipはメモリ経由の簡易ドライバを提供しているが、最終目標はRK35世代をカバーする新しいrkisp2ドライバの開発（Collabora＋Rockchip＋Ideas on Boardの共同作業）。
- アーキテクチャ的注意点：VICAP→ISPの「MUX-TOISP」直結はメモリ経由より低遅延で帯域効率が良いが、ソフトウェア側（V4L2 media-controller）での連携設計が必要。設計を後回しにすると後で対応が難しくなる。
- 実績とデモ：FOSDEM 2026などでSony IMXセンサの静止画取得などのブリッジング実験が公開（ソフトデバイヤで低フレームレート等の制約あり）。今後Embedded Recipes等でISPデモ予定。

## 実践ポイント
- すぐ試せる：libcameraのソフトISPでまず動作確認してみる（デバイス検出やraw取り込みの練習に有効）。
- 開発者向け：linux-rockchipメーリングリスト／kernelパッチトラッカーを監視し、rkcif／MIPIパッチを追う。評価板でメモリ経由ストリームを実験して、遅延・帯域の測定を行うと設計上の判断材料になる。
- 製品設計：将来のメインライン対応を見越し、ベンダーカーネル依存を避ける設計（アップストリームドライバでの開発）を検討することで保守コストと規制リスクを下げられる。
- コントリビュート：ISP（rkisp2）やIPA/libcamera側の整備はまだ需要大。企業・開発者はテストデータ提供やパッチレビューで貢献可能。

興味があれば、CollaboraやIdeas on Boardの公開リポジトリ／発表スライドをチェックすると最新パッチやデモの詳細が得られます。
