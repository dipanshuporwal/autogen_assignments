def generate_visualization_html_report(
    visualization_json: dict
) -> str:
    charts_base64 = visualization_json.get("charts_base64", [])
    summary_insights = visualization_json.get("summary_insights", "")
    additional_content = visualization_json.get("additional_content", "")

    images_html = "".join(
        [
            f'<img src="data:image/png;base64,{img}" style="max-width:600px;'
            ' margin:10px;" />'
            for img in charts_base64
        ]
    )

    html = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                h2 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h2>📊 Visual Summary</h2>
            {images_html}
            <h2>🧠 Summary Insights</h2>
            <p>{summary_insights}</p>
            <h2>📄 Additional Report Content</h2>
            {additional_content}
        </body>
    </html>
    """
    return html
