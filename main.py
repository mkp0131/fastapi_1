import requests  # get 요청을 받는 파이썬 기본 라이브러리
from fastapi import FastAPI, Request  # fastapi 라이브러리, Request 값 import
from pydantic import BaseModel  # 파라미터 검증을 도와주는 라이브러리
from fastapi.responses import HTMLResponse  # 응답 데이터 타입
from fastapi.templating import Jinja2Templates  # HTML view engine

app = FastAPI()

template = Jinja2Templates(directory="templates")

# 플로우 정리
# http://worldtimeapi.org/api/timezone/Asia/Seoul
# get_cities: 저장된 도시 정보 리스트를 가져온다.
# get_city(city_id): 지정한 도시의 정보를 가져온다.
# create_city(city_id): 도시 정보 리스트에 도시를 추가한다.
# delete_city(city_id): 도시 정보 리스트에 도시를 제거한다.


# index
@app.get("/")
def root():
    return {"name": "mkp"}


# 도시 리스트
city_list = []

# 파라미터 인터페이스 정의
class City(BaseModel):
    name: str
    timezone: str


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


# 도시 입력
# 데이터 형식
# {
#   "name": "서울",
#   "timezone": "Asia/Seoul"
# }
@app.post("/cities")
def create_cities(city: City):  # City 클래스 형식에 맞지 않으면 오류가 발생한다.
    city_list.append(city.dict())  # object 형태로 만들어서 배열에 push 한다
    print(city_list)
    return city_list[-1]


# 도시
@app.post("/cities/{city_id}")
def get_city(city_id: int):
    city = city_list[city_id - 1]
    # api 요청
    url = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
    data = requests.get(url)
    return data.json()


# 도시 삭제
@app.delete("/cities/{city_id}")
def delete_city(city_id: int):
    if len(city_list):  # 빈배열일때 에러 보호
        city_list.pop(city_id - 1)
    return "삭제완료"
