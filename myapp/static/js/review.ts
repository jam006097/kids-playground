

/**
 * 口コミ管理を行うクラス
 */
class ReviewManager {
  private modalElement: HTMLElement;
  private formElement: HTMLFormElement;
  private document: Document;
  private modal: bootstrap.Modal;
  private playgroundIdInput: HTMLInputElement | null;
  private modalTitle: HTMLElement | null;

  constructor(modalElement: HTMLElement, formElement: HTMLFormElement, documentObj: Document = document) {
    if (!modalElement || !formElement) {
      throw new Error('ReviewManagerにはモーダルとフォームの要素が必要です。');
    }
    this.modalElement = modalElement;
    this.formElement = formElement;
    this.document = documentObj;
    this.modal = new window.bootstrap.Modal(this.modalElement);

    this.playgroundIdInput = this.formElement.querySelector<HTMLInputElement>('#playgroundId');
    this.modalTitle = this.modalElement.querySelector<HTMLElement>('.modal-title');

    this.handleSubmit = this.handleSubmit.bind(this);

    this.initEventHandlers();
  }

  getCsrfToken(): string {
    const tokenElement = this.document.querySelector<HTMLInputElement>('[name=csrfmiddlewaretoken]');
    return tokenElement ? tokenElement.value : '';
  }

  initEventHandlers(): void {
    this.modalElement.addEventListener('show.bs.modal', (event: Event) => {
      const button = (event as any).relatedTarget as HTMLButtonElement | null;
      if (!button) return;
      const playgroundId = button.dataset.playgroundId;
      const playgroundName = button.dataset.playgroundName;
      if (this.playgroundIdInput && playgroundId) {
        this.playgroundIdInput.value = playgroundId;
      }
      if (this.modalTitle && playgroundName) {
        this.modalTitle.textContent = playgroundName + 'への口コミ';
      }
    });

    this.formElement.addEventListener('submit', this.handleSubmit);
  }

  async handleSubmit(event: Event): Promise<void> {
    event.preventDefault();

    const urlEncodedData = new URLSearchParams(new FormData(this.formElement) as any);
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

      const data: { message: string } = await response.json();
      alert(data.message);
      this.modal.hide();
    } catch (error) {
      alert('口コミの投稿に失敗しました。');
    }
  }
}

export { ReviewManager };
