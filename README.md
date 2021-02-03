# Songbook

This project builds upon the **Superzpěvník** project by *simberaj* by allowing
to apply user custom configuration to the built songbook.

## Usage

How to use this project?

1. Clone this project with `git clone --recursive` or (if you have forgotten), run `git submodule update --init` in the root directory of the project.
2. Figure out the changes you'd like to make to the default songbook.
3. Write a configuration file to represent the changes
4. Run `python3 run.py <path-to-config-file>`

## Configuration file

The configuration file is a YAML file with the following syntax:

```yaml
page_numbers: <bool>
songs:
- "[<author>:]<title>":
- "[<author>:]<title>":
      [ capo: <int> ]
      [ transpose: <int> ]
```

Example:
```yaml
page_numbers: true
songs:
   - "A té Réhradice":
   - "Mám jizvu na rtu":
         transpose: -2
   - "Nohavica:*":
   - "Co jste has":
   - "Colorado":
         capo: 2
```

The first line matching a song shall be applied - write your config files in "specific-to-generic" order.

Use `*` as placeholders for "anything". More specialized regexes are not supported yet.

## How does it work

1. Scan all source directories and build a list of (title, author, path) SongFiles.
2. Build a _source_ directory
   1. For each song in the configuration:
      1. Copy the song to the _source_ directory
      2. If there are any transformations to be applied, apply them
3. Build the _init_ file
   1. Take the _init.tex_
   2. Apply unconditional fixes
   3. Based on the configuration, apply additional fixes
   4. Write the modified file to the _source_ directory
4. Build the song-book using the original scripts, but using our modified _init.tex_ and the songs from the _source_ directory