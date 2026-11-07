# Image, video, and audio recipes

These are observations from this user's installation, collected in October 2026. Read the live model help and exported presets for the current schema. Support varies with the installed model.

## Images: Krea 2 / Turbo

The user confirmed this installed image setup worked well:

| Setting | Starting value |
| --- | --- |
| UI model family | Krea 2 |
| Variant | Turbo |
| Inference steps | 8 |
| Resolution category | 720p |
| Resolution budget | 1280x512 |

Use the current exported preset's actual `model_type`, dimensions, mode, and remaining required fields. The display name is not necessarily the API model ID. Choose another supported size when the project requires a different composition. Reuse downloaded models/settings instead of starting setup over.

### Repeatable image batch

1. Identify asset roles and final paths in the current project: background, character reference, item, texture, or illustration.
2. Establish art direction and framing. Reuse approved descriptions for a consistent series. Preserve existing character/setting references when provided.
3. Export/read the selected image preset. Create one queue record per image with a complete prompt, its own ID, and a recorded seed.
4. For image-to-image/reference work, inspect that model's supported mode and reference fields. Use a ZIP bundle containing the images. Do not assume text-to-image settings enable reference conditioning.
5. Write the manifest and submit through the API workflow. Use a small representative job before committing to a large batch with unproven settings.
6. Follow the same process handle while doing independent work. Collect original outputs, record actual dimensions and source paths, and copy accepted images to the requesting project's asset folder.
7. View the images. Check framing, unwanted text, missing objects, style, and aspect ratio. An API receipt is not visual review.

The UI says each prompt line generates a new image. For API batches, use explicit queue records rather than relying on blank lines or added spaces to create jobs. Preserve the full submitted prompt for each image.

### Prompt structure

Use a single complete prompt containing:

```text
[style and medium]. [subject/location and required objects].
[camera angle, composition, aspect ratio, and framing].
[lighting and palette]. [constraints needed by the asset's role].
```

For this user's Room Studio adventures, the established direction is **SCUMM-style, mildly cartoonish game art**. Apply that only when relevant to the current project:

- Room backgrounds: readable architecture and exits, floor visible from the farthest to nearest walkable locations, no baked-in characters when characters will be 3D objects. Leave useful space around interaction targets.
- Character model reference: whole body including feet, requested neutral/T/A pose, clear silhouette, simple background, no cropped limbs or unwanted handheld props.
- Inventory items: isolated readable silhouette, large enough within the frame to work at icon size. Do not promise transparent output unless the active workflow actually produces an alpha channel.
- Close-ups/overlays: generate framing for that view rather than enlarging a mismatched background detail.

These are art guidelines, not instructions to edit the game engine, floor calibration, or story JSON during an asset-generation task.

## Video, music, and sound effects

Discover the installed model for the requested modality and inspect its help/preset. Do not assume Krea or OmniVoice can do every modality. Preserve model-specific frame counts, duration limits, input requirements, and resolution formats from current settings. The queue/session/manifest workflow is shared; generation parameters are model-specific.

For video, keep reference/start/end images in the bundle when required. For music and effects, record requested duration, loop requirements, prompt, and whether vocals are wanted. Review the actual result and record its length/format. Do not label audio seamless or a video loopable without inspecting the boundary.

## OmniVoice speech

An older local speech batch produced static; the user subsequently supplied a clear sample on **2026-10-22** with:

| Setting | Successful sample |
| --- | --- |
| Model | TTS OmniVoice |
| Language | Auto |
| Voice instruction | female |
| Guidance | 2 |
| Steps | 32 |
| Pause | 0.2 seconds |
| Adjust Speed | No |
| Seed | 22029000 |

Text in that sample:

```text
I told you this would happen.[laughter] But no, nobody listened. Dont you feel dumb now ? [question-en] What now?
```

The reported output was 6.8 seconds mono and took 17 seconds to generate at that time. This is historical evidence, not a performance guarantee. Language/settings are a useful lead for the static issue; the exact root cause was not isolated. Avoid reintroducing the failed forced-language/temperature overrides without a reviewed sample.

The existing queue settings used this baseline (merge into a live compatible preset):

```json
{
  "model_type": "omnivoice",
  "model_mode": "auto",
  "num_inference_steps": 32,
  "guidance_scale": 2,
  "duration_seconds": 0,
  "pause_seconds": 0.2,
  "custom_settings": {"adjust_speed_to_max_duration": "No"},
  "multi_prompts_gen_type": "FG",
  "repeat_generation": 1
}
```

### Voice design versus cloning

- **Voice Design:** Voice Instruction contains supported comma-separated tags such as `female, young adult, british accent`.
- **Voice Cloning:** That field instead contains the **exact reference transcript**, or is blank for automatic transcription. Do not substitute design tags for the transcript.
- **Dialogue:** Use `Speaker 1:`, `Speaker 2:`, etc. matching the supplied references.
- **Performance:** Supported non-verbal tags such as `[laughter]` or `[sigh]` belong in spoken text. Inspect the model's input help for its complete tag list. Tags differ across providers.
- Save clean display subtitles separately from the tagged generation text, with a stable speaker ID and audio path.

The previous cloning builder supplied:

```python
params.update(
    prompt='Exact spoken line',
    alt_prompt='Exact words spoken in the reference audio',
    audio_prompt_type='A',
    audio_guide='references/speaker.wav',
    seed=22029001,
)
```

Use the current preset to verify those field names remain valid. Package `references/speaker.wav` in a ZIP with `queue.json`; plain queue JSON previously discarded reference paths.

### Speech quality and voice continuity

Generate and listen to a representative line when establishing or changing a voice. Check intelligibility, static, character age/accent, acting, missing words, and long silences. A valid WAV, nonzero waveform, or successful status cannot prove clear speech. If listening is unavailable, provide the sample for the user and state that limitation before treating a large batch as approved quality.

Keep approved references, exact transcripts, voice settings, seeds, speaker names, clean subtitles, and output filenames together in the requesting project. Clone only references the user has supplied or authorized for that project. Do not resume old failed voice batches merely because the app is available. The earlier Mara project's use of ElevenLabs does not establish a provider requirement for other projects.
