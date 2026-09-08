// استبدل الرابط الوهمي بالروابط الفعلية لخدماتك
const AUTH_BASE = "https://auth-service-h31r.onrender.com";
const API_BASE = "https://aggregator-ncjl.onrender.com";

let sessionToken = "";

async function authenticate() {
    const p1 = document.getElementById("p1").value;
    const p2 = document.getElementById("p2").value;
    const p3 = document.getElementById("p3").value;

    if (!p1 || !p2 || !p3) {
        alert("يرجى إدخال كلمات المرور الثلاث");
        return;
    }

    try {
        const res = await fetch(`${AUTH_BASE}/auth`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pass1: p1, pass2: p2, pass3: p3 })
        });

        const data = await res.json();
        if (res.ok) {
            sessionToken = data.token;
            document.getElementById("auth").style.display = "none";
            document.getElementById("search").style.display = "block";
            document.getElementById("query").focus();
        } else {
            alert("❌ كلمات المرور غير صحيحة");
        }
    } catch (e) {
        alert("⚠️ خطأ في الاتصال بالخادم");
    }
}

async function doSearch() {
    const query = document.getElementById("query").value.trim();
    if (!query) return;

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<div style='text-align:center;padding:30px;'>⏳ جاري البحث...</div>";

    try {
        const res = await fetch(`${API_BASE}/search`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${sessionToken}`
            },
            body: JSON.stringify({ query })
        });

        const data = await res.json();
        if (!Array.isArray(data)) throw new Error("Invalid response");

        if (data.length === 0) {
            resultsDiv.innerHTML = "<div style='text-align:center;color:#888;'>🔍 لا توجد نتائج</div>";
            return;
        }

        resultsDiv.innerHTML = data.map(item => `
            <div class="result-item">
                <span class="source">${item.source || "Unknown"}</span>
                <span class="ip">${item.ip || "N/A"}:${item.port || "?"}</span>
                <div class="banner">${(item.banner || "").slice(0, 200)}</div>
                ${item.cve && item.cve.length > 0 ? `<div style="color:#ff5555;">🔴 ${item.cve.join(", ")}</div>` : ""}
            </div>
        `).join("");

    } catch (e) {
        resultsDiv.innerHTML = `<div style="color:#ff5555;">❌ خطأ: ${e.message}</div>`;
    }
}

document.getElementById("query").addEventListener("keypress", function(e) {
    if (e.key === "Enter") doSearch();
});