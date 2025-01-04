import os
import flet as ft
from yt_dlp import YoutubeDL
from pathlib import Path

def create_folder():
    """Ensure 'damtube' folder exists in the internal storage."""
    base_path = Path.home() / "Documents/damtube"
    if not base_path.exists():
        os.makedirs(base_path)
    return str(base_path)

DAMTUBE_FOLDER = create_folder()

def fetch_video_formats(url, page, quality_dropdown):
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
                for f in formats if "video" in f["acodec"]
            ]

        quality_dropdown.options = [ft.dropdown.Option(option) for option in quality_options]
        quality_dropdown.value = quality_options[0] if quality_options else None
        page.update()
    except Exception as e:
        page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"))
        page.snack_bar.open = True
        page.update()

def download_video(url, format_id, page):
    """Download the video in the selected format."""
    if not url.strip() or not format_id:
        page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid URL and select a quality"))
        page.snack_bar.open = True
        page.update()
        return

    try:
        page.snack_bar = ft.SnackBar(ft.Text("Downloading..."))
        page.snack_bar.open = True
        page.update()

        ydl_opts = {
            "format": format_id.split(" - ")[0],
            "outtmpl": f"{DAMTUBE_FOLDER}/%(title)s.%(ext)s",
            "quiet": True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Video")
            page.snack_bar = ft.SnackBar(ft.Text(f"Downloaded: {title}\nSaved to: {DAMTUBE_FOLDER}"))
            page.snack_bar.open = True
            page.update()
    except Exception as e:
        page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"))
        page.snack_bar.open = True
        page.update()

def main(page: ft.Page):
    page.title = "YouTube Video Downloader with Quality Selection"
    page.scroll = "adaptive"

    url_input = ft.TextField(label="YouTube URL", expand=True)
    quality_dropdown = ft.Dropdown(label="Select Video Quality", expand=True)
    fetch_button = ft.ElevatedButton(
        "Fetch Formats",
        on_click=lambda e: fetch_video_formats(url_input.value, page, quality_dropdown),
    )
    download_button = ft.ElevatedButton(
        "Download",
        on_click=lambda e: download_video(url_input.value, quality_dropdown.value, page),
    )

    page.add(
        ft.Column(
            [
                ft.Row([url_input, fetch_button], alignment="center"),
                quality_dropdown,
                download_button,
                ft.Text(f"Downloads will be saved to: {DAMTUBE_FOLDER}"),
            ],
            alignment="center",
            expand=True,
        )
    )

ft.app(target=main)
