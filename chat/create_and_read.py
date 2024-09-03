from locust import HttpUser, TaskSet, task, between
import random


# DTO 클래스
class UserDTO:
    class Login:
        def __init__(self, email, password):
            self.email = email
            self.password = password


class OpenChatDTO:
    def __init__(self, title, max_personnel):
        self.title = title
        self.max_personnel = max_personnel


# 사용자 행동 정의
class UserBehavior(TaskSet):
    def on_start(self):
        # 사용자가 시작할 때 로그인
        self.login()

    def on_stop(self):
        # 사용자가 종료할 때 로그아웃
        self.logout()

    @task(1)
    def login(self):
        # 랜덤 로그인
        n = random.randint(2, 1000)
        email = f"test{n}@test.com"
        password = "test"

        login_data = UserDTO.Login(email=email, password=password)

        # 로그인 시도
        response = self.client.post("/api/users/login", json={
            "email": login_data.email,
            "password": login_data.password
        })

        if response.status_code == 200:
            print(f"로그인 성공 유저: {email}")
            # 쿠키 저장
            self.cookies = response.cookies
            # 로그인 후 채팅방 생성
            self.create_open_chat()
            # 채팅방 생성 후 채팅방 리스트 조회
            self.get_all_open_chats()
        else:
            print(f"로그인 실패 유저: {email}")

    def create_open_chat(self):
        # OpenChat 생성
        chat_data = OpenChatDTO(title="title", max_personnel=10)
        response = self.client.post("/api/open-chats/create", json={
            "title": chat_data.title,
            "maxPersonnel": chat_data.max_personnel
        }, cookies=self.cookies)

        if response.status_code == 200:
            print(f"채팅 생성 성공: {response.json()}")
        else:
            print(f"채팅 생성 실패: {response.text}")

    def get_all_open_chats(self):
        # OpenChat 조회
        response = self.client.get("/api/open-chats", cookies=self.cookies)

        if response.status_code == 200:
            print(f"채팅 조회 성공: {response.json()}")
        else:
            print(f"채팅 조회 실패: {response.text}")

    def logout(self):
        # 로그아웃 시도
        if hasattr(self, 'cookies'):
            # 로그아웃 시도, 로그인 시 받은 쿠키를 포함
            response = self.client.post("/api/users/logout", cookies=self.cookies)

            if response.status_code == 200:
                print("로그아웃 성공")
            else:
                print("로그아웃 실패")
        else:
            print("쿠키 확인 불능 문제 발생")


# HttpUser 클래스 정의
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    # 사용자 대기시간 정의
    wait_time = between(1, 5)



"""
1차 테스트 결과

[2024-09-03 18:09:42,458] gimdongjun-ui-MacBookPro/WARNING/root: CPU usage above 90%! This may constrain your throughput and may even give inconsistent response time measurements!

- 테스트에 든 부하를 너무 크게 설정했나? 유저수 999명에 램프업 15초가 너무 과한가. 런타임 2분은 상관없을듯

Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /api/open-chats                                                                 5053 2078(41.12%) |  11041      12   33292  11000 |   15.33        6.31
POST     /api/open-chats/create                                                          5094   447(8.78%) |  11065      12   32839  11000 |   15.46        1.36
POST     /api/users/login                                                                6000  906(15.10%) |  19750     474   81003  18000 |   18.21        2.75
POST     /api/users/logout                                                                999     0(0.00%) |  28001   26780   28865  28000 |    3.03        0.00

- 예상은 했지만 채팅창 리스트 조회에서 에러 발생률이 높다. 리스트 전체를 들고 와서 조회하는 거니까
- 아무래도 페이징 처리가 필요할

Error report
# occurrences      Error                                                                                               
------------------|---------------------------------------------------------------------------------------------------------------------------------------------
2078               GET /api/open-chats: OSError(57, 'Socket is not connected')                                         
906                POST /api/users/login: OSError(57, 'Socket is not connected')                                       
447                POST /api/open-chats/create: OSError(57, 'Socket is not connected')                                 
------------------|---------------------------------------------------------------------------------------------------------------------------------------------

- 이 문제는 클라이언트와 서버 간의 약속 문제긴 한, 서버 응답 이전에 클라이언트의 연결 단절 문제

"""
