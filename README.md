---
name: wan2gp-local
description: Connect to the user's local Wan2GP (WanGP, wangp, or wan2gp) installation and generate images, video, speech, music, or sound effects using its installed models. Use for local asset generation, Krea image batches, OmniVoice speech, reference-media jobs, queue submission, output collection, or troubleshooting the local Gradio connection. Includes a reusable queue client and this machine's known working image and voice settings.
---

# Wan2GP local generation

Generate assets for the project that invoked this skill. This package is self-contained; it does not require the original Room Studio project.

## Read the relevant reference

- Connection, API submission, receipts, and recovery: [Local API workflow](references/local-api.md).
- Images, Krea 2 Turbo, video, speech, and audio: [Generation recipes](references/generation-recipes.md).
- Submission client: [queue.py](scripts/queue.py). It uploads and starts work immediately; it is not a discovery or dry-run command.

## Workflow

1. **Resolve the running app.** Try the known local direct address `http://127.0.0.1:42003` with a read-only `/config` request. Treat this as a historical starting address, not a permanent port. Read the current URL from the app/launcher when needed. Use an available Pinokio skill for discovery if it is managed there. A container's localhost is not the Windows host.
2. **Inspect the live model and queue.** Discover endpoints and parameter IDs from the current config/API. Preserve installed models and current presets. Do not reinstall, download models, restart the app, clear the queue, or switch providers merely to connect. Inspect pending jobs before calling a process endpoint, which may start other queued work too.
3. **Prepare the project's batch.** Use its requested art style, dimensions, audio direction, and output folder. Start from a current exported preset for the intended installed model. Write a manifest and a unique receipt before submission. Record prompts, seeds, model/settings, source references, intended filenames, and destination. Keep spoken text and clean subtitles separately.
4. **Submit once.** Create queue JSON for text-only jobs or ZIP with `queue.json` and relative reference files for jobs using media. The bundled client preserves one session across upload/load/process and discovers IDs at runtime. Confirm endpoint signatures still match its supported workflow before invoking it.
5. **Follow the existing job.** Preserve the process/session handle and JSONL log. Work on independent tasks while generation runs. A disconnected stream is not proof that generation failed; reconcile the log, queue, and output folder before retrying. Never silently duplicate a batch.
6. **Collect and review.** Find outputs from the current app settings or returned paths; match them using seeds and metadata, not modification time alone. Copy accepted files to the current project and update its manifest. Preserve app originals. Inspect images and listen to speech; successful API completion alone does not establish quality. Use a representative result before a large batch when the settings or voice are unproven.

## Image generation is a primary use

- The known working image setup is **Krea 2 / Turbo**, **8 steps**, **720p category**, **1280x512 resolution budget**. Use it as a baseline, not a restriction on requested aspect ratio or resolution.
- Resolve the actual model ID and full parameters from the running app. Do not derive the ID from the display label.
- Use one queue record per intended image for repeatable API batches. Save the exact prompt and seed with each output.
- Apply the current project's art direction. For this user's Room Studio game, the established style is mildly cartoonish SCUMM-style adventure art. Other projects need their own direction.
- See the image recipe for room backgrounds, character references, and consistent series.

## Boundaries

- Generating assets does not authorize replacing a project's scene JSON, changing its model installs, or publishing files. Integrate assets according to the user's current request.
- Do not resume old or unrelated batches. Do not default outputs to the Mara story paths from earlier work.
- Audio/video capability depends on models installed in the live app. Inspect model help rather than inventing parameters or supported tags.
- Keep credentials and private references out of shared receipts. Do not silently fall back to a paid service.
- Report submitted, running, completed, and reviewed states accurately. Do not claim a file was generated or sounds right without evidence.
