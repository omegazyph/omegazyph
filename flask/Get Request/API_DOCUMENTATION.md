# 🌐 Flask Request Handler API

This server-side script demonstrates basic routing and HTTP method handling using the **Flask** framework. It is designed to differentiate between standard browser requests and data submissions.

## 📌 Endpoint Overview

| Endpoint | Supported Methods | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Returns the current HTTP method being used. |
| `/bacon` | `GET`, `POST` | Responds with a unique message based on the request type. |

## 🧠 Technical Logic

The script utilizes the `request` object from the Flask library to inspect incoming traffic.

1. **GET Request**: Triggered when you visit a URL in your browser.
2. **POST Request**: Triggered when data is sent to the server (e.g., via a form or an API tool like Postman).

## 🚀 How to Run

1. **Install Flask** (if not already installed):

   ```bash
   pip install flask
