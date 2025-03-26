import os
import sys
import re
import yt_dlp
from colorama import init, Fore, Style
from moviepy.editor import VideoFileClip, vfx

# Initialize colorama for colored terminal output
init(autoreset=True)

# Predefined quality options and fallback order
QUALITY_OPTIONS = {
    "1": "bestvideo+bestaudio/best",  # High
    "2": "best[height<=720]",         # Medium
    "3": "worst"                      # Low
}
FALLBACK_ORDER = ["bestvideo+bestaudio/best", "best[height<=720]", "worst"]

def safe_input(prompt):
    """Prompt user and exit if 'q' is entered."""
    user_input = input(Fore.LIGHTCYAN_EX + prompt + Style.RESET_ALL).strip()
    if user_input.lower() == 'q':
        sys.exit(Fore.RED + "Exiting." + Style.RESET_ALL)
    return user_input

def prompt_choice(prompt, valid_choices):
    """Prompt until a valid (case-insensitive) choice is entered (q allowed)."""
    while True:
        choice = safe_input(prompt).lower()
        if choice in valid_choices:
            return choice
        else:
            print(Fore.RED + "Invalid input! Please try again." + Style.RESET_ALL)

def print_header():
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.MAGENTA + Style.BRIGHT + "          TikTok Downloader".center(60))
    print(Fore.MAGENTA + "=" * 60 + Style.RESET_ALL)

def show_quality_menu():
    """
    Display quality options:
      1. High     => bestvideo+bestaudio/best
      2. Medium   => best[height<=720]
      3. Low      => worst
      4. List available formats and choose custom
      q. Exit from code
    """
    print(Fore.CYAN + "Choose desired quality:" + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + "1." + Style.RESET_ALL + " High     (bestvideo+bestaudio/best)")
    print(Fore.LIGHTCYAN_EX + "2." + Style.RESET_ALL + " Medium   (best[height<=720])")
    print(Fore.LIGHTCYAN_EX + "3." + Style.RESET_ALL + " Low      (worst)")
    print(Fore.LIGHTCYAN_EX + "4." + Style.RESET_ALL + " List available formats and choose custom")
    print(Fore.LIGHTCYAN_EX + "q." + Style.RESET_ALL + " Exit from code")
    return prompt_choice("Select (1-4 or q): ", {"1", "2", "3", "4", "q"})

def choose_quality(url):
    """Handles quality selection with listing formats, back option, or quit."""
    while True:
        option = show_quality_menu()
        if option == "q":
            sys.exit(Fore.RED + "Exiting." + Style.RESET_ALL)
        if option in {"1", "2", "3"}:
            return QUALITY_OPTIONS[option]
        elif option == "4":
            list_formats(url)
            custom = safe_input("Enter a new format (or 'b' to go back, 'q' to quit): ").lower()
            if custom == "b":
                continue
            elif custom:
                return custom
            else:
                print(Fore.RED + "Invalid input, try again." + Style.RESET_ALL)

