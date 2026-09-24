# 🎬 YouTube → Shorts Pipeline

> An automated, **$0-cost** workflow that turns a long-form YouTube video into original short-form vertical clips — with local transcription, programmatic charts, and no paid APIs.


---


## 🎯 What This Does

This pipeline takes **one YouTube video** and produces **multiple original short-form clips** ready for TikTok, YouTube Shorts, or Instagram Reels.

```
┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌──────────────┐
│  1. Audio   │ → │ 2. Transcribe│ → │ 3. Rewrite  │ → │ 4. Generate  │
│  Extraction │   │   (Whisper)  │   │  + Charts   │   │    Videos    │
└─────────────┘   └──────────────┘   └─────────────┘   └──────────────┘
     yt-dlp          local CPU         matplotlib          FFmpeg
     FFmpeg          $0                Edge TTS            $0
     $0                                $0                  $0
```

**Every stage runs locally. No API keys. No subscriptions. No cloud upload.**

---

## ⚙️ How It Works

| Step | What Happens | Tool | Output |
|------|--------------|------|--------|
| **1** | Downloads audio from YouTube | `yt-dlp` + FFmpeg | `data/source_audio.mp3` |
| **2** | Transcribes speech to text | Whisper `medium` (local) | `data/source_audio.txt` |
| **3a** | Renders charts from raw data | matplotlib | `data/chart*.png` |
| **3b** | Generates voiceover narration | Edge TTS | `data/voice*.mp3` |
| **4** | Combines chart + voice into vertical video | FFmpeg | `data/clip*.mp4` |

---

## ✅ Prerequisites

Before you start, make sure you have:

