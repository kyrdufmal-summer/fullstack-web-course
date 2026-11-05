# TIL | 2026-11-05 | SQLAlchemy ORM CRUD · 예외 처리 · Logging · TestClient

> 학습 범위: Chapter 12 복습과 Chapter 13 실습 · Windows / VS Code / PowerShell / Python 가상환경 / FastAPI / SQLAlchemy / PostgreSQL 18.4 / DBeaver / pytest 9.2.0
> 이 문서는 당일 대화와 화면에서 확인한 실행 결과를 바탕으로 작성했다. 확인하지 않은 동작은 완료로 표시하지 않는다.

## 1. 오늘의 결론

- Chapter 13 회원 API의 **GET 200, GET 404, POST 201, 중복 이메일 POST 409, 잘못된 회원번호 GET 422** 테스트가 전부 통과했다 (**5 passed, 1 warning**).
- 중복 가입에 대한 **WARNING 로그**가 실제 출력됐고, **chapter13_test.public.members**에서 테스트 데이터 8건을 조회했다.
- 과제 소스는 **kyrdufmal-summer/fullstack-web-course** 저장소의 **main** 브랜치에 커밋 및 푸시했다. 확인된 과제 커밋: **808d529**.
- 학습의 중심은 문법 암기가 아니라 **정상 흐름이 깨지는 지점, 증거의 의미, 실제 운영 사고 및 재발 방지**를 구분하는 것이다.

## 2. 왜 이 실습을 했는가? (문제 정의)

Chapter 12에서 SQLAlchemy ORM을 통해 회원 CRUD를 구현했지만, 'API가 동작한다'는 사실만으로 운영 안정성을 보장할 수는 없다. 회원이 없을 때 404를 반환하는지, 중복 이메일을 409로 거절하는지, 잘못된 입력을 422로 차단하는지, 문제가 발생했을 때 추적할 로그가 남는지, 수정 후 동일한 검사를 반복할 수 있는지를 확인할 필요가 있었다.

비즈니스 이해관계자는 신규 가입 고객, 고객센터, 개발자, 운영 담당자, 데이터 분석 담당자다. 오류 코드가 틀리면 고객에게 잘못된 안내가 전달되고, 가입 전환율·VOC·장애 통계도 왜곡될 수 있다.

## 3. 전체 호출 흐름과 파일별 책임

```text
pytest (tests/test_members.py: 테스트 발견·실행)
  └─ TestClient: client.get() / client.post()
       └─ FastAPI app (app/main.py: 앱 생성·라우터 등록)
            └─ Router (app/routers/member_router.py: 경로와 HTTP 계약)
                 ├─ Pydantic Schema (app/schemas.py: 요청 형식 검증)
                 ├─ Depends(get_db) (app/db.py: 요청용 Session 제공)
                 └─ Service (app/services/member_service.py: 업무 규칙·오류 판단)
                      └─ Repository (app/repositories/member_repository.py: DB 조회·저장)
                           └─ SQLAlchemy ORM Model / Session
                                └─ PostgreSQL chapter13_test.public.members
    ← 응답 상태 및 JSON ← pytest assert 비교 → PASS / FAIL
```

- **main.py:** 앱이 처음 import될 때 FastAPI 객체와 Router를 등록한다. 요청마다 main.py가 재실행되는 구조가 아니다.
- **Schema / MemberCreate:** 입력값만으로 판단 가능한 이메일 형식·필수값·자료형을 검사한다. FastAPI 기본 요청 검증 실패는 422다.
- **Service:** '이미 가입된 이메일은 거절한다'처럼 회사 정책에 해당하는 결정을 내린다. 데이터의 존재 여부 자체는 Repository에 조회시킨다.
- **Repository:** 실제 DB 조회 및 INSERT 등 SQLAlchemy 작업을 수행한다.
- **db.py:** Engine, SessionLocal, get_db로 연결 및 세션 사용을 지원한다. Session은 단순히 DB 주소가 아니라 ORM 상태와 트랜잭션을 관리한다.
- **models.py:** Python Member 객체와 PostgreSQL members 테이블을 매핑한다.
- **test_members.py:** 고객처럼 API 요청을 보내고 기대한 상태코드와 응답 내용을 assert로 자동 검사한다.

### Chapter 12 복습: ORM의 핵심

