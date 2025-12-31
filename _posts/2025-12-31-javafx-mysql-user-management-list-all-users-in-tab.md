---
layout: post
title: "JavaFX + MySQL User Management: List All Users in Table (MVC & DAO) - JavaFX + MySQL ユーザー管理：テーブルに全ユーザーを表示（MVC と DAO）"
date: 2025-12-31T06:38:28.497Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=GbdzaSQTZ8g"
source_title: "JavaFX + MySQL User Management: List All Users in Table (MVC &amp; DAO)"
source_id: 475844559
excerpt: "JavaFXとMySQLでMVC/DAO構成のユーザー一覧表示を手順付きで学べる実践ガイド"
---

# JavaFX + MySQL User Management: List All Users in Table (MVC & DAO) - JavaFX + MySQL ユーザー管理：テーブルに全ユーザーを表示（MVC と DAO）
魅せるUIでDBの全ユーザーを安全に一覧表示する――JavaFXとMySQLをMVC/DAOで組み立てる実践ガイド

## 要約
JavaFXのTableViewにMySQLのユーザー情報をJDBC経由で読み出し、Model・DAO・Controllerで責務を分離して表示する手順を解説。堅牢で保守しやすいアプリ構造を短時間で実装できる。

## この記事を読むべき理由
JavaデスクトップアプリでDBデータを一覧表示する基本は、業務ツールや社内管理ツールで頻出。日本の現場では文字化け対策や接続設定、運用性（接続プールや例外処理）が重要なため、そのポイントを押さえた実装例はすぐ役立つ。

## 詳細解説
- アーキテクチャ（MVC + DAO）
  - Model: Userクラス（id, name, email, createdAt などのフィールド）。
  - DAO: DBアクセスを集中させるクラスで、SELECT文を送りResultSetをModelにマッピングする。
  - Controller: JavaFX側のTableViewとDAOを繋ぎ、初期化時にデータを取得してObservableListに詰める。

- 必要な要素
  - JDBC接続: MySQLドライバ（Connector/J）を依存に追加。接続文字列はUTF-8やタイムゾーン指定を忘れない。
    - 例: jdbc:mysql://host:3306/dbname?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Tokyo
  - SQLとセキュリティ: 常にPreparedStatementを使いSQLインジェクションを防ぐ（一覧取得はプレーンSELECTだが、検索条件がある場合は必須）。
  - TableView連携: TableColumn#setCellValueFactoryでUserプロパティを紐付け、ObservableListで変更を反映させる。
  - リソース管理: try-with-resourcesでConnection/PreparedStatement/ResultSetを確実にクローズ。
  - 文字コードとロケール: 日本語データを扱う際の文字化け防止と日付表示のローカライズ。

- 実装の流れ（概略）
  1. Userモデルを定義（フィールド＋getter）。
  2. UserDAOにlistAllUsers()を実装：SELECT * FROM users を実行してList<User>を返す。
  3. Controllerのinitialize()でDAOを呼び出し、ObservableListに変換してTableViewにセット。
  4. UIはFXMLでTableViewと列を定義、fx:idでControllerに紐づける。

- 注意点
  - 大量レコードは一括読み込みを避け、ページングやLIMIT/OFFSET、サーバサイド検索を導入する。
  - パスワードなど機密データは一覧に出さない。ハッシュ値も表示不要。
  - 実運用では接続プール（HikariCPなど）導入を検討。

## 実践ポイント
- 最低限のコード例（DAOとControllerの肝）:

```java
// java - UserDAO: listAllUsers
public List<User> listAllUsers() throws SQLException {
    String sql = "SELECT id, name, email, created_at FROM users";
    try (Connection conn = DriverManager.getConnection(URL, USER, PASS);
         PreparedStatement ps = conn.prepareStatement(sql);
         ResultSet rs = ps.executeQuery()) {
        List<User> list = new ArrayList<>();
        while (rs.next()) {
            list.add(new User(rs.getInt("id"), rs.getString("name"),
                              rs.getString("email"), rs.getTimestamp("created_at")));
        }
        return list;
    }
}
```

```java
// java - Controller: initialize
@FXML private TableView<User> table;
@FXML private TableColumn<User, String> nameCol, emailCol;

public void initialize() {
    nameCol.setCellValueFactory(new PropertyValueFactory<>("name"));
    emailCol.setCellValueFactory(new PropertyValueFactory<>("email"));
    ObservableList<User> data = FXCollections.observableArrayList(new UserDAO().listAllUsers());
    table.setItems(data);
}
```

- 日本向けの運用チェックリスト
  - 接続文字列にUTF-8/Asia/Tokyo指定を追加。
  - DBユーザー権限は最小権限（SELECTのみ）で運用。
  - テーブルの日本語カラムや日付を適切に表示するフォーマット処理を行う。
  - 開発時はローカルでMySQLコンテナ（Docker）を使うと環境差が出にくい。

## 引用元
- タイトル: JavaFX + MySQL User Management: List All Users in Table (MVC & DAO)
- URL: https://www.youtube.com/watch?v=GbdzaSQTZ8g
