// Force dark theme only
(function () {
  const root = document.documentElement;
  root.classList.remove("light");
  try {
    localStorage.removeItem("theme");
  } catch (e) {}
})();

// Mobile nav toggle
(function () {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      links.classList.toggle("open");
    });
    links
      .querySelectorAll("a")
      .forEach((a) =>
        a.addEventListener("click", () => links.classList.remove("open"))
      );
  }
})();

// Intersection Observer reveal + nav highlight
(function () {
  const sections = document.querySelectorAll("section");
  const reveals = document.querySelectorAll(".reveal");
  const navLinks = document.querySelectorAll(".nav-link");

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.12 }
  );
  reveals.forEach((el) => revealObserver.observe(el));

  const spy = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          const id = e.target.id;
          navLinks.forEach((l) => {
            const isActive = l.getAttribute("href") === `#${id}`;
            l.classList.toggle("active", isActive);
          });
        }
      });
    },
    { rootMargin: "-40% 0px -55% 0px", threshold: [0, 0.2, 0.6] }
  );
  sections.forEach((s) => spy.observe(s));
})();

// Contact form (mailto fallback)
(function () {
  const form = document.getElementById("contactForm");
  const status = document.getElementById("formStatus");
  if (!form) return;
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const name = encodeURIComponent(data.get("name"));
    const email = encodeURIComponent(data.get("email"));
    const message = encodeURIComponent(data.get("message"));
    const mailto = `mailto:arvindguru83@gmail.com?subject=Portfolio%20Contact%20from%20${name}&body=${message}%0A%0AReply%20to:%20${email}`;
    status.textContent = "Opening your email client...";
    window.location.href = mailto;
    setTimeout(() => {
      status.textContent =
        "If your email client did not open, email me directly.";
    }, 1200);
  });
})();

// Year
document.getElementById("year").textContent = new Date().getFullYear();

// Vanta NET background on hero
(function () {
  const el = document.getElementById("vanta-net");
  if (el && typeof VANTA !== "undefined" && VANTA.NET) {
    VANTA.NET({
      el,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.0,
      minWidth: 200.0,
      scale: 1.0,
      scaleMobile: 1.0,
      color: 0x2f40cd,
      backgroundColor: 0x030305,
    });
  }
  // Use only one Vanta instance for both Home and About; background is fixed
})();

// Simple chat widget calling local RAG bot
(function () {
  const toggle = document.getElementById("chatToggle");
  const box = document.getElementById("chatBox");
  const closeBtn = document.getElementById("chatClose");
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatPrompt");
  const messages = document.getElementById("chatMessages");
  if (!toggle || !box || !form) return;
  const API_URL = window.RAG_API_URL || "http://127.0.0.1:5000/chat";

  function addMsg(text, who) {
    const el = document.createElement("div");
    el.className = `msg ${who}`;
    el.textContent = text;
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }
  toggle.addEventListener("click", () => {
    box.hidden = !box.hidden;
    if (!box.hidden) input.focus();
  });
  closeBtn &&
    closeBtn.addEventListener("click", () => {
      box.hidden = true;
    });
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const prompt = input.value.trim();
    if (!prompt) return;
    addMsg(prompt, "user");
    input.value = "";
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      addMsg(data.response || "No response", "bot");
    } catch (err) {
      addMsg(
        "Error contacting bot. Is the backend running on 127.0.0.1:5000?",
        "bot"
      );
    }
  });
})();
