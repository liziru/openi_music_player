#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:   LiPingping
# Time:     2021/10/14
# Desc:     Open mini music player main program.

import os
import time
import threading
import numpy as np
import pygame
from musicdl.musicdl import musicdl
from enum import Enum
from pydub.audio_segment import AudioSegment
import datetime

class Status(Enum):
    ''' Status enum of music player.'''
    IS_STOP = 0
    IS_PLAY = 1
    IS_PAUSE = 2


class Musicplayer():
    def __init__(self):
        pygame.init()
        # pygame.mixer.init()
        # musicdl init.
        self.mlclient = musicdl.musicdl(
            config={'logfilepath': 'player.log', 'savedir': '/home/lee/Desktop/workspace/tests/open_project/openi_music_player/download/music', 'search_size_per_source': 5,
                    'proxies': {}})
        # self.musicdl_srcs = ['qq', 'netease']
        self.musicdl_srcs = [
            'baiduFlac', 'kugou', 'kuwo', 'qq', 'qianqian',
            'netease', 'migu', 'xiami', 'joox', 'yiting',
        ]
        self.search_records = {}
        # self.songinfos = []
        self.playlist = []
        self.play_status = Status.IS_STOP  # 0:stop, 1:playing, 2:pause
        self.play_index = 0  # play index to play.
        self.cursong_duration: int = 0

        self.pyevent_process()

    def musicdl_search(self, keyword):
        song_items, self.search_records = self.mlclient.run_by_input(self.musicdl_srcs, user_input=keyword)
        return song_items

    def pyevent_process(self):
        ''' Process pygame event.'''
        # When a song is finished, pygame will add the ONG_FINISHED event to the event queue.
        SONG_FINISHED = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(SONG_FINISHED)

        def wait_event():
            clock = pygame.time.Clock()
            done = False

            while not done:
                # print(1)
                event = pygame.event.wait()
                # for event in pygame.mixer.music.get_endevent():
                # event = pygame.mixer.music.get_endevent()
                # for event in events:
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    # Press right arrow key to increment the
                    # song index. Modulo is needed to keep
                    # the index in the correct range.
                    # if event.key == pygame.K_RIGHT:
                    #     print('Next song.')
                    #     song_idx += 1
                    #     song_idx %= len(SONGS)
                    #     pygame.mixer.music.load(SONGS[song_idx])
                    #     pygame.mixer.music.play(0)
                    pass
                    # When a song ends the SONG_FINISHED event is emitted.
                    # Then just pick a random song and play it.
                elif event.type == SONG_FINISHED:
                    print('INFO: Song finished. Play next song.')
                    self.generate_play_index(ops="plus")
                    self.play_song_of_playlist()

                clock.tick(30)

        # create new thread to listen to target event.
        task = threading.Thread(target=wait_event)
        task.start()

    def check_songinfos(self, songinfos):
        '''Check existence of songinfos.'''
        # check whether song is already downloaded.
        songinfos_done = []
        for si in songinfos:
            song_path = os.path.join(si['savedir'], si['savename'] + '.' + si['ext'])
            if os.access(song_path, os.R_OK):
                print("INFO: Music({}) already exists, no need to download again.".format(song_path))
                songinfos_done.append(si)
        for s in songinfos_done:
            songinfos.remove(s)
        return songinfos, songinfos_done

    # def get_cur_song(self):
    #     ''' Get current playing song.'''
    #     return self.playlist[self.play_index]

    def get_songinfo_by_records(self, records):
        '''Get song items to show from song_infos.'''
        songinfos = []
        for key, value in records.items():
            songinfo = records.get(key, '')
            print(songinfo)
            if songinfo:
                songinfos.append(songinfo)

        return songinfos

    def get_showitems_by_songinfos(self, song_infos):
        '''Get song items to show from song_infos.'''
        items, idx = [], 0
        for songinfo in song_infos:
            items.append(
                [str(idx), songinfo['singers'], songinfo['songname'], songinfo['filesize'], songinfo['duration'],
                 songinfo['album'], songinfo['source']])
            idx += 1
        return items

    def get_playlist(self):
        ''' Get current playing list.'''
        return self.get_showitems_by_songinfos(self.playlist), self.play_index

    def generate_play_index(self, ops="plus"):
        assert ops in ["plus", "sub"], "index ops should be either \"plus\" or \"sub\"."
        # set current index
        if ops == "plus":
            self.play_index += 1
        elif ops == "sub":
            self.play_index -= 1
        if self.play_index < 0 or self.play_index > len(self.playlist):
            print("WARNING: play index({}) will be clipped.".format(self.play_index))
        self.play_index = np.clip(self.play_index, 0, len(self.playlist) - 1)

    def play_last_song(self):
        ''' Last song to play.'''
        self.generate_play_index(ops="sub")
        self.play_song_of_playlist()

    def play_next_song(self):
        ''' Next song to play.'''
        self.generate_play_index(ops="plus")
        self.play_song_of_playlist()

    def play_song_of_playlist(self):
        ''' Play song of playlist according index.'''
        song = self.playlist[self.play_index]
        song_path = os.path.join(song['savedir'], song['savename'] + '.' + song['ext'])
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        # set playing status
        self.play_status = Status.IS_PLAY

        # set current song duratin
        self.set_cursong_duration(song)

    def play(self):
        ''' Play song of playlist.'''

        assert len(self.playlist) != 0, 'No song in playlist.'
        assert pygame.mixer.music.get_busy() is False, 'Play program is busy.'

        if self.play_status == Status.IS_PAUSE:
            print("INFO: cancel pausing.")
            self.unpause()
            return
        self.play_song_of_playlist()

        # song_path_list = []
        # for song in self.playlist:
        #     song_path = os.path.join(song['savedir'], song['savename'] + '.' + song['ext'])
        #     song_path_list.append(song_path)
        # pygame.mixer.music.load(song_path_list[0])
        #
        # if pygame.mixer.music.get_busy() == False:
        #     pygame.mixer.music.play()
        #     # set playing status
        #     self.play_status = Status.IS_PLAY
        #
        # for s in song_path_list[1:]:
        #     pygame.mixer.music.queue(s)

    def pause(self):
        pygame.mixer.music.pause()  # 暂停
        # set playing status
        self.play_status = Status.IS_PAUSE

    def unpause(self):
        pygame.mixer.music.unpause()  # 继续播放
        # set playing status
        self.play_status = Status.IS_PLAY

    def stop(self):
        pygame.mixer.music.stop()  # 停止播放
        # empty playlist
        self.empty_playlist()
        # set playing status
        self.play_status = Status.IS_STOP

    def empty_playlist(self):
        '''Empty playback list.'''
        print("WARNING: playlist is emptyed.")
        self.playlist.clear()

    def add_songs_to_playlist(self, idxs):
        ''' Add songs to playback list by indexes.'''

        songinfos = []
        for i in idxs:
            songinfo = self.search_records.get(i, '')
            print(songinfo)
            if songinfo:
                songinfos.append(songinfo)

        # print(songinfos)
        ## Warning: if file exists, no need to download.
        songinfos_todo, songinfos_done = self.check_songinfos(songinfos)
        songinfos_avail = self.mlclient.download(songinfos_todo)
        songinfos_avail.extend(songinfos_done)
        if len(songinfos_avail) == 0:
            print("WARNING: No songs are available for downloading.")
            return
        print("INFO: Song({}) is added to playlist.".format([songinfo["songname"] for songinfo in songinfos_avail]))
        self.playlist.extend(songinfos_avail)

    ''' Volume setting '''

    def set_volume(self, v):
        ''' Set volume to v.'''
        pygame.mixer.music.set_volume(int(v) / 100)

    ''' Time length setting '''
    def get_cursong_duration(self):
        '''Get duration seconds of current song.'''
        # print(self.cursong_duration)
        # return self.cursong_duration
        return int(self.cursong_duration)

    def set_cursong_duration(self, songinfo):
        '''Compute duration seconds of current song.'''
        # if songinfo["duration"] == '-:-:-':
        #     song_path = os.path.join(songinfo['savedir'], songinfo['savename'] + '.' + songinfo['ext'])
        #     self.cursong_duration = AudioSegment.from_file(song_path).duration_seconds
        # else:
        #     self.cursong_duration = datetime.datetime.strptime(songinfo["duration"], "%H:%M:%S")
        song_path = os.path.join(songinfo['savedir'], songinfo['savename'] + '.' + songinfo['ext'])
        self.cursong_duration = AudioSegment.from_file(song_path).duration_seconds