| SQL 의미 | SQLAlchemy 표현 | 오해하기 쉬운 점 |
|---|---|---|
| INSERT | Member(...) + session.add() | add()만으로 영구 저장이 확정되지는 않는다 |
| SELECT | select(Member), session.get() | 필터 조건이 없으면 의도치 않은 전체 조회가 될 수 있다 |
| UPDATE | 로딩한 객체 속성 변경 | commit 등 트랜잭션 확정이 필요하다 |
| DELETE | session.delete() | 실제 반영·확정 시점을 구별해야 한다 |
| COMMIT | session.commit() | 트랜잭션을 확정한다 |
| ROLLBACK | session.rollback() | 이미 성공적으로 commit된 이전 트랜잭션까지 취소하는 기능은 아니다 |
| REFRESH | session.refresh(member) | DB의 현재 값을 객체에 다시 읽어온다 |

교육용 예제는 Repository 안에서 commit/rollback을 다뤘다. 실제 주문·재고처럼 여러 Repository가 하나의 성공·실패 단위여야 하는 작업에서는 Service/Unit of Work가 같은 Session의 트랜잭션 경계를 관리하는 설계를 고려한다.

## 4. 오늘 실제 수행한 작업 순서

### 4-1. Chapter 13 프로젝트 구조

Chapter 12의 app 구조를 Chapter 13에 복사한 뒤, 잘못 중첩된 폴더를 고쳤다. tests 폴더도 처음에는 app 아래에 만들었으나, 최종적으로 app과 동등한 위치로 이동했다.

```text
practice/phase02/chapter13/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/member_router.py
│   ├── services/member_service.py
│   └── repositories/member_repository.py
└── tests/test_members.py
```

__init__.py는 빈 파일이어도 일반 Python 패키지임을 명시한다. 최신 Python에서는 없어도 namespace package로 import될 수 있다. 이 파일이 사용자 소속이나 인증을 검사하는 것은 아니다.

### 4-2. Import 오류 수정

- 테스트 실행 초기에는 **No module named pytest**가 발생해 가상환경에 pytest/httpx를 준비했다. 확인된 버전: **pytest 9.2.0**.
- 그다음 **cannot import name 'app' from 'app.main'**이 발생했다. main.py에 Logging 설정만 있고 FastAPI 앱 객체가 없어서 **app = FastAPI(...)** 및 **app.include_router(member_router)**를 추가했다.
- 이어서 Router의 **NameError: name 'Session' is not defined**가 발생했고 **from sqlalchemy.orm import Session**을 추가했다.
- 이후 터미널에서 **APP IMPORT OK**를 확인했다. 단, 이 출력은 import 성공이지 DB CRUD 전체 성공 증거가 아니다.
- **python -m py_compile app/services/member_service.py** 문법 검사는 통과했다. 문법 검사만으로 업무 조건의 논리 오류를 잡을 수는 없다.

### 4-3. 404 오류의 서로 다른 원인 발견

처음 없는 회원 GET 테스트는 HTTP 상태가 404였으나 JSON detail은 **Not Found**였다. 테스트가 기대한 **Member not found**와 달라 FAIL이었다. 이때에는 상세 조회 Router 자체가 빠진 상태였다. GET /members/{member_id} Router와 Service의 find_by_id/HTTPException(404)를 연결한 뒤 PASS가 됐다.

**교훈:** '404가 나왔으니 기능이 정상'이라고 결론 내리면 안 된다. 라우트가 존재하지 않아서 나온 404와, 라우트를 통과해 DB에서 회원을 찾지 못해 나온 404를 구분해야 한다.

### 4-4. HTTP 계약과 로깅

- 신규 회원 정상 생성: **201 Created** (POST Router에 status_code=201 명시).
- 기존 회원이 없는 상세 조회: **404 Not Found**.
- 중복 이메일: Service 사전 조회 후 **409 Conflict** 및 WARNING 로그.
- 정수가 아닌 member_id: 경로 자료형 검증에 의해 **422**.
- Service에서 logger = logging.getLogger(__name__)을 사용하고, 중복 가입 시 logger.warning('duplicate member registration attempted')를 남겼다.
- 개인정보인 이메일 원문·비밀번호·토큰을 로그에 직접 남기지 않는 원칙을 확인했다.

### 4-5. PostgreSQL 테스트 DB 분리

기존 데이터베이스 **postgres**의 public.members를 그대로 사용하면 반복 POST/DELETE 테스트가 기존 회원 데이터에 영향을 줄 수 있었다. DBeaver에서 CREATE DATABASE chapter13_test를 실행하고 pg_database 조회로 DB의 존재를 확인했다. 별도 DBeaver 연결을 만들어 **chapter13_test**에 연결 성공한 뒤, public.members가 처음에는 존재하지 않음(NULL)을 확인했다.

