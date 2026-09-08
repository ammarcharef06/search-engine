#!/bin/bash
set -e

echo "🚀 بدء نشر محرك البحث الموحد..."

# توليد ملح عشوائي
export SALT=$(openssl rand -hex 32)
echo "SALT=$SALT" > .env

# توليد مفتاح التشفير الأساسي
export MASTER_KEY=$(openssl rand -hex 32)
echo "MASTER_KEY=$MASTER_KEY" >> .env

# تشفير ملف مفاتيح API
echo "🔐 تشفير مفاتيح API..."
python3 scripts/encrypt_keys.py

# بناء الحاويات
echo "📦 بناء الحاويات..."
docker-compose build

# تشغيل الخدمات
echo "▶️ تشغيل الخدمات..."
docker-compose up -d

# إعداد SSL (إن وجد اسم نطاق)
if [ ! -z "$DOMAIN" ]; then
    echo "🔒 تثبيت شهادة SSL..."
    docker run --rm -v /etc/letsencrypt:/etc/letsencrypt certbot/certbot certonly --standalone -d $DOMAIN
    cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem nginx/ssl/cert.pem
    cp /etc/letsencrypt/live/$DOMAIN/privkey.pem nginx/ssl/key.pem
    docker-compose restart nginx
fi

echo "✅ اكتمل النشر!"
echo "🌐 الرابط: https://search.your-domain.com"
echo "🔑 كلمات المرور الثلاث: (تم إرسالها بشكل منفصل)"