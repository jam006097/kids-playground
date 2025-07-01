# シーケンス図（Mermaid記法）

## 例：ユーザーがお気に入り登録を行う場合

```mermaid
sequenceDiagram
    participant User
    participant Web as Webブラウザ
    participant View as Django View
    participant DB as DB

    User->>Web: お気に入りボタンをクリック
    Web->>View: お気に入り登録リクエスト送信
    View->>DB: Favoriteレコード作成
    DB-->>View: 登録結果返却
    View-->>Web: レスポンス（成功/失敗）
    Web-->>User: お気に入り登録完了メッセージ表示
```

---

## 例：ユーザーがレビューを投稿する場合

```mermaid
sequenceDiagram
    participant User
    participant Web as Webブラウザ
    participant View as Django View
    participant DB as DB

    User->>Web: レビュー投稿フォームに入力し送信
    Web->>View: レビュー投稿リクエスト送信
    View->>DB: Reviewレコード作成
    DB-->>View: 登録結果返却
    View-->>Web: レスポンス（成功/失敗）
    Web-->>User: レビュー投稿完了メッセージ表示
```

---

## 例：ユーザーが施設を検索する場合

```mermaid
sequenceDiagram
    participant User
    participant Web as Webブラウザ
    participant View as Django View
    participant DB as DB

    User->>Web: 検索フォームに条件を入力し送信
    Web->>View: 検索リクエスト送信
    View->>DB: Playgroundテーブルを検索
    DB-->>View: 検索結果返却
    View-->>Web: 検索結果をHTMLで返却
    Web-->>User: 検索結果を画面に表示
```

---

## 例：ユーザーが新規会員登録を行う場合

```mermaid
sequenceDiagram
    participant User
    participant Web as Webブラウザ
    participant View as Django View
    participant DB as DB

    User->>Web: 登録フォームに入力し送信
    Web->>View: 会員登録リクエスト送信
    View->>DB: Userレコード作成
    DB-->>View: 登録結果返却
    View-->>Web: レスポンス（成功/失敗）
    Web-->>User: 登録完了メッセージ表示
```

---

## 例：ユーザーがログインする場合

```mermaid
sequenceDiagram
    participant User
    participant Web as Webブラウザ
    participant View as Django View
    participant DB as DB

    User->>Web: ログインフォームに入力し送信
    Web->>View: ログインリクエスト送信
    View->>DB: User認証
    DB-->>View: 認証結果返却
    View-->>Web: レスポンス（成功/失敗）
    Web-->>User: マイページへ遷移またはエラーメッセージ表示
```

---

## 例：ユーザーがマイページを表示する場合

```mermaid
sequenceDiagram
    participant User
    participant Web as Webブラウザ
    participant View as Django View
    participant DB as DB

    User->>Web: マイページを開く
    Web->>View: マイページ表示リクエスト送信
    View->>DB: お気に入り・レビュー情報取得
    DB-->>View: 取得結果返却
    View-->>Web: マイページHTML返却
    Web-->>User: マイページ表示
```

---

## 例：ユーザーがレビューを削除・編集する場合

```mermaid
sequenceDiagram
    participant User
    participant Web as Webブラウザ
    participant View as Django View
    participant DB as DB

    User->>Web: レビュー削除/編集ボタンをクリック
    Web->>View: 削除/編集リクエスト送信
    View->>DB: Reviewレコード削除/更新
    DB-->>View: 結果返却
    View-->>Web: レスポンス（成功/失敗）
    Web-->>User: 完了メッセージ表示
```

---

## 例：ユーザーがお気に入りを削除する場合

```mermaid
sequenceDiagram
    participant User
    participant Web as Webブラウザ
    participant View as Django View
    participant DB as DB

    User->>Web: お気に入り解除ボタンをクリック
    Web->>View: お気に入り削除リクエスト送信
    View->>DB: Favoriteレコード削除
    DB-->>View: 結果返却
    View-->>Web: レスポンス（成功/失敗）
    Web-->>User: 完了メッセージ表示
```

---
