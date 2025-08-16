/**
 * 口コミ管理を行うクラス。
 * モーダルの表示、フォームのデータ取得、AJAXによる口コミ投稿処理を管理します。
 */
class ReviewManager {
  /**
   * ReviewManagerのコンストラクタ。
   * @param {object} jQuery - jQueryオブジェクト。
   * @param {Document} [documentObj=document] - Documentオブジェクト。テスト用にモックを注入できるようにします。
   */
  constructor(jQuery, documentObj = document) {
    this.$ = jQuery;
    this.document = documentObj;
    this.initReviewHandlers();
  }

  /**
   * CSRFトークンをDOMから取得します。
   * @returns {string} CSRFトークンの値。
   */
  getCsrfToken() {
    return this.document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

  /**
   * 口コミ関連のイベントハンドラを初期化します。
   * モーダルの表示時とフォーム送信時の処理を設定します。
   */
  initReviewHandlers() {
    const self = this; // `this` コンテキストを保持

    // モーダルが開かれるときに施設情報を設定
    // 関連するボタンから遊び場IDと名前を取得し、モーダル内の要素に設定します。
    self.$('#reviewModal').on('show.bs.modal', (event) => {
      const button = self.$(event.relatedTarget); // モーダルをトリガーしたボタン
      const playgroundId = button.data('playground-id'); // ボタンから遊び場IDを取得
      const playgroundName = button.data('playground-name'); // ボタンから遊び場名を取得
      const modal = self.$(event.currentTarget); // 現在のモーダル要素

      modal.find('#playgroundId').val(playgroundId); // 隠しフィールドに遊び場IDを設定
      modal.find('.modal-title').text(playgroundName + 'への口コミ'); // モーダルのタイトルを設定
    });

    // 口コミフォームの送信処理
    // フォームの送信をインターセプトし、AJAXでデータを送信します。
    self.$('#reviewForm').on('submit', (event) => {
      event.preventDefault(); // デフォルトのフォーム送信を防止

      const formData = self.$(event.currentTarget).serialize(); // フォームデータをシリアライズ
      const playgroundId = self.$('#playgroundId').val(); // 遊び場IDを取得
      const csrfToken = self.getCsrfToken(); // CSRFトークンを取得

      self.$.ajax({
        url: `/playground/${playgroundId}/add_review/`, // 口コミ投稿のエンドポイント
        method: 'POST',
        data: formData + '&csrfmiddlewaretoken=' + csrfToken, // フォームデータとCSRFトークンを結合
        success: (response) => {
          // 成功時の処理
          // グローバルなalert関数を直接呼び出しています。
          // GEMINI.mdの指示に従い、組み込み関数の呼び出しは直接行うのが安全です。
          alert(response.message);
          self.$('#reviewModal').modal('hide'); // モーダルを閉じる
        },
        error: () => {
          // 失敗時の処理
          // グローバルなalert関数を直接呼び出しています。
          alert('口コミの投稿に失敗しました。');
        },
      });
    });
  }
}

export { ReviewManager };
