# tidy

A small command-line tool that sorts the files in a folder into subfolders by type
(Images, Documents, Spreadsheets, and so on). Python standard library only.

It previews by default and never overwrites an existing file.

## Usage

```
python tidy.py ~/Downloads            # preview what would move
python tidy.py ~/Downloads --apply    # actually move the files
```

Only files directly inside the folder are touched. Subfolders and hidden files are left alone.
If a file with the same name already exists at the destination, the new one is renamed
`name (1).ext` instead of replacing it.

## Tests

```
python -m unittest -v
```

## Customizing

Edit the `CATEGORIES` dictionary at the top of `tidy.py` to add file types or new folders.
