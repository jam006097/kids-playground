# データベース設計書

## ER図（Mermaid記法）
```mermaid
erDiagram
    CustomUser ||--o{ Favorite : "has"
    CustomUser ||--o{ Review : "writes"
    Playground ||--o{ Favorite : "is_favorited_by"
    Playground ||--o{ Review : "receives (reviews)"

    CustomUser {
        int id PK
        string email UK
        string account_name
        bool is_staff
        bool is_active
        datetime date_joined
    }
    Playground {
        int id PK
        string prefecture
        string name
        string address
        string phone nullable
        float latitude nullable
        float longitude nullable
        text description nullable
        string website
        bool nursing_room_available
        bool diaper_changing_station_available
        bool stroller_accessible
        bool lunch_allowed
        string google_map_url nullable
        bool indoor_play_area
        bool kids_toilet_available
        time opening_time nullable
        time closing_time nullable
        int target_age_start nullable
        int target_age_end nullable
        decimal fee_decimal nullable
        string parking_info nullable
    }
    Favorite {
        int id PK
        int user_id FK
        int playground_id FK
    }
    Review {
        int id PK
        int playground_id FK
        int user_id FK
        text content
        int rating
        datetime created_at
    }
```

---

## 各テーブル（モデル）詳細

### CustomUser（カスタムユーザー）
| フィールド名   | 型              | 説明・制約                 |
|----------------|-----------------|----------------------------|
| id             | AutoField       | 主キー (PK)                |
| email          | EmailField      | メールアドレス (UK)        |
| account_name   | CharField(50)   | アカウント名               |
| is_staff       | BooleanField    | 管理サイトへのアクセス権限   |
| is_active      | BooleanField    | ユーザーが有効か           |
| date_joined    | DateTimeField   | アカウント作成日時         |

### Playground（施設）
| フィールド名                        | 型              | 説明・制約                                   |
|-------------------------------------|-----------------|----------------------------------------------|
| id                                  | AutoField       | 主キー (PK)                                  |
| prefecture                          | CharField(100)  | 都道府県名                                   |
| name                                | CharField(200)  | 施設名                                       |
| address                             | CharField(300)  | 住所                                         |
| phone                               | CharField(30)   | 電話番号 (nullable)                          |
| latitude                            | FloatField      | 緯度 (nullable)                              |
| longitude                           | FloatField      | 経度 (nullable)                              |
| description                         | TextField       | 施設説明 (nullable, default: "")            |
| website                             | URLField        | ウェブサイトURL (default: "")                |
| nursing_room_available              | BooleanField    | 授乳室の有無                                 |
| diaper_changing_station_available   | BooleanField    | おむつ交換台の有無                           |
| stroller_accessible                 | BooleanField    | ベビーカーアクセス可否                       |
| lunch_allowed                       | BooleanField    | 持ち込みランチ可否                           |
| google_map_url                      | URLField(500)   | GoogleマップURL (nullable)                   |
| indoor_play_area                    | BooleanField    | 屋内遊び場の有無                             |
| kids_toilet_available               | BooleanField    | 子供用トイレの有無                           |
| opening_time                        | TimeField       | 開園時間 (nullable)                          |
| closing_time                        | TimeField       | 閉園時間 (nullable)                          |
| target_age_start                    | IntegerField    | 対象年齢（開始） (nullable)                  |
| target_age_end                      | IntegerField    | 対象年齢（終了） (nullable)                  |
| fee_decimal                         | DecimalField    | 料金 (nullable)                              |
| parking_info                        | CharField(10)   | 駐車場情報 (nullable, choices)               |

### Favorite（お気に入り）
| フィールド名   | 型            | 説明・制約                                   |
|----------------|---------------|----------------------------------------------|
| id             | AutoField     | 主キー (PK)                                  |
| user           | ForeignKey    | ユーザー (FK)                                |
| playground     | ForeignKey    | お気に入りの施設 (FK)                        |
| (制約)         | -             | `user`と`playground`の組み合わせはユニーク   |

### Review（口コミ）
| フィールド名   | 型                | 説明・制約                                   |
|----------------|-------------------|----------------------------------------------|
| id             | AutoField         | 主キー (PK)                                  |
| playground     | ForeignKey        | 口コミ対象の施設 (FK, related_name='reviews') |
| user           | ForeignKey        | 投稿ユーザー (FK)                            |
| content        | TextField         | 口コミ内容                                   |
| rating         | PositiveInteger   | 評価（1〜5）                                 |
| created_at     | DateTimeField     | 投稿日時 (auto_now_add=True)                 |

---

## 注意事項
- 外部キーは`on_delete=models.CASCADE`（親が消えると子も消える）をデフォルトとします。
