# fastAPI

## 설치 및 기본문서

### 설치

```
poetry add fastapi
poetry add uvicorn
```

### 실행

```
# poetry 가상환경 실행
poetry shell

# uvicorn 실행(main.py 의 app 함수 실행)
# --reload: 코드가 변경되면 재실행
# --host: 접근가능 호스트 설정(0.0.0.0 은 모든 접근이 가능)
# --port: 접속 원하는 포트
uvicorn main:app --reload
```

### 기본문서

- 🧤 api의 문서를 자동으로 생성해준다.(Super Cool!)
- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc
- api정의 명세서: http://127.0.0.1:8000/openapi.json
