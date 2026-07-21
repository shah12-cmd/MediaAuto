# مشارکت در MediaAuto

تشکر از علاقه‌مندی برای کمک به MediaAuto!

## راهنمای مشارکت

### قبل از شروع

1. مخزن را Fork کنید
2. مخزن را Clone کنید: `git clone https://github.com/YOUR_USERNAME/MediaAuto.git`
3. وابستگی‌ها را نصب کنید: `pip install -r requirements-dev.txt`

### مراحل

1. یک branch جدید ایجاد کنید:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. تغییرات را انجام دهید و آن‌ها را test کنید:
   ```bash
   python -m pytest
   flake8 mediauto/
   black mediauto/
   ```

3. تغییرات را commit کنید:
   ```bash
   git commit -m 'Add: description of changes'
   ```

4. برای branch push کنید:
   ```bash
   git push origin feature/your-feature-name
   ```

5. یک Pull Request باز کنید

### استاندارد کدنویسی

- از Black برای قالب‌بندی استفاده کنید
- از type hints استفاده کنید
- تست‌های واحد برای ویژگی‌های جدید بنویسید
- مستندات را به‌روز کنید

### Commit Messages

```
Type: Description

Detailed explanation if needed.

Types: Add, Fix, Update, Remove, Refactor, Test, Docs
```

مثال:
```
Add: Support for MongoDB database

Implements MongoDB adapter with connection pooling
and automatic migration support.
```

### Pull Requests

- عنوان واضح و شفاف بنویسید
- توضیح کامل از تغییرات ارائه دهید
- اگر issue مرتبط‌ای وجود دارد، آن را reference کنید
- تست‌های جدید اضافه کنید

### سوالات و پیشنهادات

- برای سوالات عمومی: [GitHub Discussions](https://github.com/shah12-cmd/MediaAuto/discussions)
- برای bugs: [GitHub Issues](https://github.com/shah12-cmd/MediaAuto/issues)
- برای feature requests: [GitHub Issues](https://github.com/shah12-cmd/MediaAuto/issues)
