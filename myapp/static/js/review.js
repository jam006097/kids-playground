class ReviewManager {
  constructor(jQuery, documentObj = document) {
    this.$ = jQuery;
    this.document = documentObj;
    this.initReviewHandlers();
  }

  getCsrfToken() {
    return this.document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

  initReviewHandlers() {
    const self = this; // Store this context

    // モーダルが開かれるときに施設情報を設定
    self.$('#reviewModal').on('show.bs.modal', (event) => {
      const button = self.$(event.relatedTarget);
      const playgroundId = button.data('playground-id');
      const playgroundName = button.data('playground-name');
      const modal = self.$(event.currentTarget); // Use currentTarget for the modal element
      modal.find('#playgroundId').val(playgroundId);
      modal.find('.modal-title').text(playgroundName + 'への口コミ');
    });

    // 口コミフォームの送信処理
    self.$('#reviewForm').on('submit', (event) => {
      event.preventDefault();
      const formData = self.$(event.currentTarget).serialize(); // Use currentTarget for the form element
      const playgroundId = self.$('#playgroundId').val();
      const csrfToken = self.getCsrfToken(); // CSRFトークンを取得

      self.$.ajax({
        url: `/playground/${playgroundId}/add_review/`,
        method: 'POST',
        data: formData + '&csrfmiddlewaretoken=' + csrfToken, // CSRFトークンを追加
        success: (response) => {
          alert(response.message); // Direct call to global alert
          self.$('#reviewModal').modal('hide');
        },
        error: () => {
          alert('口コミの投稿に失敗しました。'); // Direct call to global alert
        },
      });
    });
  }
}

export { ReviewManager };
