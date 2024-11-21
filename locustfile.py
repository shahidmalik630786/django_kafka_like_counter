from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://127.0.0.1:8000"

    @task
    def like_post(self):
        post_id = 1  # Random post_id between 1 and 100
        self.client.get(f'/like/{post_id}', headers={"Content-type": "application/json"})
