# Python Web Server
---
    The goal of this project is to demystify the magic behind web backends by stripping away complex third-party wrappers and dealing directly with low-level network sockets, protocol specifications, and process management.
    The system operates as a classic structural pipeline connecting a web client all the way through to a modern web application framework:
    
---

---

## Architecture Pipeline

               [ Web Client ]
                     │
                     ▼
       │─────────────────────────────│
       │      Custom Web Server      │
       │      (Parent Process)       │
       │─────────────────────────────│
                     │
            ┌────────┴────────┐
            ▼                 ▼
      [Child Proc A]    [Child Proc B]   ... (Scales per incoming request)
            │                 │
            ▼                 ▼
       [WSGI App]        [WSGI App]     (Flask / Django / Pyramid)

---
##  Requirements & Installation

* **Operating System**: Linux, macOS, or WSL (Windows Subsystem for Linux). *Note: The multi-processing layer uses UNIX system calls (`fork`) which are natively unsupported on Windows cmd/PowerShell.*
* **Python**: `Python 3.7+` (Uses native `socket`, `sys`, and `os` standard libraries).

1. Clone the repository:
   ```bash
   git clone https://github.com/2radu3/web-server.git
   cd web-server
   ```

2. Set up a virtual environment to install a framework to test the WSGI layer. Tested with Flask, Django, Pyramid
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install Flask
    pip install Django
    pip install Pyramid
    ```

---

## How to Run & Test

* **Running the Basic Server:**
    ```bash
    python3 webserver1.py
    ```
* Open a separate terminal window and verify the raw HTTP response headers using `curl`:

    ```bash
    curl -i http://localhost:8888/
    ```
    
* **Running the Concurrent WSGI Server:**

    Start the WSGI server by pointing it directly to your Flask application instance `(flaskapp:flask_app)`:

    ```python
    python3 wsgi_server.py app:flask_app
    ```

* **Running the concurrent server:**
    ```python
    python3 concurrent_server.py flaskapp:flask_app
    ```
    Test it with a specific amount of clients: 
    ```bash
    python3 clients.py --max-clients 128
    ```


