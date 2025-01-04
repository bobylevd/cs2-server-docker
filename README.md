# CS2 dedicated server
## aimed at as little configuration as possible (work in progress obviously)

### Current run instructions:
Set SRCDS_TOKEN 

mkdir -p cs2

sudo chown -R 1000:1000 cs2

sudo chmod -R 755 cs2

docker compose up

## TODO:
- mount configs folder/separate config files
- refactor update plugins
- set up pre/post scripts to unload matchzy / load retakes, or try to use game modemanager
- set up rest api so it would be possible to manage server through discord/telegram bots