---
layout: post
title: "QtNat – Open you port with Qt - QtNat — Qtでポートを開く"
date: 2026-01-09T21:08:07.135Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://renaudguezennec.eu/index.php/2026/01/09/qtnat-open-you-port-with-qt/"
source_title: "QtNat &#8211; Open you port with Qt &#8211; Renaud Guezennec"
source_id: 46558739
excerpt: "Qt6 C++ライブラリでUPnPを自動化、アプリから簡単にポート開放"
---

# QtNat – Open you port with Qt - QtNat — Qtでポートを開く

QtでUPnPを使って手軽にポート開放するライブラリ「QtNat」を紹介 — 面倒なルーター設定をアプリ側で自動化します。

## 要約
Qt6ベースの軽量C++ライブラリで、UPnPを使ったNATのポートマッピング（ポート開放）を自動化します。SSDPでルーターを検出し、説明XMLを取得・解析してSOAPでAddPortMappingを投げる流れを簡単なAPIで扱えます。

## この記事を読むべき理由
家庭やオフィスのルーター越しに動くP2P・ゲーム・リモートアクセス・IoTアプリを作るとき、ユーザーにルーター設定を頼らずに外向き接続を確保できると導入障壁が劇的に下がります。日本では家庭用ルーターやプロバイダの設定が多様なので、自動化の有用性は高いです。

## 詳細解説
QtNatの主な流れは以下のとおりです。

1. SSDPによる発見（discovery）
   - M-SEARCH をマルチキャストアドレス 239.255.255.250:1900 に送信し、UPnP対応デバイス（ルーター）からの応答を待ちます。
   - Qtでは QUdpSocket を使って問い合わせと応答受付を行い、応答本文から説明URL（description URL）を抽出します。

2. 説明ファイル（description XML）の取得
   - 抽出した URL に対して QNetworkAccessManager で HTTP GET を行い、デバイス/サービス一覧を取得します。
   - 注目するデバイスタイプ例：
     - urn:schemas-upnp-org:device:InternetGatewayDevice
     - urn:schemas-upnp-org:device:WANDevice
     - urn:schemas-upnp-org:device:WANConnectionDevice
   - サービスタイプ例：
     - urn:schemas-upnp-org:service:WANIPConnection
     - urn:schemas-upnp-org:service:WANPPPConnection
   - 最終的に controlURL と serviceType を見つけて、ポートマッピング準備完了とします。

3. ポートマッピング要求（AddPortMapping）
   - SOAP エンベロープ（AddPortMapping）を生成し、controlURL に対して POST。ヘッダに Content-Type と SOAPAction を付与します。
   - 成功応答が返ればポートマッピング成立、エラーならエラーハンドリングへ。

簡易的な使用例（状態変化に応じて処理を進める）:

```cpp
// cpp
UpnpNat nat;
QObject::connect(&nat, &UpnpNat::statusChanged, [&nat, &app]() {
    switch(nat.status()) {
    case UpnpNat::NAT_FOUND:
        nat.requestDescription();
        break;
    case UpnpNat::NAT_READY:
        nat.addPortMapping("QtNatTest", nat.localIp(), 6664, 6664, "TCP");
        break;
    case UpnpNat::NAT_ADD:
        qDebug() << "Port mapping added";
        app.quit();
        break;
    case UpnpNat::NAT_ERROR:
        qDebug() << "Error:" << nat.error();
        app.exit(1);
        break;
    default:
        break;
    }
});
nat.discovery();
```

注意点
- UPnPが無効化されているルーターやISPによるブロックがあると動作しません。
- セキュリティ面で開放するポートや説明文、リーズ時間を慎重に設計してください。
- 一部の機器は複数のUPnPデバイス／バージョン情報を返すため、XML解析で正しいservice/controlURLを選ぶ実装が必要です。

## 実践ポイント
- まず自宅ルーターでUPnPが有効か確認する（管理画面）。
- テストは自分のネットワーク環境で実施し、外部からの接続を検証する（外部端末やオンラインポートチェックを利用）。
- 失敗時はフォールバック戦略を用意する：STUN/TURNやNAT-PMP/PCP、あるいはユーザー向け手動ポート設定案内。
- 公開するソフトでは、どのポートを開くか明示し最小権限で運用する（不要なポートは開放しない）。
- ライブラリを改良する場合は、XML解析の堅牢化とエラーの詳しいログ出力を優先すると保守性が上がります。

元記事では作者がソース公開やフィードバックを呼びかけています。Qtベースのデスクトップ／組込みアプリで外向き接続を楽にしたい方は、まず自分の環境で試してみてください。
