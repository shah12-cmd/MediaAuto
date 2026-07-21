# 🤖 MediaAuto - Professional Telegram Media Automation Bot

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/shah12-cmd/MediaAuto?style=social)](https://github.com/shah12-cmd/MediaAuto)

یک ربات حرفه‌ای Python برای خودکارسازی انتشار محتوا در تلگرام. **MediaAuto** به صورت 24/7 روی VPS اجرا می‌شود و تمام مدیریت از طریق رابط کاربری تلگرام انجام می‌شود.

## ✨ ویژگی‌های اصلی

### 🎯 دریافت خودکار محتوا
- دریافت پست‌های جدید از چند کانال تلگرام
- پشتیبانی از عکس، ویدیو، GIF، فایل و آلبوم
- جلوگیری از ارسال محتوای تکراری
- ذخیره تاریخچه کامل ارسال‌ها

### 📝 پردازش متقدم محتوا
- حذف خودکار لینک‌های کانال مبدا
- حذف آیدی‌های کانال و شناسه‌های خصوصی
- حذف تبلیغات نامناسب
- حذف هشتگ‌های اضافی
- اضافه کردن متن و تبلیغات دلخواه

### 🎨 بهبود ظاهری
- افزودن واترمارک به عکس و ویدیو
- اضافه کردن ایموجی برای جذاب‌تر کردن متن
- ویرایش اختیاری کپشن

### 🕐 زمان‌بندی هوشمند
- ۵ دقیقه
- ۱۰ دقیقه
- ۳۰ دقیقه
- ۱ ساعت
- زمان دلخواه

### 🤖 هوش مصنوعی (اختیاری)
- بازنویسی هوشمند کپشن
- کوتاه‌کردن متن طولانی
- جذاب‌کردن محتوا
- ترجمه خودکار به فارسی
- یکی‌سازی ایموجی‌ها

### 💾 ذخیره‌سازی و پشتیبان‌گیری
- پشتیبانی از SQLite و PostgreSQL
- بکاپ خودکار دریافت‌ها
- ثبت تفصیلی لاگ‌ها
- صیانت‌پذیری کامل داده‌ها

### 🔐 امنیت
- رمز مدیریت برای دسترسی
- احراز هویت Telethon
- پشتیبانی از تایید دو مرحله‌ای
- رمزگذاری اطلاعات حساس

### 🖥️ مدیریت راحت
- تمام تنظیمات از طریق دکمه‌های تلگرام
- نمایش آمار و گزارش‌ها
- مشاهده لاگ‌های زنده
- ری‌استارت سریع

### 🐳 استقرار
- پشتیبانی Docker و Docker Compose
- خودکار اجرا با systemd
- نصب یک‌دستوری

## 🚀 نصب و راه‌اندازی سریع

### متطلبات سیستمی
- **OS**: Ubuntu 22.04 / Ubuntu 24.04
- **Python**: 3.11 یا بالاتر
- **RAM**: حداقل 512 MB
- **Storage**: حداقل 1 GB برای دیتابیس و رسانه‌ها

### نصب خودکار (توص��ه شده)

```bash
git clone https://github.com/shah12-cmd/MediaAuto.git
cd MediaAuto
bash install.sh
```

**نصب شامل موارد زیر است:**
1. ✅ نصب تمام وابستگی‌های Python
2. ✅ ایجاد محیط مجازی (Virtual Environment)
3. ✅ تنظیم توکن تلگرام
4. ✅ تنظیم API تلگرام
5. ✅ پیکربندی کانال‌های مبدا و مقصد
6. ✅ انتخاب بازه‌های ارسال
7. ✅ تنظیم واترمارک (اختیاری)
8. ✅ فعال‌سازی هوش مصنوعی (اختیاری)
9. ✅ تنظیم عمل‌کرد خودکار با systemd

### اطلاعات مورد نیاز برای نصب

هنگام اجرای اسکریپت نصب، مراحل زیر پیش‌رو خواهد بود:

```
🤖 Telegram Bot Token
   از @BotFather در تلگرام دریافت کنید

🔑 Telegram API ID و API Hash
   از https://my.telegram.org دریافت کنید

📱 شماره تلگرام
   شماره‌ای که برای ورود استفاده می‌کنید

🔐 رمز مدیریت ربات
   برای دسترسی به تنظیمات

📥 کانال‌های مبدا
   شناسه کانال‌های منبع (مثال: @source_channel)

📤 کانال مقصد
   شناسه کانال هدف (مثال: @dest_channel)

⏰ بازه‌های ارسال
   انتخاب از 5 دقیقه تا 1 ساعت یا دلخواه

🤖 تنظیمات هوش مصنوعی (اختیاری)
   OpenAI، Anthropic یا Google API Key
```

## 🎮 استفاده

### شروع ربات

**روش 1: با systemd (پیشنهادی)**
```bash
sudo systemctl start mediauto
sudo systemctl status mediauto
```

**روش 2: اجرای مستقیم**
```bash
cd MediaAuto
./run.sh
```

### مدیریت رابط کاربری

```
/start - نمایش منو اصلی
```

**گزینه‌های منو:**

```
📥 مدیریت کانال‌های مبدا
   ➕ افزودن کانال
   ❌ حذف کانال
   📋 لیست کانال‌ها

📤 تنظیم کانال مقصد
   تنظیم مقصد ارسال پست‌ها

⏰ تنظیم زمان ارسال
   انتخاب بازه زمانی

📝 تنظیم متن تبلیغاتی
   افزودن متن دلخواه به کپشن

✏️ تنظیم ویرایش کپشن
   ✅/❌ حذف لینک‌ها
   ✅/❌ حذف آیدی‌ها
   ✅/❌ حذف تبلیغات
   ✅/❌ حذف هشتگ‌های اضافی

🤖 تنظیم هوش مصنوعی
   فعال‌سازی/غیرفعال‌سازی
   انتخاب پرومپت‌های AI

🖼 تنظیم واترمارک
   فعال‌سازی/غیرفعال‌سازی
   متن یا تصویر واترمارک

📊 آمار ربات
   تعداد پیام‌های ارسال شده
   تعداد کانال‌های فعال

📜 مشاهده لاگ‌ها
   نمایش آخرین 20 لاگ

⚙️ تنظیمات
   تنظیم‌های پیشرفته

🔄 ری‌استارت ربات
   دوباره‌راه‌اندازی برنامه
```

## 🐳 استفاده با Docker

### نصب Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### اجرا با Docker Compose

```bash
git clone https://github.com/shah12-cmd/MediaAuto.git
cd MediaAuto

# ویرایش docker-compose.yml و تنظیم متغیرهای محیط
nano docker-compose.yml

# اجرا
docker-compose up -d
```

### بررسی لاگ‌ها
```bash
docker-compose logs -f mediauto
```

## 📁 ساختار پروژه

```
MediaAuto/
├── mediauto/
│   ├── __init__.py              # پکیج اصلی
│   ├── main.py                  # برنامه اصلی
│   ├── config.py                # مدیریت پیکربندی
│   ├── database.py              # مدیریت دیتابیس
│   ├── logger.py                # تنظیم لاگ‌ها
│   ├── scheduler.py             # زمان‌بندی پیام‌ها
│   ├── content_processor.py     # پردازش محتوا
│   ├── telethon_client.py       # کلاینت Telethon
│   ├── bot_handler.py           # مدیریت رابط ربات
│   └── test_bot.py              # تست‌های واحد
├── data/                        # دیتابیس و رسانه‌ها
│   └── media/                   # فایل‌های دانلود شده
├── logs/                        # فایل‌های لاگ
├── backups/                     # نسخه‌های پشتیبان
├── config.json                  # پیکربندی ربات
├── requirements.txt             # وابستگی‌های Python
├── requirements-dev.txt         # وابستگی‌های توسعه
├── Dockerfile                   # پیکربندی Docker
├── docker-compose.yml           # Docker Compose
├── install.sh                   # اسکریپت نصب
├── run.sh                       # اسکریپت اجرا
└── README.md                    # این فایل
```

## ⚙️ تنظیمات پیشرفته

### فایل config.json

```json
{
    "telegram_token": "YOUR_BOT_TOKEN",
    "api_id": 123456789,
    "api_hash": "YOUR_API_HASH",
    "phone_number": "+989xxxxxxxxx",
    "admin_password": "YOUR_ADMIN_PASSWORD",
    "source_channels": ["@channel1", "@channel2"],
    "destination_channel": "@dest_channel",
    "send_delay": 600,
    "ad_text": "Follow us for more content",
    "ai_enabled": true,
    "ai_provider": "openai",
    "ai_api_key": "sk-...",
    "watermark_enabled": true,
    "watermark_text": "© MediaAuto",
    "database_type": "sqlite",
    "database_url": "sqlite:///./data/mediauto.db",
    "remove_channel_links": true,
    "remove_channel_ids": true,
    "remove_ads": true,
    "remove_extra_hashtags": true,
    "save_files": true,
    "files_directory": "./data/media",
    "backup_enabled": true,
    "backup_interval": 3600,
    "log_level": "INFO"
}
```

### متغیرهای محیط

```bash
export TELEGRAM_TOKEN="your_token"
export API_ID=123456789
export API_HASH="your_api_hash"
export DATABASE_URL="postgresql://user:pass@localhost/mediauto"
export LOG_LEVEL="DEBUG"
```

## 📊 مراقبت و نگهداری

### مشاهده لاگ‌ها

```bash
# systemd
sudo journalctl -u mediauto -f

# فایل
tail -f logs/mediauto_*.log

# Docker
docker-compose logs -f mediauto
```

### بکاپ دیتابیس

```bash
# SQLite
cp data/mediauto.db backups/mediauto_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL
pg_dump -U mediauto mediauto > backups/mediauto_$(date +%Y%m%d_%H%M%S).sql
```

### بازدر آوری از بکاپ

```bash
# SQLite
cp backups/mediauto_backup.db data/mediauto.db

# PostgreSQL
psql -U mediauto mediauto < backups/mediauto_backup.sql
```

## 🧪 تست

### اجرای تست‌ها

```bash
# نصب وابستگی‌های توسعه
pip install -r requirements-dev.txt

# اجرای تست‌ها
python -m pytest mediauto/test_bot.py -v

# بررسی کد
flake8 mediauto/
mypy mediauto/

# قالب‌بندی کد
black mediauto/
```

## 🔗 منابع مفید

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Telethon Documentation](https://docs.telethon.dev/)
- [OpenAI API](https://platform.openai.com/docs)
- [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/)

## 🐛 عیب‌یابی

### مشکل: ربات متصل نمی‌شود

```bash
# بررسی لاگ‌ها
sudo journalctl -u mediauto -n 50

# بررسی توکن و API credentials
cat config.json

# تست اتصال
python -c "from telegram import Bot; Bot('YOUR_TOKEN').get_me()"
```

### مشکل: رسانه‌های دانلود نمی‌شوند

```bash
# بررسی دسترسی فایل
ls -la data/media/

# بررسی فضای خالی
df -h data/

# بررسی دسترسی Telethon
python -m mediauto.telethon_client
```

### مشکل: پیام‌های ارسال نمی‌شوند

```bash
# بررسی دسترسی کانال مقصد
# اطمینان از اینکه ربات admin کانال مقصد باشد

# بررسی تنظیمات کانال
cat config.json | grep destination_channel
```

## 📝 نوشتن لاگ دلخواه

```python
from mediauto.logger import logger

logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.debug("Debug message")
```

## 🤝 مشارکت

مشارکت در پروژه به‌استقبال می‌آید! لطفا:

1. Fork کنید
2. یک branch جدید ایجاد کنید (`git checkout -b feature/AmazingFeature`)
3. تغییرات را commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. برای branch push کنید (`git push origin feature/AmazingFeature`)
5. یک Pull Request باز کنید

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای جزئیات بیشتر [`LICENSE`](LICENSE) را ببینید.

## ⚠️ سلب مسئولیت

این ابزار برای مقاصد آموزشی و قانونی طراحی شده است. استفاده کننده مسئول هرگونه استفاده غیرقانونی یا نادرست از آن است.

## 📞 تماس و پشتیبانی

- 📧 Email: support@mediauto.dev
- 🐛 Issues: [GitHub Issues](https://github.com/shah12-cmd/MediaAuto/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/shah12-cmd/MediaAuto/discussions)

---

**ساخته شده با ❤️ برای انجمن تلگرام**

⭐ اگر این پروژه برایتان مفید بود، لطفاً یک ستاره بدهید!

