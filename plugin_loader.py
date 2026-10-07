import os
import importlib
import difflib
import traceback

plugins = {}
plugin_commands = {}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_FOLDER = os.path.join(BASE_DIR, "plugins")


def load_plugins():
    """
    Loads every plugin inside the plugins folder.
    """

    plugins.clear()
    plugin_commands.clear()

    loaded = 0

    if not os.path.exists(PLUGIN_FOLDER):
        print("Plugin folder not found.")
        return

    for filename in sorted(os.listdir(PLUGIN_FOLDER)):

        if not filename.endswith(".py"):
            continue

        if filename == "__init__.py":
            continue

        module_name = filename[:-3]

        try:

            module = importlib.import_module(f"plugins.{module_name}")

            # Reload automatically during development
            module = importlib.reload(module)

            if not hasattr(module, "PLUGIN"):
                print(f"✗ {module_name}: Missing PLUGIN dictionary.")
                continue

            if not hasattr(module, "run"):
                print(f"✗ {module_name}: Missing run() function.")
                continue

            metadata = module.PLUGIN

            if "commands" not in metadata:
                print(f"✗ {module_name}: Missing PLUGIN['commands']")
                continue

            plugins[module_name] = module

            for phrase in metadata["commands"]:

                phrase = phrase.lower().strip()

                if phrase in plugin_commands:
                    print(
                        f"⚠ Duplicate command '{phrase}' "
                        f"({plugin_commands[phrase]} and {module_name})"
                    )

                plugin_commands[phrase] = module

            loaded += 1

            print(f"✓ Loaded {module_name}")

        except Exception:

            print(f"✗ Failed to load {module_name}")
            traceback.print_exc()

    print(f"\nLoaded {loaded} plugin(s).\n")


def get_plugin(command):
    """
    Returns the best matching plugin.
    """

    command = command.lower().strip()

    # ---------------------------------
    # Priority 1 : Exact match
    # ---------------------------------

    if command in plugin_commands:
        return plugin_commands[command]

    # ---------------------------------
    # Priority 2 : Startswith
    # ---------------------------------

    for trigger, plugin in plugin_commands.items():

        if command.startswith(trigger):
            return plugin

    # ---------------------------------
    # Priority 3 : Contains
    # ---------------------------------

    for trigger, plugin in plugin_commands.items():

        if trigger in command:
            return plugin

    # ---------------------------------
    # Priority 4 : Fuzzy match
    # ---------------------------------

    triggers = list(plugin_commands.keys())

    matches = difflib.get_close_matches(
        command,
        triggers,
        n=1,
        cutoff=0.65
    )

    if matches:
        return plugin_commands[matches[0]]

    return None


def reload_plugins():
    """
    Reloads every plugin without restarting Jarvis.
    """
    load_plugins()


def get_plugin_info(name):

    plugin = plugins.get(name)

    if plugin is None:
        return None

    return plugin.PLUGIN


def list_plugins():
    return sorted(plugins.keys())


def list_commands():
    return sorted(plugin_commands.keys())