---
layout: post
title: "Custom-engineered artificial machine kept a 33-year-old man with an empty cavity in his chest alive without lungs for 48 hours | Infections had turned his lungs to soup and had to be cleared before transplant. - 感染で「肺が溶けた」33歳男性を48時間生かした特注人工装置の実例"
date: 2026-01-29T23:43:41.668Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/health/2026/01/custom-machine-kept-man-alive-without-lungs-for-48-hours/"
source_title: "Custom machine kept man alive without lungs for 48 hours - Ars Technica"
source_id: 414297578
excerpt: "感染で肺が溶けた33歳を、48時間の全人工肺装置で命をつなぎ移植に導いた実例"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/01/GettyImages-1358869815-1152x648.jpg"
---

# Custom-engineered artificial machine kept a 33-year-old man with an empty cavity in his chest alive without lungs for 48 hours | Infections had turned his lungs to soup and had to be cleared before transplant. - 感染で「肺が溶けた」33歳男性を48時間生かした特注人工装置の実例

肺がない状態を48時間支えた「人工肺システム」――命をつなぎ、移植への道を切り開いた技術の中身

## 要約
重篤な肺感染で「肺が壊死（溶ける）」した患者に対し、ノースウェスタン大チームが独自設計の全人工肺システム（TAL）で胸腔を空にしたまま48時間生命維持し、その後二重肺移植を成功させた事例報告。

## この記事を読むべき理由
- 日本でもパンデミックや耐性菌増加でARDS（急性呼吸窮迫症候群）や敗血症例が増える可能性があり、臨床と医療機器の新しい解法は実務的関心が高い。
- 医療デバイス設計・臨床工学・AI制御に携わる技術者にとって、「生体力学と回路制御を同時に満たす」実装例は学ぶ点が多い。

## 詳細解説
- 背景問題：肺はガス交換だけでなく、肺血管床が右心室の吐出を受け止める「循環のバッファ」役を担う。両肺を摘出すると右室に行き場がなくなり圧が急上昇、左心への前負荷が消え全循環が崩壊する。
- 従来手法の限界：ECMO（体外式膜型人工肺）は肺が体内に残る場合は長期運用可能だが、胸腔が空になると心臓位置の不安定化・出血・血栓・脳卒中リスクが急増する。
- TAL（flow-adaptive extracorporeal total artificial lung system）の主な構成と機能
  - デュアルルーメンカニューレ：内頸静脈から右心側の静脈血を直接排出し、右室の仕事を軽減。
  - フロー適応シャント：右肺動脈→右房へ低抵抗で再循環させる経路。外部ポンプが処理しきれない流量を逃がして右室圧上昇を防ぐ（1.1–6.3 L/minを自律調整）。
  - デュアル左心房還流：人工酸素化血を左房に戻し、左心へ十分な前負荷を保持。スターリングの法則（心室は適切に満たされるほど拍出が改善）を維持。
  - 胸郭シェル再建：牛心膜やエキスパンダーで心臓位置を安定化、出血と機械的損傷を防止。
- 臨床経過：TAL接続後24時間で乳酸値が高値から正常域へ回復、血圧昇圧薬は12時間で中止。48時間後にドナー肺が得られ移植成功。術後組織解析（空間トランスクリプトミクス）で「再生不能」の分子的指標（異常基底様細胞の増加・幹細胞消失・線維化）が確認され、早期移植の正当性が示唆された。
- 制約と課題：単一症例の報告であり、汎用化には熟練チーム・専施設・ドナー供給という資源が必要。病因や病期によって不可逆性の分子指標は変わる可能性がある。

## 実践ポイント
- 医療技術者向け
  - 流量分配と圧制御（右室保護と左室前負荷維持）が全体設計の鍵。フロー適応ループは重要な設計パターン。
  - 血栓リスク対策（還流経路の配置、抗凝固管理）を回路設計段階で組み込む。
- 臨床・病院運営向け
  - 重症ARDSでの「不可逆性判断」には分子的診断（空間トランスクリプトミクス等）が有用だが、実装には設備と専門性が要る。
  - 日本におけるドナー不足・専門センター集中の課題を踏まえ、地域連携と搬送計画の整備が必須。
- ビジネス・研究開発向け
  - TALのような複合システムはハード・ソフト・臨床ワークフローの統合が求められるため、医工連携と規制対応（医療機器承認）が早期検討ポイント。
  - 耐性菌や新興ウイルス対策として、迅速に「不可逆」を見極めるバイオマーカー研究に投資する価値あり。

短期的には単発の先進症例だが、技術的アイデア（流量適応シャント、左房還流など）は医療デバイス開発やICU運用改善に直接応用可能です。
