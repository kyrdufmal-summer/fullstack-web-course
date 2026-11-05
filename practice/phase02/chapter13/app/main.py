
# 서버에서 발생한 일을 기록하는 Python 도구
import logging

# FastAPI 서버를 만드는 도구
from fastapi import FastAPI

# 회원 관련 API 주소를 관리하는 Router
from app.routers.member_router import router as member_router


# 서버 로그에 기록할 정보와 출력 형식 설정
logging.basicConfig(
    # INFO 이상의 로그를 출력
    level=logging.INFO,

    # 발생 시간 / 심각도 / 발생 위치 / 메시지
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)


# FastAPI 애플리케이션 생성
# Uvicorn과 TestClient가 이 객체를 사용해요.
app = FastAPI(title="Chapter 13 Exception Logging Test")


# 회원 API를 서버에 등록
# GET /members, POST /members 등 등록된 경로를 연결해요.
app.include_router(member_router)
