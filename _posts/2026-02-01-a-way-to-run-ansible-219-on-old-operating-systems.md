---
layout: post
title: "A way to run Ansible 2.19 on old operating systems like Ubuntu 18.04 with working Apt - 古いUbuntu（18.04等）でAnsible 2.19を動かしつつaptを使えるようにする方法"
date: 2026-02-01T10:42:37.597Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://raymii.org/s/blog/Ansible_2.19_on_old_ubuntu_18.04_with_working_apt.html"
source_title: "A way to run Ansible 2.19 on old operating systems like Ubuntu 18.04 with working Apt - Raymii.org"
source_id: 1264660862
excerpt: "Ubuntu 18.04でAnsible 2.19をpyenv導入＋rawでapt実行して動かす手順"
---

# A way to run Ansible 2.19 on old operating systems like Ubuntu 18.04 with working Apt - 古いUbuntu（18.04等）でAnsible 2.19を動かしつつaptを使えるようにする方法
古いサーバ（Ubuntu 18.04等）でAnsible 2.19を使いたいが、Pythonバージョンやpython3-apt周りでハマる際の実務的な回避策

## 要約
Ansible 2.17以降、ターゲット上の古いPython（例: Ubuntu 18.04のPython 3.6）は非対応になり、Ansible 2.19ではモジュール実行やapt系が失敗する。pyenvで新しいPython（例: 3.12）を入れてansible_python_interpreterを指定し、aptはrawで直接apt-getするワークアラウンドが有効。

## この記事を読むべき理由
日本でもUbuntu 18.04を延長サポートやオンプレで使い続けている現場は多く、Ansibleを最新にしたいが「aptだけ動かない」「謎のSyntaxError」に悩む場面が現実的にあるため、手早く実装できる実践解を知っておくと現場で助かります。

## 詳細解説
- 問題点: Ansible 2.17以降、ターゲットノードでの古いPythonサポートが切られている。結果、古いシステムでplaybook実行時にモジュールがJSONを返せず失敗（例: future feature annotations関連のSyntaxErrorのような表示）。
- 実務解: ターゲットに新しいPythonを入れてansible_python_interpreterで指定する。pyenvを使えばユーザー領域に比較的簡単に新しいPythonをビルド・配置できる。
- 陥りどころ: pyenv環境にはsystem連携のpython3-aptが入らないことが多く、Ansibleのapt系モジュール（apt、apt_key、apt_repositoryなど）がpython3-apt不足で失敗する。
- 回避策: aptインストールだけはidempotent（冪等）に自前で処理する。dpkg-queryでインストール状況を確認し、インストールされていなければrawでapt-get update && apt-get install -qyyを流す条件付きタスクにする。さらに、対象は古いディストリビューションのみ（例: Debian <11、Ubuntu <20）に限定する。

Execution Environments（コンテナ化されたEE）の運用は理想的だが、中小チームや現場運用者には導入負荷が高く、今回のような手早い回避が現実的。

## 実践ポイント
- 依存パッケージ（ビルドツール）を入れる:
```bash
# bash
apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
 libsqlite3-dev curl libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
```

- pyenvでPython 3.12をインストール:
```bash
# bash
git clone https://github.com/pyenv/pyenv.git /home/admin/pyenv
export PYENV_ROOT=/home/admin/pyenv
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.12.12
# 例: /home/admin/pyenv/versions/3.12.12/bin/python3
```

- inventoryでansible_python_interpreterを指定:
```yaml
# yaml
mygroup:
  hosts:
    myhost.domain.ext:
      ansible_host: 192.168.123.45
      ansible_user: admin
      ansible_python_interpreter: /home/admin/pyenv/versions/3.12.12/bin/python3
```

- aptインストールをワークアラウンドするAnsibleタスク例（古いDebian/Ubuntu向け）:
```yaml
# yaml
- name: Check if packages are installed
  ansible.builtin.raw: "dpkg-query -W -f='${Status}' {{ item }}"
  loop:
    - logwatch
    - rsyslog
  register: pkg_check
  ignore_errors: true
  when: >
    (ansible_facts['distribution'] == 'Debian' and (ansible_facts['distribution_major_version'] | int) < 11)
    or
    (ansible_facts['distribution'] == 'Ubuntu' and (ansible_facts['distribution_major_version'] | int) < 20)

- name: Install packages if not installed
  ansible.builtin.raw: "apt-get update && apt-get install -qyy {{ item.item }}"
  loop: "{{ pkg_check.results }}"
  when: >
    (
      (ansible_facts['distribution'] == 'Debian' and (ansible_facts['distribution_major_version'] | int) < 11)
      or
      (ansible_facts['distribution'] == 'Ubuntu' and (ansible_facts['distribution_major_version'] | int) < 20)
    )
    and (item.stdout is not defined or 'install ok installed' not in item.stdout)
```

- 補足:
  - この方法はapt系の代替回避であり、apt_keyやapt_repositoryなど他のモジュールは別途対応が必要。
  - 長期的にはExecution EnvironmentsやターゲットのOSアップグレード、あるいはsystem側に対応Pythonパッケージを入れる方が望ましい。

以上を実行すれば、古いUbuntu上でもAnsible 2.19で大半の作業を継続しつつ、aptインストールのみ安全に回避できます。
