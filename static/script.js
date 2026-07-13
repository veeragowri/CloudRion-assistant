let selectedService = "";
let productsLoaded = false;
let demoMode = false;
let supportMode = false;
let contactMode = false;
let demoCompleted = false;
let flowCompleted = false;
let activeDateTimePickerId = null;
let selectedProduct = "";

const chatBox = document.getElementById("chat-box");

const BOT_AVATAR = `
    <div class="bot-avatar" aria-hidden="true">
        <img src="/static/images/cloudrion-c-logo.png?v=circle3" alt="" class="brand-mark brand-mark--avatar">
    </div>
`;
const AVATAR_SPACER = `<div class="bot-avatar-spacer" aria-hidden="true"></div>`;

function resetFlowModes() {
    demoMode = false;
    supportMode = false;
    contactMode = false;
}

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function formatBotText(text) {
    return text.replace(/\n/g, "<br>").replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
}

function botRowHtml(bubbleHtml, buttonsHtml = "") {
    return `
        <div class="bot-row">
            ${BOT_AVATAR}
            <div class="bot-content">
                <div class="bot-bubble">${bubbleHtml}</div>
                ${buttonsHtml ? `<div class="service-buttons">${buttonsHtml}</div>` : ""}
            </div>
        </div>
    `;
}

function appendUserMessage(message) {
    chatBox.innerHTML += `
        <div class="user-row">
            <div class="user-bubble">${message}</div>
        </div>
    `;
    scrollToBottom();
}

function appendBotMessage(text, buttonsHtml = "") {
    chatBox.innerHTML += botRowHtml(formatBotText(text), buttonsHtml);
    scrollToBottom();
}

function appendServiceButtons(buttons) {
    chatBox.innerHTML += `
        <div class="bot-row service-row">
            ${AVATAR_SPACER}
            <div class="service-buttons">${buttons}</div>
        </div>
    `;
    scrollToBottom();
}

function showTyping() {
    chatBox.innerHTML += `
        <div class="bot-row typing" id="typing">
            ${BOT_AVATAR}
            <div class="bot-bubble typing-bubble">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
    `;
    scrollToBottom();
}

function hideTyping() {
    const typing = document.getElementById("typing");
    if (typing) {
        typing.remove();
    }
}

function renderActionButtons(buttons) {
    if (!buttons || !buttons.length) {
        return;
    }

    appendServiceButtons(
        buttons.map(btn => `
            <button onclick="handleButtonAction('${btn.action}')">${btn.label}</button>
        `).join("")
    );
}

function handleButtonAction(action) {
    switch (action) {
        case "book_demo":
            showDemoOptions();
            break;
        case "continue_asking":
            selectedService = "question";
            resetFlowModes();
            appendBotMessage("Sure! What else would you like to know about CloudRion?");
            break;
        case "learn_more":
            if (selectedProduct) {
                showLearnMore(selectedProduct);
            }
            break;
        case "contact_sales":
            showContactInfo(selectedProduct || null);
            break;
    }
}

function handleFlowResponse(data) {
    const responseText = data.response || data.message || "Sorry, something went wrong. Please try again.";
    appendBotMessage(responseText);

    if (data.products) {
        appendServiceButtons(
            data.products.map(product => `
                <button onclick="selectFlowProduct('${product}')">${product}</button>
            `).join("")
        );
    }

    if (data.datetime_picker) {
        renderDateTimePicker();
    }

    if (data.buttons) {
        renderActionButtons(data.buttons);
    }

    if (isCompletionMessage(responseText)) {
        flowCompleted = true;
        resetFlowModes();
        appendServiceButtons(`
            <button onclick="location.reload()">🔄 Start New Conversation</button>
        `);
    }
}

function isCompletionMessage(text) {
    return (
        text.includes("Thank you! Our team will contact you shortly to schedule your") ||
        text.includes("Your support request has been forwarded")
    );
}

function renderDateTimePicker() {
    activeDateTimePickerId = Date.now();
    const pickerId = activeDateTimePickerId;

    chatBox.innerHTML += `
        <div class="datetime-box" id="picker-${pickerId}">
            <label>Preferred date</label>
            <input type="date" id="demoDate-${pickerId}">
            <label>Preferred time</label>
            <input type="time" id="demoTime-${pickerId}">
            <button onclick="submitDateTime(${pickerId})">Submit</button>
        </div>
    `;
    scrollToBottom();
}

