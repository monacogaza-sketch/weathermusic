import streamlit as st
import requests
import datetime
import random
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
API_KEY = os.getenv("API_KEY")


# 도시명 변환 및 지원 도시 관리 통합
city_dict = {
    "서울": "Seoul", "인천": "Incheon", "수원": "Suwon", "고양": "Goyang", "성남": "Seongnam", "부천": "Bucheon", "안양": "Anyang", "안산": "Ansan", "의정부": "Uijeongbu", "파주": "Paju", "평택": "Pyeongtaek",
    "강릉": "Gangneung", "춘천": "Chuncheon", "원주": "Wonju", "동해": "Donghae", "속초": "Sokcho", "삼척": "Samcheok", "양양": "Yangyang",
    "부산": "Busan", "대구": "Daegu", "울산": "Ulsan", "창원": "Changwon", "포항": "Pohang", "진주": "Jinju", "경주": "Gyeongju", "구미": "Gumi", "김해": "Gimhae", "통영": "Tongyeong",
    "광주": "Gwangju", "전주": "Jeonju", "여수": "Yeosu", "목포": "Mokpo", "순천": "Suncheon", "군산": "Gunsan", "광양": "Gwangyang", "나주": "Naju",
    "대전": "Daejeon", "청주": "Cheongju", "천안": "Cheonan", "아산": "Asan", "공주": "Gongju", "논산": "Nonsan", "서산": "Seosan",
    "제주": "Jeju", "서귀포": "Seogwipo",
    "이천": "Icheon", "여주": "Yeoju", "충주": "Chungju", "김포": "Gimpo"
}

def kor_to_eng_city(city):
    kor = city
    eng = city_dict.get(city, city)
    return kor, eng

def get_supported_city(city_input):
    city_input = city_input.strip()
    if city_input in city_dict:
        return city_dict[city_input]
    elif city_input in city_dict.values():
        return city_input
    return None

def get_location_by_ip():
    try:
        res = requests.get("https://ipinfo.io/json")
        city = res.json().get("city", "")
        return city
    except:
        return ""


debug = False  # 디버깅 모드 활성화 여부


# 중복 API 호출 함수 통합
def get_api_response(city, endpoint):
    _, eng_city = kor_to_eng_city(city)
    for q in [eng_city, city]:
        url = f"http://api.openweathermap.org/data/2.5/{endpoint}?q={q}&appid={API_KEY}&units=metric&lang=kr"
        response = requests.get(url)
        if debug:
            st.write(f"{endpoint} API 응답 상태 코드:", response.status_code)
            st.write(f"{endpoint} API 응답 내용:", response.json())
        if response.status_code == 200:
            return response.json()
    return None

def get_weather(city):
    return get_api_response(city, "weather")

def get_forecast(city):
    return get_api_response(city, "forecast")

def get_air_quality(city):
    _, eng_city = kor_to_eng_city(city)
    for q in [eng_city, city]:
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={q}&limit=1&appid={API_KEY}"
        geo_res = requests.get(geo_url)
        if geo_res.status_code == 200 and geo_res.json():
            lat = geo_res.json()[0]['lat']
            lon = geo_res.json()[0]['lon']
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "list" in data and len(data["list"]) > 0:
                    return data["list"][0]["components"]["pm2_5"]
    return None

def get_season():
    month = datetime.datetime.now().month
    if month in [3, 4, 5]:
        return "봄"
    elif month in [6, 7, 8]:
        return "여름"
    elif month in [9, 10, 11]:
        return "가을"
    else:
        return "겨울"

st.set_page_config(page_title="웨더뮤직", layout="wide", page_icon="🎵")
st.markdown(
    """
    <style>
    body { background-color: #1E90FF; } /* 다바색 (Dodger Blue) */
    .stButton>button {background-color: #4f8cff; color: white;}
    .stTextInput>div>input {font-size:16px;}
    </style>
    """,
    unsafe_allow_html=True
)

