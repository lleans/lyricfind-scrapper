# Lyric Find Scrapper 🎹

LyricsFind is free online lyrics database, using simple scrapper PyQuery and Aiohttp to grab lyrics from the free-website.

## Option 💽

There's an multiple option on <code>Search</code> class. On there you can change the:

- **<code>teritory</code> iso code e.g 'us'(all lower)** _(optional)_<br>
  The usage of this params is, to limit yourself based on country you are( the default value is by searching your ip location)

  ```python
  from LyricsFindScrapper import Search

  session = #your http client
  client: Search = Search(
      session=session,
      teritory='us'
      )
  ```

- **<code>limit</code> use in params** _(optional)_<br>
  You can change the limit request to service. Defaulting on 10, just be mindful what you do.

  ```python
  from LyricsFindScrapper import Search

  session = #your http client
  client: Search = Search(
      session=session,
      limit=10 # Be mindful what you change, bigger number may cuase you're being blocked by server
      )
  ```

## Function 🪛

There are a few funstions that usable as:

- **<code>get_tracks(query: str)</code> query as params(type str)**<br>
  Just like on the website, you can search an multiple tracks by using the query/title/artist/etc. This will return multiple list of <code>Track</code> class.

  ```python
  from LyricsFindScrapper import Search, Track

  session = #your http client
  client: Search = Search(session=session)

  #Make sure you're on async func.
  #Getting tracks e.g
  tracks: list[Track] = client.get_tracks(
     query=#Your song title
  )
  ```

- **<code>get_lyrics(track: Track)</code> track as params(type Track)**<br>
  The tracks that you already got, pass it here to get the lyrics. This will return class of <code>SongData</code>.

  ```python
  from LyricsFindScrapper import Search, Track, SongData

  session = #your http client
  client: Search = Search(session=session)

  #Make sure you're on async func.
  #Getting tracks e.g
  tracks: list[Track] = client.get_tracks(
     query=#Your song title
  )

  #Getting lyrics e.g
  lyrics: SongData = client.get_lyrics(
     track=tracks[0]
  )
  ```

- **<code>get_translation(track: Track, lang: str)</code> tracks and lang as params(type Track and str)**<br>
  Sometime LyricFind will provide the translation of the lyrics(if it exist. Check on their website). On <code>Track</code> class you can find the <code>available_translation</code>(if it exist) select the language you wanted, pass it on <code>lang</code> as params. It will return you <code>Translation</code> class(identical with <code>SongData</code> only few changes).

  ```python
    from LyricsFindScrapper import Search, Track, SongData

    session = #your http client
    client: Search = Search(session=session)

    #Make sure you're on async func.
    #Getting tracks e.g
    tracks: list[Track] = client.get_tracks(
       query=#Your song title
    )

    #Getting lyrics e.g
    lyrics: SongData = client.get_lyrics(
       track=tracks[0]
    )

    #Getting Translation e.g
    translation: Translation = client.get_translation(
       track=tracks[0],
       lang='en'
    )
  ```

## Data Model 📅

All data model, you can acccess it [here 🎯](LyricsFindScrapper/model.py)

## Setup 🧩

If you want to use this on your local machine, download this repo, and make sure you run on virtualenv(it's optional)

1. Open terminal on the repo just you download, then run 📚
   <br />`pip install -r requirements.txt` to install required library
2. Then read and run it(dont mind the error, it's just for example) 📖
   <br />`press f5 if you on vscode`
   <br />`python demo.py` if you using terminal

## About PyPi ? 🐍

about that, if you wanted to install this repo as library search on google pip install from github, currently i dont wanna this published on PyPi i just wanna keep this humble on underground library, let's see if i need it to published later
