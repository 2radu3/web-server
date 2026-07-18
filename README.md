# web-server

The system operates as a classic structural pipeline connecting a web client all the way through to a modern web application framework:

[Web Client: Browser / cURL]
       │
       │ (HTTP Request / Response)
       ▼
[Custom Web Server: This Project]
       │
       │ (WSGI Environment / Application Interface)
       ▼
[Web Application: Flask / Django / Pyramid]

---
