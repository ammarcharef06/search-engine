package main

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"golang.org/x/crypto/argon2"
	"golang.org/x/crypto/chacha20poly1305"
	"github.com/ethereum/go-ethereum/crypto/keccak"
)

var salt = os.Getenv("SALT")
var encryptedKeys []byte

func deriveKey(p1, p2, p3 string) []byte {
	concat := p1 + ":" + p2 + ":" + p3 + ":" + salt
	hash := argon2.IDKey([]byte(concat), []byte(salt), 10, 256*1024, 4, 64)
	keccakHash := keccak.New1024()
	keccakHash.Write(append(hash, []byte(salt)...))
	keccakOut := keccakHash.Sum(nil)
	nonce := make([]byte, chacha20poly1305.NonceSize)
	rand.Read(nonce)
	aead, _ := chacha20poly1305.New(keccakOut)
	return aead.Seal(nil, nonce, keccakOut, nil)
}

func authHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Pass1 string `json:"pass1"`
		Pass2 string `json:"pass2"`
		Pass3 string `json:"pass3"`
	}
	json.NewDecoder(r.Body).Decode(&req)

	key := deriveKey(req.Pass1, req.Pass2, req.Pass3)
	aead, _ := chacha20poly1305.New(key)
	_, err := aead.Open(nil, make([]byte, 24), encryptedKeys, nil)
	if err != nil {
		http.Error(w, "Invalid credentials", http.StatusUnauthorized)
		return
	}
	w.Write([]byte(`{"status":"ok"}`))
}

func main() {
	encryptedKeys, _ = ioutil.ReadFile("/run/secrets/api_keys.enc")
	http.HandleFunc("/auth", authHandler)
	log.Fatal(http.ListenAndServe(":8081", nil))
}