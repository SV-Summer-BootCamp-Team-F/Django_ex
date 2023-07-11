# 베이스 이미지 선택
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /django_ex

RUN apt-get update
RUN apt-get install -y python3 pip

# 필요한 파일 복사
COPY requirements.txt .
COPY . .

# 필요한 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 환경 변수 설정
ENV DJANGO_SECRET_KEY secret_value

EXPOSE 8000

# 컨테이너 실행 시 실행할 명령 설정
CMD python3 manage.py runserver 0.0.0.0:8000
