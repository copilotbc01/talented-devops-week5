FROM python:3.12-alpine AS build
WORKDIR /build
COPY app.py .
RUN python -m py_compile app.py

FROM python:3.12-alpine AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080
WORKDIR /app
RUN apk upgrade --no-cache && addgroup -g 10001 app && adduser -D -H -u 10001 -G app app
COPY --from=build --chown=app:app /build/app.py /app/app.py
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=2)"]
CMD ["python", "app.py"]