window.onload = function () {
    showWelcomeMessage();
};

// ---------------- Welcome ----------------

async function showWelcomeMessage() {
    showTyping();

    try {
        const response = await fetch("/welcome");
        const data = await response.json();
        hideTyping();

        const actionButtons = data.actions.map(action => `
            <button onclick="handleAction('${action}')">${action}</button>
        `).join("");

        chatBox.innerHTML = botRowHtml(formatBotText(data.message), actionButtons);
    } catch (error) {
        hideTyping();
        appendBotMessage("Sorry, I couldn't load the welcome message. Please refresh the page.");
    }
}

// ---------------- Action Buttons ----------------

function handleAction(action) {
    switch (action) {
        case "🚀 Explore Solutions":
            loadProducts();
            break;

        case "💬 Ask a Question":
            selectedService = "question";
            resetFlowModes();
            appendUserMessage("💬 Ask a Question");
            appendBotMessage(
                "Go ahead — ask me anything about CloudRion. For example:\n\n" +
                "• What does CloudRion do?\n" +
                "• Can it work for my business?\n" +
                "• Does it support manufacturing?\n" +
                "• Can I customize it?"
            );
            break;

        case "📅 Book a Demo":
            showDemoOptions();
            break;

        case "🎫 Technical Support":
            showSupportOptions();
            break;

        case "📞 Contact Our Team":
            showContactInfo();
            break;
    }
}

// ---------------- Demo & Support Options ----------------

function showDemoOptions(product = null) {
    if (product) {
        selectedProduct = product;
    }

    resetFlowModes();
    appendUserMessage(product ? `📅 Book a Demo — ${product}` : "📅 Book a Demo");
    appendBotMessage(
        "How would you like to book your demo?",
        `
            <button onclick="startDemoFlow()">💬 Guide Me Step by Step</button>
            <button onclick="openDemoForm()">📝 Fill Form Myself</button>
        `
    );
}

function showSupportOptions() {
    resetFlowModes();
    appendUserMessage("🎫 Technical Support");
    appendBotMessage(
        "How would you like to get support?",
        `
            <button onclick="startSupportFlow()">💬 Guide Me Step by Step</button>
            <button onclick="openTicketForm()">📝 Raise Ticket Myself</button>
        `
    );
}

// ---------------- Self-Service Forms ----------------

function setFormError(id, message) {
    const el = document.getElementById(id);
    if (!el) return;
    if (message) {
        el.textContent = message;
        el.hidden = false;
    } else {
        el.textContent = "";
        el.hidden = true;
    }
}

function openDemoForm() {
    const productSelect = document.getElementById("demoProduct");
    if (selectedProduct) {
        productSelect.value = selectedProduct;
    }
    setFormError("demoFormError", "");
    const modal = document.getElementById("demoModal");
    modal.hidden = false;
    modal.style.display = "flex";
}

function closeDemoForm() {
    const modal = document.getElementById("demoModal");
    modal.hidden = true;
    modal.style.display = "none";
    setFormError("demoFormError", "");
}

function clearDemoForm() {
    const form = document.getElementById("demoForm");
    if (form) form.reset();
    setFormError("demoFormError", "");
}

async function submitDemoForm(event) {
    if (event) event.preventDefault();

    const name = document.getElementById("demoName").value.trim();
    const company = document.getElementById("demoCompany").value.trim();
    const email = document.getElementById("demoEmail").value.trim();
    const phone = document.getElementById("demoPhone").value.trim();
    const product = document.getElementById("demoProduct").value;
    const date = document.getElementById("demoDate").value;
    const time = document.getElementById("demoTime").value;
    const submitBtn = document.getElementById("demoSubmitBtn");

    if (!name || !company || !email || !phone || !product || !date || !time) {
        setFormError("demoFormError", "Please fill in all fields before booking.");
        return false;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        setFormError("demoFormError", "Please enter a valid email address.");
        return false;
    }

    setFormError("demoFormError", "");
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Booking...";
    }

    try {
        const response = await fetch("/book-demo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name,
                company,
                email,
                phone,
                product,
                preferred_datetime: `${date} ${time}`,
            }),
        });

        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw new Error(data.error || "Booking failed");
        }

        closeDemoForm();
        clearDemoForm();

        flowCompleted = true;
        resetFlowModes();
        appendBotMessage(data.message || "Demo booked successfully.");
        appendServiceButtons(`
            <button type="button" onclick="location.reload()">🔄 Start New Conversation</button>
        `);
    } catch (error) {
        setFormError("demoFormError", "Failed to book demo. Please try again.");
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = "Book Demo";
        }
    }
    return false;
}

