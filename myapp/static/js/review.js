/**
 * 口コミ管理を行うクラス。(jQuery依存なし)
 */
class ReviewManager {
  constructor(modalElement, formElement, documentObj = document) {
    if (!modalElement || !formElement) {
      throw new Error('ReviewManagerにはモーダルとフォームの要素が必要です。');
    }
    this.modalElement = modalElement;
    this.formElement = formElement;
    this.document = documentObj;
    this.modal = new bootstrap.Modal(this.modalElement);

    this.playgroundIdInput = this.formElement.querySelector('#playgroundId');
    this.modalTitle = this.modalElement.querySelector('.modal-title');

    // this.handleSubmitをこのクラスインスタンスにバインドする
    this.handleSubmit = this.handleSubmit.bind(this);

    this.initEventHandlers();
  }

  getCsrfToken() {
    const tokenElement = this.document.querySelector('[name=csrfmiddlewaretoken]');
    return tokenElement ? tokenElement.value : '';
  }

  // メソッド名を変更
  initEventHandlers() {
    this.modalElement.addEventListener('show.bs.modal', (event) => {
      const button = event.relatedTarget;
      if (!button) return;
      const playgroundId = button.dataset.playgroundId;
      const playgroundName = button.dataset.playgroundName;
      if (this.playgroundIdInput) {
        this.playgroundIdInput.value = playgroundId;
      }
      if (this.modalTitle) {
        this.modalTitle.textContent = playgroundName + 'への口コミ';
      }
    });

    // イベントリスナーは、新しいhandleSubmitメソッドを参照するだけ
    this.formElement.addEventListener('submit', this.handleSubmit);
  }

  // フォーム送信ロジックを独立したメソッドとして切り出す
  async handleSubmit(event) {
    event.preventDefault();

    const urlEncodedData = new URLSearchParams(new FormData(this.formElement));
    const csrfToken = this.getCsrfToken();
    urlEncodedData.append('csrfmiddlewaretoken', csrfToken);

    const playgroundId = this.playgroundIdInput ? this.playgroundIdInput.value : '';

    try {
      const response = await fetch(`/playground/${playgroundId}/add_review/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken,
        },
        body: urlEncodedData.toString(),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok.');
      }

      const data = await response.json();
      alert(data.message);
      this.modal.hide();
    } catch (error) {
      alert('口コミの投稿に失敗しました。');
    }
  }
}

export { ReviewManager };
