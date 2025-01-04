import flet as ft
from yt_dlp import YoutubeDL

def fetch_video_formats(url, page, quality_dropdown, download_button):
    """Fetch available formats for the given YouTube URL."""
    if not url.strip():
        page.snack_bar = ft.SnackBar(ft.Text("Please enter a YouTube URL"))
        page.snack_bar.open = True
        page.update()
        return

    try:
        page.snack_bar = ft.SnackBar(ft.Text("Fetching video formats..."))
        page.snack_bar.open = True
        page.update()

        ydl_opts = {"quiet": True, "noplaylist": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            quality_options = [
                f"{f['format_id']} - {f['format_note']} - {f['ext']}"
                for f in formats if "url" in f
            ]

        quality_dropdown.options = [ft.dropdown.Option(option) for option in quality_options]
        quality_dropdown.value = quality_options[0] if quality_options else None
        quality_dropdown.disabled = False
        download_button.disabled = False
        page.update()
    except Exception as e:
        page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"))
        page.snack_bar.open = True
        page.update()

def generate_download_url(url, format_id, download_button):
    """Get the direct download link and update the button."""
    if not url.strip() or not format_id:
        return None

    try:
        ydl_opts = {"quiet": True, "noplaylist": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            selected_format = next(
                (f for f in formats if f["format_id"] == format_id.split(" - ")[0]), None
            )
            return selected_format.get("url") if selected_format else None
    except Exception:
        return None

def main(page: ft.Page):
    page.title = "YouTube Downloader (Download Button)"
    page.scroll = ft.ScrollMode.ADAPTIVE

    url_input = ft.TextField(label="YouTube URL", expand=True)
    quality_dropdown = ft.Dropdown(label="Select Video Quality", expand=True, disabled=True)
    download_button = ft.ElevatedButton(
        "Download",
        disabled=True,
        on_click=lambda e: page.launch_url(
            generate_download_url(url_input.value, quality_dropdown.value, download_button)
        ),
    )

    fetch_button = ft.ElevatedButton(
        "Fetch Formats",
        on_click=lambda e: fetch_video_formats(url_input.value, page, quality_dropdown, download_button),
    )

    page.add(
        ft.Column(
            [
                ft.Row([url_input, fetch_button], alignment="center"),
                quality_dropdown,
                download_button,
            ],
            alignment="center",
            expand=True,
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER)