function openTicketForm() {
    const productSelect = document.getElementById("ticketProduct");
    if (selectedProduct) {
        productSelect.value = selectedProduct;
    }
    setFormError("ticketFormError", "");
    const modal = document.getElementById("ticketModal");
    modal.hidden = false;
    modal.style.display = "flex";
}

function closeTicketForm() {
    const modal = document.getElementById("ticketModal");
    modal.hidden = true;
    modal.style.display = "none";
    setFormError("ticketFormError", "");
}

function clearTicketForm() {
    const form = document.getElementById("ticketForm");
    if (form) form.reset();
    setFormError("ticketFormError", "");
}

async function submitTicketForm(event) {
    if (event) event.preventDefault();

    const name = document.getElementById("ticketName").value.trim();
    const company = document.getElementById("ticketCompany").value.trim();
    const email = document.getElementById("ticketEmail").value.trim();
    const phone = document.getElementById("ticketPhone").value.trim();
    const product = document.getElementById("ticketProduct").value;
    const issue = document.getElementById("ticketIssue").value.trim();
    const submitBtn = document.getElementById("ticketSubmitBtn");

    if (!name || !company || !email || !phone || !product || !issue) {
        setFormError("ticketFormError", "Please fill in all fields before submitting.");
        return false;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        setFormError("ticketFormError", "Please enter a valid email address.");
        return false;
    }

    setFormError("ticketFormError", "");
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Submitting...";
    }

    try {
        const response = await fetch("/raise-ticket", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name,
                company,
                email,
                phone,
                product,
                issue,
            }),
        });

        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw new Error(data.error || "Ticket failed");
        }

        closeTicketForm();
        clearTicketForm();

        flowCompleted = true;
        resetFlowModes();
        appendBotMessage(data.message || "Ticket submitted successfully.");
        appendServiceButtons(`
            <button type="button" onclick="location.reload()">🔄 Start New Conversation</button>
        `);
    } catch (error) {
        setFormError("ticketFormError", "Failed to submit ticket. Please try again.");
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = "Submit Ticket";
        }
    }
    return false;
}

// ---------------- Support Flow ----------------

async function startSupportFlow() {
    selectedService = "support";
    resetFlowModes();
    supportMode = true;
    flowCompleted = false;

    showTyping();

    try {
        const response = await fetch("/support", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: "", start: true }),
        });

        const data = await response.json();
        hideTyping();
        handleFlowResponse(data);
    } catch (error) {
        hideTyping();
        appendBotMessage("Sorry, I couldn't start the support flow. Please try again.");
        supportMode = false;
    }
}

// ---------------- Contact (info only — not saved) ----------------

async function showContactInfo(product = null) {
    selectedService = "contact";
    resetFlowModes();
    contactMode = false;

    if (product) {
        selectedProduct = product;
        appendUserMessage(`📞 Contact Sales — ${product}`);
    } else {
        appendUserMessage("📞 Contact Our Team");
    }

    try {
        const response = await fetch("/contact");
        const data = await response.json();
        const extra = product
            ? `\n\nYou're interested in **${product}**. Reach out and our team will help you further.`
            : "";
        appendBotMessage((data.message || "") + extra);
    } catch (error) {
        appendBotMessage("Sorry, contact information is unavailable right now. Please try again later.");
    }
}

function closeChat() {
    const widget = document.getElementById("chat-widget");
    const launcher = document.getElementById("chat-launcher");
    if (widget) {
        widget.classList.add("is-hidden");
    }
    if (launcher) {
        launcher.hidden = false;
    }
    closeDemoForm();
    closeTicketForm();
}

function openChat() {
    const widget = document.getElementById("chat-widget");
    const launcher = document.getElementById("chat-launcher");
    if (widget) {
        widget.classList.remove("is-hidden");
    }
    if (launcher) {
        launcher.hidden = true;
    }
}