테스트 DB에 회원번호 자동 증가 PK, 이름, UNIQUE 이메일, 나이 컬럼을 갖는 public.members 테이블을 생성했다. Chapter 13 db.py의 접속 대상 이름을 임시로 chapter13_test로 지정하고 엔진 URL에 대해 **CONNECTED DB: chapter13_test**를 확인했다. 이는 URL 설정 확인이며 실제 DB 읽기/쓰기 증명과는 다르다. 이후 pytest POST와 DBeaver 조회로 실제 동작을 별도 확인했다.

주의: DBeaver 연결을 바꿔도 FastAPI 연결은 자동으로 바뀌지 않는다. 테스트용 DB를 만들었다는 사실만으로 데이터 격리가 성립하는 것이 아니라, 실행 프로세스의 DATABASE_URL과 권한을 확인해야 한다.

### 4-6. pytest 테스트 및 로그 검증

실행 명령:

```powershell
python -m pytest tests/test_members.py -v
python -m pytest tests/test_members.py -v --log-cli-level=WARNING
```

| 테스트 함수 | 확인 사항 | 실제 결과 |
|---|---|---|
| test_get_members_returns_200 | 목록 조회가 200 및 JSON list를 반환 | PASS |
| test_get_unknown_member_returns_404 | 없는 회원 요청 시 404와 정확한 오류 문구 | PASS |
| test_create_member_returns_201 | 고유한 이메일로 생성 시 201 | PASS |
| test_duplicate_email_returns_409 | 같은 이메일을 순차적으로 두 번 가입하면 두 번째가 409 | PASS |
| test_member_id_validation_returns_422 | 숫자가 아닌 회원번호를 입력하면 422 | PASS |

**터미널 실증:** 최종 **5 passed, 1 warning**. WARNING 로그는 **app.services.member_service:member_service.py:33 duplicate member registration attempted**로 확인했다.

**경고 구분:** Starlette TestClient 사용 경로와 관련된 StarletteDeprecationWarning은 테스트 실패가 아니다. 추후 의존성 버전/호환성을 점검할 사항이다.

### 4-7. DBeaver 데이터 증거

새 연결 **public@chapter13_test**에서 public.members를 SELECT했다. 최종 캡처에서 **8 rows fetched**가 확인되었으며 Test User 및 First 계정들이 존재했다. 이메일에 UUID가 포함되어 반복 실행 간 충돌을 줄인 흔적도 확인했다.

**중요:** uuid4()는 이메일 식별값을 매번 바꾸지만 테스트 회원을 자동 삭제하지 않는다. 8건이 누적된 것은 테스트 데이터 정리가 아직 설계되지 않았음을 보여 준다. 동일 이메일의 행 수가 정확히 1건인지 별도 집계 SQL까지 검증한 것은 아니다.

## 5. Swagger · pytest · Logging · DB의 차이

| 수단 | 누가/무엇을 실행하나? | 답할 수 있는 질문 | 답하지 못하는 질문 |
|---|---|---|---|
| Swagger UI | 개발자가 브라우저에서 직접 Execute | 지금 이 API의 응답이 어떻게 보이나? | 변경될 때마다 모든 경로가 자동 재검증되나? |
| pytest + TestClient | Python 테스트 코드가 ASGI 앱을 직접 호출하고 assert 검사 | 정의한 계약이 반복 실행 시 유지되나? | 테스트하지 않은 사고까지 모두 안전한가? |
| Logging | 앱이 처리 과정에서 이벤트 기록 | 어떤 코드 위치에서 어떤 경로가 실행됐나? | DB의 모든 결과가 정확하다는 확정 증거인가? |
| DBeaver / SQL | 권한 있는 개발자가 DB 데이터 조회 | 실제 어떤 행이 존재하나? | 프론트엔드의 응답이 올바른가? |

Swagger는 API 시험용 웹 UI이지 실제 쇼핑몰 고객용 프론트엔드가 아니다. TestClient는 별도 Uvicorn 서버 없이 앱을 직접 호출할 수 있으며, 두 방법 모두 잘못 설정하면 동일한 기존 DB를 건드릴 수 있다.

## 6. 비정상 흐름 / 운영 사고 / 예방 설계

