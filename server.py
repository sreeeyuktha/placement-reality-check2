# -------------------------------
# PLACEMENT REALITY CHECK SERVER
# -------------------------------

# -------------------------------
# PLACEMENT REALITY CHECK SERVER
# -------------------------------

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Job Database
job_database = {
    "data scientist": {
        "skills": ["python", "machine learning", "statistics", "pandas", "numpy"],
        "salary": "6 - 12 LPA (India Entry Level)"
    },
    "web developer": {
        "skills": ["html", "css", "javascript", "react", "node"],
        "salary": "3 - 8 LPA (India Entry Level)"
    },
    "cyber security": {
        "skills": ["networking", "linux", "ethical hacking", "python", "cryptography"],
        "salary": "5 - 10 LPA (India Entry Level)"
    }
}

# Folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Serve HTML, CSS, JS files or simple server message"""
        if self.path == "/":
            filepath = os.path.join(BASE_DIR, "index.html")
            content_type = "text/html"
        elif self.path.endswith(".css"):
            filepath = os.path.join(BASE_DIR, self.path[1:])
            content_type = "text/css"
        elif self.path.endswith(".js"):
            filepath = os.path.join(BASE_DIR, self.path[1:])
            content_type = "application/javascript"
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")
            return

        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Server error: cannot read file")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/analyze":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)

                user_input = data.get("skills", "")
                dream_job = data.get("dream_job", "").lower()
                user_skills = [
                    skill.strip().lower()
                    for skill in user_input.split(",") if skill.strip() != ""
                ]

                if dream_job not in job_database:
                    response = {"error": "Job role not found."}
                else:
                    required_skills = job_database[dream_job]["skills"]
                    salary = job_database[dream_job]["salary"]
                    matched_skills = [s for s in required_skills if s in user_skills]
                    missing_skills = [s for s in required_skills if s not in user_skills]
                    score = (len(matched_skills) / len(required_skills)) * 100

                    if score >= 70:
                        message = "✅ You are placement ready! Improve projects and apply."
                    elif score >= 40:
                        message = "⚠️ You are halfway there. Focus on missing skills."
                    else:
                        message = "🚨 Skill gap is high. Build fundamentals first."

                    response = {
                        "dream_job": dream_job.title(),
                        "salary": salary,
                        "matched_skills": matched_skills,
                        "missing_skills": missing_skills,
                        "score": score,
                        "message": message
                    }
            except Exception as e:
                response = {"error": "Server error occurred."}

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()


# Run Server
if __name__ == "__main__":
    server = HTTPServer(("localhost", 5000), RequestHandler)
    print("Server running at http://localhost:5000")
    server.serve_forever()
