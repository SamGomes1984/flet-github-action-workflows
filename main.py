import flet as ft
import requests
import os
import json
import time

# Replace with your DeepSeek API key
DEEPSEEK_API_KEY = os.getenv("sk-b2897ac0c3ab428ca2edbbc96f6f2c69")
API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

def main(page: ft.Page):
    page.title = "DeepSeek Chat"
    page.horizontal_alignment = "stretch"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Initialize chat messages list
    messages = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # Create loading indicator
    loading_indicator = ft.ProgressRing(visible=False)

    # Input field and send button
    user_input = ft.TextField(
        hint_text="Type your message...",
        expand=True,
        multiline=True,
        min_lines=1,
        max_lines=5,
    )

    async def send_message(e):
        if not user_input.value.strip():
            return

        # Add user message
        messages.controls.append(
            ft.Container(
                ft.Markdown(
                    user_input.value,
                    extension_set="gitHubWeb",
                    code_theme="atom-one-dark",
                ),
                alignment=ft.alignment.center_right,
                bgcolor=ft.colors.BLUE_100,
                padding=10,
                border_radius=10,
            )
        )

        # Show loading indicator
        loading_indicator.visible = True
        await page.update_async()

        try:
            # Prepare API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": user_input.value}],
                "temperature": 0.7
            }

            # Make API call
            response = requests.post(
                API_ENDPOINT,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()

            # Parse response
            result = response.json()
            reply = result['choices'][0]['message']['content']

            # Add bot response
            messages.controls.append(
                ft.Container(
                    ft.Markdown(
                        reply,
                        extension_set="gitHubWeb",
                        code_theme="atom-one-dark",
                    ),
                    alignment=ft.alignment.center_left,
                    bgcolor=ft.colors.GREEN_100,
                    padding=10,
                    border_radius=10,
                )
            )

        except Exception as e:
            messages.controls.append(
                ft.Text(f"Error: {str(e)}", color=ft.colors.RED)
            )
        finally:
            # Hide loading indicator and clear input
            loading_indicator.visible = False
            user_input.value = ""
            await page.update_async()

    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        on_click=send_message,
        tooltip="Send message",
    )

    # Build the UI
    page.add(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("DeepSeek Chat", style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
                messages,
                loading_indicator,
                ft.Row([user_input, send_button])
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
