# Devoice

Devoice is a QT app that extracts stems (voice, drums, etc) from a song.
At the moment, it only supports the [Demucs](https://github.com/facebookresearch/demucs) backend, but [Spleeter](https://github.com/deezer/spleeter) is also planned to be an option.

# TODO

- [ ] Move progress bar to a modal dialog (and create worker thread there)
- [ ] Bulk convert interface

# Requirements

- Python >= 3.7
- PyQt5 5.11.3
- Demucs 2.0.2 (And its own dependencies -- Latest version might also work)
