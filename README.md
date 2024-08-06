# Sub autofixer

Auto fix subtitles styles and resample using Advanced SubStation Alpha.

## Features

- ### ass converter
  changes subtitles into ass format, supported:
  - srt
- ### resample resolution (aegisub function)
  resolution will be resampled if video path is provided.
- ### perspective resample resolution (arch1t3ct lua macro)
- ### restyler

  Custom restyler, change the styles.txt with you own styles to restyle subs with them.\
  The first style is used to dialogue lines, the second for ovelaps.\
  (If there is a style like "ItalicTop" with an8 and i1 these 2 tags will be added inline if your style doesn't have them)\
  It's possible to add more than two style, but they will only be added to the output file.

  In addition, all events are sorted, keeping dialogue events at the top and typesetting events at the end of the file.

- ### overlapper
  Auto overlap lines using timing and alignment.\
  If there are more than two lines for alignment, the style name is set to "Error" for manual correction.
- ### dialogue layer correction
  All dialogue layers are setted to the provided value (Optional, default 90).
- ### cleanup function
  Runs unanimated ScriptCleanup for remove unused styles

## Requirements

- [aegisub](https://github.com/arch1t3cht/Aegisub)
- [aegisub-cli](https://github.com/arch1t3cht/Aegisub) (precompiled binaries in bin folder [here](https://github.com/I-Muxettieri/sub-autofixer/blob/main/bin/aegisub-cli.exe))
- [arch1t3ct perspective resample](https://github.com/TypesettingTools/arch1t3cht-Aegisub-Scripts/blob/main/macros/arch.Resample.moon)
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
