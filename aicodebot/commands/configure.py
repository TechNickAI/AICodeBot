import asyncio
import sys
import webbrowser

import click
import yaml

from aicodebot import AICODEBOT
from aicodebot.config import detect_api_keys, fetch_models_for_provider, get_config_file, read_config
from aicodebot.helpers import create_and_write_file
from aicodebot.output import get_console
from aicodebot.prompts import DEFAULT_PERSONALITY, PERSONALITIES


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("--openai-api-key", envvar="OPENAI_API_KEY", help="Your OpenAI API key")
@click.option("--anthropic-api-key", envvar="ANTHROPIC_API_KEY", help="Your Anthropic API key")
def configure(verbose, openai_api_key, anthropic_api_key):  # noqa: ARG001 - verbose for future use
    """Create or update the configuration file with dynamic provider and model selection"""
    console = get_console()

    def write_config_file(config_data):
        create_and_write_file(get_config_file(), yaml.dump(config_data), overwrite=True)
        console.print(f"✅ Updated config file at {get_config_file()}")

    # Check if we're in a terminal for interactive mode
    is_terminal = sys.stdout.isatty()
    if not is_terminal:
        # Non-interactive mode - create config with detected API keys and defaults
        detected_keys = detect_api_keys()

        # Also check command-line arguments for API keys
        api_key = None
        selected_provider = None

        if openai_api_key:
            api_key = openai_api_key
            selected_provider = "openai"
        elif anthropic_api_key:
            api_key = anthropic_api_key
            selected_provider = "anthropic"
        elif "openai" in detected_keys:
            api_key = detected_keys["openai"]["key"]
            selected_provider = "openai"
        elif "anthropic" in detected_keys:
            api_key = detected_keys["anthropic"]["key"]
            selected_provider = "anthropic"

        if not api_key:
            console.print("Non-interactive mode detected. Use --openai-api-key or --anthropic-api-key to set keys.")
            return

        # Select default model for provider
        if selected_provider == "openai":
            selected_model = {"id": "gpt-5", "name": "gpt-5"}
        else:
            selected_model = {"id": "claude-opus-4-1", "name": "claude-opus-4-1"}

        # Create config with defaults
        config_data = {
            "version": 1.3,
            "provider": selected_provider,
            "model": selected_model["id"],
            "personality": DEFAULT_PERSONALITY.name,
        }

        # Always store API key in non-interactive mode (needed for tests)
        if selected_provider == "openai":
            config_data["openai_api_key"] = api_key
        else:
            config_data["anthropic_api_key"] = api_key

        write_config_file(config_data)
        console.print(f"✅ Created config file in non-interactive mode with {selected_provider}")
        return

    # Check for existing configuration
    existing_config = read_config() or {}
    if existing_config and not click.confirm("Config file already exists. Do you want to reconfigure?", default=True):
        return

    console.print(f"\n🔧 Welcome to {AICODEBOT} Configuration!\n", style=console.bot_style)

    # Step 1: Detect existing API keys
    detected_keys = detect_api_keys()

    console.print("🔍 Scanning for existing API keys...", style=console.bot_style)
    if detected_keys:
        console.print("✅ Found the following API keys:", style="green")
        for provider, key_info in detected_keys.items():
            console.print(f"  • {provider.title()}: {'*' * 8 + key_info['key'][-8:]} (from {key_info['source']})")
    else:
        console.print("ℹ️ No API keys found in environment variables", style="yellow")

    # Step 2: Provider selection
    console.print("\n🤖 Choose your AI provider:", style=console.bot_style)

    available_providers = []
    if detected_keys.get("openai") or openai_api_key:
        available_providers.append(("OpenAI", "openai"))
    if detected_keys.get("anthropic") or anthropic_api_key:
        available_providers.append(("Anthropic", "anthropic"))

    # Always allow manual entry
    if not available_providers:
        console.print("No API keys detected. You'll need to enter one manually.")

    all_providers = [("OpenAI", "openai"), ("Anthropic", "anthropic")]
    for i, (display_name, provider_id) in enumerate(all_providers, 1):
        status = "✅ Available" if any(p[1] == provider_id for p in available_providers) else "❌ Needs API key"
        console.print(f"{i}. {display_name} - {status}")

    provider_choice = click.prompt("Select provider (1-2)", type=click.IntRange(1, 2), default=1)

    selected_provider_display, selected_provider = all_providers[provider_choice - 1]
    console.print(f"Selected: {selected_provider_display}")

    # Step 3: Handle API key
    api_key = None
    if selected_provider == "openai":
        api_key = detected_keys.get("openai", {}).get("key") or openai_api_key
        env_var = "OPENAI_API_KEY"
        api_url = "https://platform.openai.com/account/api-keys"
    else:  # anthropic
        api_key = detected_keys.get("anthropic", {}).get("key") or anthropic_api_key
        env_var = "ANTHROPIC_API_KEY"
        api_url = "https://console.anthropic.com/account/keys"

    if not api_key:
        console.print(f"\n🔑 You need a {selected_provider_display} API key.", style=console.bot_style)
        if click.confirm(f"Open {selected_provider_display} API keys page in browser?", default=True):
            webbrowser.open(api_url)

        api_key = click.prompt(f"Enter your {selected_provider_display} API key").strip()
        console.print("💡 Consider setting this as an environment variable:", style="dim")
        console.print(f"   export {env_var}={api_key}", style="dim")

    # Step 4: Fetch and select model
    console.print(f"\n🧠 Fetching available models from {selected_provider_display}...", style=console.bot_style)

    models = asyncio.run(fetch_models_for_provider(selected_provider, api_key))

    if not models:
        raise ValueError(f"No models returned from {selected_provider_display}")

    console.print(f"✅ Found {len(models)} available models:")

    for i, model in enumerate(models[:10], 1):  # Show first 10 models
        console.print(f"{i:2}. {model['name']} - {model['description']}")

    if len(models) > 10:
        console.print(f"... and {len(models) - 10} more models")

    # Add option for custom model
    console.print(f"{len(models) + 1:2}. [Custom] Enter your own model name")

    max_choice = min(len(models), 10) + 1
    model_choice = click.prompt(f"Select model (1-{max_choice})", type=click.IntRange(1, max_choice), default=1)

    if model_choice <= len(models):
        # User selected from the list
        selected_model = models[model_choice - 1]
        console.print(f"Selected: {selected_model['name']}")
    else:
        # User wants to enter custom model
        console.print("\n💡 You can enter any model ID (e.g., claude-opus-4-1, gpt-4o, claude-3-5-sonnet-20241022)")
        console.print("This allows you to use newer models that aren't in our list yet.")

        custom_model_id = click.prompt("Enter model ID").strip()
        selected_model = {
            "id": custom_model_id,
            "name": custom_model_id,
            "description": f"Custom model: {custom_model_id}",
        }
        console.print(f"Selected: {selected_model['name']} (custom)")

    # Step 5: Personality selection
    console.print("\n🎭 Choose your AI personality:", style=console.bot_style)

    personality_list = list(PERSONALITIES.items())
    for i, (key, personality) in enumerate(personality_list, 1):
        console.print(f"{i}. {key} - {personality.description}")

    personality_choice = click.prompt(
        f"Select personality (1-{len(personality_list)})", type=click.IntRange(1, len(personality_list)), default=1
    )

    selected_personality = personality_list[personality_choice - 1][0]

    # Step 6: Build and save configuration
    config_data = {
        "version": 1.3,  # Updated version for new format
        "provider": selected_provider,
        "model": selected_model["id"],
        "personality": selected_personality,
    }

    # Always store API key in config file
    if selected_provider == "openai":
        config_data["openai_api_key"] = api_key
    else:
        config_data["anthropic_api_key"] = api_key

    write_config_file(config_data)

    # Summary
    console.print("\n🎉 Configuration complete!", style="green bold")
    console.print(f"Provider: {selected_provider_display}")
    console.print(f"Model: {selected_model['name']}")
    console.print(f"Personality: {selected_personality}")
    console.print(f"\nYou're ready to use {AICODEBOT}! 🚀")


# Helper function for async execution in click context
def run_async(coro):
    """Run an async coroutine in a click command context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(coro)
