---
  layout: post
  title: "83. Remove Duplicates from Sorted List - ソート済みリストの重複削除"
  date: 2026-01-04T07:45:11.523Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://leetcode.com/problems/remove-duplicates-from-sorted-list/submissions/1873925286/"
  source_title: "83. Remove Duplicates from Sorted List"
  source_id: 471499150
  excerpt: "ソート済みリストの重複をO(n)/O(1)で一掃する実践解説、コード例付き"
---

# 83. Remove Duplicates from Sorted List - ソート済みリストの重複削除
手早くO(n)/O(1)で解く！LeetCode 83 — ソート済み単方向リストの重複を一掃する賢いポインタテクニック

## 要約
ソート済みの単方向リンクリストから重複ノードをその場で削除し、各値が1回だけ残るようにする問題。走査は1回で済み、追加メモリは不要。

## この記事を読むべき理由
面接やアルゴリズム学習で頻出の基本問題であり、ポインタ操作やインプレースの思考が鍛えられる。日本の開発現場でもメモリ制約や低レイヤ実装（組み込み・C++）で役立つ知見です。

## 詳細解説
問題設定のポイント：
- 入力は「昇順にソートされた」単方向リンクリスト（ListNode）。
- 同じ値が連続する場合、重複ノードを削除して1つだけ残す。
- 出力は変更済みのリストの先頭。

アルゴリズム（イテレーティブ）：
1. current を head に置く。
2. current と current.next が存在する限りループ：
   - current.val == current.next.val のとき：
     - current.next = current.next.next として次のノードを飛ばす（これで重複を削除）。
     - current は動かさず、さらに重複が続く限り同じ処理を繰り返す。
   - 異なる場合は current = current.next で先に進む。
3. 最後に head を返す。

計算量：
- 時間計算量 O(n)（各ノードを最大1回処理）
- 空間計算量 O(1)（追加の構造を使わない）

実装例（Python）:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def deleteDuplicates(head: ListNode) -> ListNode:
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            # duplicate -> skip next node
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head
```

再帰実装も可能だが、深いリストではスタックが問題になるため実務や面接ではイテレーションが無難。

注意点：
- 空リスト（head is None）や単一ノードはそのまま返す。
- リストが大きく重複が連続するケースでは、while の中で同一値を連続してスキップする挙動を確認する。

## 実践ポイント
- ローカルでの単体テストを用意する（空リスト、1要素、全要素同値、重複が途中にあるケース）。
- 言語によっては参照操作のコストや所有権ルール（Rust/C++のmove/unique_ptr 等）に注意。
- ソート済みであることが前提：ソートされていないリストにはこの手法は使えない（先にソートが必要）。
- 面接では「なぜ O(1) でできるか」を説明できるようにしておくと好印象。

この記事の手法は小さなユーティリティ関数としてプロダクトコードにも応用可能。まずは手早くイテレーションで実装し、単体テストで境界条件を確かめよう。
