import re

# Expressão regular para canais de TV m3u
m3u_channel_pattern = re.compile(
    r'#EXTINF:-1.*?tvg-id="(?P<tvg_id>[^"]+\.br)".*?tvg-name="(?P<channel>.+?)".*?tvg-logo="(?P<tvg_logo>[^"]+)".*?group-title="(?P<group_title>[^"]+)",(?P<channel_name>.+?)\n(?P<url>http[^\n]+)'
)
# Expressão regular para canais de TV m3u
m3u_channel_pattern = re.compile(
    r'#EXTINF:-1.*?tvg-id="(?P<tvg_id>[^"]+\.br)".*?tvg-name="(?P<channel>.+?)".*?tvg-logo="(?P<tvg_logo>[^"]+)".*?group-title="(?P<group_title>[^"]+)",(?P<channel_name>.+?)\n(?P<url>http[^\n]+)'
)
# Expressão regular para filmes
movie_pattern = re.compile(
    r'group-title="Filmes(?! \|.*(?:Adultos|[Xx]{3}.*Adultos)).*?",(?P<movie>.*?)\n(?P<url>http[^\n]+)',
    flags=re.IGNORECASE,
)
