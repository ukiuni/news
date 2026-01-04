---
  layout: post
  title: "No longer a rumour: Microsoft silently kills Windows and Office phone activation and forces online activation with a Microsoft account - マイクロソフトが電話でのWindows/Office認証をひっそり終了、Microsoftアカウントでのオンライン認証へ強制移行"
  date: 2026-01-04T23:56:15.256Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.tomshardware.com/software/windows/microsoft-silently-kills-windows-and-office-phone-activation-and-forces-online-activation-with-a-microsoft-account-windows-users-are-now-herded-into-an-online-only-portal-for-activation"
  source_title: "Microsoft silently kills Windows and Office phone activation and forces online activation with a Microsoft account &mdash; Windows users are now herded into an online-only portal for activation | Tom's Hardware"
  source_id: 472213064
  excerpt: "電話認証終了、Microsoftアカウント必須化で旧端末の復旧が困難に—対策必読"
  image: "https://cdn.mos.cms.futurecdn.net/3wshZh7uVXqjpEBBAxFKK5-1920-80.png"
---

# No longer a rumour: Microsoft silently kills Windows and Office phone activation and forces online activation with a Microsoft account - マイクロソフトが電話でのWindows/Office認証をひっそり終了、Microsoftアカウントでのオンライン認証へ強制移行
「電話で済んだ“最後の手段”が消える――古いPCやオフライン環境はどうする？」

## 要約
最近、電話によるWindows/Officeのアクティベーション（プロダクトキーを電話で有効化する手順）が実質的に使えなくなり、電話で誘導された先はオンラインの認証ポータルにリダイレクトされ、Microsoftアカウントでのサインインが必須になっています。

## この記事を読むべき理由
日本では製造機械、POS、検査機器など“インターネットに接続しにくい”レガシー環境が多く残っています。電話認証の終焉は、そうした現場の運用やセキュリティ/コンプライアンス方針に直接影響します。個人ユーザーも再インストールや中古PC購入時に想定外の手間を強いられる可能性があります。

## 詳細解説
- 何が起きたか：従来は認証できないときに「電話での自動応答＋確認ID」でオフラインでも有効化できた仕組みが、電話を掛けても「アクティベーションはオンラインで行ってください」という自動音声とSMSのリンク送信に置き換わるケースが報告されています。結局、リンク先は現行のMicrosoft Product Activation Portalで、Microsoftアカウントでのサインインを要求します。
- 影響範囲：Windows 7 / Office 2010 のような古い製品で、内部からのオンライン認証が失敗する（公式の認証サーバが機能していない）状況で電話認証が最後の砦でした。これが使えなくなると、完全にオフラインの環境やネットワーク分離された端末での復旧が難しくなります。
- 企業向けの違い：大規模環境ではKMSやMAK、ボリュームライセンスセンター（VLSC）経由の認証があるため即座に破綻するわけではありません。ただし、中小企業や組込み機器で個別版（OEM／Retail）を使っている場合、Microsoftアカウント必須は運用負荷とセキュリティ懸念を生みます。
- 技術的なトラブル例：ブラウザ互換性の問題でポータル操作がうまくいかない事例（あるブラウザで受付できず別のブラウザで成功）や、電話がSMSリンクを送る仕様に変わった点などが報告されています。

## 実践ポイント
- 個人ユーザー
  - 再インストール前にSettings → Activationで「デジタルライセンスがMicrosoftアカウントにリンクされているか」を必ず確認・リンクしておく。
  - 古いOSを使い続けるリスクを考え、可能ならサポート中のOSへ移行する。どうしても残す場合はイメージバックアップを作成しておく。
- 中小企業 / 現場機器運用者
  - インターネット非接続端末がある場合は、事前にボリュームライセンス（KMS/MAK）やオフライン対応の認証ルートが使えるかMicrosoftまたは正規パートナーに相談する。
  - Microsoftアカウントの必須化に伴う情報管理ポリシー（アカウント管理、2要素認証、業務アカウントの分離）を整備する。
- トラブル発生時
  - まずslmgr.vbsやSettingsのActivation画面で現在の状態を確認し、必要ならスクリーンショットやエラーコードを取得してMicrosoftサポート（日本マイクロソフト）へ連絡する。
  - 電話認証でSMSが来たがブラウザで動かない場合、別ブラウザやPCでポータルを試すと成功することがある。
- 最終手段の検討
  - 業務でオフライン必須の用途があるなら、ライセンス体系の見直し（ボリュームライセンス／オフライン対応製品への移行）や、長期保守可能なOS選定、あるいはLinuxなどの代替を検討する。

短く言えば、「電話で済ませていた“最後の保険”が事実上消えた」ため、再インストール前のライセンス確認と企業側の事前対策がますます重要になりました。まずは自分の環境でライセンスがMicrosoftアカウントに紐づいているかを確認することをおすすめします。
