# komga-ingest

A simple and quick ingest system for Komga library

## Requirements
1. Python 3.10+
2. Poetry

## Setup

You will need to setup your source folder at a specific format:

```
/home/ingest/
  ∟ Publisher A
     ∟ Manga 1
        ∟ Volume 1.cbz
  ∟ Publisher B
     ∟ Manga 2
        ∟ Volume 1.cbz
```

The output folder will then be mapped into the following Komga library format
```
/opt/komga/library/
   ∟ Manga 1
     ∟ v01c01.cbz
     ∟ v01c02.cbz
   ∟ Manga 2
     ∟ v01c01.cbz
     ∟ v01c02.cbz
     ∟ v01c03.cbz
```

You can also ignore subfolder if you want to.
