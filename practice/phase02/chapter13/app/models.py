# DB 테이블과 Python 클래스를 연결하는 도구
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# ORM 모델들이 공통으로 상속받을 기본 클래스
class Base(DeclarativeBase):
    pass


# PostgreSQL의 members 테이블을 Python 클래스로 표현
class Member(Base):

    # 연결할 DB 테이블 이름
    __tablename__ = "members"

    # 회원번호: 기본키(PK)
    member_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    # 회원 이름
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # 이메일: 중복 불가
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )

    # 회원 나이
    age: Mapped[int] = mapped_column(Integer, nullable=False)