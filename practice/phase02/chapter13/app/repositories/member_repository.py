# SQLAlchemy에서 SELECT(조회) 기능을 가져와요.
from sqlalchemy import select

# DB 작업을 관리하는 Session 타입
from sqlalchemy.orm import Session

# members 테이블과 연결된 Python 모델
from app.models import Member

# 회원 전체 수정(PUT), 일부 수정(PATCH) 데이터 검사
from app.schemas import MemberUpdate, MemberPatch


# 회원 전체 조회 함수
def find_all(db: Session):

    # members 테이블의 회원을 번호순으로 조회
    stmt = select(Member).order_by(Member.member_id)

    # SQL을 실행하고 조회 결과를 리스트로 반환
    return db.scalars(stmt).all()


# 회원 한 명 조회 함수
def find_by_id(db: Session, member_id: int):

    # 회원번호(PK)로 회원 한 명 조회
    # 존재하지 않으면 None 반환
    return db.get(Member, member_id)


    # 회원 정보를 DB에 등록하는 함수
def create_member(db: Session, name: str, email: str, age: int):

    # 전달받은 회원 정보로 Python 객체 생성
    member = Member(name=name, email=email, age=age)

    try:
        # 새 회원 객체를 Session에 등록
        db.add(member)

        # DB에 INSERT하고 변경 사항 확정
        db.commit()

        # DB에서 생성된 회원번호 등 값을 다시 읽어옴
        db.refresh(member)

        # 등록된 회원 정보 반환
        return member

    except Exception:
        # 오류 발생 시 아직 확정되지 않은 DB 작업 취소
        db.rollback()

        # 오류를 상위 계층에 전달
        raise

# 이메일이 이미 등록되어 있는지 DB에서 조회하는 함수
def find_by_email(db: Session, email: str):

    # members 테이블에서 같은 이메일을 찾는다.
    stmt = select(Member).where(Member.email == email)

    # 회원이 있으면 Member 객체, 없으면 None 반환
    return db.scalar(stmt)

# 회원 정보를 수정하는 함수
def update_member(db: Session, member: Member, payload: MemberUpdate):

    # 회원 이름을 새로운 값으로 변경해요.
    member.name = payload.name

    # 이메일을 새로운 값으로 변경해요.
    member.email = str(payload.email)

    # 나이를 새로운 값으로 변경해요.
    member.age = payload.age

    try:
        # 수정된 내용을 DB에 반영하고 확정해요.
        db.commit()

        # DB에 확정된 값을 다시 Python 객체에 읽어와요.
        db.refresh(member)

        # 수정된 회원 정보를 반환해요.
        return member

    except Exception:
        # 오류가 발생하면 확정되지 않은 DB 작업을 취소해요.
        db.rollback()

        # 어떤 오류가 발생했는지 상위 코드에 알려줘요.
        raise    

    # 회원정보 중 전달된 항목만 수정하는 함수
def patch_member(db: Session, member: Member, payload: MemberPatch):

    # 고객이 실제로 보낸 항목만 추출
    # 예: {"age": 31}
    changes = payload.model_dump(exclude_unset=True)

    # 수정할 항목을 하나씩 확인
    for field, value in changes.items():

        # 이메일은 문자열로 변환
        if field == "email":
            value = str(value)

        # 회원 객체의 해당 항목만 변경
        setattr(member, field, value)

    try:
        # 변경 내용을 DB에 확정
        db.commit()

        # DB의 최신 값을 다시 가져오기
        db.refresh(member)

        # 수정된 회원정보 반환
        return member

    except Exception:
        # 오류 발생 시 미확정 변경 취소
        db.rollback()

        # 오류를 상위 계층에 전달
        raise

    # DB에서 회원을 삭제하는 함수
def delete_member(db: Session, member: Member):

    # DB 작업 중 오류가 발생할 수 있으므로 예외 처리
    try:
        # 삭제할 회원 객체를 Session에 등록
        db.delete(member)

        # DB에 DELETE를 실행하고 삭제 확정
        db.commit()

    # 삭제 작업 중 오류가 발생하면
    except Exception:

        # 현재 트랜잭션의 미확정 변경을 취소
        db.rollback()

        # 오류를 Service 등 상위 계층에 전달
        raise