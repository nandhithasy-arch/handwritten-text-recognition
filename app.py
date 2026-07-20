import gradio as gr
from datetime import datetime
from ocr_pipeline import recognize_text

def render_history(items):
    if not items:
        return "<div class='history-empty'>No OCR history yet.</div>"

    cards = []
    for i, item in enumerate(reversed(items[-10:]), start=1):
        cards.append(f"""
        <div class="history-card">
            <div class="history-top">
                <span class="history-badge">#{i}</span>
                <span class="history-time">{item['time']}</span>
            </div>
            <div class="history-name">{item['name']}</div>
            <div class="history-text">{item['text']}</div>
        </div>
        """)

    return "<div class='history-list'>" + "".join(cards) + "</div>"

def ocr_run(image, history_state):
    if image is None:
        return "Upload an image first.", render_history(history_state), history_state, None

    text = recognize_text(image)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    item = {
        "time": now,
        "name": "uploaded image",
        "text": text
    }
    history_state = (history_state or []) + [item]

    return text, render_history(history_state), history_state, image

def clear_all():
    return "", "<div class='history-empty'>No OCR history yet.</div>", [], None

def clear_history():
    return "<div class='history-empty'>No OCR history yet.</div>", []

def toggle_theme(mode):
    if mode == "Dark":
        return "dark-mode"
    return "light-mode"

css = """
.gradio-container {
    min-height: 100vh !important;
    background:
        radial-gradient(circle at top left, rgba(139,92,246,.35), transparent 30%),
        radial-gradient(circle at top right, rgba(34,211,238,.28), transparent 28%),
        radial-gradient(circle at bottom center, rgba(244,114,182,.18), transparent 25%),
        linear-gradient(120deg, #020617, #0f172a, #111827) !important;
    background-size: 200% 200% !important;
    animation: bgmove 14s ease infinite;
    color: #e5e7eb !important;
}

@keyframes bgmove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

#hero {
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 28px;
    padding: 24px 26px;
    background: linear-gradient(135deg, rgba(139,92,246,.18), rgba(34,211,238,.12), rgba(244,114,182,.10));
    box-shadow: 0 20px 80px rgba(0,0,0,.4);
    backdrop-filter: blur(18px);
    margin-bottom: 18px;
}

#title {
    font-size: 54px;
    font-weight: 900;
    letter-spacing: -2px;
    line-height: 1.02;
    margin: 0;
    text-shadow: 0 0 20px rgba(139,92,246,.25);
}

#subtitle {
    margin-top: 10px;
    font-size: 18px;
    color: #cbd5e1;
    max-width: 900px;
}

.panel {
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 24px !important;
    background: rgba(5, 8, 22, .7) !important;
    backdrop-filter: blur(18px);
    box-shadow: 0 18px 50px rgba(0,0,0,.28) !important;
    padding: 16px !important;
}

.section-title {
    font-size: 18px;
    font-weight: 800;
    color: white;
    margin-bottom: 12px;
}

.neon-btn button {
    border: none !important;
    border-radius: 14px !important;
    height: 48px !important;
    font-weight: 800 !important;
    color: white !important;
    background: linear-gradient(135deg, #8b5cf6, #ec4899) !important;
    box-shadow: 0 0 20px rgba(139,92,246,.3);
}

.neon-btn button:hover {
    transform: translateY(-1px) scale(1.01);
}

.sample-btn button {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    border-radius: 12px !important;
}

#output textarea {
    min-height: 320px !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}

.history-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.history-card {
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 18px;
    padding: 14px 16px;
    background: rgba(15, 23, 42, .72);
}

.history-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}

.history-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 800;
    padding: 5px 10px;
    border-radius: 999px;
    color: white;
    background: linear-gradient(135deg, #22d3ee, #8b5cf6);
}

.history-time {
    font-size: 12px;
    color: #94a3b8;
}

.history-name {
    font-size: 14px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 8px;
}

.history-text {
    white-space: pre-wrap;
    color: #dbeafe;
    font-size: 13px;
    line-height: 1.55;
}

.history-empty {
    color: #cbd5e1;
    padding: 10px 2px;
}

.light-mode .gradio-container {
    background:
        radial-gradient(circle at top left, rgba(139,92,246,.20), transparent 28%),
        radial-gradient(circle at top right, rgba(34,211,238,.18), transparent 25%),
        linear-gradient(120deg, #eef2ff, #f8fafc, #e0f2fe) !important;
    color: #111827 !important;
}

.light-mode #hero,
.light-mode .panel {
    background: rgba(255,255,255,.78) !important;
    border: 1px solid rgba(15, 23, 42, .08) !important;
}

.light-mode #title,
.light-mode .section-title,
.light-mode .history-name {
    color: #0f172a !important;
}

.light-mode #subtitle,
.light-mode .history-text {
    color: #334155 !important;
}

.light-mode .history-card {
    background: rgba(255,255,255,.88);
    border: 1px solid rgba(15,23,42,.08);
}

.light-mode .history-time {
    color: #64748b;
}
"""

with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    history_state = gr.State([])
    theme_state = gr.State("Dark")

    gr.HTML("""
    <div id="hero">
        <div id="title">Neon OCR Nexus</div>
        <div id="subtitle">
            Handwriting OCR with TrOCR, Gradio, animated styling, history tracking, and a polished demo interface.
        </div>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=3, elem_classes=["panel"]):
            gr.Markdown("<div class='section-title'>Controls</div>")
            theme_mode = gr.Dropdown(["Dark", "Light"], value="Dark", label="Theme")
            image = gr.Image(type="pil", label="Upload Handwritten Image", height=340)

            gr.Markdown("### Quick Samples")
            with gr.Row():
                sample1 = gr.Button("CSE", elem_classes=["sample-btn"])
                sample2 = gr.Button("AAACET", elem_classes=["sample-btn"])
            with gr.Row():
                sample3 = gr.Button("HELLO", elem_classes=["sample-btn"])
                sample4 = gr.Button("OCR", elem_classes=["sample-btn"])

            run_btn = gr.Button("Recognize Text", elem_classes=["neon-btn"])
            clear_btn = gr.Button("Clear All", elem_classes=["sample-btn"])
            clear_hist_btn = gr.Button("Clear History", elem_classes=["sample-btn"])

        with gr.Column(scale=5, elem_classes=["panel"]):
            gr.Markdown("<div class='section-title'>OCR Output</div>")
            output = gr.Textbox(label="Recognized Text", lines=12, elem_id="output", value="Upload an image to begin.")
            status = gr.Textbox(label="Status", value="Ready", interactive=False)

        with gr.Column(scale=4, elem_classes=["panel"]):
            gr.Markdown("<div class='section-title'>OCR History</div>")
            history_html = gr.HTML(render_history([]))

    def use_sample(text):
        return text

    theme_mode.change(toggle_theme, inputs=theme_mode, outputs=demo)

    run_btn.click(
        ocr_run,
        inputs=[image, history_state],
        outputs=[output, history_html, history_state, image]
    )

    clear_btn.click(
        clear_all,
        outputs=[output, history_html, history_state, image]
    )

    clear_hist_btn.click(
        clear_history,
        outputs=[history_html, history_state]
    )

    sample1.click(lambda: None, outputs=None)
    sample2.click(lambda: None, outputs=None)
    sample3.click(lambda: None, outputs=None)
    sample4.click(lambda: None, outputs=None)

if __name__ == "__main__":
    demo.launch()
