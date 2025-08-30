from django.views import View
from django.http import JsonResponse, HttpRequest, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from myapp.models import Playground, Review
from myapp.clients.ai_summary_client import call_summary_api
import logging

logger = logging.getLogger(__name__)


class SummarizeReviewsView(View):
    """AIによる口コミ要約を提供するビュー"""

    def get(self, request: HttpRequest, playground_id: int) -> JsonResponse:
        """GETリクエストを処理し、口コミの要約を返す"""
        try:
            playground = get_object_or_404(Playground, id=playground_id)
            reviews = self._get_reviews(playground)
            self._validate_reviews(reviews)

            combined_text = self._get_combined_text(reviews)
            summary = call_summary_api(combined_text)

            return JsonResponse({"summary": summary})

        except Http404:
            raise
        except ValueError as e:
            logger.warning(f"Validation error for playground {playground_id}: {e}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.exception(
                f"Error summarizing reviews for playground {playground_id}: {e}"
            )
            return JsonResponse(
                {"error": "サーバーでエラーが発生しました。"}, status=500
            )

    def _get_reviews(self, playground: Playground) -> list[Review]:
        """施設に関連する口コミを取得する"""
        return list(playground.reviews.all())

    def _validate_reviews(self, reviews: list[Review]):
        """口コミが要約実行の条件を満たすか検証する"""
        if len(reviews) < 3:
            raise ValueError("口コミが3件未満のため、要約できません。")

        total_length = sum(len(r.content) for r in reviews)
        if total_length < 300:
            raise ValueError("口コミの合計文字数が300文字未満のため、要約できません。")

    def _get_combined_text(self, reviews: list[Review]) -> str:
        """口コミのリストを単一の文字列に結合する"""
        return "\n\n".join([r.content for r in reviews])