// ---------------- Demo ----------------

async function startDemoFlow() {
    selectedService = "demo";
    resetFlowModes();
    demoMode = true;
    demoCompleted = false;
    flowCompleted = false;

    showTyping();

    try {
        const response = await fetch("/demo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: "", start: true }),
        });

        const data = await response.json();
        hideTyping();
        handleFlowResponse(data);
    } catch (error) {
        hideTyping();
        appendBotMessage("Sorry, I couldn't start the demo booking. Please try again.");
        demoMode = false;
    }
}

// ---------------- Send ----------------

async function sendMessage() {
    if (demoCompleted || flowCompleted) {
        return;
    }

    const input = document.getElementById("message");
    const message = input.value.trim();

    if (message === "") {
        return;
    }

    appendUserMessage(message);
    input.value = "";
    showTyping();

    let url = "/chat";
    if (demoMode) {
        url = "/demo";
    } else if (supportMode) {
        url = "/support";
    } else if (contactMode) {
        url = "/contact-flow";
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                service: selectedService,
                message: message,
            }),
        });

        const data = await response.json();
        hideTyping();
        handleFlowResponse(data);

        if (demoMode && isCompletionMessage(data.response || "")) {
            demoCompleted = true;
        }
    } catch (error) {
        hideTyping();
        appendBotMessage("Sorry, I couldn't process your message. Please try again.");
    }
}

// ---------------- Products ----------------

async function loadProducts() {
    appendUserMessage("🚀 Explore Solutions");

    try {
        const response = await fetch("/products");
        const data = await response.json();

        appendBotMessage(data.intro || "Here are our available CloudRion solutions:");

        appendServiceButtons(
            data.products.map(product => `
                <button onclick="showProduct('${product}')">${product}</button>
            `).join("")
        );

        productsLoaded = true;
    } catch (error) {
        appendBotMessage("Sorry, I couldn't load our products. Please try again.");
    }
}

// ---------------- Product Details ----------------

async function showProduct(product) {
    selectedProduct = product;

    try {
        const response = await fetch(`/product/${encodeURIComponent(product)}`);
        const data = await response.json();

        if (!response.ok || data.error || !(data.pitch || data.description)) {
            throw new Error(data.error || "Product not found");
        }

        appendUserMessage(product);
        appendBotMessage(data.pitch || data.description);

        appendServiceButtons(`
            <button onclick="selectedProduct='${product}'; handleButtonAction('learn_more')">Learn More</button>
            <button onclick="showDemoOptions('${product}')">Book Demo</button>
            <button onclick="showContactInfo('${product}')">Contact Sales</button>
        `);
    } catch (error) {
        appendBotMessage("Sorry, I couldn't load product details. Please try again.");
    }
}

async function showLearnMore(product) {
    try {
        const response = await fetch(`/product/${encodeURIComponent(product)}`);
        const data = await response.json();

        if (!response.ok || data.error || !(data.details || data.description)) {
            throw new Error(data.error || "Product not found");
        }

        appendUserMessage("Learn More");
        appendBotMessage(data.details || data.description);

        appendServiceButtons(`
            <button onclick="showDemoOptions('${product}')">Book Demo</button>
            <button onclick="showContactInfo('${product}')">Contact Sales</button>
        `);
    } catch (error) {
        appendBotMessage("Sorry, I couldn't load more details. Please try again.");
    }
}

// ---------------- Helpers ----------------

document.getElementById("message").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function selectFlowProduct(product) {
    document.getElementById("message").value = product;
    sendMessage();
}

function selectProduct(product) {
    selectFlowProduct(product);
}

function submitDateTime(pickerId) {
    const date = document.getElementById(`demoDate-${pickerId}`).value;
    const time = document.getElementById(`demoTime-${pickerId}`).value;

    if (date === "" || time === "") {
        alert("Please select both date and time.");
        return;
    }

    document.getElementById("message").value = date + " " + time;
    sendMessage();
}

window.addEventListener("click", function (event) {
    if (event.target === document.getElementById("demoModal")) {
        closeDemoForm();
    }
    if (event.target === document.getElementById("ticketModal")) {
        closeTicketForm();
    }
});

document.getElementById("demoForm")?.addEventListener("submit", submitDemoForm);
document.getElementById("ticketForm")?.addEventListener("submit", submitTicketForm);
