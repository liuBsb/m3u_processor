import re

# Expressão regular para canais de TV m3u
channel_pattern = re.compile(
    r'#EXTINF:-1.*?tvg-id="(?P<tvg_id>[^"]+\.br)".*?tvg-name="(?P<channel>.+?)".*?tvg-logo="(?P<tvg_logo>[^"]+)".*?group-title="(?P<group_title>[^"]+)",(?P<channel_name>.+?)\n(?P<url>http[^\n]+)'
)
# Expressão regular para séries
series_pattern = re.compile(
    r'group-title="[^"]*S[ée]ries[^"]*",?(?P<serie>.+?)\s*S(?P<season>\d{2})\s*E(?P<episode>\d{2})[^\n]*\n(?P<url>http[^\n]+)',
    re.IGNORECASE,
)
# Expressão regular para filmes
movie_pattern = re.compile(
    r'group-title="(?:FILM|FILME|FILMES)(?! \|.*(?:ADULTO[S]?|[Xx]{3}.*ADULTO[S]?)).*?",'
    r"(?P<movie>(?!.*(?:\b[Xx]{3}\b|FHD|H265|HD|4K|UHD|SD|[Cc]anal|[Ll]ive)).*?)\n"
    r"(?P<url>http[^\n]+)",
    flags=re.IGNORECASE,
)
# Expressão regular para conteúdo adulto
adult_pattern = re.compile(
    r'tvg-name="(?P<adult_name>.*?(XXX|ADULTOS).*?)".*?group-title="(?P<adult_group>.*?(FILMES|XXX|ADULTOS).*?)".*?\n(?P<url>http[^\n]+)'
)
