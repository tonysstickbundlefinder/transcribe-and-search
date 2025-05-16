<h1 style="text-align: center;">Tony's Stick Bundle Finder</h1>

<div style="text-align: center;">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/version-0.1.0-green.svg" alt="Version">
</div>

## 📌 Overview

Tony Hinchcliffe [hires two people](https://youtu.be/SGECF7cIeFo?t=3461) to count the number of occurrences of a 
certain word mentioned in Kill Tony, so they can censor it to avoid demonetization.

This tool uses a locally run AI transcription model to do this automatically.

## ✨ Features
- Locally run web app to load the relevant video, enter words/phrases of interest, and submit for processing.

![run.png](img/run.png)

- Produces a summary with timestamps and context of all instances of that word identified. Clicking a row will jump to 
    that portion of the video for manual review.

![results.png](img/results.png)

- Runs entirely locally, so there is no concern about the video being leaked, or requirement to trust a third-party 
    provider. 
- Takes less than 5 minutes to transcribe and search a 2hr 20min video on my power-limited Nvidia RTX 3090

## 🚨 Requirements
- Nvidia GPU with at least 6GB of vRAM.
- Either Windows or Linux (can run on a windows/linux machine and access the web app from a MacOS computer connected to
    the same local network if required).
- Anybody with a low-mid tier gaming PC can run this.

## 🚀 Quick Start - Docker Desktop

### 1. Install Docker Desktop
- **Download**: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
- **Install**: Double-click the downloaded file and follow installation prompts

### 2. Enable GPU Support
1. Open Docker Desktop
2. Click ⚙️ **Settings** → **Resources** → **GPU**
3. Check `Enable GPU support`
4. Select your GPU(s) from the list
5. Click **Apply & Restart**

## 3. Get the Application
**UI Method**:
1. Open Docker Desktop
2. Go to **Images** tab
3. Search `tonysstickbundlefinder/transcribe-and-search` in search bar
4. Click **Pull** and select `v0.1.0` tag

**CLI Method**:  
```bash
docker pull tonysstickbundlefinder/transcribe-and-search:v0.1.0
```

## 4. Start the Application
**UI Method**:
1. In **Images** tab, find the pulled image
2. Click **Run**
3. Under **Optional settings**:
   - Ports: `7860:7860`
   - GPU: Check `Use all available GPUs`
4. Click **Run**

**CLI Method**:  
```bash
docker run --gpus all -p 7860:7860 --rm tonysstickbundlefinder/transcribe-and-search:v0.1.0
```

## 5. Use the Web Interface
1. Open your browser to: [http://localhost:7860](http://localhost:7860)
2. **Upload** your video file
3. Enter search terms (comma-separated)
4. Click **Submit**
5. Wait for processing and view results

**Tip**: Both methods can be used interchangeably - the web interface remains the same once running.

## 🛠️ Methodology

- Audio is extracted from the uploaded video.
- Extracted audio is run through the [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) 
    model to produce a complete transcript with timestamps.
- That transcript is then searched for each word/phrase entered (and variants of those words)
    to identify when they occur.

## 📄 License
This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.
