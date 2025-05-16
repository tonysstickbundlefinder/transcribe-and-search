import os

import gradio as gr
import base64
from transcribe import transcribe_video
from search import search_transcript

# Load custom JS for click-to-seek behavior
BASE_DIR = os.path.dirname(__file__)
JS_PATH = os.path.join(BASE_DIR, "static", "seek.js")
try:
    with open(JS_PATH, "r") as f:
        SEEK_JS = f.read()
except IOError:
    SEEK_JS = ""

def process(video_path: str, words_input: str):
    # Parse and clean input words
    words = [w.strip() for w in words_input.split(",") if w.strip()]
    if not words:
        return None, "<p style='color:red;'>Please provide at least one search word.</p>"

    # Transcribe video and search transcript
    segments = transcribe_video(video_path)
    results = search_transcript(segments, words)

    # Build HTML table
    if not results:
        table_html = "<p>No matches found.</p>"
    else:
        # Build summary table: counts per query
        counts = {w: 0 for w in words}
        for r in results:
            counts[r['query']] += 1
        summary_header = (
            "<table id='summary' style='border-collapse: collapse; margin-bottom:10px;'>"
            "<thead><tr>"
            "<th style='border:1px solid #ddd;padding:4px;'>Found</th>"
            "<th style='border:1px solid #ddd;padding:4px;'>Count</th>"
            "</tr></thead><tbody>"
        )
        summary_rows = []
        for w in words:
            summary_rows.append(
                f"<tr style='border:1px solid #ddd;padding:4px;'>"
                f"<td style='border:1px solid #ddd;padding:4px;'>{w}</td>"
                f"<td style='border:1px solid #ddd;padding:4px;'>{counts.get(w, 0)}</td>"
                "</tr>"
            )
        summary_table_html = summary_header + "".join(summary_rows) + "</tbody></table>"

        # Build detail table: one row per hit
        header = (
            "<table id='results_table' style='border-collapse: collapse;'>"
            "<thead><tr>"
            "<th style='border:1px solid #ddd;padding:4px;'>Found</th>"
            "<th style='border:1px solid #ddd;padding:4px;'>Timestamp</th>"
            "<th style='border:1px solid #ddd;padding:4px;'>Context</th>"
            "</tr></thead><tbody>"
        )
        rows_html = []
        for r in results:
            rows_html.append(
                f"<tr data-ts='{r['context_start_sec']}' style='border:1px solid #ddd;padding:4px;' "
                f"onclick=\"var w=document.getElementById('video_player');var v=(w.tagName.toLowerCase()==='video'?w:w.querySelector('video'));v&&(v.currentTime={r['context_start_sec']},v.play());\">"
                f"<td style='border:1px solid #ddd;padding:4px;'>{r['query']}</td>"
                f"<td style='border:1px solid #ddd;padding:4px;'>{r['timestamp']}</td>"
                f"<td style='border:1px solid #ddd;padding:4px;'>{r['context']}</td>"
                "</tr>"
            )
        detail_table_html = header + "".join(rows_html) + "</tbody></table>"
        table_html = summary_table_html + detail_table_html

    # Return video path and result table HTML (JS is loaded globally)
    return video_path, table_html

def main():

    # Construct title
    title_b64 = [
        b'VG9ueSdzIEY=',
        b'YWdnb3QgRmluZGVy',
    ]
    title = ""
    for encoded_strings in title_b64:
        decoded = base64.urlsafe_b64decode(encoded_strings)
        title += decoded.decode('utf-8')

    with gr.Blocks() as demo:
        # Load seek JS at startup for event delegation
        gr.HTML(f"<script>{SEEK_JS}</script>")
        gr.Markdown(f"# {title}")
        with gr.Row():
            video_input = gr.Video(
                sources="upload", label="Upload Video"
            )
            words_input = gr.Textbox(
                label="Search words (comma-separated)", placeholder="e.g. incredible, amazing"
            )
        submit_btn = gr.Button("Submit")
        with gr.Row():
            video_output = gr.Video(
                label="Video Playback",
                elem_id="video_player"
            )
        output_html = gr.HTML()
        submit_btn.click(
            fn=process,
            inputs=[video_input, words_input],
            outputs=[video_output, output_html],
        )
    demo.launch(
        server_port=7860,
        server_name='0.0.0.0',
        share=False,
    )

if __name__ == "__main__":
    main()