- [ ] **Python 3.10+** — [download here](https://python.org/downloads/)
- [ ] **FFmpeg** on your PATH
- [ ] **~2 GB free disk space** (for the Whisper model)
- [ ] **Internet connection** (for model download + Edge TTS)
- [ ] **Firefox** installed and logged into YouTube *(if you hit bot-detection errors)*

---

## 🚀 Installation

### Step 1 — Install Python

Download from [python.org](https://python.org/downloads/) and **check the box "Add python.exe to PATH"** during installation.

Verify:

```cmd
python --version
```

You should see something like `Python 3.13.2`.

---

### Step 2 — Install FFmpeg

<details>
<summary><b>🪟 Windows</b> (click to expand)</summary>

1. Download a build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) — get `ffmpeg-release-essentials.zip`
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH:
   - Press `Win + R` → type `sysdm.cpl` → Enter
   - **Advanced** tab → **Environment Variables**
   - Under **User variables**, select **Path** → **Edit** → **New**
   - Add `C:\ffmpeg\bin`
   - Click OK on all windows
4. **Close and reopen** your terminal
5. Verify:

```cmd
ffmpeg -version
```

</details>

<details>
<summary><b>🍎 macOS</b></summary>

```bash
brew install ffmpeg
```

</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Debian/Ubuntu
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

</details>

---

### Step 3 — Clone and Install Dependencies

```cmd
git clone https://github.com/<your-username>/yt-shorts-pipeline.git
cd yt-shorts-pipeline
python -m pip install -r requirements.txt
```

> 💡 **Why `python -m pip` instead of `pip`?**
> On Windows, the `pip` shim often isn't on PATH even when Python is. `python -m pip` always works.

---

## ▶️ Running the Pipeline

All outputs go into `data/`. Create it first:

```cmd
mkdir data
```

### 🔹 Step 1 — Extract Audio

```cmd
python src/step1_download_audio.py "https://www.youtube.com/watch?v=KjAI9r8tnOs"
```

**Output:** `data/source_audio.mp3`

<details>
<summary><b>⚠️ Getting HTTP 403 / "Sign in to confirm you're not a bot"?</b></summary>

YouTube blocks unauthenticated downloads intermittently. Fix it by passing Firefox cookies:

1. Open **Firefox** and log into YouTube
2. Re-run:

```cmd
python src/step1_download_audio.py "https://www.youtube.com/watch?v=KjAI9r8tnOs" --cookies-from-browser firefox
```

> Chrome/Edge cookies **do not work** on Windows due to encryption changes. Use Firefox.

</details>

---

### 🔹 Step 2 — Transcribe

```cmd
python src/step2_transcribe.py data/source_audio.mp3 --model medium --language zh
```

**Output:** `data/source_audio.txt`

> ⏱️ **First run downloads ~1.4 GB** (the Whisper `medium` model) to `~/.cache/whisper/`. Subsequent runs load instantly from disk.
>
> 🐢 **On CPU**, expect roughly 1–2× the audio length. A 10-minute file takes 10–20 minutes.
>
> 💾 **Tight on RAM?** Use `--model small` instead (466 MB).

---

### 🔹 Step 3a — Generate Charts

```cmd
python src/step3_make_charts.py
```

**Output:** `data/chart1_payments.png`, `data/chart2_tainan.png`, `data/chart3_burden.png`

> 📊 Charts are rendered **from raw data** with matplotlib — no screenshots of the original source. This is both a legal requirement and a cost win.

---

### 🔹 Step 3b — Generate Voiceovers

Edit the scripts in `scripts/` to your rewritten narration, then:

```cmd
python src/step3_make_voiceover.py
```

**Output:** `data/voice1.mp3`, `data/voice2.mp3`, `data/voice3.mp3`

<details>
<summary><b>🎙️ Want a different voice?</b></summary>

```cmd
python src/step3_make_voiceover.py --voice en-US-JennyNeural
```

| Voice | Description |
|-------|-------------|
| `en-US-GuyNeural` | Male, US English *(default)* |
| `en-US-JennyNeural` | Female, US English |
| `en-US-AriaNeural` | Female, expressive |
| `en-GB-RyanNeural` | Male, British |

</details>

---

### 🔹 Step 4 — Assemble Videos

```cmd
python src/step4_assemble_video.py
```

**Output:** `data/clip1.mp4`, `data/clip2.mp4`, `data/clip3.mp4` — vertical 1080×1920 shorts.

---

### 🔹 Deduplication Check

Before reprocessing a URL, check the cache:

```cmd
python src/dedup.py "https://www.youtube.com/watch?v=KjAI9r8tnOs"
```

| First run | Second run |
|-----------|------------|
| `New video. Proceeding.` | `Already processed on <timestamp>. Skipping.` |

This prevents redundant downloads, transcriptions, and generations.

---

## 💰 Cost Breakdown

### Total: **$0**

| Stage | Tool | Cost | Why |
|-------|------|------|-----|
| Audio extraction | yt-dlp + FFmpeg | **$0** | Open-source, local |
| Transcription | Whisper `medium` (local) | **$0** | One-time model download, no per-minute fees |
| Charts | matplotlib | **$0** | Programmatic, no design tools |
| Voiceover | Edge TTS | **$0** | Microsoft neural voices, free |
| Assembly | FFmpeg | **$0** | Industry-standard, scriptable |
| **Total** | | **$0** | |

### The Real Cost: Time

| Stage | Wall-clock (10-min source) |
|-------|----------------------------|
| Audio extraction | ~10 sec |
| Whisper model download *(first run)* | ~3.5 min |
| Transcription (`medium`, CPU) | ~10–20 min |
| Chart generation | ~2 sec |
| Voiceover (3 clips) | ~15 sec |
| Video assembly | ~10 sec |
| **Total** | **~25–30 min** |

> 🚀 **GPU or Apple Silicon?** Whisper uses it automatically and cuts transcription to ~1–2 minutes.

---

## ⚖️ Copyright & Legal

This pipeline produces **original derivative content**, not reproductions.

- ✅ **Scripts are rewritten** — sentence structure and wording differ completely from the source
- ✅ **Charts are regenerated** — matplotlib renders from raw data, no screenshots
- ✅ **Source is cited verbally** — every script begins with *"According to [source]'s reporting..."*
- ❌ **No narration is copied word-for-word**

---


---

## ❓ FAQ

<details>
<summary><b>Do I need an OpenAI API key?</b></summary>

No. Whisper runs entirely locally. The only "download" is the model weights (~1.4 GB), which is a one-time cost.
</details>

<details>
<summary><b>Can I use this for any YouTube video?</b></summary>

Technically yes, but **legally you must rewrite the content**. This pipeline is designed for creating original derivative works, not republishing.
</details>

<details>
<summary><b>Why is transcription so slow?</b></summary>

Whisper on CPU is compute-heavy. The `medium` model trades speed for accuracy. If you need speed, use `small` or `base`.
</details>

<details>
<summary><b>Can I run this without Firefox?</b></summary>

Yes — but if YouTube blocks you with a 403, Firefox cookies are the most reliable fix on Windows.
</details>

<details>
<summary><b>How do I add more clips?</b></summary>

Add a `script4.txt` to `scripts/`, add a matching chart function in `step3_make_charts.py`, and add an entry to the `CLIPS` list in `step4_assemble_video.py`.
</details>

<details>
<summary><b>Can I use a different TTS voice?</b></summary>

Yes — pass `--voice` to `step3_make_voiceover.py`. Run `python -m edge_tts --list-voices` to see all options.
</details>

<details>
<summary><b>Does this work on macOS / Linux?</b></summary>

Yes. Only the FFmpeg install and the PATH setup differ. All Python scripts are cross-platform.
</details>

---

## 📄 License

MIT — free to use, modify, and distribute.

---

## 🙏 Credits

Built as a demonstration of **cost-aware pipeline design** — proving that a full video-generation workflow can run at $0 with local, open-source tools.

**Source material:** [The Reporter (報導者)](https://www.twreporter.org/) — used here for educational/demo purposes under fair use, with full attribution.
