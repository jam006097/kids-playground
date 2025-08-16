## JavaScriptの基本を学ぼう！ウェブページを動かす魔法の言葉

こんにちは！ウェブサイトがどのように動いているのか、不思議に思ったことはありませんか？ボタンをクリックすると何か表示されたり、情報が更新されたり…そんな「動き」を作り出しているのが、JavaScriptというプログラミング言語です。

このガイドでは、ウェブサイトの「脳みそ」とも言えるJavaScriptの基本的な書き方を、実際のコード例を交えながら、優しく解説していきます。一緒にJavaScriptの魔法を解き明かしましょう！

### 1. JavaScriptって何？

JavaScriptは、ウェブページに動きや対話性（インタラクティブ性）を与えるためのプログラミング言語です。例えば、以下のようなことができます。

*   ボタンをクリックしたときに、メッセージを表示する
*   入力フォームに入力された内容をチェックする
*   サーバーから新しい情報を取得して、ページを更新する
*   アニメーションを表示する

私たちが今見ているウェブサイトでも、JavaScriptがたくさん使われています。

### 2. JavaScriptの基本的な書き方を見てみよう

まずは、JavaScriptの最も基本的な要素から見ていきましょう。

#### 2.1. 変数：情報をしまっておく箱

プログラミングでは、数字や文字などの情報を一時的に保存しておく「箱」のようなものを使います。これを「変数」と呼びます。JavaScriptでは、`let` や `const` というキーワードを使って変数を作ります。

*   `let`：後から中身を書き換えられる変数
*   `const`：一度中身を入れたら、後から書き換えられない変数（定数）

**例：`myapp/static/js/utils.js` から**

```javascript
export function getCookie(name) {
  let cookieValue = null; // ① 後から値が変わる可能性があるので 'let' を使う
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';'); // ② 一度クッキーのリストを取得したら変わらないので 'const' を使う
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim(); // ③ ループ内で一時的に使う変数なので 'const' を使う
      // ...
    }
  }
  return cookieValue;
}
```

この例では、`cookieValue` という箱に最初は `null` を入れていますが、後でクッキーの値が見つかればその値に変わる可能性があります。`cookies` や `cookie` は、一度値を入れたらそのブロック内では変わらないので `const` を使っていますね。

#### 2.2. 関数：処理をまとめるブロック

同じような処理を何度も書くのは大変ですよね。そんなときに便利なのが「関数」です。関数は、特定の処理をひとまとまりにしたもので、名前を付けておけば必要なときにいつでも呼び出すことができます。

**例：`myapp/static/js/utils.js` から**

```javascript
export function getCookie(name) { // ① 'getCookie' という名前の関数を定義
  // ここに関数が行う処理を書く
  let cookieValue = null;
  // ...
  return cookieValue; // ② 処理の結果を返す
}
```

この `getCookie` 関数は、`name` という情報（引数と呼びます）を受け取って、その名前のクッキーを探し、見つかったクッキーの値を返してくれます。`export` は、この関数を他のファイルでも使えるようにするためのキーワードです。

#### 2.3. 条件分岐：もし〜なら、この処理をする

プログラムは、状況に応じて異なる処理をしたい場合があります。「もし〜なら、この処理をする」というように、条件によって処理を分けることを「条件分岐」と呼び、`if` 文を使います。

**例：`myapp/static/js/utils.js` から**

```javascript
export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') { // ① もしクッキーが存在し、空でなければ
    const cookies = document.cookie.split(';');
    // ... クッキーを処理する
  }
  return cookieValue;
}
```

ここでは、「もしブラウザにクッキーが保存されていて、それが空でなければ」という条件が満たされた場合に、クッキーを処理する部分が実行されます。

#### 2.4. 繰り返し処理：同じことを何度も行う

同じ処理を何度も繰り返したいときに使うのが「繰り返し処理（ループ）」です。`for` 文などがよく使われます。

**例：`myapp/static/js/utils.js` から**

```javascript
export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) { // ① 'cookies' の数だけ繰り返す
      const cookie = cookies[i].trim();
      // ... 各クッキーをチェックする処理
    }
  }
  return cookieValue;
}
```

この `for` ループは、`cookies` というリストに入っているクッキーの数だけ、一つ一つのクッキーをチェックする処理を繰り返しています。

