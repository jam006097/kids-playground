/**
 * 口コミ管理を行うクラス
 */

interface BootstrapModalEvent extends Event {
  relatedTarget: EventTarget | null;
}

class ReviewManager {
  private modalElement: HTMLElement;
  private formElement: HTMLFormElement;
  private document: Document;
  private modal: bootstrap.Modal;
  private playgroundIdInput: HTMLInputElement | null;
  private modalTitle: HTMLElement | null;

  constructor(
    modalElement: HTMLElement,
    formElement: HTMLFormElement,
    documentObj: Document = document,
  ) {
    if (!modalElement || !formElement) {
      throw new Error('ReviewManagerにはモーダルとフォームの要素が必要です。');
    }
    this.modalElement = modalElement;
    this.formElement = formElement;
    this.document = documentObj;
    this.modal = new window.bootstrap.Modal(this.modalElement);

    this.playgroundIdInput =
      this.formElement.querySelector<HTMLInputElement>('#playgroundId');
    this.modalTitle =
      this.modalElement.querySelector<HTMLElement>('.modal-title');

    this.handleSubmit = this.handleSubmit.bind(this);

    this.initEventHandlers();
  }

  getCsrfToken(): string {
    const tokenElement = this.document.querySelector<HTMLInputElement>(
      '[name=csrfmiddlewaretoken]',
    );
    return tokenElement ? tokenElement.value : '';
  }

  initEventHandlers(): void {
    this.modalElement.addEventListener(
      'show.bs.modal',
      (event: BootstrapModalEvent) => {
        const button = event.relatedTarget;
        if (button instanceof HTMLButtonElement) {
          const playgroundId = button.dataset.playgroundId;
          const playgroundName = button.dataset.playgroundName;
          if (this.playgroundIdInput && playgroundId) {
            this.playgroundIdInput.value = playgroundId;
          }
          if (this.modalTitle && playgroundName) {
            this.modalTitle.textContent = playgroundName + 'への口コミ';
          }
        }
      },
    );

    this.formElement.addEventListener('submit', this.handleSubmit);

    // モーダルが完全に閉じられた後に、フォーカスをbody要素に戻す
    this.modalElement.addEventListener('hidden.bs.modal', () => {
      this.document.body.focus();
    });
  }

  async handleSubmit(event: Event): Promise<void> {
    event.preventDefault();

    const urlEncodedData = new URLSearchParams(
      new FormData(this.formElement) as unknown as Iterable<[string, string]>,
    );
    const csrfToken = this.getCsrfToken();
    urlEncodedData.append('csrfmiddlewaretoken', csrfToken);

    const playgroundId = this.playgroundIdInput
      ? this.playgroundIdInput.value
      : '';

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
      // Focesd element in modal is blurred before hiding modal.
      (this.document.activeElement as HTMLElement)?.blur();
      this.modal.hide();
    } catch (_error) {
      alert('口コミの投稿に失敗しました。');
    }
  }
}

export { ReviewManager };
