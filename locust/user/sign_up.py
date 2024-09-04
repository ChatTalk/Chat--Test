from locust import HttpUser, TaskSet, task, between
import random


class UserBehavior(TaskSet):
    @task
    def signup(self):
        # n값을 3부터 1000 사이의 값으로 설정
        n = random.randint(3, 1000)

        # 이메일 주소 생성
        email = f"test{n}@test.com"

        # 회원가입에 사용할 데이터 정의
        user_data = {
            "email": email,
            "password": "test",
            "phone": "000-000-0000",
            "role": "USER"
        }

        # POST 요청으로 회원가입 엔드포인트 호출
        with self.client.post("/api/users/signup", json=user_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to sign up with email {email}. Status code: {response.status_code}")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

"""
결과
- 중복 가입 방어 불능 동시성 이슈 발생
- 엔티티 ORM 어노테이션 중복 방지 할당, 서비스 로직만의 책임을 데이터베이스 레벨 중복 방지로 책임 분담
"""