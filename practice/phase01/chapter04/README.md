# Chapter 04 학습 기록

## 1. 오늘 이해한 CSS 개념

### 1.1 CSS 선택자

| 선택자 | 예시 | 역할 |
|---|---|---|
| 태그 선택자 | `p` | 같은 HTML 태그에 스타일 적용 |
| 클래스 선택자 | `.highlight` | 여러 요소에 동일한 스타일 재사용 |
| 아이디 선택자 | `#goal` | 특정 요소에 스타일 적용 |

### 1.2 CSS 기본 개념

- **HTML**: 웹페이지의 구조와 내용을 담당한다.
- **CSS**: 웹페이지의 색상, 글꼴, 배경 등의 디자인을 담당한다.
- **상속(Inheritance)**: 부모 요소의 일부 CSS 속성이 자식 요소에 전달된다.
- **우선순위(Specificity)**: 여러 CSS 규칙이 충돌할 때 어떤 선언을 적용할지 결정하는 기준이다.

### 1.3 HTML과 CSS 연결

`profile.html`의 `<head>` 영역에 다음 코드를 추가하여 외부 CSS 파일을 연결하였다.

```html
<link rel="stylesheet" href="profile.css">
```

---

## 2. 상속을 확인한 예제

### 적용한 CSS

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f8fafc;
    color: #334155;
}
```

### 학습 내용

- `body`에 기본 글자색을 지정하면 자식 요소가 해당 색상을 상속받을 수 있다.
- 자식 요소에 별도의 글자색이 지정되어 있다면 해당 스타일이 적용된다.
- `font-family` 역시 자식 요소에 상속될 수 있다.

**결론:** 공통 스타일은 부모 요소에 지정하여 반복적인 CSS 작성을 줄일 수 있다.

---

## 3. CSS 우선순위 실험 결과

### 실험 목적

하나의 HTML 요소에 태그, 클래스, 아이디 선택자가 동시에 적용되었을 때 어떤 스타일이 최종 적용되는지 확인한다.

### HTML

```html
<p id="goal" class="highlight">
    목표: Full-stack 개발자가 되기
</p>
```

### CSS

```css
p {
    color: blue;
}

.highlight {
    color: green;
}

#goal {
    color: red;
}
```

### DevTools 검증 결과

| CSS 선택자 | 지정 색상 | 실제 결과 |
|---|---|---|
| `p` | blue | 취소선 표시 |
| `.highlight` | green | 취소선 표시 |
| `#goal` | red | 최종 적용 |

**최종 결과: 빨간색(red)**

### 원인 분석

동일한 요소의 `color` 속성에 여러 규칙이 지정되었으며, ID 선택자의 우선순위가 가장 높기 때문이다.

일반적인 선택자 우선순위는 다음과 같다.

**ID 선택자 > 클래스 선택자 > 태그 선택자**

단, `!important`, 인라인 스타일, CSS 출처 등의 조건에 따라 실제 적용 결과가 달라질 수 있다.

---

## 4. DevTools를 이용한 CSS 검증

### 확인 절차

1. 브라우저에서 `profile.html` 실행
2. `F12`로 개발자 도구 실행
3. `Elements` 탭 선택
4. `<p id="goal" class="highlight">` 요소 선택
5. `Styles` 패널에서 CSS 규칙 확인

### 실제 확인 결과

- `profile.css` 파일이 정상 연결됨
- `#goal { color: red; }` 적용 확인
- `.highlight { color: green; }` 취소선 확인
- `p { color: blue; }` 취소선 확인
- 목표 문장이 실제 브라우저에서 빨간색으로 표시됨

**검증 결과: PASS**

---

## 5. LLM에게 질문한 내용

### 질문 1. CSS 선택자 차이

태그, 클래스, 아이디 선택자의 차이와 사용 방법을 학습하였다.

### 질문 2. padding과 margin 차이

- `padding`: 콘텐츠와 테두리 사이의 내부 여백
- `margin`: 요소 바깥쪽의 외부 여백

### 질문 3. box-sizing 차이

- `content-box`: 지정한 너비에 padding과 border가 추가됨
- `border-box`: 지정한 너비에 padding과 border가 포함됨

### 질문 4. display 속성 차이

- `block`: 요소가 새로운 줄에서 시작
- `inline`: 글자처럼 같은 줄에 배치
- `inline-block`: 같은 줄에 배치하면서 너비와 높이 지정 가능

---

## 6. 내가 직접 확인하거나 수정한 부분

- [x] `profile.html` 파일 작성
- [x] `profile.css` 파일 작성
- [x] HTML과 CSS 정상 연결 확인
- [x] 이름 및 소개 문장 작성
- [x] HTML, CSS, JavaScript 학습 기술 3개 표시
- [x] GitHub 링크 추가
- [x] 클래스 및 아이디 선택자 적용
- [x] 글자색, 배경색, 글꼴 스타일 적용
- [x] DevTools에서 CSS 우선순위 확인
- [x] 목표 문장의 빨간색 적용 확인
- [ ] Git Commit 완료
- [ ] Git Push 완료

---

## 7. 학습 결과 및 회고

이번 실습을 통해 HTML 구조와 CSS 디자인의 역할을 구분하고, 선택자에 따라 스타일이 적용되는 방식을 이해하였다.

특히 CSS 규칙이 충돌할 경우 단순히 작성 순서만으로 결정되는 것이 아니라 선택자의 우선순위가 중요한 역할을 한다는 점을 확인하였다.

또한 브라우저 개발자 도구를 활용하면 어떤 CSS 규칙이 적용되고 무시되는지 직접 확인할 수 있음을 학습하였다.

### 향후 개선 방향

- DevTools를 활용하여 CSS 오류를 직접 분석하는 연습
- `margin`, `padding`, `border`를 이용한 레이아웃 실습
- `box-sizing: border-box`를 적용한 크기 관리
- Flexbox와 Grid를 이용한 반응형 레이아웃 학습

---

## 8. 제출 정보

- **과제명:** Chapter 04 — Student Profile Card
- **실습 경로:** `practice/phase01/chapter04/`
- **제출 파일:** `profile.html`, `profile.css`, `README.md`
- **검증 상태:** HTML/CSS 및 DevTools 확인 완료
- **GitHub 제출 상태:** Commit/Push 확인 필요