### 3. ウェブページを操作しよう（DOM操作）

JavaScriptの大きな役割の一つは、表示されているウェブページの内容を動的に変更することです。ウェブページの要素（ボタン、テキスト、画像など）は「DOM（Document Object Model）」という仕組みで管理されており、JavaScriptを使ってこれらを操作できます。

**例：`myapp/static/js/favorite.js` から**

```javascript
class FavoriteManager {
  // ...
  updateFavoriteButtons(favorite_ids) {
    // ① 'data-playground-id' 属性を持つすべてのボタン要素を探す
    document
      .querySelectorAll('.btn-outline-success[data-playground-id]')
      .forEach((button) => {
        const playgroundId = button.getAttribute('data-playground-id'); // ② ボタンから 'data-playground-id' の値を取得
        // ...
        button.textContent = isFavorite // ③ ボタンの表示テキストを変更
          ? 'お気に入り解除'
          : 'お気に入りに追加';
        button.disabled = false; // ④ ボタンを有効/無効にする
      });
  }
}
```

*   `document.querySelectorAll('.btn-outline-success[data-playground-id]')`：これは、ウェブページの中から特定の条件（`.btn-outline-success`というクラスと`data-playground-id`という属性を持つ要素）に合うすべての要素を探し出す命令です。
*   `button.getAttribute('data-playground-id')`：見つけたボタン要素から、`data-playground-id`という属性に設定されている値を取得しています。
*   `button.textContent = '...'`：ボタンに表示されているテキストを書き換えています。
*   `button.disabled = false;`：ボタンがクリックできない状態（無効）を、クリックできる状態（有効）に戻しています。

このように、JavaScriptを使うと、ウェブページ上のあらゆる要素を自由自在に操作できるのです。

### 4. サーバーと通信しよう（Fetch API）

ウェブサイトは、サーバーから情報を取得したり、サーバーに情報を送ったりすることで成り立っています。JavaScriptでは、`fetch` という機能を使って、サーバーと簡単に通信できます。

**例：`myapp/static/js/favorite.js` から**

```javascript
class FavoriteManager {
  // ...
  toggleFavorite(button, playgroundId) {
    // ...
    return fetch(url, { // ① 指定したURLにリクエストを送る
      method: 'POST', // ② POSTメソッドで送ることを指定
      headers: { // ③ 送信する情報の種類や認証情報を設定
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken,
      },
      body: `playground_id=${playgroundId}`, // ④ サーバーに送るデータ
    })
      .then((response) => response.json()) // ⑤ サーバーからの応答をJSON形式で受け取る
      .then((data) => { // ⑥ 受け取ったデータを使って処理を行う
        if (data.status === 'ok') {
          // ... 成功時の処理
        } else {
          alert('操作に失敗しました。'); // ⑦ 失敗時のメッセージ表示
        }
      })
      .catch((error) => { // ⑧ 通信中にエラーが起きた場合の処理
        console.error('フェッチエラー:', error);
        alert('エラーが発生しました。');
      })
      .finally(() => { // ⑨ 成功・失敗に関わらず最後に実行される処理
        button.disabled = false;
      });
  }
}
```

この `fetch` の例では、お気に入りボタンがクリックされたときに、サーバーに対して「この遊び場をお気に入りに追加/解除してほしい」というリクエストを送っています。

*   `fetch(url, {...})`：`url`で指定されたアドレスに、`{...}`で指定された方法（POSTメソッド、ヘッダー、データなど）で通信を開始します。
*   `.then(...)`：サーバーからの応答が返ってきたときに実行される処理です。ここでは、応答をJSON形式に変換したり、そのデータを使ってボタンの表示を更新したりしています。
*   `.catch(...)`：通信中に何か問題（エラー）が発生した場合に実行される処理です。
*   `.finally(...)`：通信が成功しても失敗しても、最後に必ず実行される処理です。ここでは、無効にしていたボタンを再び有効にしています。

このように、`fetch` と `.then`、`.catch`、`.finally` を組み合わせることで、非同期で行われるサーバーとの通信をスムーズに扱うことができます。

### 5. コードを整理しよう（クラスとモジュール）

