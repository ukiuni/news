#!/usr/bin/env python3
import csv
import re
import os

# CSVファイルを読み込む
csv_path = 'scripts/post_titles.csv'
posts_dir = '_posts'

# CSVデータを読み込む
post_data = {}
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        filepath = row['ファイルパス']
        title = row['タイトル']
        japanese_title = row['タイトルの日本語訳']
        # 新しいタイトル: "英語タイトル - 日本語タイトル"
        new_title = f"{title} - {japanese_title}"
        post_data[filepath] = new_title

# 各投稿ファイルを更新
for filepath, new_title in post_data.items():
    full_path = os.path.join(posts_dir, os.path.basename(filepath))
    
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue
    
    # ファイルを読み込む
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Front matterのtitleを更新
    # title: で始まる行を見つけて置換
    content = re.sub(
        r'^title: .*$',
        f'title: {new_title}',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    # 最初の # 見出しを更新
    # Front matter (---...---) の後に出てくる最初の # で始まる行を置換
    def replace_first_heading(match):
        front_matter = match.group(1)
        after_front_matter = match.group(2)
        # after_front_matter内の最初の # で始まる行を置換
        after_updated = re.sub(
            r'^# .*$',
            f'# {new_title}',
            after_front_matter,
            count=1,
            flags=re.MULTILINE
        )
        return front_matter + after_updated
    
    content = re.sub(
        r'(---.*?---\n)(.*)',
        replace_first_heading,
        content,
        count=1,
        flags=re.DOTALL
    )
    
    # ファイルに書き込む
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {full_path}")

print("\nAll posts updated successfully!")
