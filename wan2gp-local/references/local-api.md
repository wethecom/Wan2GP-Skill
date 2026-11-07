# Local connection and queue workflow

## Known machine details

These addresses were recorded from the user's Windows installation in October 2026. They are discovery hints, not a claim of current availability:

| Purpose | Address |
| --- | --- |
| Direct Gradio app | `http://127.0.0.1:42003` |
| Local sharing/proxy | `http://127.0.0.1:999` |
| Previously advertised LAN URL | `http://192.168.1.10:999` |

The recorded Gradio version was **5.29.0**. Ports, API signatures, LAN IP, and selected models can change. The direct Gradio app is preferred for API work. Do not assume the sharing page exposes the same routes. A remote/container executor must reach the Windows host, not its own localhost. The LAN URL was advertised by the app; remote reachability was not confirmed.

The app install and output directories are not hard-coded in this package. Resolve them from the current launcher, runtime settings, and returned output paths. A directory named `WanGP-Recovery-20261021` contains historical recovery material; it is not evidence of the live install or output directory.

## Read-only discovery

Use an available Python runtime with the standard library. This snippet only reads configuration:

```python
import json
import urllib.request

base = 'http://127.0.0.1:42003'  # replace with the running URL
with urllib.request.urlopen(base + '/config', timeout=10) as response:
    config = json.load(response)
print('Gradio:', config.get('version'))
names = {'load_queue_action', 'init_process_queue_if_any', 'process_tasks'}
for dep in config.get('dependencies', []):
    if dep.get('api_name') in names:
        print({key: dep.get(key) for key in
               ('api_name', 'id', 'inputs', 'outputs', 'targets')})
```

Use the running app's API information and model help for full signatures. Filter configuration output; complete dumps can be several megabytes. Do not treat cached endpoint dumps as live truth. If a known endpoint is missing or its inputs differ, adapt to the current API before submitting.

## Queue bundle format

The observed importer accepts a JSON list of records:

```json
[
  {
    "id": 1,
    "params": {
      "model_type": "ACTUAL_ID_FROM_CURRENT_PRESET",
      "prompt": "The complete prompt for this asset",
      "seed": 22029001
    }
  }
]
```

This shows the structure only. Copy the full required settings from a current exported preset for the intended model. Use distinct IDs and recorded seeds for each job. Do not invent the model's resolution, mode, or reference-field parameter names.

For references, create a ZIP containing:

```text
queue.json
references/speaker.wav
references/source-image.png
```

Use only the referenced files needed for the jobs. Reference paths in `params` must match ZIP entries exactly. **The observed plain JSON importer clears reference-media paths. Use a ZIP when a job depends on reference audio or images.** Retain the exact transcript alongside a voice reference.

## Submission client

`../scripts/queue.py` is the existing working standard-library client copied from the local project. It has no additional pip dependency. Resolve its absolute path relative to this installed skill folder, then run:

```powershell
python 'C:/Users/Administrator/.codex/skills/wan2gp-local/scripts/queue.py' --base-url 'http://127.0.0.1:42003' --bundle 'C:/path/to/current-project/output/batch-001.zip' --log 'C:/path/to/current-project/output/batch-001.jsonl'
```

Replace the example paths and URL. Other installations should use their own skill directory.

The command uploads the bundle, calls `load_queue_action`, then `init_process_queue_if_any` and `process_tasks`. It appends via the observed importer and does not explicitly clear the queue. **Starting processing may also run existing queued jobs.** Inspect queue ownership first; if another task owns pending work, resolve that conflict before invoking processing.

Implementation details that matter:

- Derive dependency and component IDs from `/config`; never reuse saved `fn_index` values.
- Pass the declared upload component's ID as `trigger_id` on `load_queue_action`. Omitting it previously invoked queue autoload instead.
- Preserve a single `session_hash` across upload, load, initialization, and processing.
- Read the Gradio event stream and match `event_id`. A queue/join receipt is acceptance, not generation completion.
- The copied client has long HTTP timeouts. Run it as a tracked process and poll its handle with short waits so the user still receives updates.
- It logs operation receipts, errors, and completion, excluding gallery base64. It does not create the project manifest, copy generated files, or establish media quality.
- Write a submission-intent receipt **before** launching it; a connection could fail before the client's first receipt is logged.

Keep a receipt like:

```json
{
  "batch_id": "project-image-001",
  "status": "prepared",
  "base_url": "http://127.0.0.1:42003",
  "bundle": "batch-001.zip",
  "jobs": [
    {
      "id": 1,
      "seed": 22029001,
      "model_type": "FROM_LIVE_PRESET",
      "prompt": "Exact submitted prompt",
      "intended_output": "Art/room-background.png"
    }
  ]
}
```

Also preserve the exact submitted settings/bundle. Update states with evidence and record actual source/output paths on collection. Seeds are useful matching keys, but compare metadata as well because seeds can repeat.

## Recovery

| Symptom | Next action |
| --- | --- |
| Connection refused | Read current app URL and process/launcher state. Do not immediately reinstall or restart. |
| HTML returned instead of JSON | Confirm the direct Gradio URL and API route; the sharing URL may be a proxy landing page. |
| Missing endpoint or unexpected inputs | Inspect live config and API signatures. Do not guess indices. |
| Reference ignored | Inspect ZIP paths, reference mode, transcript, and the current model's reference field names. |
| Timeout/disconnect after submission | Check receipt, existing queue/process, and output folder before retry. If acceptance is uncertain, report uncertainty and reconcile it. |
| Completed with no matching output | Check the configured output folder and returned paths; do not assume a story's historical folder. |
| Speech static or wrong voice | Follow the OmniVoice recipe; review a small sample before continuing the batch. |

Do not execute internal WanGP Python modules as a shortcut to public API generation. Do not stop someone else's queue or GPU work as a recovery step.
