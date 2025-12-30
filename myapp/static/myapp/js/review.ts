/**
 * Handles review form submission via AJAX and dynamically updates the UI.
 */
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
        if (toastBody && notificationToast) {
            toastBody.textContent = message;
            toastElement?.classList.toggle('bg-danger', isError);
            toastElement?.classList.toggle('text-white', isError);
            notificationToast.show();
        } else {
            // Fallback to alert if toast elements are not found
            alert(message);
        }
    };

    const addReviewToDom = (review: { content: string, rating: number, user_account_name: string, created_at: string }) => {
        if (noReviewsMessage) {
            noReviewsMessage.remove();
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

            const formData = new FormData(reviewForm);
            const urlEncodedData = new URLSearchParams(Array.from(formData.entries()) as [string, string][]);
            const csrfToken = getCsrfToken();
            const playgroundId = (document.getElementById('playgroundId') as HTMLInputElement)?.value;

            if (!playgroundId) {
                showToast('Playground IDが見つかりません。', true);
                return;
            }

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
                    throw new Error('サーバーとの通信に失敗しました。');
                }

                const data = await response.json();

                if (data.status === 'success' && data.review) {
                    addReviewToDom(data.review);
                    reviewForm.reset();
                    reviewModal?.hide();
                    showToast('口コミが投稿されました！');
                } else {
                    throw new Error(data.message || '口コミの投稿に失敗しました。');
                }
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : '不明なエラーが発生しました。';
                showToast(errorMessage, true);
            }
        });
    }
});
