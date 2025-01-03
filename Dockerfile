FROM cm2network/csgo:latest

WORKDIR /home/steam/csgo

RUN apt-get update && apt-get install -y \
    unzip \
    curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -SL "http://www.metamodsource.net/mmsdrop/1.12/mmsource-1.12.0-git1145-linux.tar.gz" -o mmsource.tar.gz && \
    mkdir -p addons/metamod && \
    tar -xzf mmsource.tar.gz -C addons/metamod --strip-components=1 && \
    rm mmsource.tar.gz

RUN curl -SL "https://github.com/YourCounterStrikeCSharpRepo/Release/latest/download/CounterStrikeCSharp.zip" -o cscsharp.zip && \
    unzip cscsharp.zip -d addons/sourcemod/plugins && \
    rm cscsharp.zip

RUN chown -R steam:steam /home/steam/csgo

ENTRYPOINT ["/home/steam/csgo/srcds_run"]
CMD ["-game", "csgo", "-console", "-usercon", "+game_type", "0", "+game_mode", "1", "+mapgroup", "mg_active", "+map", "de_dust2"]