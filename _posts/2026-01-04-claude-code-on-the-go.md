---
  layout: post
  title: "Claude Code On-the-Go - Claude Code モバイルで動かす"
  date: 2026-01-04T20:56:50.991Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://granda.org/en/2026/01/02/claude-code-on-the-go/"
  source_title: "Claude Code On-The-Go - granda"
  source_id: 46491486
  excerpt: "スマホ＋クラウドでtmux/Claudeを動かし、通知で非同期開発を回す実践ガイド"
---

# Claude Code On-the-Go - Claude Code モバイルで動かす
通勤・隙間時間で「開発を回す」──スマホ + クラウドで実現する非同期コーディングの新常識

## 要約
スマホ（iOS/Termius＋mosh）からTailscale経由でVultrの使い捨てVMを起動し、tmux上で複数のClaude Codeエージェントを並列実行。ユーザー入力はWebhook経由のプッシュ通知で受け取り、どこでも非同期開発が可能になる手法を紹介する。

## この記事を読むべき理由
日本の通勤・育児・カフェ文化では、まとまった「デスク時間」が取りにくい。この記事は「短い隙間時間を有効活用して実装やレビューを進める」ための具体的なインフラと運用手順を示し、コスト・セキュリティに配慮した実践案を提示する。

## 詳細解説
- インフラの骨子  
  - 軽量なオンデマンドVM（例: Vultr Silicon Valley, vhf-8c-32gb, $0.29/hr）を必要時だけ起動し課金を抑制。全てのSSHはTailscaleのプライベートネットワーク経由にしてパブリックSSHを閉じる。ファイアウォール、nftables、fail2banで防御を重ねる。
- モバイル接続の肝：mosh + Termius  
  - moshはネットワーク切替やスリープを越えてセッションを維持するため、移動中の作業に最適。TermiusはiOS/Androidでmosh/ssh接続を扱えるクライアント。
  - ただし mosh は SSH エージェント転送をしないため、GitHub操作など認証が必要な作業は通常のSSH（tmux内）で行う運用が必要。
- セッション永続化：tmux の自動アタッチ  
  - ログイン時に自動で tmux セッションにアタッチすることで、端末を閉じても作業状態を維持。例（.zshrc）:

```bash
# bash
if [[ -z "$TMUX" ]] ; then
  tmux attach -t main 2>/dev/null || tmux new -s main
fi
```

- プッシュ通知で「非同期開発」を成立させる仕組み  
  - Claude Code のフック（PreToolUse -> AskUserQuestion）で質問が発生したら、Webhook（例: Poke）にPOSTしてスマホを鳴らす。ユーザーは通知から即レスポンスを送り、生成ループを継続できる。
  - フック設定（抜粋）:

```json
// json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "AskUserQuestion",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/poke-notify.sh question"
          }
        ]
      }
    ]
  }
}
```

- 複数エージェント＋複数作業ツリー  
  - Git worktree を使い、各ブランチごとに tmux ウィンドウと Claude エージェントを割り当てる。ポート割当はブランチ名ハッシュで決めて衝突を回避する。ハッシュ計算は概念的に $hash\_val = \sum \mathrm{ord}(c)$ で、ポートは例えば次の式で決定する:
$$\text{django\_port} = 8001 + (hash\_val \bmod 99)$$

- リスクと信頼モデル  
  - VMは「焼却可能」な環境に限定。プロダクションアクセスや過剰なシークレットを渡さないことで被害を限定する。かつ従量課金なので暴走時のコストは限定的。

## 実践ポイント
1. 最低限のVMテンプレートを用意する  
   - Tailscaleインストール、tmux/zsh、fail2ban、nftablesの初期化を含むイメージを作る。起動スクリプトで早期にTailscaleがUPするようにする。
2. スマホからの起動フローを用意する  
   - Vultr API を叩く iOS Shortcut を作り、外出先からVMを起動 → Termiusでmosh接続。vm-start / vm-stop スクリプトで起動停止を自動化。
3. 通知フックを実装する（例: poke-notify.sh）  
   - Claude のイベントから質問を抽出してWebhookへPOST。受け取った通知から即レスで開発ループを回す。
```bash
# bash (例)
QUESTION=$(echo "$EVENT_DATA" | jq -r '.tool_input.questions[0].question')
curl -X POST "$API_URL" -d "{\"message\":\"$PROJECT_NAME : Claude needs input - $QUESTION\"}"
```
4. mosh と SSH の使い分けを明確にする  
   - 端末操作やREPLはmosh/tmuxで。Git push/pullや認証が必要な操作はSSH（エージェント転送）で行う。
5. セキュリティ運用ポリシーを決める  
   - VMに渡す鍵やトークンを最小化。ログ監視と停止ルール（例: 一定時間非アクティブで自動停止）を導入してコストとリスクを管理する。

このパターンは「まとまった机時間が取れない」日本の現場に非常にマッチします。通勤・育児・隙間時間でのレビューや軽い実装、リファクタの着手を現実にするワークフローとして試す価値が高いでしょう。
