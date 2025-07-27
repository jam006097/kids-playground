# Project directives for jam006097/kidsPlayGround

## 🎯 作業前（Before Start）
- 必ず GitHub リポジトリ `jam006097/kidsPlayGround` に Issue を新規登録。
- Issueには、目的・完了条件・範囲を明記してください。

## 🧪 開発方針
- twadaさんスタイルの TDD をベースに進行。
- PDCA サイクル（Plan, Do, Check, Act）を繰り返しながら作業。
- コードは保守性・可読性を最優先に設計し、SOLID原則（単一責任・オープン/クローズ・リスコフ・インターフェース分離・依存性逆転）を意識して実装すること。
- クラスや関数は、責務ごとに適切に分離し、再利用・テストしやすい構造とすること。
- クラス設計では「1クラス1責務」を基本とし、処理の流れや依存関係が見通しやすいようにする。
- 必要に応じてデザインパターン（Strategy, Factoryなど）を活用し、柔軟で拡張可能な構成を心がける。


### 🧪 TDDスタイルの基本ルール
- Red → Green → Refactor の順に進める
- 最小のテスト → 最小の実装 → リファクタリング
- 1ステップごとにコミット、最小粒度を保つ

## 🔀 Git 運用ルール
- Commitはしない

## ✅ 作業後（After Done）
- 対象 Issue を `Closed` にする。
- コメントや振り返り（Check, Act）を残す。
- 作業内容を初心者でも理解できるよう、わかりやすい解説文を記述すること。
- 作業から得られた知見が、設定ファイル（GEMINI.mdなど）に反映すべきと判断される場合は、提案を行うこと。

## 🛠 技術スタック
- フレームワーク: Django 5.1.5 
- 言語: Python 3.12.3
- テスト: pytest
- バージョン管理: GitHub
- 開発環境: PythonAnywhere / VSCode

## 🗂 命名規則と構成
- アプリ構成は Django 標準に準拠
- `templates`, `static`, `tests` を明確に分離
- テストファイル名は `test_*.py`

