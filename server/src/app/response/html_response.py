from fastapi.responses import HTMLResponse as BaseHTMLResponse
import htmlmin


class HTMLResponse(BaseHTMLResponse):
    def render(self, content: str) -> bytes:
        return htmlmin.minify(
            content,
            remove_empty_space=True,
            remove_comments=True
        ).encode('utf-8')
