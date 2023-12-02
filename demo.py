from asyncio import get_event_loop
from aiohttp import ClientSession
from LyricsFindScrapper import Search, Track, SongData, Translation

async def test():
    session: ClientSession = ClientSession()
    client: Search = Search(session=session)
    # Search all of database, return list
    tracks: list[Track] = await client.get_tracks('Anytime anywhere milet')
    # Get only one track, using track id
    track: Track = await client.get_track(trackid=f'lfid:{tracks[0].lfid}')
    # Get lyric info
    first_track: SongData = await client.get_lyrics(track=track)
    
    # Print all the attributes(access the origin if you want the raw data)
    res: dict = first_track.__dict__
    res.pop('origin')
    print(res)

    print("\n\n")

    # Get translated lyric, based passed language
    translated_first_track: Translation = await client.get_translation(track=tracks[0], lang='en')

    res: dict = translated_first_track.__dict__
    res.pop('origin')
    print(res)

    await session.close()

c = get_event_loop()
c.run_until_complete(test())
c.close()