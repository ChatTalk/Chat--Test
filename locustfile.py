from locust import HttpUser, task

# 테스트용
class Test(HttpUser):
    @task
    def get_open_chats(self):
        self.client.get("/api/open-chats")