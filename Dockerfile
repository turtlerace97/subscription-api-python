# 베이스 이미지
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /code

# 의존성 파일 복사
COPY ./requirements.txt /code/requirements.txt

# 의존성 설치
RUN pip install --no-cache-dir -r /code/requirements.txt

# 앱 파일 복사
COPY ./app /code/app

# Gunicorn을 사용하여 애플리케이션 실행
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8181"]