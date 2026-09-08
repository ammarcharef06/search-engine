package main

import (
    "crypto/rand"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "os"

    "github.com/ethereum/go-ethereum/crypto/keccak"
    "golang.org/x/crypto/argon2"
    "golang.org/x/crypto/chacha20poly1305"
)

var salt = os.Getenv("SALT")
var encryptedKeys []byte

// دالة التشفير الجهني
func deriveKey(p1, p2, p3 string) ([]byte, error) {
    // 1. دمج المدخلات
    concat := fmt.Sprintf("%s:%s:%s:%s", p1, p2, p3, salt)

    // 2. Argon2id (مقاوم للـ GPU/ASIC)
    hash1 := argon2.IDKey(
        []byte(concat),
        []byte(salt),
        10,          // الوقت
        256*1024,    // الذاكرة (256MB)
        4,           // الخيوط
        64,          // المخرجات 64 بايت
    )

    // 3. Keccak-1024 (إضافة طبقة كمومية)
    keccakHash := keccak.New1024()
    keccakHash.Write(append(hash1, []byte(salt)...))
    hash2 := keccakHash.Sum(nil)

    // 4. XChaCha20-Poly1305 (تشفير المفتاح النهائي)
    nonce := make([]byte, chacha20poly1305.NonceSize)
    if _, err := rand.Read(nonce); err != nil {
        return nil, err
    }

    aead, err := chacha20poly1305.New(hash2)
    if err != nil {
        return nil, err
    }

    finalKey := aead.Seal(nil, nonce, hash2, nil)
    return finalKey, nil
}

// معالج المصادقة
func authHandler(w http.ResponseWriter, r *http.Request) {
    var req struct {
        Pass1 string `json:"pass1"`
        Pass2 string `json:"pass2"`
        Pass3 string `json:"pass3"`
    }

    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }

    // اشتقاق المفتاح
    key, err := deriveKey(req.Pass1, req.Pass2, req.Pass3)
    if err != nil {
        http.Error(w, "Crypto error", http.StatusInternalServerError)
        return
    }

    // محاولة فك تشفير ملف المفاتيح (للتحقق من صحة كلمات المرور)
    aead, err := chacha20poly1305.New(key)
    if err != nil {
        http.Error(w, "Invalid credentials", http.StatusUnauthorized)
        return
    }

    if len(encryptedKeys) < 24 {
        http.Error(w, "Invalid key file", http.StatusInternalServerError)
        return
    }

    nonce := encryptedKeys[:24]
    ciphertext := encryptedKeys[24:]

    _, err = aead.Open(nil, nonce, ciphertext, nil)
    if err != nil {
        http.Error(w, "Invalid credentials", http.StatusUnauthorized)
        return
    }

    // إنشاء رمز جلسة مؤقت (JWT-like)
    sessionToken := generateSessionToken()
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{
        "status":  "ok",
        "token":   sessionToken,
        "message": "تم المصادقة بنجاح",
    })
}

// توليد رمز جلسة عشوائي
func generateSessionToken() string {
    bytes := make([]byte, 32)
    rand.Read(bytes)
    return fmt.Sprintf("%x", bytes)
}

func main() {
    // قراءة ملف المفاتيح المشفر
    var err error
    encryptedKeys, err = ioutil.ReadFile("/run/secrets/api_keys.enc")
    if err != nil {
        log.Fatal("Failed to read encrypted keys:", err)
    }

    http.HandleFunc("/auth", authHandler)
    log.Println("Auth service running on :8081")
    log.Fatal(http.ListenAndServe(":8081", nil))
}