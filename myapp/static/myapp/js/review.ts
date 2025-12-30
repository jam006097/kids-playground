/**
 * review.ts
 *
 * このファイルは、レビュー投稿機能に関するロジックとUIイベントの結合を扱います。
 * Core Logic: APIへのレビュー送信とレスポンス処理を行う純粋な関数。
 * UI Binding: DOMイベントを監視し、コアロジックを呼び出してUIを更新する部分。
 */

/**
 * レビューデータの型定義
 */
export interface Review {
  user_account_name: string;
  rating: number;
  content: string;
  created_at: string;
}

/**
 * APIレスポンスの型定義
 */
interface ApiResponse {
  status: 'success' | 'error';
  review?: Review;
  message?: string;
}

/**
 * Core Logic: レビュー投稿処理
 *
 * この関数は、引数で受け取った情報をもとにAPIリクエストを送信し、
 * 結果を返すことに専念します。DOMには一切依存しません。
 *
 * @param playgroundId - 公園のID
 * @param csrfToken - CSRFトークン
 * @param formData - フォームデータ
 * @throws ネットワークエラー、サーバーエラー、アプリケーションエラー時に例外をスローする
 * @returns 成功時にはレビューデータを返す
 */
export const submitReview = async (
  playgroundId: string,
  csrfToken: string,
  formData: FormData,
): Promise<Review> => {
  if (!playgroundId) {
    throw new Error('Playground ID is not provided.');
  }
  if (!csrfToken) {
    throw new Error('CSRF token is not provided.');
  }

  const response = await fetch(`/playground/${playgroundId}/add_review/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      // FormDataを直接送信するため、Content-Typeはブラウザに任せる
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Server responded with status: ${response.status}`);
  }

  const data: ApiResponse = await response.json();

  if (data.status === 'success' && data.review) {
    return data.review;
  } else {
    throw new Error(data.message || 'An unknown error occurred.');
  }
};

/**
 * UI Binding: DOM要素とイベントリスナーの設定
 *
 * この部分は、DOMの準備ができた後に実行され、UI要素のイベントと
 * `submitReview`関数を結合します。
 */
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('reviewForm') as HTMLFormElement;
    const reviewList = document.getElementById('review-list') as HTMLUListElement;
    const noReviewsMessage = document.getElementById('no-reviews-message');
    const modalElement = document.getElementById('reviewModal');
    const reviewModal = modalElement ? new window.bootstrap.Modal(modalElement) : null;
    const toastElement = document.getElementById('notificationToast');
    const toastBody = document.getElementById('notificationToastBody');
    const notificationToast = toastElement ? new window.bootstrap.Toast(toastElement) : null;

    const getCsrfToken = (): string => {
      const tokenElement = document.querySelector<HTMLInputElement>('[name=csrfmiddlewaretoken]');
      return tokenElement ? tokenElement.value : '';
    };

    const showToast = (message: string, isError: boolean = false) => {
      if (toastBody && notificationToast && toastElement) {
        toastBody.textContent = message;
        toastElement.classList.toggle('bg-danger', isError);
        toastElement.classList.toggle('text-white', isError);
        notificationToast.show();
      } else {
        alert(message);
      }
    };

    const addReviewToDom = (review: Review) => {
      if (noReviewsMessage) {
        noReviewsMessage.style.display = 'none';
      }
      const reviewEl = document.createElement('li');
      reviewEl.className = 'list-group-item';
      reviewEl.innerHTML = `
        <strong>${review.user_account_name}</strong> (評価: ${review.rating})<br>
        <p class="mt-2">${review.content.replace(/\n/g, '<br>')}</p>
        <small class="text-muted d-block text-end">投稿日: ${review.created_at}</small>
      `;
      reviewList.prepend(reviewEl);
    };

    if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const playgroundId = (document.getElementById('playgroundId') as HTMLInputElement)?.value;
        const csrfToken = getCsrfToken();
        const formData = new FormData(reviewForm);

        try {
          const review = await submitReview(playgroundId, csrfToken, formData);
          addReviewToDom(review);
          reviewForm.reset();
          reviewModal?.hide();
          showToast('口コミが投稿されました！');
        } catch (error) {
          const message = error instanceof Error ? error.message : '不明なエラーが発生しました。';
          showToast(message, true);
        }
      });
    }
  });
}
