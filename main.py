from musicdl.musicdl import musicdl

# config = {'logfilepath': 'musicdl.log', 'savedir': 'downloaded', 'search_size_per_source': 5, 'proxies': {}}
# target_srcs = [
#     'baiduFlac', 'kugou', 'kuwo', 'qq', 'qianqian',
#     'netease', 'migu', 'xiami', 'joox', 'yiting',
# ]
# client = musicdl.musicdl(config=config)
# # client.run(target_srcs)
# client.run_by_input(target_srcs, user_input='ai')

mlclient = musicdl.musicdl(
    config={'logfilepath': 'musicdl.log', 'savedir': 'downloaded', 'search_size_per_source': 5, 'proxies': {}})
mlclient.run_by_input(['qq', 'netease'], user_input='ai')
