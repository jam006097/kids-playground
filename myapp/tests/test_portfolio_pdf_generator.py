import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from myapp.utils.portfolio_pdf_generator import BrowserOperator, PdfComposer


def test_browser_operator_initialization():
    """初期化時に属性が None であること"""
    operator = BrowserOperator()
    assert operator.browser is None
    assert operator.page is None


@patch("myapp.utils.portfolio_pdf_generator.sync_playwright")
def test_browser_operator_start_should_launch_browser(mock_playwright):
    """start メソッドを呼ぶとブラウザが起動すること"""
    mock_p = mock_playwright.return_value.start.return_value
    mock_browser = mock_p.chromium.launch.return_value

    operator = BrowserOperator()
    operator.start()

    assert mock_p.chromium.launch.called
    assert operator.browser == mock_browser


@patch("myapp.utils.portfolio_pdf_generator.sync_playwright")
def test_browser_operator_save_page_as_pdf_should_call_pdf_method(mock_playwright):
    """save_page_as_pdf が PDF 保存メソッドを呼ぶこと"""
    mock_p = mock_playwright.return_value.start.return_value
    mock_browser = mock_p.chromium.launch.return_value
    mock_context = mock_browser.new_context.return_value
    mock_page = mock_context.new_page.return_value

    operator = BrowserOperator()
    url = "http://localhost:8000"
    output_path = "output.pdf"

    operator.save_page_as_pdf(url, output_path)

    mock_page.goto.assert_called_with(url)
    mock_page.pdf.assert_called_with(path=output_path, format="A4")


def test_pdf_composer_merge_should_call_pypdf_writer():
    """merge メソッドが PdfWriter を正しく呼ぶこと"""
    with patch(
        "myapp.utils.portfolio_pdf_generator.PdfWriter"
    ) as mock_writer_class, patch(
        "myapp.utils.portfolio_pdf_generator.Path.exists", return_value=True
    ):
        mock_writer = mock_writer_class.return_value
        composer = PdfComposer()

        inputs = ["file1.pdf", "file2.pdf"]
        output = "merged.pdf"

        composer.merge(inputs, output)

        assert mock_writer.append.call_count == 2
        mock_writer.write.assert_called_with(output)
