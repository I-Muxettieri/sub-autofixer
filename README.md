# Sub autofixer

Auto fix subtitles styles and resample using Advanced SubStation Alpha.

## Features

- ### ass converter
  changes subtitles into ass format, supported:
  - srt
- ### resample resolution (aegisub function)
  resolution will be resampled if video path is provided.
- ### prospectic resample resolution (arch1t3ct lua macro)
- ### restyler

  Custom restyler, change the styles.txt with you own styles to restyle subs with them.\
  It's possible to add more than one style, but they will only be added to the output file.

  In addition, all events are sorted, keeping dialogue events at the top and typesetting events at the end of the file.

## Requirements

- [aegisub](https://github.com/arch1t3cht/Aegisub)
- [aegisub-cli](https://github.com/arch1t3cht/Aegisub) (precompiled binaries in bin folder [here](https://github.com/I-Muxettieri/sub-autofixer/blob/main/bin/aegisub-cli.exe))
- [arch1t3ct prospectic resample](https://github.com/TypesettingTools/arch1t3cht-Aegisub-Scripts/blob/main/macros/arch.Resample.moon)
- python
- pysubs2

## Usage

Put aegisub-cli binaries in aegisub folder and add it to PATH.

Put arch1t3ct resample script in your automation folder:

```bash
  appdata/aegisub/automation/autoload
```

Install pysubs2:

```bash
  pip install pysubs2
```

Run the script:

```bash
  python sub_autofixer.py test/input -v path/to/video.mkv -o test/output
```

Out dir is optional, default is "output".