if __name__ == '__main__':
    song_info = [{'source': 'netease', 'songid': '1473430314', 'singers': 'GHOSTEMANE', 'album': 'AI', 'songname': 'AI',
                  'savedir': 'download/music', 'savename': 'netease_AI',
                  'download_url': 'http://m10.music.126.net/20211017115157/a7826f8ca5bb0cb69418dcceac51f850/ymusic/obj/w5zDlMODwrDDiGjCn8Ky/3738198513/395f/a0b8/ceb3/b34024e7f99e15ca300932ecb4186832.mp3',
                  'lyric': "[00:00.000] 作曲 : Eric Ghoste/Parv0\n[00:01.000] 制作人 : Eric Ghoste/Parv0\n[00:02.31]Produced by Ghostemane & Parv0\n[00:03.49]When you die, ain't nobody gonna remember you\n[00:06.10]When you die, ain't nobody gonna remember you\n[00:09.14]When you die, ain't nobody gonna remember you\n[00:12.21]When you die, ain't nobody gonna remember you\n[00:15.42]When you die, ain't nobody gonna remember you\n[00:17.58]Yeah\n[00:18.65]When you die, ain't nobody gonna remember you\n[00:21.69]When you die, ain't nobody gonna remember you\n[00:23.87]When you die, ain't nobody gonna remember you\n[00:26.71]If you don't know me by now, I don't want you to\n[00:29.43]None of your favorite rappers ever tell the truth\n[00:32.25]Lie, lie, lie, lie, lie, out of my mind\n[00:34.51]It's about damn time y'all startin' to die\n[00:37.09]Lay low, I'm the ghost at your window\n[00:40.59]Went away, now I'm way away\n[00:42.97]There he go, **** an icon, eyes on A.I.\n[00:46.78]Oh, I ****ed around and put a pipe bomb in your radio\n[00:49.85]A.I., A.I., A.I., A.I.\n[00:53.00]A.I., A.I., A.I. (A.I.)\n[00:55.91]A.I., A.I., A.I., A.I.\n[00:59.01]A.I., A.I., A.I., A.I.\n[01:01.95](Ooh) A.I., (Ooh) A.I., (Ooh) A.I., (Ooh) A.I.\n[01:04.79](Ooh) A.I., (Ooh) A.I., (Ooh) A.I., (Ooh) A.I.\n[01:07.88]I don't wanna be the one to bear the bad news\n[01:09.31]But a man who's claiming he's the man ain't a man at all\n[01:11.23]Overcompensating for the lack of ability\n[01:22.05]To really be an icon, not even a bygone\n[01:14.32]Modern-day unsustainable, painfully mundane\n[01:16.02]Forgettable, gets old in a minute\n[01:17.65]Get sold to a label then never (See them again)\n[01:20.44]I spend all my time listening to guys who committed suicide\n[01:24.51]It's about time, it's about time\n[01:27.18]And I only ever really cry\n[01:29.47]To wash away the blood\n[01:30.46]To wash away the blood\n[01:32.57]I only ever cry\n[01:33.38]To wash away the blood\n[01:35.19]To wash away the blood\n[01:36.47]To wash away the blood\n[01:38.01]And I only ever cry\n[01:39.98]To wash away the blood\n[01:41.14]To wash away the blood\n[01:42.71]To wash away the blood\n[01:44.16]To wash away\n[01:45.61]Don't give a damn about a critic, they don't really get it\n[01:47.15]They don't make a difference, they don't buy the tickets, ah\n[01:48.65]Only really give a damn about the kids\n[01:50.48]Live and die for the kids, live and die for the kids, ah\n[01:51.48]A.I., A.I., A.I., A.I.\n[01:54.58]A.I., A.I., A.I., A.I.\n[01:57.62](Ooh) A.I., (Ooh) A.I., (Ooh) A.I., (Ooh) A.I.\n[02:00.52](Ooh) A.I., (Ooh) A.I., (Ooh) A.I., (Ooh) A.I.\n[02:04.09]A.I., A.I., A.I., A.I.\n[02:06.98]A.I., A.I., A.I., A.I.\n[02:10.02](Ooh) A.I., (Ooh) A.I., (Ooh) A.I., (Ooh) A.I.\n[02:13.18](Ooh) A.I., (Ooh) A.I., (Ooh) A.I., (Ooh) A.I.\n[02:21.27]I only ever really\n[02:27.60]I only ever really\n[02:33.93]Cry to wash away all the blood\n",
                  'filesize': '6.66MB', 'ext': 'mp3', 'duration': '00:02:54'},
                 {'source': 'netease', 'songid': '255294', 'singers': '刘惜君', 'album': '爱情花园', 'songname': '我很快乐',
                  'savedir': 'download/music', 'savename': 'netease_我很快乐',
                  'download_url': 'http://m801.music.126.net/20211017115200/45f8afb5c33e9d975bdd2a3a945a644a/jdymusic/obj/wo3DlMOGwrbDjj7DisKw/10798500124/33e6/78ad/7d0b/fa08c625a28f13061e6ccf66d3b2b428.mp3',
                  'lyric': '[00:00.000] 作词 : 祈合/张海\n[00:01.000] 作曲 : 祈合\n[00:02.000] 编曲 : 张明\n[00:03.000] 制作人 : 秋言\n[03:29.20]吉他 Guitar : 张明\n[03:29.30]贝斯 Bass : 陈昕\n[03:29.35]和声 Backing Vocals : 常石磊\n[03:29.40]录音师 Recording Engineer : 祈合\n[03:29.55]录音室 Recording Studio : 深圳傲旗录音棚\n[03:29.60]混音师 Mixing Engineer : 阿海\n[03:29.70]混音室 Mixing Studio : 深圳傲旗录音棚\n[03:29.85]OP : SHENZHEN AOQI ARTS CULTURE CO,LTD.\n[00:16.117]说 有什么 不能说 怕什么\n[00:21.389]相信我 不会哭 我不会难过\n[00:22.999]错 谁的错 谁能说得清楚\n[00:28.118]还不如算我的错\n[00:31.988]做 有什么 不敢做\n[00:34.558]怕什么 相信我 不在乎\n[00:38.280]就算你走了\n[00:40.118]落 就算我 的心从十六楼\n[00:44.580]落下负一层 B座\n[00:46.988]我也不会难过 你不要小看我\n[00:50.988]有什么熬不过 大不了唱首歌\n[00:54.798]虽然是悲伤的歌 声音有点颤抖\n[00:58.798]也比你好得多 我还是很快乐\n[01:03.228]我再不会难过 你别太小看我\n[01:07.229]有什么熬不过 谁说我不能喝\n[01:11.229]我喝得比谁都多 走路有点颠簸\n[01:15.288]也比你强得多 我还是很快乐\n[01:22.499]\n[01:25.379]做 有什么 不忍心\n[01:27.748]怕什么 相信我 不在乎\n[01:30.748]就算你走了\n[01:33.188]落 就算我 的心从十六楼\n[01:37.679]落下负一层 B座\n[01:40.189]我也不会难过 你不要小看我\n[01:44.129]有什么熬不过 大不了唱首歌\n[01:48.490]虽然是悲伤的歌 声音有点颤抖\n[01:51.218]也比你好得多 我还是很快乐\n[01:55.528]我才不会难过 你别太小看我\n[02:00.428]有什么熬不过 谁说我不能喝\n[02:03.829]我喝得比谁都多 走路有点颠簸\n[02:09.480]也比你强得多 我还是很快乐\n[02:15.570]\n[02:29.207]我也不会难过 你不要小看我\n[02:33.317]有什么熬不过 大不了唱首歌\n[02:37.317]虽然是悲伤的歌 声音有点颤抖\n[02:41.567]也比你好得多 我还是很快乐\n[02:45.197]我才不会难过 你别太小看我\n[02:49.317]有什么熬不过 烧掉你写的信\n[02:53.317]忘掉你喜欢的歌 绑住我的眼睛\n[02:57.317]眼泪掉不下来 我还是很快乐\n',
                  'filesize': '8.14MB', 'ext': 'mp3', 'duration': '00:03:33'}]

    mplayer = Musicplayer()
    # mplayer.set_config(song_info)
    # mplayer.play()
    songs_item = mplayer.musicdl_search("ai")
    # print(songs_item)

    mplayer.add_songs_to_playlist(['0', '1'])

    mplayer.play()

    # time.sleep(8)
    # mplayer.pause()
    #
    # time.sleep(8)
    # mplayer.unpause()

    # time.sleep(8)
    # mplayer.stop()

    while True:
        time.sleep(1)
