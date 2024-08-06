# Sub autofixer

Auto fix subtitles

## Requirements

- aegisub
- aegisub-cli
- arch1t3ct prospectic resample
- python

## Features

- ass converter
- resample resolution (aegisub function)
- prospectic resample resolution (arch1t3ct lua macro)
- restyler

## Usage

Put aegisub-cli binaries in aegisub folder and add it to PATH.
Put arch1t3ct resample script in your automation folder:

```bash
  appdata/aegisub/automation/autoload
```

Run the script:

```bash
  python sub_autofixer.py test/input -v path/to/video.mkv -o test/output
```

Out dir is optional, default is "output"
