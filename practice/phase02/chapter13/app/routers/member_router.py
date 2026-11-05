# API 주소를 등록하는 FastAPI 도구
from fastapi import APIRouter, Depends

# DB Session의 타입
# 회원가입 요청과 회원정보 응답 형식
from app.schemas import MemberCreate, MemberResponse

# 요청마다 DB Session을 제공하는 함수
from app.db import get_db

# 회원 응답 형식을 정의한 Schema
from app.schemas import MemberResponse

# 회원조회 업무를 처리하는 Service
from app.services import member_service
# DB 작업용 SQLAlchemy Session 타입을 가져와요.
from sqlalchemy.orm import Session


# 회원 관련 API 주소를 관리하는 Router
router = APIRouter(prefix="/members", tags=["Members"])


# GET /members 요청을 처리하는 함수
@router.get("", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):

    # Service에 회원 전체 조회를 요청
    return member_service.get_members_service(db)

# POST /members 요청을 접수하는 API
# 회원가입 성공 시 201 응답하도록 지정
@router.post(
    "",
    response_model=MemberResponse,
    status_code=201
)
def create_member(
    # 고객이 보낸 회원정보를 Pydantic이 검사
    payload: MemberCreate,

    # 요청 처리에 사용할 DB Session을 주입
    db: Session = Depends(get_db)
):
    # Service에 회원가입 업무 처리를 요청
    return member_service.create_member_service(db, payload)


# GET /members/{member_id} 요청을 처리하는 API
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    # URL에서 회원번호를 정수로 받음
    member_id: int,

    # DB 조회에 사용할 Session 가져오기
    db: Session = Depends(get_db)
):
    # Service에서 회원 존재 여부를 확인하고 결과 반환
    return member_service.get_member_service(db, member_id)    