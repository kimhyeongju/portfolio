# 경량 Python 이미지
FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 최소화 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# 비루트 사용자 생성 (보안)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000


# 실행
CMD ["python", "app.py"]