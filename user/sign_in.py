from locust import HttpUser, TaskSet, task, between, constant
import random


# DTO 클래스
class UserDTO:
    class Login:
        def __init__(self, email, password):
            self.email = email
            self.password = password


# 로그인 후, 로그아웃
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
        else:
            print(f"로그인 실패 유저: {email}")

    @task(2)
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
    wait_time = constant(999999)

"""
- 1차 테스트
테스트 결과와 실제 서버 결과와의 정합성 차이 발생
"""
"""
- 2차 테스트
"""
