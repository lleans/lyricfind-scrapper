from asyncio import get_event_loop
from aiohttp import ClientSession
from LyricsFindScrapper import Search, Track, SongData, Translation

async def test():
    session: ClientSession = ClientSession()
    client: Search = Search(session=session)
    tracks: list[Track] = await client.get_tracks('Anytime anywhere milet')
    first_track: SongData = await client.get_lyrics(track=tracks[0])
    
    # Print all the attributes(access the origin if you want the raw data)
    attributes = vars(first_track)
    for attribute, value in attributes.items():
        if not attribute == 'origin':
            print(f"{attribute}: {value}")

    print("\n\n")

    translated_first_track: Translation = await client.get_translation(track=tracks[0], lang='en')

    attributes = vars(translated_first_track)
    for attribute, value in attributes.items():
        if not attribute == 'origin':
            print(f"{attribute}: {value}")

c = get_event_loop()
c.run_until_complete(test())
c.close()