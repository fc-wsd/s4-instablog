# Instablog

있을 거 있는 블로그 프로젝트.

## 3주차 : Model

- `Post`, `Category`, `Comment`, `Tag` 모델 생성
- admin에 연결.


## 4주차 : View, Template, Admin

- 글 목록, 보기, 생성, 편집 뷰와 템플릿 추가
- Admin 인터페이스 확장
- bootstrap3 적용

### 4주차 test 과제 수행 방법

1. 자신의 블로그 프로젝트 저장소를 만드세요.
2. `https://github.com/fc-wsd/s4-instablog`에 있는 `blogtest` 앱을 통채로 내려 받아 자신의 블로그 프로젝트에 추가하세요. (`https://github.com/fc-wsd/s4-instablog/tree/master/blogtest`)
3. `settings.py`의 `INSTALLED_APPS`에 `blogtest`를 추가하세요.
4. 마이그레이션을 수행해서 `blogtest` 앱의 모델을 데이터베이스에 반영하세요.
5. `python manage.py test blogtest`을 실행하여 테스트를 수행하세요. 
6. 다음과 같이 여섯 개 테스트를 모두 통과하도록 모델, 뷰, urls를 작성하세요.
7. 모든 테스트를 통과한 코드를 자신의 블로그 프로젝트 저장소에 push 하세요.

```
➜  $ python manage.py test blogtest
Creating test database for alias 'default'...
......
----------------------------------------------------------------------
Ran 6 tests in 0.185s

OK
Destroying test database for alias 'default'...
```

## 5주차 : Form, Authentication

- ModelForm을 이용하여 입력값 검증하고, 데이터 저장하기
- 인증 기능을 사용하여 로그인, 로그아웃 구현
- 로그인 한 사람만 글 쓰기

### 5주차 테스트 과제 추가

5주차 테스트 내용이 추가됐습니다. tests.py 파일을 다시 가져가세요. :)


## 6주차 : Middleware, Staticfile, Logging

- Middleware를 이용해 request 객첵에 속성 추가하기
- Middleware를 이용해 Exception에 대응하기
- static file, media file 설정하기
  - ImageField를 이용해 파일 업로드 구현
- Logging 다루기