プログラムが大きくなってくると、コードがごちゃごちゃになりがちです。JavaScriptには、コードを整理するための便利な仕組みがあります。

#### 5.1. クラス：関連する処理をまとめる設計図

「クラス」は、関連するデータと処理（関数）をひとまとまりにした「設計図」のようなものです。この設計図から「インスタンス」という実際の「モノ」を作り、それを使って処理を行います。

**例：`myapp/static/js/favorite.js` から**

```javascript
class FavoriteManager { // ① 'FavoriteManager' というクラスを定義
  /**
   * FavoriteManagerのコンストラクタ。
   * @param {function} [getCookie=defaultGetCookie] - クッキーを取得するための関数。
   */
  constructor(getCookie = defaultGetCookie) { // ② クラスが作られるときに最初に実行される部分
    this.getCookie = getCookie;
  }

  /**
   * 遊び場のお気に入り状態を切り替えます。
   * @param {HTMLElement} button - お気に入りボタンのDOM要素。
   * @param {string} playgroundId - 遊び場のID。
   */
  toggleFavorite(button, playgroundId) { // ③ クラスの機能（メソッド）
    // ...
  }

  /**
   * ページ上のお気に入りボタンのテキストを更新します。
   * @param {Array<string>} favorite_ids - お気に入り登録されている遊び場のIDの配列。
   */
  updateFavoriteButtons(favorite_ids) { // ④ クラスの別の機能（メソッド）
    // ...
  }
}

export { FavoriteManager }; // ⑤ このクラスを他のファイルで使えるようにする
```

`FavoriteManager` クラスは、お気に入り機能に関するすべての処理（お気に入り状態の切り替え、ボタンの表示更新など）をまとめています。`constructor` は、`FavoriteManager` のインスタンス（実体）が作られるときに最初に実行される特別な関数です。`toggleFavorite` や `updateFavoriteButtons` は、このクラスが持つ機能（メソッド）です。

#### 5.2. モジュール：ファイルを分けて管理する

プログラムの規模が大きくなると、一つのファイルにすべてのコードを書くのは非効率です。JavaScriptでは「モジュール」という仕組みを使って、コードを複数のファイルに分割し、必要な部分だけを読み込んで使うことができます。

**例：`myapp/static/js/favorite.js` から**

```javascript
import { getCookie as defaultGetCookie } from './utils.js'; // ① 'utils.js' から 'getCookie' 関数を読み込む

// ...

export { FavoriteManager }; // ② 'FavoriteManager' クラスを他のファイルで使えるようにする
```

*   `import { getCookie as defaultGetCookie } from './utils.js';`：これは、同じディレクトリにある `utils.js` というファイルから `getCookie` という関数を読み込んで、このファイルの中では `defaultGetCookie` という名前で使えるようにする、という意味です。
*   `export { FavoriteManager };`：これは、このファイルで定義した `FavoriteManager` クラスを、他のファイルから `import` して使えるようにする、という意味です。

このようにモジュールを使うことで、コードの見通しが良くなり、チームでの開発も効率的に行えるようになります。

### 6. まとめと次のステップ

このガイドでは、JavaScriptの基本的な要素から、ウェブページを操作する方法、サーバーと通信する方法、そしてコードを整理する方法まで、幅広く見てきました。

*   **変数**で情報を保存し、**関数**で処理をまとめ、**条件分岐**や**繰り返し処理**でプログラムの流れを制御します。
*   **DOM操作**でウェブページの内容を動的に変更し、**Fetch API**でサーバーと通信します。
*   **クラス**や**モジュール**を使って、コードを整理し、再利用しやすくします。

これらはJavaScriptのほんの一部ですが、ウェブ開発の第一歩として非常に重要な知識です。

もし、もっと深く学びたいと思ったら、以下のキーワードで調べてみてください。

*   **イベントリスナー**: ユーザーの操作（クリック、キー入力など）に反応する方法
*   **非同期処理**: 時間のかかる処理を待たずに、他の処理を進める方法（Promise, async/await）
*   **デバッグ**: プログラムの誤りを見つけて修正する方法

JavaScriptの世界は奥深く、学ぶほどに新しい発見があります。このガイドが、あなたのJavaScript学習のきっかけになれば嬉しいです！
