import os
import re
import tarfile
import zipfile

import requests
import yaml

base_url = "https://mms.alliedmods.net/mmsdrop/2.0/mmsource-2.0.0-git{}-{}.tar.gz"
game_path = "cs2/game/csgo/addons/metamod"


def download_metamod(file_path="scripts/config.yaml"):
    with open(file_path) as f:
        config = yaml.safe_load(f)

    metamod_version = config['version']
    metamod_platform = config['platform']

    metamod_next_version = int(metamod_version) + 1

    def download_and_write(version: int, platform: str):
        archive_name = f"metamod-{version}.tar.gz"
        response = requests.get(base_url.format(version, platform))
        if response.status_code == 200:
            with open(archive_name, 'wb') as f:
                f.write(response.content)
                return archive_name
        return ""

    new_version_check_response = requests.head(base_url.format(metamod_next_version, metamod_platform))
    if new_version_check_response.status_code == 200:
        archive_name = download_and_write(metamod_next_version, metamod_platform)
        config["version"] = metamod_next_version
        with open(file_path, "w") as f:
            yaml.safe_dump(config, f)
    else:
        print(f"No new version found, will try to download: {metamod_version}")
        archive_name = download_and_write(metamod_version, metamod_platform)

    if archive_name:
        game_path = "cs2/game/csgo"
        with tarfile.open(archive_name) as tar:
            # Extract only addons directory
            members = [m for m in tar.getmembers() if m.name.startswith('addons/')]
            tar.extractall(path=game_path, members=members, filter='data')
        os.unlink(archive_name)
        print(f"Extracted to {game_path}")


def download_css(file_path="scripts/config.yaml"):
    with open(file_path) as f:
        config = yaml.safe_load(f)

    api_url = "https://api.github.com/repos/roflmuffin/CounterStrikeSharp/releases/latest"
    response = requests.get(api_url)
    latest = response.json()
    version = latest["tag_name"].lstrip("v")

    platform = config['platform']
    asset_name = f"counterstrikesharp-with-runtime-build-{version}-{platform}"  # Partial match

    for asset in latest["assets"]:
        if asset_name in asset["name"]:
            response = requests.get(asset["browser_download_url"])
            if response.status_code == 200:
                zip_path = asset["name"]

                with open(zip_path, "wb") as f:
                    f.write(response.content)

                game_path = "cs2/game/csgo"

                with zipfile.ZipFile(zip_path) as zip_ref:
                    zip_ref.extractall("cs2/game/csgo")

                os.unlink(zip_path)
                print(f"Extracted to {game_path}")
            break



def patch_gameinfo():
    file_path = "cs2/game/csgo/gameinfo.gi"
    pattern = r"Game_LowViolence\s*csgo_lv // Perfect World content override"
    line_to_add = "\t\t\tGame\tcsgo/addons/metamod"
    check_regex = r"^\s*Game\s*csgo/addons/metamod"

    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()

    # Check if line already exists
    if re.search(check_regex, content, re.MULTILINE):
        print(f"{file_path} already patched for Metamod.")
        return

    # Add line after pattern
    new_content = re.sub(
        pattern,
        lambda m: f"{m.group()}\n{line_to_add}",
        content
    )

    # Write modified content back
    with open(file_path, 'w') as f:
        f.write(new_content)
    print(f"{file_path} successfully patched for Metamod.")


def download_matchzy(file_path="scripts/config.yaml"):
    with open(file_path) as f:
        config = yaml.safe_load(f)

    api_url = "https://api.github.com/repos/shobhit-pathak/MatchZy/releases/latest"
    response = requests.get(api_url)
    latest = response.json()
    version = latest["tag_name"]

    platform = config['platform']
    asset_name = f"MatchZy-{version}-with-cssharp-{platform}.zip"

    for asset in latest["assets"]:
        if asset_name in asset["name"]:
            response = requests.get(asset["browser_download_url"])
            if response.status_code == 200:
                zip_path = asset["name"]

                with open(zip_path, "wb") as f:
                    f.write(response.content)

                game_path = "cs2/game/csgo"

                with zipfile.ZipFile(zip_path) as zip_ref:
                    zip_ref.extractall("cs2/game/csgo")

                os.unlink(zip_path)
                print(f"Extracted to {game_path}")
            break

if __name__ == "__main__":
    # download_metamod()
    # download_css()
    # patch_gameinfo()
    download_matchzy()