MikroTik AI Intrusion Detection System (IDS)
English | فارسی (Persian)

A simple but powerful Python-based Intrusion Detection System (IDS) that uses the MikroTik API to automatically detect and block port scanning attacks in real-time.

<a name="english"></a>

English
Overview
This project provides a Python script that connects to a MikroTik router, monitors its firewall logs for suspicious activity, and takes automated action to protect the network. It acts as an intelligent layer of security, identifying potential attackers by their behavior and blocking them before they can cause harm.

Features
Real-time Monitoring: Continuously watches firewall logs for new connection attempts.

Port Scan Detection: Implements a simple but effective logic to identify port scanning behavior (e.g., one IP trying to access many different ports in a short time).

Automated Blocking: Automatically adds any identified attacker's IP address to a firewall Address List, effectively blocking them from accessing the network.

Configurable: Easily adjust the sensitivity of the detection logic (thresholds for ports and time) within the script.

Lightweight: Can run on any machine on the local network, including a Raspberry Pi.

How It Works
The system follows a simple three-step architecture:

MikroTik (The Sensor/Enforcer): A firewall rule is configured to log all new incoming connection attempts. The router also holds a "block list" that it enforces.

Python Script (The Brain): The script connects to the MikroTik API, reads the firewall logs, analyzes them for patterns indicative of a port scan, and makes a decision.

API (The Connection): If an attacker is identified, the script sends a command back to the MikroTik router via the API to add the attacker's IP to the block list.

Requirements
A MikroTik router running RouterOS.

A computer or server on the same network (Windows, Linux, macOS).

Python 3.6+ installed on the computer/server.

The routeros-api Python library.

Setup Guide
Part 1: MikroTik Router Configuration
1. Create an API User:

In WinBox, go to System > Users.

In the Groups tab, create a new group named api-group with api, read, and write policies.

In the Users tab, create a new user named py-script, assign it to api-group, and set a strong password.

2. Enable the API Service:

Go to IP > Services.

Find the service named api and ensure it is enabled. The default port is 8728.

3. Create a Logging Firewall Rule:

Go to IP > Firewall > Filter Rules.

Create a new rule:

General Tab: Chain=input, Connection State=new, In. Interface=<your-WAN-interface> (e.g., ether1).

Action Tab: Action=log, check the Log box, and set Log Prefix="PORT_SCAN_LOG".

Move this rule to the top of your firewall list.

4. Create a "Block List" for Attackers:

Go to IP > Firewall > Address Lists.

Create a new list named blocked_attackers.

5. Create a Blocking Firewall Rule:

Go back to IP > Firewall > Filter Rules.

Create a new rule:

General Tab: Chain=input.

Advanced Tab: Src. Address List=blocked_attackers.

Action Tab: Action=drop.

Move this rule to be just below your logging rule.

Part 2: Python Script Setup
1. Download the Code:

Clone this repository or download the ids_script.py file to your server.

2. Install Dependencies:

Open a terminal or command prompt and run:

pip install routeros-api

3. Configure the Script:

Open ids_script.py in a text editor.

Update the configuration variables at the top of the file with your router's details:

MIKROTIK_HOST = '192.168.88.1'  # Your router's IP
MIKROTIK_USER = 'py-script'      # The API username you created
MIKROTIK_PASS = 'your_password'  # The API password you set

Running the Script
To start the IDS, simply run the script from your terminal:

python ids_script.py

The script will connect to the router and begin monitoring. You will see output in the console when an attack is detected and blocked.

Running with Docker
You can also run this project inside a Docker container for easier deployment and dependency management.

1. Build the Docker Image:
Ensure you have Docker installed. Then, open your terminal in the project directory (where the Dockerfile is) and run:

docker build -t mikrotik-ai-ids .

2. Run the Docker Container:
After building the image, run the container with this command:

docker run --name my-ids-container --restart unless-stopped -d mikrotik-ai-ids

--name: Gives your container a memorable name.

--restart unless-stopped: Ensures the container automatically restarts if the server reboots.

-d: Runs the container in detached mode (in the background).

To see the live logs of your running container, use this command:

docker logs -f my-ids-container

Disclaimer
This script is provided as a proof-of-concept. While it is effective, please test it thoroughly in a controlled environment before deploying it in a critical production network.

<a name="persian"></a>

فارسی (Persian)
معرفی
این پروژه یک سیستم تشخیص نفوذ (IDS) مبتنی بر پایتون است که با استفاده از API میکروتیک، حملات اسکن پورت (Port Scanning) را به صورت خودکار و لحظه‌ای شناسایی و مسدود می‌کند.

ویژگی‌ها
مانیتورینگ لحظه‌ای: به طور مداوم لاگ‌های فایروال را برای تلاش‌های اتصال جدید نظارت می‌کند.

شناسایی اسکن پورت: با استفاده از یک منطق ساده اما مؤثر، رفتار اسکن پورت را شناسایی می‌کند (به عنوان مثال، یک IP که در زمان کوتاه به پورت‌های مختلف زیادی دسترسی پیدا می‌کند).

مسدودسازی خودکار: به صورت اتوماتیک آدرس IP مهاجم شناسایی‌شده را به یک Address List در فایروال اضافه کرده و دسترسی آن را به شبکه قطع می‌کند.

قابل تنظیم: حساسیت منطق تشخیص (آستانه تعداد پورت‌ها و بازه زمانی) به راحتی در داخل اسکریپت قابل تغییر است.

سبک و کم‌حجم: قابلیت اجرا بر روی هر دستگاهی در شبکه محلی، از جمله یک رزبری پای را دارد.

