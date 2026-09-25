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
yt-dlp -x --audio-format mp3 --cookies-from-browser firefox "https://www.youtube.com/watch?v=KjAI9r8tnOs"
```

**Output:** `減輕利息推高房價！房市洗牌逐漸台北化！【精華版】 [KjAI9r8tnOs].mp3`

Rename it for easier handling:

```cmd
ren "減輕利息推高房價！房市洗牌逐漸台北化！【精華版】 [KjAI9r8tnOs].mp3" source_audio.mp3
```

<details>
<summary><b>⚠️ Getting HTTP 403 / "Sign in to confirm you're not a bot"?</b></summary>

YouTube blocks unauthenticated downloads with **HTTP 403: Forbidden**. Passing Firefox cookies authenticates the request.

- Open **Firefox** and log into YouTube first
- Chrome/Edge cookies **do not work** on Windows due to encryption changes
- Firefox is the only browser that works reliably for this

</details>

---


### 🔹 Step 2 — Transcribe with Local Whisper

```cmd
python -m whisper source_audio.mp3 --model medium --language zh --output_format txt
```

**Output:** `source_audio.txt`

> ⏱️ **First run downloads ~1.4 GB** (the Whisper `medium` model) to `~/.cache/whisper/`. Subsequent runs load instantly from disk.
>
> 🐢 **On CPU**, expect roughly 1–2× the audio length. A 10-minute file takes 10–20 minutes.
>
> 💾 **Tight on RAM?** Use `--model small` instead (466 MB).

---


### 🔹 Step 3 — Script Rewriting

**Tool**	Manual rewriting, AI-assisted (Deepseek)
The transcript from Step 2 is copyrighted source material. Before it can become video content, it must be **rewritten into original scripts**.

---

#### 3.1 — Extract the Key Data Points

Read the transcript and pull out the facts and figures worth building clips around. For this source:

| Data Point | Value |
|---|---|
| Monthly payment during 5-year grace period (NT$10M loan) | ~NT$15,000 |
| Monthly payment after grace, 35-year term | ~NT$36,000 |
| Monthly payment after grace, 40-year term | ~NT$32,000 |
| Tainan Anping 2024 price increase (after 新清安) | 12.8% YoY |
| Tainan Anping pre-policy unit price | NT$300,000–350,000/ping |
| Tainan Anping post-policy unit price | NT$400,000+/ping |
| Taichung prime area unit price | NT$700,000–800,000/ping |
| Taipei mortgage burden ratio | ~60% |
| Taichung mortgage burden ratio | approaching 45% |

---

#### 3.2 — Write the Rewritten Scripts

Create three script files on your Desktop:

```cmd
cd C:\Users\<you>\Desktop
notepad Script1.txt
notepad Script2.txt
notepad Script3.txt
```

Each script should:
- ✅ Use **completely different sentence structure** from the source
- ✅ Include **verbal attribution** ("According to The Reporter's reporting...")
- ✅ Contain one clear data point
- ❌ **Not copy** any narration word-for-word

<details>
<summary><b>📝 Script 1 — The Grace Period Trap</b></summary>

```
According to reporting by The Reporter, Taiwan's housing subsidy program changed how people buy homes, but not always for the better. Here is the math. On a ten million NT dollar loan, the five year grace period costs about fifteen thousand a month. That sounds manageable. But once the grace period ends, the payment jumps to roughly thirty two thousand on a forty year term, or thirty six thousand on a thirty five year term. That is more than double. The program lowers the entry barrier, but it pushes the real burden further down the road.
```

</details>

<details>
<summary><b>📝 Script 2 — The Taipei-ification of Tainan</b></summary>

```
The Reporter's data shows that since the new housing policy launched, Tainan's Anping district saw a twelve point eight percent year over year price increase. Before the policy, new units there sold for three hundred thousand to three hundred fifty thousand NT dollars per ping. Now they are above four hundred thousand. Meanwhile, Taichung's prime areas have crossed seven hundred thousand to eight hundred thousand per ping, with some high floor units hitting nine hundred thousand. What used to be a central Taiwan price ceiling has been completely rewritten. The south is starting to look like Taipei.
```

</details>

<details>
<summary><b>📝 Script 3 — The Burden Ratio Reality Check</b></summary>

```
Here is a number that matters. According to The Reporter, Taipei's mortgage burden ratio sits at around sixty percent. That means the average buyer spends six out of every ten dollars of income on housing. Central and southern cities used to be far lower. Now they have crossed forty percent, and Taichung is approaching forty five percent. When you cross forty five percent, housing becomes a genuinely heavy load. The Reporter's conclusion is blunt. The subsidy solved interest, but it pushed up total prices. Without wage growth, the real problem does not go away.
```

</details>

---

#### 3.3 — Compliance Checklist

| Requirement | Status |
|---|---|
| Sentence structure and wording rewritten | ✅ Each script is fully original phrasing |
| Charts regenerated from scratch | ✅ matplotlib from raw data (Step 4) |
| Source cited verbally | ✅ "According to The Reporter..." in every script |
| No reproduction of original narration | ✅ No sentence copied word-for-word |

---

### 🔹 Step 4 — Generate Charts
Create make_charts.py on your Desktop with the chart-generation code(uploaded), then run:
```cmd
python make_charts.py
```

**Output:** `chart1_payments.png`, `chart2_tainan.png`, `chart3_burden.png`

> 📊 Charts are rendered **from raw data** with matplotlib — no screenshots of the original source. This is both a legal requirement and a cost win.

---

### 🔹 Step 5 — Generate Voiceovers with Edge TTS

```cmd
cd C:\Users\<you>\Desktop

python -m edge_tts --file Script1.txt --voice en-US-GuyNeural --write-media voice1.mp3
python -m edge_tts --file Script2.txt --voice en-US-GuyNeural --write-media voice2.mp3
python -m edge_tts --file Script3.txt --voice en-US-GuyNeural --write-media voice3.mp3
```

**Output:** `voice1.mp3`, `voice2.mp3`, `voice3.mp3`

<details>
<summary><b>🎙️ Want a different voice?</b></summary>

| Voice | Description |
|-------|-------------|
| `en-US-GuyNeural` | Male, US English *(default)* |
| `en-US-JennyNeural` | Female, US English |
| `en-US-AriaNeural` | Female, expressive |
| `en-GB-RyanNeural` | Male, British |

</details>

---

### 🔹 Step 6 — Assemble Videos with FFmpeg

Make sure you're on the location where all six files (3 charts + 3 voiceovers) are present. In my case the files were stored in desktop:
```cmd
cd C:\Users\<you>\Desktop
dir chart*.png voice*.mp3
```

Run the three assembly commands:

```cmd
ffmpeg -loop 1 -i chart1_payments.png -i voice1.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white" clip1.mp4

ffmpeg -loop 1 -i chart2_tainan.png -i voice2.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white" clip2.mp4

ffmpeg -loop 1 -i chart3_burden.png -i voice3.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white" clip3.mp4
```

**Output:** `clip1.mp4`, `clip2.mp4`, `clip3.mp4` — vertical 1080×1920 shorts.

---

### 🔹 Deduplication Check

Before reprocessing a URL, check the cache to avoid redundant work:

```cmd
python -m dedup "https://www.youtube.com/watch?v=KjAI9r8tnOs"
```

| First run | Second run |
|-----------|------------|
| `New video. Proceeding.` | `Already processed on <timestamp>. Skipping.` |

This prevents redundant downloads, transcriptions, and generations if you accidentally re-run the pipeline on the same source..

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