# 배경화면 설정만 유지 (요트 이미지 삭제)
st.markdown(
    """
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); /* 석양 바다 이미지 */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp {
        background: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 헤더 섹션

st.markdown(
    """
    <div style='display:flex;align-items:center;gap:18px;margin-bottom:12px;'>
        <span style='font-size:2.5em;font-weight:bold;'>🎵 웨더뮤직</span>
        <img src='https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_South_Korea.svg' style='width:64px;height:64px;border:4px solid #4f8cff;border-radius:50%;box-shadow:0 0 12px #4f8cff;margin-left:8px;' alt='태극기'/>
    </div>
    <div style='font-size:1.8em;color:#555;margin-bottom:16px;'>Weather Music</div>
    """,
    unsafe_allow_html=True
)


# 케데헌 테이크다운, 케데헌 골든, 사자보이즈 새로운 링크, 블랙핑크 뚜두뚜두, 듀스 '나를 돌아봐', 브라운아이즈 '벌써일년' 유튜브 영상 나란히 배치 (작은 화면)
col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
with col1:
    st.markdown("<div style='width:160px; margin-bottom:16px;'>", unsafe_allow_html=True)
    st.markdown(
        '''
        <iframe width="160" height="90" src="https://www.youtube.com/embed/7XRcflf_E0c" frameborder="0" allowfullscreen></iframe>
        <br>
        <a href="https://www.youtube.com/watch?v=7XRcflf_E0c" target="_blank" style="font-size:0.9em;">유튜브에서 보기 (Watch on YouTube)</a>
        ''',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("케데헌 - 테이크다운")
with col2:
    st.markdown("<div style='width:160px; margin-bottom:16px;'>", unsafe_allow_html=True)
    st.markdown(
        '''
        <iframe width="160" height="90" src="https://www.youtube.com/embed/9_bTl2vvYQg" frameborder="0" allowfullscreen></iframe>
        <br>
        <a href="https://www.youtube.com/watch?v=9_bTl2vvYQg" target="_blank" style="font-size:0.9em;">유튜브에서 보기 (Watch on YouTube)</a>
        ''',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("케데헌 - 골든")
with col3:
    st.markdown("<div style='width:160px; margin-bottom:16px;'>", unsafe_allow_html=True)
    st.markdown(
        '''
        <iframe width="160" height="90" src="https://www.youtube.com/embed/0aTLAHyaQ14" frameborder="0" allowfullscreen></iframe>
        <br>
        <a href="https://www.youtube.com/watch?v=0aTLAHyaQ14" target="_blank" style="font-size:0.9em;">유튜브에서 보기 (Watch on YouTube)</a>
        ''',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("사자보이즈 - 유어아이돌")
with col4:
    st.markdown("<div style='width:160px; margin-bottom:16px;'>", unsafe_allow_html=True)
    st.markdown(
        '''
        <iframe width="160" height="90" src="https://www.youtube.com/embed/MrM8j4JtU9M" frameborder="0" allowfullscreen></iframe>
        <br>
        <a href="https://www.youtube.com/watch?v=MrM8j4JtU9M" target="_blank" style="font-size:0.9em;">유튜브에서 보기 (Watch on YouTube)</a>
        ''',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("블랙핑크 - 뚜두뚜두")
with col5:
    st.markdown("<div style='width:160px; margin-bottom:16px;'>", unsafe_allow_html=True)
    st.markdown(
        '''
        <iframe width="160" height="90" src="https://www.youtube.com/embed/nhBNnZTrWik" frameborder="0" allowfullscreen></iframe>
        <br>
        <a href="https://www.youtube.com/watch?v=nhBNnZTrWik" target="_blank" style="font-size:0.9em;">유튜브에서 보기 (Watch on YouTube)</a>
        ''',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("듀스 - 나를 돌아봐")
with col6:
    st.markdown("<div style='width:160px; margin-bottom:16px;'>", unsafe_allow_html=True)
    st.markdown(
        '''
        <iframe width="160" height="90" src="https://www.youtube.com/embed/gdj6a0hv0Uk" frameborder="0" allowfullscreen></iframe>
        <br>
        <a href="https://www.youtube.com/watch?v=gdj6a0hv0Uk" target="_blank" style="font-size:0.9em;">유튜브에서 보기 (Watch on YouTube)</a>
        ''',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("브라운아이즈 - 벌써일년")

supported_cities = {
    "서울": "Seoul", "부산": "Busan", "대구": "Daegu", "인천": "Incheon", "광주": "Gwangju", "대전": "Daejeon", "울산": "Ulsan", "수원": "Suwon", "고양": "Goyang", "성남": "Seongnam", "부천": "Bucheon", "안양": "Anyang", "안산": "Ansan", "의정부": "Uijeongbu", "파주": "Paju", "평택": "Pyeongtaek", "강릉": "Gangneung", "춘천": "Chuncheon", "원주": "Wonju", "동해": "Donghae", "속초": "Sokcho", "삼척": "Samcheok", "양양": "Yangyang", "전주": "Jeonju", "여수": "Yeosu", "목포": "Mokpo", "순천": "Suncheon", "군산": "Gunsan", "광양": "Gwangyang", "나주": "Naju", "청주": "Cheongju", "천안": "Cheonan", "아산": "Asan", "공주": "Gongju", "논산": "Nonsan", "서산": "Seosan", "제주": "Jeju", "서귀포": "Seogwipo", "이천": "Icheon", "여주": "Yeoju", "충주": "Chungju", "김포": "Gimpo", "포항": "Pohang", "진주": "Jinju", "경주": "Gyeongju", "구미": "Gumi", "김해": "Gimhae", "통영": "Tongyeong", "창원": "Changwon"
}

city_tour_map = {
    "Seoul": [
        "경복궁 (Gyeongbokgung Palace)",
        "남산타워 (Namsan Tower)",
        "북촌한옥마을 (Bukchon Hanok Village)",
        "동대문디자인플라자 (Dongdaemun Design Plaza)",
        "롯데월드타워 (Lotte World Tower)",
        "한강공원 (Hangang Park)",
        "서울숲 (Seoul Forest)",
        "명동 (Myeongdong)",
        "홍대거리 (Hongdae Street)",
        "이태원 (Itaewon)"
    ],
    "Busan": [
        "해운대 (Haeundae Beach)",
        "광안리 (Gwangalli Beach)",
        "태종대 (Taejongdae)",
        "감천문화마을 (Gamcheon Culture Village)",
        "오륙도 (Oryukdo Islands)",
        "송정해수욕장 (Songjeong Beach)",
        "부산타워 (Busan Tower)",
        "자갈치시장 (Jagalchi Market)",
        "해동용궁사 (Haedong Yonggungsa Temple)",
        "다대포해수욕장 (Dadaepo Beach)"
    ],
    "Jeju": [
        "성산일출봉 (Seongsan Ilchulbong)",
        "한라산 (Hallasan Mountain)",
        "협재해수욕장 (Hyeopjae Beach)",
        "우도 (Udo Island)",
        "천지연폭포 (Cheonjiyeon Waterfall)",
        "만장굴 (Manjanggul Cave)",
        "용두암 (Yongduam Rock)",
        "섭지코지 (Seopjikoji)",
        "제주돌문화공원 (Jeju Stone Park)",
        "카멜리아힐 (Camellia Hill)"
    ],
    # 다른 도시들도 동일한 형식으로 추가
}

# 숙박 플랫폼별 검색 URL
city_accommodation_links = {
    "Seoul": {
        "Airbnb": "https://www.airbnb.com/s/Seoul--South-Korea/homes",
        "Booking.com": "https://www.booking.com/city/kr/seoul.html",
        "Expedia": "https://www.expedia.com/Seoul-Hotels.d178308.Travel-Guide-Hotels",
        "Agoda": "https://www.agoda.com/city/seoul-kr.html",
        "Hotels.com": "https://www.hotels.com/ho12345678/seoul-hotels",
        "Trip.com": "https://www.trip.com/hotels/seoul-hotels"
    },
    "Busan": {
        "Airbnb": "https://www.airbnb.com/s/Busan--South-Korea/homes",
        "Booking.com": "https://www.booking.com/city/kr/busan.html",
        "Expedia": "https://www.expedia.com/Busan-Hotels.d6049721.Travel-Guide-Hotels",
        "Agoda": "https://www.agoda.com/city/busan-kr.html",
        "Hotels.com": "https://www.hotels.com/ho12345678/busan-hotels",
        "Trip.com": "https://www.trip.com/hotels/busan-hotels"
    },
    "Jeju": {
        "Airbnb": "https://www.airbnb.com/s/Jeju--South-Korea/homes",
        "Booking.com": "https://www.booking.com/city/kr/jeju.html",
        "Expedia": "https://www.expedia.com/Jeju-Island-Hotels.d6049718.Travel-Guide-Hotels",
        "Agoda": "https://www.agoda.com/city/jeju-island-kr.html",
        "Hotels.com": "https://www.hotels.com/ho12345678/jeju-hotels",
        "Trip.com": "https://www.trip.com/hotels/jeju-hotels"
    }
}

# 날씨 설명 번역 사전 추가
weather_translation = {
    "clear sky": "맑은 하늘",
    "few clouds": "구름 조금",
    "scattered clouds": "흩어진 구름",
    "broken clouds": "구름 많음",
    "shower rain": "소나기",
    "rain": "비",
    "thunderstorm": "천둥번개",
    "snow": "눈",
    "mist": "안개"
}


col_title, col_city = st.columns([1.5, 1])
with col_title:
    st.write("")
with col_city:
    city_input = st.text_input(
        "도시 찾기 (Search City: Korean or English, e.g. 서울/Seoul)",
        key="city_input",
        help="아래 지원 도시만 입력하세요. 한글 입력 시 자동 변환됩니다.\n(Please enter only supported cities. Korean input will be auto-converted.)\n" + ", ".join([f"{k}({v})" for k,v in supported_cities.items()])
    )
    # "찾기" 버튼 추가
    if st.button("찾기 (Search)", key="search_btn"):
        if city_input:
            matched = [k for k in supported_cities.keys() if city_input in k or city_input.lower() in supported_cities[k].lower()]
            if matched:
                st.write("검색 결과 (Search Results):")
                for city_name in matched:
                    st.write(f"- {city_name} ({supported_cities[city_name]})")
            else:
                st.write("일치하는 도시가 없습니다. (No matching city found.)")
        else:
            st.write("도시 이름을 입력하세요. (Please enter a city name.)")

city = None

if city_input:
    city_input = city_input.strip()
    if city_input in supported_cities:
        city = supported_cities[city_input]
    elif city_input in supported_cities.values():
        city = city_input
    else:
        st.warning(f"지원되지 않는 도시입니다. 아래 리스트에서 선택해 주세요. (Unsupported city. Please select from the list below.)\n" + ", ".join([f"{k}({v})" for k,v in supported_cities.items()]))
        city = None
else:
    city = get_location_by_ip()
    if city:
        st.info(f"자동 감지된 도시: {city} (Auto-detected city)")
        if city in supported_cities:
            city = supported_cities[city]
        elif city in supported_cities.values():
            city = city
        else:
            st.warning(f"자동 감지된 도시가 지원 리스트에 없습니다. 도시명을 입력해 주세요. (Auto-detected city is not supported. Please enter a city name.)")
            city = None

if city:
    try:
        kor_city, eng_city = kor_to_eng_city(city)
        data = get_weather(city)
        if not data or "weather" not in data:
            st.error("날씨 데이터를 불러올 수 없습니다.")
            st.stop()
        weather_kor = data['weather'][0]['description']
        weather_eng = data['weather'][0]['main']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        pm25 = get_air_quality(city)
        forecast = get_forecast(city)
    except Exception as e:
        st.error(f"날씨 데이터를 불러올 수 없습니다: {e}")
        st.stop()

    # 현재 날씨와 주간 예보를 한 화면에 배치
    col_now, col_forecast = st.columns([2, 3])

    with col_now:
        # 현재 날씨 표시 (한글+영어)
        st.markdown("<h3>현재 날씨 (Current Weather)</h3>", unsafe_allow_html=True)
        st.markdown(f"🌡️ **온도 (Temperature)**: {data['main']['temp']}°C")
        # 현재날씨 아이콘 매핑
        weather_icon_map = {
            "맑은 하늘": "icons/sunny.png",
            "비": "icons/rainy.png",
            "흐림": "icons/cloudy.png"
        }
        icon_path = weather_icon_map.get(weather_kor)
        icon_html = f'<img src="{icon_path}" width="32">' if icon_path else ''
        st.markdown(f"🌤️ **상태 (Condition)**: {weather_kor} ({weather_eng}) {icon_html}", unsafe_allow_html=True)
        st.markdown(f"💧 **습도 (Humidity)**: {data['main']['humidity']}%")
        st.markdown(f"🌬️ **풍속 (Wind Speed)**: {data['wind']['speed']} m/s")
        st.markdown(f"🌅 **일출 (Sunrise)**: {sunrise}")
        st.markdown(f"🌇 **일몰 (Sunset)**: {sunset}")

    with col_forecast:
        # 주간 예보 표시 (한글+영어)
        st.markdown("<h3>주간 예보 (Weekly Forecast)</h3>", unsafe_allow_html=True)
        if forecast and "list" in forecast:
            # 날씨 상태별 아이콘 매핑
            weather_icon_map = {
                "맑은 하늘": "icons/sunny.png",
                "비": "icons/rainy.png",
                "흐림": "icons/cloudy.png"
            }
            # 날짜별로 중복 제거
            daily_forecast = {}
            for item in forecast['list']:
                dt = datetime.datetime.fromtimestamp(item['dt'])
                date = dt.strftime('%m/%d')
                day_of_week = dt.strftime('%A')  # 요일 추가 (Monday, Tuesday 등)
                if date not in daily_forecast:
                    daily_forecast[date] = {"item": item, "day_of_week": day_of_week}  # 요일 포함

            # 중복 제거된 날짜별 예보 출력
            for date, data in daily_forecast.items():
                item = data["item"]
                day_of_week = data["day_of_week"]
                temp = item['main']['temp']
                desc = item['weather'][0]['description']
                desc_kor = weather_translation.get(desc, desc)
                icon_path = weather_icon_map.get(desc_kor)
                icon_html = f'<img src="{icon_path}" width="32">' if icon_path else ''
                st.markdown(f"<b>📅 {date} ({day_of_week}): {temp}°C, {desc_kor} ({desc}) {icon_html}</b>", unsafe_allow_html=True)
        else:
            st.error("주간 예보 데이터를 처리할 수 없습니다. (Unable to process weekly forecast data.)")


    st.markdown("---")

    # 추천 관광지와 숙박 플랫폼 추천을 나란히 표시
    col_tour, col_accommodation = st.columns(2)

    with col_tour:
        # 추천 관광지 표시 (한글+영어)
        st.markdown("<h3>추천 관광지 (Tourist Attractions)</h3>", unsafe_allow_html=True)
        tour_links = {
            "경복궁 (Gyeongbokgung Palace)": "https://www.royalpalace.go.kr/",
            "남산타워 (Namsan Tower)": "https://www.seoultower.co.kr/",
            "북촌한옥마을 (Bukchon Hanok Village)": "https://bukchon.seoul.go.kr/",
            "동대문디자인플라자 (Dongdaemun Design Plaza)": "https://www.ddp.or.kr/",
            "롯데월드타워 (Lotte World Tower)": "https://www.lwt.co.kr/",
            "한강공원 (Hangang Park)": "https://hangang.seoul.go.kr/",
            "서울숲 (Seoul Forest)": "https://seoulforest.or.kr/",
            "명동 (Myeongdong)": "https://www.myeongdong.org/",
            "홍대거리 (Hongdae Street)": "https://www.visitseoul.net/attractions/view?cid=1017",
            "이태원 (Itaewon)": "https://www.visitseoul.net/attractions/view?cid=1018",
            # 부산
            "해운대 (Haeundae Beach)": "https://www.haeundae.go.kr/tour/index.do",
            "광안리 (Gwangalli Beach)": "https://www.suyeong.go.kr/tour/index.do",
            "태종대 (Taejongdae)": "https://www.taejongdae.or.kr/",
            "감천문화마을 (Gamcheon Culture Village)": "https://gamcheon.or.kr/",
            "오륙도 (Oryukdo Islands)": "https://www.suyeong.go.kr/tour/index.do",
            # 대구
            "팔공산 (Palgongsan Mountain)": "https://www.daegu.go.kr/palgong/",
            "동화사 (Donghwasa Temple)": "https://donghwasa.net/",
            "서문시장 (Seomun Market)": "https://www.seomunmarket.com/",
            # 인천
            "송도 센트럴파크 (Songdo Central Park)": "https://www.songdocentralpark.com/",
            "월미도 (Wolmido)": "https://www.incheon.go.kr/tour/",
            "차이나타운 (Chinatown)": "https://www.incheon.go.kr/tour/",
            # 광주
            "무등산 (Mudeungsan Mountain)": "https://www.gwangju.go.kr/eco/",
            "국립아시아문화전당 (Asia Culture Center)": "https://www.acc.go.kr/",
            # 대전
            "엑스포과학공원 (Expo Science Park)": "https://www.expopark.co.kr/",
            "한밭수목원 (Hanbat Arboretum)": "https://www.daejeon.go.kr/hanbat/",
            # 울산
            "대왕암공원 (Daewangam Park)": "https://www.ulsan.go.kr/tour/daewangam/",
            "태화강국가정원 (Taehwagang National Garden)": "https://garden.ulsan.go.kr/",
            # 수원
            "수원화성 (Hwaseong Fortress)": "https://www.swcf.or.kr/culture/",
            "광교호수공원 (Gwanggyo Lake Park)": "https://www.suwon.go.kr/",
            # 제주
            "성산일출봉 (Seongsan Ilchulbong)": "https://www.jeju.go.kr/jejuwonders/",
            "한라산 (Hallasan Mountain)": "https://www.hallasan.go.kr/",
            "협재해수욕장 (Hyeopjae Beach)": "https://www.jeju.go.kr/",
            # 창원
            "진해군항제 (Jinhae Gunhangje Festival)": "https://gunhang.changwon.go.kr/",
            "창원해양공원 (Changwon Marine Park)": "https://www.cwmarinepark.co.kr/",
            # 전주
            "전주한옥마을 (Jeonju Hanok Village)": "https://hanok.jeonju.go.kr/",
            "경기전 (Gyeonggijeon Shrine)": "https://www.jeonju.go.kr/",
            # 강릉
            "경포대 (Gyeongpodae Pavilion)": "https://www.gn.go.kr/",
            "안목해변 (Anmok Beach)": "https://www.gn.go.kr/",
            # 춘천
            "남이섬 (Nami Island)": "https://namisum.com/",
            "소양강스카이워크 (Soyanggang Skywalk)": "https://www.chuncheon.go.kr/skywalk/"
        }
        if city and city in city_tour_map:
            for place in city_tour_map[city]:
                link = tour_links.get(place)
                if link:
                    st.markdown(f"- [{place}]({link})", unsafe_allow_html=True)
                else:
                    st.markdown(f"- {place}")
        else:
            st.markdown("도시를 선택하면 추천 관광지가 표시됩니다. (Select a city to view recommended tourist attractions.)")

    with col_accommodation:
        # 숙박 플랫폼 추천 표시 (한글+영어)
        st.markdown("<h3>숙박 플랫폼 추천 (Accommodation Platforms)</h3>", unsafe_allow_html=True)
        if city and city in city_accommodation_links:
            for platform, link in city_accommodation_links[city].items():
                st.markdown(f"- [{platform}]({link})", unsafe_allow_html=True)
        else:
            st.markdown("도시를 선택하면 숙박 플랫폼 링크가 표시됩니다. (Select a city to view accommodation platform links.)")


    st.markdown("#### 📈 앞으로의 온도 변화 (Upcoming Temperature Changes)")
    if forecast and 'list' in forecast:
        times = []
        temps = []
        for item in forecast['list'][:8]:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            times.append(dt.strftime('%m/%d %H:%M'))
            temps.append(item['main']['temp'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times, y=temps, mode='lines+markers',
            line=dict(color='#4f8cff', width=3),
            marker=dict(size=8, color='#4f8cff'),
            name='온도 (Temperature)'
        ))
        fig.update_layout(
            title='24시간 온도 변화 (24h Temperature Change)',
            xaxis_title='시간 (Time)',
            yaxis_title='온도(°C) (Temperature)',
            height=300,
            font=dict(size=12),
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("예보 데이터를 가져올 수 없습니다. (Unable to fetch forecast data.)")
else:
    st.info("도시를 입력하거나 지원 도시를 선택해 주세요. (Please enter a city or select from the supported list.)")

# 디버깅용 데이터 출력
debug = False  # 디버깅 모드 활성화 여부

if debug:
    st.write("Forecast 데이터:", forecast)

def get_music_from_fma(genre="kpop", limit=10):
    url = f"https://freemusicarchive.org/api/get/tracks?api_key={FMA_API_KEY}&limit={limit}&genre_handle={genre}"
    response = requests.get(url)
    st.write("FMA API 응답 상태 코드:", response.status_code)  # 상태 코드 출력
    st.write("FMA API 응답 내용:", response.text)  # 응답 내용 출력
    if response.status_code == 200:
        tracks = response.json().get("dataset", [])
        return [(track["track_title"], track["artist_name"], track["track_file_url"]) for track in tracks]
    else:
        st.error("FMA에서 음악 데이터를 가져오는 데 실패했습니다.")
        return []

# 날씨에 따른 추천 음악 플레이리스트 (K-pop 곡 추가)