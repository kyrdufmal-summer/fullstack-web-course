
# DB 작업용 Session 타입
from sqlalchemy.orm import Session

# HTTP 오류를 응답하는 FastAPI 도구
from fastapi import HTTPException

# 회원가입 요청 데이터 검사 모델
from app.schemas import MemberCreate

# 실제 DB 조회·저장을 담당하는 Repository
from app.repositories import member_repository

# Python 로그 기록 도구
import logging

# 이 파일 전용 Logger
logger = logging.getLogger(__name__)


# 회원가입 업무 규칙 담당
def create_member_service(db: Session, payload: MemberCreate):

    # Repository를 통해 DB에서 같은 이메일을 찾음
    existing = member_repository.find_by_email(
        db, str(payload.email)
    )

    # 같은 이메일이 이미 존재할 때만 가입 거절
    if existing is not None:

        # 개인정보 없이 중복 요청 발생 사실만 기록
        logger.warning("duplicate member registration attempted")

        # 중복이므로 409 Conflict 응답
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    # 중복이 없을 때만 새 회원 저장
    return member_repository.create_member(
        db,
        payload.name,
        str(payload.email),
        payload.age,
    )


# 회원 삭제 업무 담당
def delete_member_service(db: Session, member_id: int):

    # Repository를 통해 기존 회원 조회
    member = member_repository.find_by_id(db, member_id)

    # 회원이 없으면 삭제 불가능
    if member is None:

        # 없는 회원이라는 사실을 기록
        logger.warning("member not found: member_id=%s", member_id)

        # 404 Not Found 반환
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    # 회원이 존재하면 DB 삭제 요청
    member_repository.delete_member(db, member)


# 회원 전체 조회 업무 담당
def get_members_service(db: Session):

    # Repository에서 회원 목록 조회
    members = member_repository.find_all(db)

    # 조회 결과를 Router에 반환
    return members

# 회원 한 명을 조회하는 업무 함수
def get_member_service(db: Session, member_id: int):

    # Repository에 회원번호로 조회 요청
    member = member_repository.find_by_id(db, member_id)

    # 해당 회원이 존재하지 않으면
    if member is None:

        # 운영 로그에 조회 실패를 기록
        logger.warning("member not found: member_id=%s", member_id)

        # API 계약에 맞는 404 반환
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    # 회원이 존재하면 조회 결과 반환
    return member