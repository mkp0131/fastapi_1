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

### API Get 요청 => requests 메소드 사용

- 원격에 있는 API를 호출할 때 유용하게 사용
- requests 라이브러리 설치

```
poetry add requests
```

- 기본 사용법

```py
@app.post("/cities/{city_id}")
def get_city(city_id: int):
    city = city_list[city_id - 1]
    # api 요청
    url = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
    # requests 를 활용하여 GET 요청
    data = requests.get(url)
    # 응답받은 데이터를 JSON 으로 변환
    return data.json()
```

### jinja2 (HTML view engine)

- 설치

```
poetry add jinja2
```

- 템플릿 설정

```py
from fastapi import FastAPI, Request  # fastapi 라이브러리, Request 값 import
from fastapi.responses import HTMLResponse  # 응답 데이터 타입
from fastapi.templating import Jinja2Templates  # HTML view engine

template = Jinja2Templates(directory="templates")

# 도시 목록
@app.get("/cities", response_class=HTMLResponse)
def get_cities(request: Request):  # request에 Request 할당
    # html 에 넘겨주는 변수
    context = {}

    data_list = []
    for city in city_list:
        # api 요청
        url = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
        data = requests.get(url)

        # 응답코드
        rs_code = data.status_code
        if int(rs_code) == 200:
            print("응답완료")
            json = data.json()
            print(json)
            data_list.append(json)
        else:
            print("응답실패")
            print(rs_code)

    context["request"] = request
    context["city_list"] = data_list

    return template.TemplateResponse("cities.html", context)
```

- 템플릿에 `fastapi` 의 `Request` 를 반드시 넘겨주어야한다.
- 데이터는 객체로 할당하여 전달한다.
- jinja 템플릿에서 값을 사용한다.(Like PHP)
- 값사용시 {{}}
- 문식 사용시 {%%}

```html
<h1>City list</h1>
<ul>
  {# context 의 속성을 변수로 사용 할 수 있다 #} {% if city_list %} {% for city
  in city_list %}
  <li>{{city.timezone}}: {{city.datetime}}</li>
  {% endfor %} {% else %}
  <li>No Data</li>
  {% endif %}
</ul>
```
