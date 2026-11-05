# FastAPI API를 자동으로 호출하는 테스트 도구
from fastapi.testclient import TestClient

# 우리가 만든 FastAPI 앱 가져오기
from app.main import app


# 실제 HTTP 서버를 띄우지 않고 API를 호출하는 테스트 클라이언트
client = TestClient(app)


# 회원 목록 GET API의 정상 응답 검사
def test_get_members_returns_200():

    # GET /members 요청을 자동 실행
    response = client.get("/members")

    # HTTP 응답이 200인지 검사
    assert response.status_code == 200

    # 반환된 데이터가 회원 목록(JSON 배열)인지 확인
    assert isinstance(response.json(), list)



# 존재하지 않는 회원을 요청했을 때 404를 반환하는지 검사
def test_get_unknown_member_returns_404():

    # 존재하지 않는 회원번호로 상세 조회 요청
    response = client.get("/members/999999")

    # 회원이 없으므로 404가 반환되어야 해요.
    assert response.status_code == 404

    # 오류 메시지도 API 계약과 일치해야 해요.
    assert response.json()["detail"] == "Member not found"    

# 매번 중복되지 않는 테스트 이메일을 만드는 도구
from uuid import uuid4


# 정상 회원가입 시 HTTP 201을 반환하는지 검사
def test_create_member_returns_201():

    # 테스트마다 새로운 이메일을 생성
    email = f"test-{uuid4()}@example.com"

    # 고객처럼 회원가입 API 호출
    response = client.post(
        "/members",
        json={
            "name": "Test User",
            "email": email,
            "age": 30,
        },
    )

    # 회원가입 성공 상태코드 검사
    assert response.status_code == 201

    # 서버에서 반환한 회원정보 확인
    body = response.json()

    # 이름이 정확한지 검사
    assert body["name"] == "Test User"

    # 이메일이 정확한지 검사
    assert body["email"] == email    


    # 중복 이메일 회원가입은 409를 반환하는지 검사
def test_duplicate_email_returns_409():

    # 이번 테스트만 사용할 고유 이메일 생성
    email = f"duplicate-{uuid4()}@example.com"

    # 첫 번째 회원가입 요청
    first = client.post(
        "/members",
        json={
            "name": "First",
            "email": email,
            "age": 30,
        },
    )

    # 최초 가입은 성공해야 해요.
    assert first.status_code == 201

    # 동일 이메일로 두 번째 회원가입 요청
    second = client.post(
        "/members",
        json={
            "name": "Second",
            "email": email,
            "age": 31,
        },
    )

    # 이미 존재하는 이메일이므로 409여야 해요.
    assert second.status_code == 409

    # API 오류 메시지도 확인해요.
    assert second.json()["detail"] == "Email already exists"


    # 회원번호에 문자가 들어오면 422인지 검사하는 테스트
def test_member_id_validation_returns_422():

    # 회원번호는 숫자여야 하는데 문자를 전달
    response = client.get("/members/not-a-number")

    # FastAPI가 잘못된 입력으로 판단했는지 확인
    assert response.status_code == 422