# ZAPスキャン実施報告書

## 1. 概要

- **実施日:** 2025年12月20日
- **目的:** OWASP ZAPによるWebアプリケーションの脆弱性診断と、検出された問題への対応。
- **結果:** 中リスクの脆弱性が2件検出されました。両件とも修正対応済みです。

---

## 2. 検出された脆弱性と対策

### 脆弱性1: Content Security Policy (CSP) ヘッダーが設定されていない

- **リスクレベル:** 中
- **概要:**
  HTTPレスポンスヘッダーに`Content-Security-Policy`（CSP）が設定されていませんでした。
- **解説:**
  CSPは、信頼できるコンテンツソース（JavaScript、CSS、画像など）をブラウザに伝えるためのセキュリティ機能です。これを適切に設定することで、信頼されていないソースからのリソース読み込みがブロックされ、クロスサイトスクリプティング（XSS）などの攻撃を効果的に防ぐことができます。
- **対策内容:**
  `django-csp`ライブラリを導入し、CSPを設定しました。具体的な手順は以下の通りです。
  1.  `requirements.txt`に`django-csp`を追加し、`pip install`でインストールしました。
  2.  Djangoの設定ファイル`mysite/settings/base.py`を以下のように編集しました。
      - `INSTALLED_APPS`に`'csp'`を追加。
      - `MIDDLEWARE`に`'csp.middleware.CSPMiddleware'`を追加。
      - サイトで利用しているJavaScriptやCSSのドメイン（`cdnjs.cloudflare.com`など）を許可するルールを`CONTENT_SECURITY_POLICY`ディレクティブとして定義しました。

---

### 脆弱性2: Sub Resource Integrity (SRI) 属性の欠落

- **リスクレベル:** 中
- **概要:**
  外部のCDN（Content Delivery Network）から読み込んでいるリソースの`<link>`タグに`integrity`属性がありませんでした。
- **解説:**
  Sub Resource Integrity (SRI)は、CDNなどでホストされているファイルが、意図しない第三者によって改ざんされていないかをブラウザが検証するための仕組みです。ファイルのハッシュ値を`integrity`属性に記述しておくことで、もしファイル内容が少しでも異なれば、ブラウザはその読み込みをブロックします。
- **対策内容:**
  `templates/base.html`に記述されているFont AwesomeのCSS読み込み処理を修正しました。
  1.  `curl`と`openssl`コマンドを使用し、`https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css`のSHA-384ハッシュ値を計算しました。
  2.  対象の`<link>`タグに、算出したハッシュ値を持つ`integrity`属性と、`crossorigin="anonymous"`属性を追記しました。

---

## 3. 検証

上記2点の対策を適用後、Django管理コマンド`run_all_tests`を実行し、すべての自動テスト（pytest, jest）が正常に完了することを確認しました。これにより、今回のセキュリティ対策による既存機能への影響（デグレード）がないことを確認済みです。
