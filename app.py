import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="The Unofficial Housing Guide") as demo:
    gr.Markdown("# 🏠 The Unofficial Off-Campus Housing Guide")
    gr.Markdown("Ask any question about off-campus housing for college students!")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Your Question",
            placeholder="e.g. How do I get my security deposit back?",
            lines=2
        )
    
    btn = gr.Button("Ask", variant="primary")
    
    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=8)
        sources = gr.Textbox(label="Sources", lines=8)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()