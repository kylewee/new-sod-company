/**
 * Sod.Company AI Chatbot
 * Engages visitors and captures leads 24/7
 */

class SodChatbot {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.leadData = {};
        this.currentStep = 'greeting';
        this.init();
    }

    init() {
        this.createWidget();
        this.attachEventListeners();
        // Auto-open after 8 seconds on page
        setTimeout(() => this.greetVisitor(), 8000);
    }

    createWidget() {
        const widget = document.createElement('div');
        widget.innerHTML = `
            <div id="sod-chatbot" class="chatbot-container">
                <div class="chatbot-toggle" id="chatbot-toggle">
                    <span class="chat-icon">💬</span>
                    <span class="notification-dot"></span>
                </div>
                <div class="chatbot-window" id="chatbot-window">
                    <div class="chatbot-header">
                        <span class="header-title">🌱 Sod.Company</span>
                        <span class="header-status">Online</span>
                        <button class="close-btn" id="chatbot-close">×</button>
                    </div>
                    <div class="chatbot-messages" id="chatbot-messages"></div>
                    <div class="chatbot-input">
                        <input type="text" id="chatbot-input" placeholder="Type your message...">
                        <button id="chatbot-send">Send</button>
                    </div>
                </div>
            </div>
            <style>
                .chatbot-container {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }
                .chatbot-toggle {
                    width: 60px;
                    height: 60px;
                    background: #2d7a3a;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                    transition: transform 0.2s;
                    position: relative;
                }
                .chatbot-toggle:hover {
                    transform: scale(1.05);
                }
                .chat-icon {
                    font-size: 28px;
                }
                .notification-dot {
                    position: absolute;
                    top: 5px;
                    right: 5px;
                    width: 12px;
                    height: 12px;
                    background: #ff4444;
                    border-radius: 50%;
                    animation: pulse 2s infinite;
                }
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
                .chatbot-window {
                    display: none;
                    position: absolute;
                    bottom: 70px;
                    right: 0;
                    width: 350px;
                    height: 450px;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 5px 25px rgba(0,0,0,0.2);
                    flex-direction: column;
                    overflow: hidden;
                }
                .chatbot-window.open {
                    display: flex;
                }
                .chatbot-header {
                    background: #2d7a3a;
                    color: white;
                    padding: 15px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .header-title {
                    font-weight: 600;
                    flex: 1;
                }
                .header-status {
                    font-size: 0.75rem;
                    opacity: 0.9;
                }
                .close-btn {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 24px;
                    cursor: pointer;
                    padding: 0 5px;
                }
                .chatbot-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 15px;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                .message {
                    max-width: 85%;
                    padding: 10px 14px;
                    border-radius: 12px;
                    font-size: 0.9rem;
                    line-height: 1.4;
                }
                .message.bot {
                    background: #f0f0f0;
                    align-self: flex-start;
                    border-bottom-left-radius: 4px;
                }
                .message.user {
                    background: #2d7a3a;
                    color: white;
                    align-self: flex-end;
                    border-bottom-right-radius: 4px;
                }
                .quick-replies {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 8px;
                }
                .quick-reply {
                    background: white;
                    border: 1px solid #2d7a3a;
                    color: #2d7a3a;
                    padding: 6px 12px;
                    border-radius: 15px;
                    font-size: 0.85rem;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                .quick-reply:hover {
                    background: #2d7a3a;
                    color: white;
                }
                .chatbot-input {
                    display: flex;
                    padding: 10px;
                    border-top: 1px solid #eee;
                    gap: 8px;
                }
                .chatbot-input input {
                    flex: 1;
                    padding: 10px 12px;
                    border: 1px solid #ddd;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    outline: none;
                }
                .chatbot-input input:focus {
                    border-color: #2d7a3a;
                }
                .chatbot-input button {
                    background: #2d7a3a;
                    color: white;
                    border: none;
                    padding: 10px 18px;
                    border-radius: 20px;
                    cursor: pointer;
                    font-weight: 500;
                }
                .chatbot-input button:hover {
                    background: #1e5428;
                }
                .typing {
                    display: flex;
                    gap: 4px;
                    padding: 10px 14px;
                    background: #f0f0f0;
                    border-radius: 12px;
                    align-self: flex-start;
                    border-bottom-left-radius: 4px;
                }
                .typing span {
                    width: 8px;
                    height: 8px;
                    background: #999;
                    border-radius: 50%;
                    animation: typing 1s infinite;
                }
                .typing span:nth-child(2) { animation-delay: 0.2s; }
                .typing span:nth-child(3) { animation-delay: 0.4s; }
                @keyframes typing {
                    0%, 100% { opacity: 0.3; }
                    50% { opacity: 1; }
                }
                @media (max-width: 480px) {
                    .chatbot-window {
                        width: calc(100vw - 40px);
                        height: 400px;
                        bottom: 70px;
                        right: 0;
                    }
                }
            </style>
        `;
        document.body.appendChild(widget);
    }

    attachEventListeners() {
        document.getElementById('chatbot-toggle').addEventListener('click', () => this.toggle());
        document.getElementById('chatbot-close').addEventListener('click', () => this.close());
        document.getElementById('chatbot-send').addEventListener('click', () => this.sendUserMessage());
        document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendUserMessage();
        });
    }

    toggle() {
        this.isOpen ? this.close() : this.open();
    }

    open() {
        this.isOpen = true;
        document.getElementById('chatbot-window').classList.add('open');
        document.querySelector('.notification-dot').style.display = 'none';
        if (this.messages.length === 0) {
            this.startConversation();
        }
    }

    close() {
        this.isOpen = false;
        document.getElementById('chatbot-window').classList.remove('open');
    }

    greetVisitor() {
        if (!this.isOpen && this.messages.length === 0) {
            document.querySelector('.notification-dot').style.display = 'block';
        }
    }

    startConversation() {
        this.addBotMessage("Hi there! 👋 I'm here to help you get a beautiful new lawn.", [
            { text: "Get a quote", value: "quote" },
            { text: "See pricing", value: "pricing" },
            { text: "Ask a question", value: "question" }
        ]);
    }

    addBotMessage(text, quickReplies = null) {
        const messagesDiv = document.getElementById('chatbot-messages');

        // Show typing indicator
        const typing = document.createElement('div');
        typing.className = 'typing';
        typing.innerHTML = '<span></span><span></span><span></span>';
        messagesDiv.appendChild(typing);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // Remove typing and show message
        setTimeout(() => {
            typing.remove();

            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot';
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);

            if (quickReplies) {
                const repliesDiv = document.createElement('div');
                repliesDiv.className = 'quick-replies';
                quickReplies.forEach(reply => {
                    const btn = document.createElement('button');
                    btn.className = 'quick-reply';
                    btn.textContent = reply.text;
                    btn.addEventListener('click', () => this.handleQuickReply(reply.value));
                    repliesDiv.appendChild(btn);
                });
                messagesDiv.appendChild(repliesDiv);
            }

            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            this.messages.push({ type: 'bot', text });
        }, 800);
    }

    addUserMessage(text) {
        const messagesDiv = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user';
        messageDiv.textContent = text;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        this.messages.push({ type: 'user', text });

        // Remove quick replies
        document.querySelectorAll('.quick-replies').forEach(el => el.remove());
    }

    sendUserMessage() {
        const input = document.getElementById('chatbot-input');
        const text = input.value.trim();
        if (!text) return;

        this.addUserMessage(text);
        input.value = '';
        this.processUserInput(text);
    }

    handleQuickReply(value) {
        switch (value) {
            case 'quote':
                this.addUserMessage("Get a quote");
                this.currentStep = 'get_name';
                setTimeout(() => {
                    this.addBotMessage("Great! I'll help you get a quick quote. What's your name?");
                }, 500);
                break;
            case 'pricing':
                this.addUserMessage("See pricing");
                this.addBotMessage("Our pricing starts at $0.85/sqft installed. For a typical 5,000 sqft lawn, that's $4,250-$5,500 total.", [
                    { text: "Get my exact quote", value: "quote" },
                    { text: "What's included?", value: "included" }
                ]);
                break;
            case 'question':
                this.addUserMessage("Ask a question");
                this.addBotMessage("Sure! What would you like to know?", [
                    { text: "Best grass type?", value: "grass" },
                    { text: "How long does it take?", value: "timeline" },
                    { text: "Service areas?", value: "areas" }
                ]);
                break;
            case 'included':
                this.addBotMessage("Our price includes: premium sod, professional installation, delivery, soil prep, and a 30-day warranty. No hidden fees!", [
                    { text: "Get my quote", value: "quote" }
                ]);
                break;
            case 'grass':
                this.addBotMessage("The best grass depends on your location and shade. St. Augustine is great for Florida, Bermuda for full sun areas. Want me to recommend the best for your yard?", [
                    { text: "Yes, help me choose", value: "quote" }
                ]);
                break;
            case 'timeline':
                this.addBotMessage("Most installations take just 1 day! We can usually schedule within 5-7 days of booking.", [
                    { text: "Schedule my install", value: "quote" }
                ]);
                break;
            case 'areas':
                this.addBotMessage("We serve 40+ cities across FL, TX, AZ, GA, NC, SC, TN, and more! Enter your zip code for availability.", [
                    { text: "Check my area", value: "quote" }
                ]);
                break;
            case 'yes_contact':
                this.submitLead();
                break;
            case 'no_contact':
                this.addBotMessage("No problem! Feel free to browse our site or call us anytime. Is there anything else I can help with?", [
                    { text: "Get pricing info", value: "pricing" }
                ]);
                break;
        }
    }

    processUserInput(text) {
        switch (this.currentStep) {
            case 'get_name':
                this.leadData.name = text;
                this.currentStep = 'get_phone';
                setTimeout(() => {
                    this.addBotMessage(`Nice to meet you, ${text}! What's the best phone number to reach you?`);
                }, 500);
                break;
            case 'get_phone':
                this.leadData.phone = text;
                this.currentStep = 'get_size';
                setTimeout(() => {
                    this.addBotMessage("Got it! About how big is your lawn? (in square feet, or just say 'small', 'medium', or 'large')");
                }, 500);
                break;
            case 'get_size':
                this.leadData.lawn_size = text;
                this.currentStep = 'confirm';
                setTimeout(() => {
                    this.addBotMessage(`Perfect! Here's what I have:\n\n📋 ${this.leadData.name}\n📱 ${this.leadData.phone}\n📐 ${this.leadData.lawn_size}\n\nCan I have a specialist reach out with your exact quote?`, [
                        { text: "Yes, contact me!", value: "yes_contact" },
                        { text: "Not right now", value: "no_contact" }
                    ]);
                }, 500);
                break;
            default:
                // Default response
                setTimeout(() => {
                    this.addBotMessage("I'd be happy to help! Would you like to get a free quote?", [
                        { text: "Yes, get quote", value: "quote" },
                        { text: "Just browsing", value: "pricing" }
                    ]);
                }, 500);
        }
    }

    submitLead() {
        // Get city from URL or page
        const pathParts = window.location.pathname.split('/');
        this.leadData.city = pathParts[2] || 'Unknown';
        this.leadData.state = pathParts[1] || 'Unknown';
        this.leadData.source = 'chatbot';
        this.leadData.page = window.location.href;

        // Send to backend
        fetch('/contact-handler.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.leadData)
        }).catch(() => {});

        this.addBotMessage("🎉 Awesome! A sod specialist will call you shortly with your personalized quote. Thanks for chatting with us!");

        // Track conversion
        if (typeof gtag !== 'undefined') {
            gtag('event', 'lead_chatbot', { 'event_category': 'Lead' });
        }
    }
}

// Initialize chatbot
document.addEventListener('DOMContentLoaded', () => {
    new SodChatbot();
});
