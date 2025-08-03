class ReviewManager {
    constructor() {
        this.initReviewHandlers();
    }

    initReviewHandlers() {
        // モーダルが開かれるときに施設情報を設定
        $('#reviewModal').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget);
            var playgroundId = button.data('playground-id');
            var playgroundName = button.data('playground-name');
            var modal = $(this);
            modal.find('#playgroundId').val(playgroundId);
            modal.find('.modal-title').text(playgroundName + 'への口コミ');
        });

        // 口コミフォームの送信処理
        $('#reviewForm').on('submit', function (event) {
            event.preventDefault();
            var formData = $(this).serialize();
            var playgroundId = $('#playgroundId').val();
            $.ajax({
                url: `/playground/${playgroundId}/add_review/`,
                method: 'POST',
                data: formData,
                success: function (response) {
                    alert(response.message);
                    $('#reviewModal').modal('hide');
                },
                error: function (xhr) {
                    alert('口コミの投稿に失敗しました。');
                }
            });
        });
    }
}

export { ReviewManager };