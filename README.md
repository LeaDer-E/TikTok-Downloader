# TikTok Downloader with Mirror Option

A Python-based TikTok downloader that allows you to download single videos or entire channels with advanced features such as:

- **Quality selection:** Choose between high, medium, and low quality, or list available formats and choose a custom format.
- **Automatic fallback:** If the chosen quality isn't available, the script will automatically try lower-quality options.
- **Mirroring:** Optionally create a horizontally mirrored version of each video.
- **Channel Range Download:** Download all videos from a channel or specify a range (e.g., 5-7) for more flexibility.
- **User-friendly Terminal Output:** Clear, colorized output with visible exit options at every prompt.

## Features

- **Multiple Download Modes:**
  - **Single Video Download:** Download one TikTok video and optionally create a mirrored version.
  - **Channel Download:** Download all videos from a TikTok channel or a specific range of videos.
  
- **Quality Options:**
  - **High Quality:** `bestvideo+bestaudio/best`
  - **Medium Quality:** `best[height<=720]`
  - **Low Quality:** `worst`
  - **Custom Option:** List available formats and enter a custom format string.
  - **Automatic Fallback:** If a chosen format is unavailable, the script automatically tries lower-quality options in order.

- **Mirroring Option:**
  - Uses MoviePy to apply a horizontal flip (mirror) to the downloaded video.

- **Robust Input Validation:**
  - Every prompt includes a visible **"q. Exit from code"** option.
  - In channel mode, you are first asked if you want to download all videos or specify a range. If you choose a range, the script displays the total video count and then prompts for a range (e.g., `5-7`).

- **Beautiful Terminal Output:**
  - Uses Colorama to produce a clean, colorized, and well-spaced terminal interface.

## Requirements

- Python 3.7 or higher
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [colorama](https://pypi.org/project/colorama/)
- [moviepy](https://github.com/Zulko/moviepy)

You can install these dependencies using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Installation

1. **Clone the repository** (if applicable) or download the project files (`TDw.py` and `requirements.txt`).
2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script using Python:

```bash
python3 TDw.py
```

### Interactive Prompts

- **Download Mode:**  
  Choose between single video download or channel download.
  ```
  Choose download mode:
  1. Single video download
  2. Download entire channel
  q. Exit from code
  Enter 1 or 2 (or q to exit):
  ```

- **Channel Mode – Range Selection:**  
  In channel mode, you are immediately asked:
  ```
  Download all videos (a) or specify a range (r) (or q to exit):
  ```
  - If you choose **a**, the script downloads all videos immediately.
  - If you choose **r**, it then displays the total number of videos found and prompts:
    ```
    Enter the range (e.g., 5-7):
    ```
    * **Note:** When choosing to download videos using a specific range, the script may take some time to count the total number of videos in the channel. The time required depends on the number of videos available, and for large channels with over 2000 videos, it may take up to 15 minutes.
    
- **Quality Selection:**  
  Choose the desired quality from the menu. Options include:
  ```
  1. High (bestvideo+bestaudio/best)
  2. Medium (best[height<=720])
  3. Low (worst)
  4. List available formats and choose custom  
  Each prompt displays an option **q. Exit from code**.
  ```

- **Available Video Formats:**  
  When selecting custom formats, the following options are available:
  ```
  ID                     EXT RESOLUTION │  FILESIZE   TBR PROTO │ VCODEC ACODEC MORE INFO
  ─────────────────────────────────────────────────────────────────────────────────────────
  download               mp4 unknown    │                 https │ h264   aac    watermarked
  h264_480p_1555457-0    mp4 480x854    │  11.45MiB 1555k https │ h264   aac
  h264_480p_1555457-1    mp4 480x854    │  11.45MiB 1555k https │ h264   aac
  h264_540p_946110-0     mp4 576x1024   │   6.96MiB  946k https │ h264   aac
  h264_540p_946110-1     mp4 576x1024   │   6.96MiB  946k https │ h264   aac
  h264_540p_1477035-0    mp4 576x1024   │  10.87MiB 1477k https │ h264   aac
  h264_540p_1477035-1    mp4 576x1024   │  10.87MiB 1477k https │ h264   aac
  bytevc1_540p_1210832-0 mp4 576x1024   │   8.91MiB 1210k https │ h265   aac
  bytevc1_540p_1210832-1 mp4 576x1024   │   8.91MiB 1210k https │ h265   aac
  bytevc1_720p_1698004-0 mp4 720x1280   │  12.50MiB 1698k https │ h265   aac
  bytevc1_720p_1698004-1 mp4 720x1280   │  12.50MiB 1698k https │ h265   aac
  ```


- **Mirroring Option:**  
  Decide whether you want a mirrored version of the video(s).

- **Universal Exit:**  
  At every prompt, type **q** to exit the program immediately.

## File Naming Convention

- **Single Video Downloads:**  
  Saved in the `Downloaded` folder as `0001 - <videoID>.mp4` and, if mirrored, as `0001 - Mirrored_<videoID>.mp4`.

- **Channel Downloads:**  
  Saved in `Downloaded/<channel_username>` (or `Download/Mirrored_<channel_username>` if mirroring is enabled) with 4-digit numbering (e.g., `0005 - <videoID>.mp4`).

## License

This project is provided "as is" without any warranty. You are free to use and modify it for your personal projects.

### Disclaimer
This project is for educational purposes only. The use of this software must comply with the **TikTok Terms of Service**, which prohibit downloading content without explicit permission unless a download option is provided within the app. The creator of this project is not responsible for any misuse, legal issues, or violations arising from its use. Users are solely responsible for ensuring they comply with local laws and platform policies.
