# Video Calling Solution with Django and Zego Cloud SDK

This Django project implements a video calling solution using the Zego Cloud SDK. With this solution, users can establish real-time video calls with each other over the internet.

## Features

- **User Authentication**: Users can sign up, log in, and manage their accounts.
- **Video Calling**: Seamless video calling experience powered by Zego Cloud SDK.
- **Responsive Design**: Works seamlessly across different devices and screen sizes.

## Requirements

- Python 3.11
- Django 5.0.2
- Zego Cloud SDK
- Modern web browser with WebRTC support

## Installation

1. Clone the repository:

   ```bash
   git clone <https://github.com/Kavyashah26/Let-s-Meet-Django-Project>
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Django development server:

   ```bash
   python manage.py runserver
   ```

2. Access the application in your web browser:

   ```
   http://localhost:8000
   ```

3. Sign up for an account and start making video calls!

### Project Structure

*   `baseapp`: The main Django app containing models, views, and templates.
*   `LetsMeet`: The Django app that redirects all work to baseapp .
*   `templates`: HTML templates for the user interface.
*   `static`: Static files such as CSS and JavaScript.


### Project Creator
This project was created by [Kavya Shah](https://github.com/Kavyashah26/)and [Dev Shah](https://github.com/Devs1203) as part of termwork of SP subject
