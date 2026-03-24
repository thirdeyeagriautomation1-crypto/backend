import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

def replace_none(obj):
    if isinstance(obj, dict):
        return {k: replace_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_none(i) for i in obj]
    elif obj is None:
        return ""
    return obj

class SanitizeNullMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Only sanitize JSON responses
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            # Read original body
            body = b"".join([chunk async for chunk in response.body_iterator])
            try:
                data = json.loads(body)
                sanitized = replace_none(data)
                new_body = json.dumps(sanitized).encode("utf-8")

                # Reconstruct the response with correct Content-Length
                return Response(
                    content=new_body,
                    status_code=response.status_code,
                    headers={k: v for k, v in response.headers.items() if k.lower() != "content-length"},
                    media_type="application/json"
                )
            except Exception:
                # Fallback to original response if JSON parsing fails
                return response

        return response
