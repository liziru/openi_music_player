from musicdl import musicdl

config = {'logfilepath': 'musicdl.log', 'savedir': 'downloaded', 'search_size_per_source': 5, 'proxies': {}}
target_srcs = [
    'baiduFlac', 'kugou', 'kuwo', 'qq', 'qianqian', 
    'netease', 'migu', 'xiami', 'joox', 'yiting',
]
client = musicdl.musicdl(config=config)
client.run(target_srcs)

