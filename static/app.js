// State
let isSignUpMode = false;

// DOM Elements
const userNav = document.getElementById("user-nav");
const userEmail = document.getElementById("user-email");
const logoutBtn = document.getElementById("logout-btn");

const authContainer = document.getElementById("auth-container");
const authTitle = document.getElementById("auth-title");
const authSubtitle = document.getElementById("auth-subtitle");
const authError = document.getElementById("auth-error");
const authForm = document.getElementById("auth-form");
const authSubmit = document.getElementById("auth-submit");
const authToggleBtn = document.getElementById("auth-toggle-btn");
const authToggleText = document.getElementById("auth-toggle-text");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const chatContainer = document.getElementById("chat-container");
const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatSend = document.getElementById("chat-send");
const chatError = document.getElementById("chat-error");

// Toggle Auth Mode (Sign in vs Sign up)
authToggleBtn.addEventListener("click", () => {
    isSignUpMode = !isSignUpMode;
    authError.classList.add("hidden");
    if (isSignUpMode) {
        authTitle.textContent = "Create an account";
        authSubtitle.textContent = "Sign up to start chatting with AI";
        authSubmit.textContent = "Sign up";
        authToggleText.textContent = "Already have an account?";
        authToggleBtn.textContent = "Sign in";
    } else {
        authTitle.textContent = "Welcome to Anza";
        authSubtitle.textContent = "Sign in to start chatting with AI";
        authSubmit.textContent = "Sign in";
        authToggleText.textContent = "Don't have an account?";
        authToggleBtn.textContent = "Sign up";
    }
});

// Check Session on Page Load
async function checkAuth() {
    try {
        const res = await fetch("/api/me");
        if (res.ok) {
            const data = await res.json();
            showChat(data.user.email);
        } else {
            showAuth();
        }
    } catch {
        showAuth();
    }
}

function showChat(email) {
    userEmail.textContent = email;
    userNav.classList.remove("hidden");
    userNav.classList.add("flex");
    authContainer.classList.add("hidden");
    chatContainer.classList.remove("hidden");
    chatInput.focus();
}

function showAuth() {
    userNav.classList.add("hidden");
    userNav.classList.remove("flex");
    chatContainer.classList.add("hidden");
    authContainer.classList.remove("hidden");
}

// Handle Auth Form Submission
authForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    authError.classList.add("hidden");
    authSubmit.disabled = true;

    const endpoint = isSignUpMode ? "/api/signup" : "/api/login";
    try {
        const res = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: emailInput.value,
                password: passwordInput.value,
            }),
        });
        const data = await res.json();
        if (!res.ok) {
            authError.textContent = data.detail || "Authentication failed";
            authError.classList.remove("hidden");
        } else {
            emailInput.value = "";
            passwordInput.value = "";
            showChat(data.user.email);
        }
    } catch (err) {
        authError.textContent = "Network error. Please try again.";
        authError.classList.remove("hidden");
    } finally {
        authSubmit.disabled = false;
    }
});

// Handle Logout
logoutBtn.addEventListener("click", async () => {
    try {
        await fetch("/api/logout", { method: "POST" });
    } finally {
        showAuth();
    }
});

// Chat UI Helpers
function appendMessage(text, isUser = false) {
    const wrapper = document.createElement("div");
    wrapper.className = isUser ? "flex justify-end" : "flex justify-start";

    const bubble = document.createElement("div");
    bubble.className = isUser
        ? "max-w-lg bg-indigo-600 text-white rounded-2xl rounded-tr-sm px-4 py-2.5 text-sm shadow-sm whitespace-pre-wrap"
        : "max-w-lg bg-slate-100 text-slate-800 rounded-2xl rounded-tl-sm px-4 py-2.5 text-sm shadow-sm whitespace-pre-wrap";
    bubble.textContent = text;

    wrapper.appendChild(bubble);
    chatMessages.appendChild(wrapper);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return bubble;
}

// Handle Chat Message Submission
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage(message, true);
    chatInput.value = "";
    chatError.classList.add("hidden");
    chatSend.disabled = true;

    const loadingBubble = appendMessage("Thinking...", false);
    loadingBubble.classList.add("opacity-60", "italic");

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });
        const data = await res.json();
        if (!res.ok) {
            loadingBubble.textContent = "Error: " + (data.detail || "Unable to get response");
            loadingBubble.classList.add("text-red-600");
        } else {
            loadingBubble.textContent = data.reply;
        }
    } catch {
        loadingBubble.textContent = "Network error communicating with AI server.";
        loadingBubble.classList.add("text-red-600");
    } finally {
        loadingBubble.classList.remove("opacity-60", "italic");
        chatSend.disabled = false;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        chatInput.focus();
    }
});

// Register Service Worker for PWA
if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker.register("/sw.js").catch(() => {});
    });
}

// Initialize
checkAuth();