| 비정상 패턴 | 발생 조건 | 고객·운영 피해 | 예방 및 검증 |
|---|---|---|---|
| 정상 회원가입인데 409 | if문 바깥에 raise를 잘못 들여쓰기 | 가입 실패, 전환율 하락, VOC 증가 | 신규 201과 중복 409를 반드시 함께 검사 |
| Router가 없는데 404 | 상세 API 미등록 | DB 자원 없음과 경로 없음의 원인 혼동 | 응답 detail 및 경로 등록까지 검증 |
| 중복 이메일 동시 가입 | 두 요청이 사전 중복 조회를 모두 통과 | 중복 계정 또는 처리되지 않은 DB 오류 | DB UNIQUE + IntegrityError의 제약조건별 처리 + 동시성 테스트 |
| 테스트는 PASS지만 DB 오염 | DATABASE_URL이 기존 DB를 가리킴 | 테스트 계정 누적, 통계 왜곡, 삭제 위험 | 실행 시 DB 이름 검증, 테스트 계정 분리/전용 권한 |
| UUID 기반 테스트 데이터 증가 | 테스트가 INSERT 후 정리하지 않음 | DB 용량 증가, 테스트 결과 혼란 | fixture·DB 초기화·정리 절차 도입 |
| 500을 200 JSON으로 숨김 | except Exception으로 오류 문자열만 return | 화면 성공 오인, 운영 알림 누락 | HTTP 상태 계약 테스트, 예외별 처리 |
| commit 이후 응답 유실 | DB 저장은 확정됐으나 네트워크 응답 실패 | 고객 재시도로 중복 업무 가능 | 멱등키, 결과 재조회, 재시도 정책 |
| PASS하지만 잘못된 데이터 반환 | 200과 list 자료형만 확인 | 타 회원 정보 노출 등 심각한 오류를 놓침 | 응답 내용·인가·데이터 격리 assert 추가 |

관찰된 사고와 가정 시나리오를 혼동하지 말 것: 이 표의 여러 사고는 **실제 발생한 사고가 아니라 실무 검증용 가설**이다.

## 7. GitHub 과제 제출 결과

- 저장소: https://github.com/kyrdufmal-summer/fullstack-web-course
- 제출 경로: practice/phase02/chapter13/
- 브랜치: main
- 커밋: **808d529**
- 커밋 메시지: **feat: chapter13 exception logging and pytest tests**
- Push 결과: 원격 main 업데이트 성공 (스크린샷 확인).
- 주의: 해당 커밋에 Chapter 13 소스 9개 외에 **practice/phase02/chapter06/main.py**도 포함됐다. 과제 제출 범위의 잔여 정리 사항으로 남긴다.
- Git 커밋 시 .pyc, __pycache__, .env 등의 자동 생성 파일 및 비밀정보는 제외하도록 스테이징 대상을 정리했다.

커밋 링크: https://github.com/kyrdufmal-summer/fullstack-web-course/commit/808d529

## 8. 미완료·추가 검증 항목

- 실제 테스트 격리: db.py의 DB 이름을 하드코딩한 교육용 임시 구성을 .env.test 또는 명시적인 테스트용 설정/fixture로 분리할 것.
- DB 제약조건으로 인한 IntegrityError를 이메일 UNIQUE 위반에 한해 409로 바꾸는지, 동시 요청에서 재현·검증할 것.
- 테스트 실행 후 데이터 정리, 각 테스트 간 독립성, 타 테스트 순서의 영향을 검증할 것.
- PUT / PATCH / DELETE 및 PATCH의 필드 생략과 explicit null의 계약에 대한 회귀 테스트를 추가할 것.
- 인증/인가를 도입할 경우 타 회원 데이터 조회 차단 및 개인정보 로그 마스킹 검사를 추가할 것.
- 단순 import와 테스트 PASS만이 아니라 HTTP 응답, 로그, DB 행, 테스트 결과를 함께 Evidence로 남길 것.

## 9. 오늘의 핵심 학습 문장

**코드가 실행된다 ≠ 업무가 정확하다 ≠ 운영이 안전하다.**

정상 처리의 흐름을 추적한 다음, 경로 누락·논리적 들여쓰기 실수·DB 연결 대상 오류·동시 가입·재시도·부분 성공 같은 **비정상 흐름**을 먼저 상상해야 한다. 이후 HTTP 상태, 로그, DB 상태, 자동 테스트를 서로 다른 증거로 교차 검증하는 것이 실제 회사의 운영 품질 관리에 더 가깝다.

---

보안 확인: API 키, 토큰, Webhook URL, DB 비밀번호, .env 값 등은 이 문서에 포함하지 않았다. 향후 추가 시 반드시 `***`로 마스킹한다.