نحوه عملکرد
این سیستم از یک معماری سه مرحله‌ای ساده پیروی می‌کند:

روتر میکروتیک (سنسور و مجری): یک قانون فایروال برای ثبت (Log) تمام تلاش‌های اتصال ورودی جدید تنظیم می‌شود. روتر همچنین لیستی از IPهای مسدود شده را نگهداری و اجرا می‌کند.

اسکریپت پایتون (مغز متفکر): این اسکریپت به API میکروتیک متصل شده، لاگ‌های فایروال را می‌خواند، آن‌ها را برای یافتن الگوهای مشکوک به اسکن پورت تحلیل کرده و تصمیم‌گیری می‌کند.

رابط API (ارتباط): اگر یک مهاجم شناسایی شود، اسکریپت از طریق API دستوری را به روتر میکروتیک ارسال می‌کند تا IP مهاجم را به لیست مسدودی‌ها اضافه کند.

پیش‌نیازها
یک روتر میکروتیک با سیستم‌عامل RouterOS.

یک کامپیوتر یا سرور در همان شبکه (ویندوز، لینوکس، مک).

پایتون نسخه ۳.۶ یا بالاتر نصب شده بر روی کامپیوتر/سرور.

کتابخانه پایتون routeros-api.

راهنمای راه‌اندازی
بخش ۱: تنظیمات روتر میکروتیک
۱. ساخت کاربر API:

در WinBox به منوی System > Users بروید.

در تب Groups، یک گروه جدید به نام api-group با دسترسی‌های api, read و write بسازید.

در تب Users، یک کاربر جدید به نام py-script بسازید، آن را به گروه api-group اختصاص دهید و یک رمز عبور قوی برای آن تنظیم کنید.

۲. فعال‌سازی سرویس API:

به IP > Services بروید.

سرویس api را پیدا کرده و مطمئن شوید که فعال (Enable) است. پورت پیش‌فرض 8728 است.

۳. ساخت قانون فایروال برای لاگ‌برداری:

به IP > Firewall > Filter Rules بروید.

یک قانون جدید ایجاد کنید:

تب General: Chain=input, Connection State=new, In. Interface=<اینترفیس-WAN-شما> (مثلاً ether1).

تب Action: Action=log، تیک گزینه Log را بزنید و Log Prefix="PORT_SCAN_LOG" را تنظیم کنید.

این قانون را به بالای لیست فایروال خود منتقل کنید.

۴. ساخت "لیست مسدودی" برای مهاجمان:

به IP > Firewall > Address Lists بروید.

یک لیست جدید به نام blocked_attackers ایجاد کنید.

۵. ساخت قانون فایروال برای مسدودسازی:

به IP > Firewall > Filter Rules برگردید.

یک قانون جدید ایجاد کنید:

تب General: Chain=input.

تب Advanced: Src. Address List=blocked_attackers.

تب Action: Action=drop.

این قانون را درست به زیر قانون لاگ‌برداری خود منتقل کنید.

بخش ۲: تنظیمات اسکریپت پایتون
۱. دانلود کد:

این مخزن (Repository) را Clone کرده یا فایل ids_script.py را بر روی سرور خود دانلود کنید.

۲. نصب پیش‌نیازها:

یک ترمینال یا Command Prompt باز کرده و دستور زیر را اجرا کنید:

pip install routeros-api

۳. تنظیم اسکریپت:

فایل ids_script.py را با یک ویرایشگر متن باز کنید.

متغیرهای تنظیمات در بالای فایل را با اطلاعات روتر خود به‌روزرسانی کنید:

MIKROTIK_HOST = '192.168.88.1'  # IP روتر شما
MIKROTIK_USER = 'py-script'      # نام کاربری API که ساختید
MIKROTIK_PASS = 'your_password'  # رمز عبور API که تنظیم کردید

اجرای اسکریپت
برای شروع به کار سیستم، کافیست اسکریپت را از طریق ترمینال اجرا کنید:

python ids_script.py

اسکریپت به روتر متصل شده و مانیتورینگ را آغاز می‌کند. هنگام شناسایی و مسدودسازی یک حمله، خروجی مربوطه در کنسول نمایش داده خواهد شد.

اجرا با داکر (Docker)
شما همچنین می‌توانید این پروژه را برای مدیریت ساده‌تر وابستگی‌ها و استقرار آسان، داخل یک کانتینر داکر اجرا کنید.

۱. ساخت ایمیج داکر:
مطمئن شوید داکر روی سیستم شما نصب است. سپس ترمینال خود را در پوشه پروژه (جایی که Dockerfile قرار دارد) باز کرده و دستور زیر را اجرا کنید:

docker build -t mikrotik-ai-ids .

۲. اجرای کانتینر داکر:
پس از ساخت ایمیج، کانتینر را با دستور زیر اجرا کنید:

docker run --name my-ids-container --restart unless-stopped -d mikrotik-ai-ids

--name: یک نام مشخص برای کانتینر شما تعیین می‌کند.

--restart unless-stopped: تضمین می‌کند که اگر سرور ریبوت شد، کانتینر به صورت خودکار دوباره اجرا شود.

-d: کانتینر را در حالت detached (در پس‌زمینه) اجرا می‌کند.

برای مشاهده لاگ‌های زنده کانتینر در حال اجرا، از دستور زیر استفاده کنید:

docker logs -f my-ids-container

سلب مسئولیت
این اسکریپت به عنوان یک نمونه مفهومی (Proof-of-Concept) ارائه شده است. اگرچه این اسکریپت کارآمد است، لطفاً قبل از استفاده از آن در یک شبکه حساس و عملیاتی، آن را به طور کامل در یک محیط آزمایشی تست کنید.