def list_formats(url):
    """List all available formats for the given URL."""
    print(Fore.CYAN + f"\nListing available formats for: {url}\n" + Style.RESET_ALL)
    opts = {
        "quiet": False,
        "listformats": True,
        "extractor_args": {"tiktok": {"app": "android"}}
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    print()

def extract_info_with_fallback(url, chosen_format):
    """
    Attempt to extract info using the chosen format.
    For predefined quality options, automatically try lower-quality fallbacks.
    Otherwise, prompt the user for fallback actions.
    """
    def attempt_extract(fmt):
        opts = {
            "quiet": True,
            "noprogress": True,
            "extractor_args": {"tiktok": {"app": "android"}},
            "format": fmt
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)
    try:
        return attempt_extract(chosen_format)
    except yt_dlp.utils.DownloadError as e:
        print(Fore.RED + f"Error with format '{chosen_format}': {e}" + Style.RESET_ALL)
    if chosen_format in FALLBACK_ORDER:
        start_index = FALLBACK_ORDER.index(chosen_format)
        for fmt in FALLBACK_ORDER[start_index+1:]:
            try:
                info = attempt_extract(fmt)
                print(Fore.CYAN + f"Falling back to quality '{fmt}'..." + Style.RESET_ALL)
                return info
            except yt_dlp.utils.DownloadError as e:
                print(Fore.RED + f"Format '{fmt}' not available: {e}" + Style.RESET_ALL)
        sys.exit(Fore.RED + "All fallback formats failed. Exiting." + Style.RESET_ALL)
    else:
        while True:
            print(Fore.LIGHTCYAN_EX + "\nFormat not available. What would you like to do?" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "1." + Style.RESET_ALL + " Fallback to High quality (bestvideo+bestaudio/best)")
            print(Fore.LIGHTCYAN_EX + "2." + Style.RESET_ALL + " List available formats and choose custom")
            print(Fore.LIGHTCYAN_EX + "3." + Style.RESET_ALL + " Exit")
            choice = prompt_choice("Select (1-3 or q): ", {"1", "2", "3", "q"})
            if choice in {"q", "3"}:
                sys.exit(Fore.RED + "Exiting due to format error." + Style.RESET_ALL)
            elif choice == "1":
                fallback_fmt = "bestvideo+bestaudio/best"
                print(Fore.CYAN + f"Falling back to '{fallback_fmt}'..." + Style.RESET_ALL)
                try:
                    return attempt_extract(fallback_fmt)
                except yt_dlp.utils.DownloadError as e:
                    sys.exit(Fore.RED + f"Fallback also failed: {e}" + Style.RESET_ALL)
            elif choice == "2":
                list_formats(url)
                new_fmt = safe_input("Enter a new format (or 'b' to go back, 'q' to quit): ").lower()
                if new_fmt == "b":
                    continue
                elif new_fmt:
                    print(Fore.CYAN + f"Trying '{new_fmt}'..." + Style.RESET_ALL)
                    try:
                        return attempt_extract(new_fmt)
                    except yt_dlp.utils.DownloadError as e:
                        print(Fore.RED + f"That format also failed: {e}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid input, please try again." + Style.RESET_ALL)

def mirror_video(input_path, output_path):
    """Creates a horizontally mirrored version of the video."""
    print(Fore.CYAN + f"⏩ Mirroring video: {os.path.basename(input_path)}" + Style.RESET_ALL)
    try:
        clip = VideoFileClip(input_path)
        mirrored_clip = clip.fx(vfx.mirror_x)
        mirrored_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        print(Fore.GREEN + f"✔ Mirrored video saved as: {os.path.basename(output_path)}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"❌ Error mirroring video: {e}" + Style.RESET_ALL)

def download_video(url, output_template, format_str):
    """Download a single video to the specified path using yt-dlp."""
    opts = {
        "quiet": False,
        "noprogress": False,
        "extractor_args": {"tiktok": {"app": "android"}},
        "format": format_str,
        "outtmpl": output_template
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

def single_video_mode():
    """Download a single TikTok video."""
    video_url = safe_input("Enter the TikTok video URL: ")
    mirror_flag = prompt_choice("Do you want the mirrored version? (y/n or q to exit): ", {"y", "n", "q"}) == "y"
    quality_choice = choose_quality(video_url)
    info = extract_info_with_fallback(video_url, quality_choice)
    if not info:
        sys.exit(Fore.RED + "Failed to extract video info." + Style.RESET_ALL)
    video_id = info.get("id", "unknown")
    output_dir = "Downloaded"
    os.makedirs(output_dir, exist_ok=True)
    filename_no_ext = f"0001 - {video_id}"
    download_path = os.path.join(output_dir, filename_no_ext + ".mp4")

    print(Fore.BLUE + "-" * 60 + Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT + f"Downloading single video: {video_id}".center(60) + Style.RESET_ALL)
    print(Fore.BLUE + "-" * 60 + Style.RESET_ALL)
    download_video(video_url, download_path, info.get("requested_formats") or quality_choice)

    if mirror_flag and os.path.exists(download_path):
        mirrored_path = os.path.join(output_dir, f"0001 - Mirrored_{video_id}.mp4")
        mirror_video(download_path, mirrored_path)

    print(Fore.GREEN + Style.BRIGHT + f"✔ Finished downloading single video: {video_id}" + Style.RESET_ALL)

def channel_mode():
    """Download multiple videos from a TikTok channel."""
    channel_url = safe_input("Enter the TikTok channel URL: ")
    while "/video/" in channel_url:
        print(Fore.RED + "It appears you entered a video URL instead of a channel URL." + Style.RESET_ALL)
        channel_url = safe_input("Please enter a valid TikTok channel URL (e.g., https://www.tiktok.com/@username): ")
    mirror_flag = prompt_choice("Do you want the mirrored version for channel videos? (y/n or q to exit): ", {"y", "n", "q"}) == "y"
    quality_choice = choose_quality(channel_url)
    # Immediately ask if user wants to download all or specify a range
    mode_choice = safe_input("Download all videos (a) or specify a range (r) (or q to exit): ").lower()
    if mode_choice not in {"a", "r"}:
        print(Fore.RED + "Invalid input! Exiting." + Style.RESET_ALL)
        sys.exit(1)

    # Extract channel info (this process takes time in any case)
    info = extract_info_with_fallback(channel_url, quality_choice)
    if not info:
        sys.exit(Fore.RED + "Failed to extract channel info." + Style.RESET_ALL)
    entries = info.get("entries", [info])
    total_videos = len(entries)
    if total_videos == 0:
        print(Fore.RED + "No videos found in this channel!" + Style.RESET_ALL)
        return

    if mode_choice == "r":
        print(Fore.CYAN + f"Total videos found: {total_videos}" + Style.RESET_ALL)
        range_input = safe_input("Enter the range (e.g., 5-7): ").lower()
        if re.match(r"^\d+-\d+$", range_input):
            parts = range_input.split("-")
            start_index = int(parts[0])
            end_index = int(parts[1])
        else:
            print(Fore.RED + "Invalid input! Must be in the format '5-7'." + Style.RESET_ALL)
            return
    else:
        start_index, end_index = 1, total_videos

    if start_index < 1 or end_index > total_videos or start_index > end_index:
        print(Fore.RED + "Invalid index range!" + Style.RESET_ALL)
        return

    if "/@" in channel_url:
        username = channel_url.split("/@")[1].split("/")[0]
    else:
        username = "unknown_channel"
    base_folder = "Downloaded"
    channel_folder = os.path.join(base_folder, f"Mirrored_{username}" if mirror_flag else username)
    os.makedirs(channel_folder, exist_ok=True)

    print(Fore.GREEN + Style.BRIGHT + f"✔ Videos will be saved in:\n  {channel_folder}\n" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + f"Starting download of videos {start_index} to {end_index}...".center(60) + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL + "\n")

    selected_entries = entries[start_index - 1:end_index]
    for i, entry in enumerate(selected_entries, start=start_index):
        video_id = entry.get("id", "unknown")
        webpage_url = entry.get("webpage_url", channel_url)
        tmp_filename = f"TMP_{video_id}.mp4"
        tmp_path = os.path.join(channel_folder, tmp_filename)
        print(Fore.BLUE + "-" * 60 + Style.RESET_ALL)
        print(Fore.BLUE + Style.BRIGHT + f"Downloading video {i}/{total_videos}: {video_id}".center(60) + Style.RESET_ALL)
        print(Fore.BLUE + "-" * 60 + Style.RESET_ALL)
        try:
            download_video(webpage_url, tmp_path, entry.get("requested_formats") or quality_choice)
        except yt_dlp.utils.DownloadError as e:
            print(Fore.RED + f"Download error: {e}" + Style.RESET_ALL)
            continue

        number_str = f"{i:04d}"
        final_filename = f"{number_str} - {video_id}.mp4"
        final_path = os.path.join(channel_folder, final_filename)
        if os.path.exists(tmp_path):
            os.rename(tmp_path, final_path)
        else:
            print(Fore.RED + "❌ Downloaded file not found after download!" + Style.RESET_ALL)
            continue

        if mirror_flag:
            mirrored_filename = f"{number_str} - Mirrored_{video_id}.mp4"
            mirrored_path = os.path.join(channel_folder, mirrored_filename)
            mirror_video(final_path, mirrored_path)

        print(Fore.GREEN + Style.BRIGHT + f"✔ Finished downloading video {i}/{total_videos}: {video_id}" + Style.RESET_ALL)
        print()

    print(Fore.GREEN + "=" * 60 + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + "Download Complete!".center(60) + Style.RESET_ALL)
    print(Fore.GREEN + "=" * 60 + Style.RESET_ALL + "\n")
    print(Fore.GREEN + Style.BRIGHT + f"All videos have been saved in:\n{channel_folder}" + Style.RESET_ALL)

def main():
    print_header()
    print(Fore.CYAN + Style.BRIGHT + "Choose download mode:" + Style.RESET_ALL)
    print(Fore.CYAN + "1. Single video download" + Style.RESET_ALL)
    print(Fore.CYAN + "2. Download entire channel" + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + "q. Exit from code" + Style.RESET_ALL)
    mode = safe_input("Enter 1 or 2 (or q to exit): ")
    while mode not in {"1", "2", "q"}:
        print(Fore.RED + "Invalid mode! Please enter 1 or 2 (or q to exit)." + Style.RESET_ALL)
        mode = safe_input("Enter 1 or 2 (or q to exit): ")

    if mode == "1":
        single_video_mode()
    elif mode == "2":
        channel_mode()
    else:
        sys.exit(Fore.RED + "Exiting." + Style.RESET_ALL)

if __name__ == "__main__":
    main()

