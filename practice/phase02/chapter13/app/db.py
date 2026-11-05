import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print(DB_HOST, DB_PORT, DB_NAME, DB_USER)


import psycopg
def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

def check_connection():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT current_database(), current_schema();"
            )
            return cur.fetchone()
def fetch_members():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, email FROM public.members ORDER BY id;"
            )
            return cur.fetchall()            


# SQLAlchemy ORM 모델의 공통 부모 클래스 가져오기
from sqlalchemy.orm import DeclarativeBase

# Member 등 ORM 모델이 상속받을 부모 클래스
class Base(DeclarativeBase):
    pass

# SQLAlchemy DB 연결 관리자
from sqlalchemy import create_engine

# ORM 작업 공간(Session)을 만드는 도구
from sqlalchemy.orm import sessionmaker

# 환경변수로 PostgreSQL 접속 주소 생성
from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",  # PostgreSQL 드라이버
    username=DB_USER,                # DB 사용자
    password=DB_PASSWORD,            # DB 비밀번호
    host=DB_HOST,                    # DB 서버 주소
    port=int(DB_PORT),               # DB 포트
    database="chapter13_test"        # DB 이름
)

# DB 연결 관리 객체 생성
engine = create_engine(DATABASE_URL, echo=True)

# Session 생성기 설정
SessionLocal = sessionmaker(
    bind=engine,       # 위에서 만든 Engine 사용
    autoflush=False,   # 자동 flush 비활성화
    autocommit=False   # 자동 commit 비활성화
)

# FastAPI 요청마다 DB 작업용 Session을 제공하는 함수
def get_db():
    # 새로운 Session을 생성해요.
    db = SessionLocal()

    try:
        # Router에서 이 Session을 사용하도록 전달해요.
        yield db

    finally:
        # 요청이 끝나면 Session을 닫아 자원을 정리해요.
        db.close()