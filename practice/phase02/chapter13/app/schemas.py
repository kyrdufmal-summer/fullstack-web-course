
# Pydantic: API로 들어온 데이터를 검사하는 도구
from pydantic import BaseModel, EmailStr, ConfigDict


# ① 회원가입 요청 데이터 검사
class MemberCreate(BaseModel):

    # 회원 이름은 문자열
    name: str

    # 이메일 형식 검사
    email: EmailStr

    # 나이는 정수
    age: int


# ② 회원정보 전체 수정(PUT) 요청 데이터 검사
class MemberUpdate(BaseModel):

    # PUT에서는 이름을 반드시 전달
    name: str

    # PUT에서는 이메일도 반드시 전달
    email: EmailStr

    # PUT에서는 나이도 반드시 전달
    age: int


# ③ 회원정보를 고객에게 반환할 때 사용하는 형식
class MemberResponse(BaseModel):

    # DB에서 생성한 회원번호
    member_id: int

    # 회원 이름
    name: str

    # 회원 이메일
    email: EmailStr

    # 회원 나이
    age: int

    # SQLAlchemy ORM 객체를 응답 데이터로 변환할 수 있도록 설정
    model_config = ConfigDict(from_attributes=True)
# PATCH 요청에서 null을 검사하는 도구
from pydantic import model_validator


# 회원정보 일부 수정 요청을 검사하는 클래스
class MemberPatch(BaseModel):

    # 이름은 생략 가능
    name: str | None = None

    # 이메일은 생략 가능
    email: EmailStr | None = None

    # 나이는 생략 가능
    age: int | None = None

    # 사용자가 명시적으로 null을 보냈는지 검사
    @model_validator(mode="before")
    @classmethod
    def reject_null(cls, data):

        # 요청이 딕셔너리 형태인지 확인
        if isinstance(data, dict):

            # 수정 가능한 항목을 하나씩 검사
            for field in ("name", "email", "age"):

                # 필드는 존재하지만 값이 null이면 오류 발생
                if field in data and data[field] is None:
                    raise ValueError(f"{field} cannot be null")

        # 문제가 없는 요청 데이터 반환
        return data