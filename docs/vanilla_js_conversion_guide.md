# バニラJavaScriptへの変換ガイド：中級者から初級者へ

## はじめに

このドキュメントは、jQueryなどのライブラリに慣れている中級者の方々が、より軽量でパフォーマンスの高いバニラJavaScript（プレーンなJavaScript）への移行をスムーズに行えるようにするためのガイドです。特に、JavaScriptの学習を始めたばかりの初級者の方々にも理解しやすいように、基本的な概念から丁寧に解説していきます。

## なぜバニラJavaScriptなのか？

現代のWeb開発において、jQueryのようなライブラリは非常に便利ですが、多くのブラウザが標準で提供するAPIが進化し、jQueryなしでも同等以上の機能を実現できるようになりました。バニラJavaScriptを使用することには、以下のようなメリットがあります。

*   **パフォーマンスの向上**: 不要なコードの読み込みが減り、ページの読み込み速度や実行速度が向上します。
*   **学習コストの削減**: 特定のライブラリのAPIを覚える必要がなく、JavaScript本来の挙動を深く理解できます。
*   **依存関係の削減**: プロジェクトの依存関係が減り、管理が容易になります。
*   **最新のWeb標準への対応**: ブラウザの最新機能を直接利用できます。

## jQueryからバニラJavaScriptへの移行の基本

jQueryの多くの機能は、バニラJavaScriptの標準APIで代替可能です。ここでは、よく使われるjQueryの機能と、それに対応するバニラJavaScriptの記述方法を紹介します。

### 1. 要素の選択 (Selectors)

| jQuery | バニラJavaScript |
|---:|---|
| `$('#myId')` | `document.getElementById('myId')` |
| `$('.myClass')` | `document.querySelectorAll('.myClass')` (NodeListを返す) |
| `$('tagName')` | `document.querySelectorAll('tagName')` |

`querySelectorAll`はNodeListを返します。これは配列のように`forEach`でループできますが、`map`などの配列メソッドは直接使えません。必要に応じて`Array.from()`で配列に変換します。

```javascript
// jQuery
$('.myClass').each(function() {
  // ...
});

// バニラJavaScript
document.querySelectorAll('.myClass').forEach(function(element) {
  // ...
});
```

### 2. イベントハンドリング (Event Handling)

| jQuery | バニラJavaScript |
|---:|---|
| `$('#myButton').on('click', function() { ... });` | `document.getElementById('myButton').addEventListener('click', function() { ... });` |

イベントリスナーの追加には`addEventListener`を使用します。

### 3. クラスの操作 (Class Manipulation)

| jQuery | バニラJavaScript |
|---:|---|
| `$('#myElement').addClass('active');` | `document.getElementById('myElement').classList.add('active');` |
| `$('#myElement').removeClass('active');` | `document.getElementById('myElement').classList.remove('active');` |
| `$('#myElement').toggleClass('active');` | `document.getElementById('myElement').classList.toggle('active');` |
| `$('#myElement').hasClass('active');` | `document.getElementById('myElement').classList.contains('active');` |

`classList`プロパティを使用することで、要素のクラスを簡単に操作できます。

### 4. 要素の属性操作 (Attribute Manipulation)

| jQuery | バニラJavaScript |
|---:|---|
| `$('#myImage').attr('src', 'new.jpg');` | `document.getElementById('myImage').setAttribute('src', 'new.jpg');` |
| `$('#myImage').attr('src');` | `document.getElementById('myImage').getAttribute('src');` |

### 5. AJAXリクエスト (AJAX Requests)

jQueryの`$.ajax`は非常に便利ですが、現代のJavaScriptでは`fetch` APIが標準で提供されており、より強力で柔軟な非同期通信が可能です。

```javascript
// jQuery
$.ajax({
  url: '/api/data',
  method: 'GET',
  success: function(data) {
    console.log(data);
  },
  error: function(error) {
    console.error(error);
  }
});

// バニラJavaScript (fetch API)
fetch('/api/data')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });
```

`fetch` APIはPromiseベースであり、より現代的な非同期処理の記述に適しています。

## まとめと次のステップ

バニラJavaScriptへの移行は、最初は少し戸惑うかもしれませんが、慣れてしまえば非常に強力なツールとなります。このガイドが、皆さんの学習と移行の一助となれば幸いです。

今後は、より具体的なユースケースや、パフォーマンス最適化のヒントなど、さらに内容を充実させていく予定です。
