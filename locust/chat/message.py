# from locust import HttpUser, TaskSet, task, between
# import random
# from websocket import create_connection
# import stomper
# import json
#
#
# # DTO 클래스
# class UserDTO:
#     class Login:
#         def __init__(self, email, password):
#             self.email = email
#             self.password = password
#
#
# class OpenChatDTO:
#     def __init__(self, title, max_personnel):
#         self.title = title
#         self.max_personnel = max_personnel
#
#
# # STOMP 클라이언트 클래스
# class StompClient:
#     def __init__(self, ws_uri):
#         self.ws_uri = ws_uri
#         self.ws = None
#
#     def connect(self, token):
#         try:
#             headers = [f"Authorization: Bearer {token}"]
#             self.ws = create_connection(self.ws_uri, header=headers)
#             connect_message = f"CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n"
#             self.ws.send(connect_message)
#             response = self.ws.recv()
#             if "CONNECTED" in response:
#                 print("WebSocket 연결 성공")
#             else:
#                 raise Exception(f"WebSocket 연결 실패: {response}")
#         except Exception as e:
#             print(f"WebSocket 연결 오류: {e}")
#             self.ws = None  # 연결에 실패하면 ws를 None으로 설정
#
#     def send(self, body, destination):
#         if not self.ws:
#             print("WebSocket이 연결되지 않음. 메시지를 보낼 수 없습니다.")
#             return
#
#         try:
#             msg = stomper.Frame()
#             msg.cmd = 'SEND'
#             msg.headers = {
#                 'destination': destination,
#                 'content-type': 'application/json'
#             }
#             msg.body = json.dumps(body)
#             self.ws.send(msg.pack())
#             print(f"메시지 전송 성공: {body}")
#         except Exception as e:
#             print(f"메시지 전송 오류: {e}")
#
#     def close(self):
#         if self.ws:
#             self.ws.close()
#             print("WebSocket 연결 종료")
#
#
# # 사용자 행동 정의
# class UserBehavior(TaskSet):
#     def on_start(self):
#         # 사용자가 시작할 때 로그인
#         self.login()
#
#     def on_stop(self):
#         # 사용자가 종료할 때 로그아웃
#         self.logout()
#
#     @task(1)
#     def login(self):
#         # 랜덤 로그인
#         n = random.randint(2, 1000)
#         email = f"test{n}@test.com"
#         password = "test"
#
#         login_data = UserDTO.Login(email=email, password=password)
#
#         # 로그인 시도
#         response = self.client.post("/api/users/login", json={
#             "email": login_data.email,
#             "password": login_data.password
#         })
#
#         if response.status_code == 200:
#             print(f"로그인 성공 유저: {email}")
#             # 쿠키 저장
#             self.cookies = response.cookies
#             token_value = response.cookies.get('Authorization')
#             token = token_value.replace("Bearer%20", "")
#             print("토큰: " + str(token))
#
#             # 로그인 후 WebSocket 연결 및 채팅방 작업 수행
#             self.handle_websocket(token)
#         else:
#             print(f"로그인 실패 유저: {email}")
#
#     def handle_websocket(self, token):
#         # WebSocket 연결 초기화 (http://localhost -> ws://localhost)
#         ws_uri = "ws://localhost:8080/stomp/chat"
#         stomp_client = StompClient(ws_uri)
#
#         # WebSocket 연결
#         stomp_client.connect(token)
#
#         # 채팅방 구독 시작
#         stomp_client.send({"chatId": "1"}, "/send/chat/enter")
#
#         # 메시지 전송
#         stomp_client.send({"chatId": "1", "message": "Hello World"}, "/send/chat/message")
#
#         # 구독 종료
#         stomp_client.send({"chatId": "1"}, "/send/chat/leave")
#         stomp_client.close()
#
#     def logout(self):
#         # 로그아웃 시도
#         if hasattr(self, 'cookies'):
#             # 로그아웃 시도, 로그인 시 받은 쿠키를 포함
#             response = self.client.post("/api/users/logout", cookies=self.cookies)
#
#             if response.status_code == 200:
#                 print("로그아웃 성공")
#             else:
#                 print("로그아웃 실패")
#         else:
#             print("쿠키 확인 불능 문제 발생")
#
#
# # HttpUser 클래스 정의
# class WebsiteUser(HttpUser):
#     tasks = [UserBehavior]
#     # 사용자 대기시간 정의
#     wait_time = between(1, 5)
