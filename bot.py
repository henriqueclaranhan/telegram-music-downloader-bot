import os
import json
import telepot
import youtube_dl
from random import randint
from youtubesearchpython import SearchVideos


bot = telepot.Bot("API_TOKEN")

def recebendoMsg(msg):
	userInput = msg['text']
	chat_id = msg['chat']['id']

	if userInput.startswith('/start'):
		bot.sendMessage(chat_id, '🤖 Hello, '+ msg['from']['first_name'] +'!\n\n'
			'📩 Send me:\n\n'
			'"*/music* _song name_"  or\n'
			'"*/music* _musician name - song name_"\n\n'
			'to order some music. 🎶', parse_mode= 'Markdown')

	elif userInput.startswith('/music') and userInput[6:]!='':
		search = SearchVideos(userInput[6:], offset = 1, mode = "json", max_results = 1)
		resultados = json.loads(search.result())

		title = resultados['search_result'][0]['title']
		link = resultados['search_result'][0]['link']
		#video_id = resultados['search_result'][0]['id']

		file_name = title +' - '+str(randint(0,999999))+'.mp3'

		ydl_opts = {
			'outtmpl': './'+file_name,
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '256',
			}],
			'prefer_ffmpeg': True
		}

		bot.sendMessage(chat_id,'🎵 '+title+'\n'+'🔗 '+link)
		DownloadingMsg = bot.sendMessage(chat_id,'⬇️ Downloading... '
			'\n_(this may take a while.)_', parse_mode= 'Markdown')

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			info_dict = ydl.extract_info(link, download=True) 

		bot.sendAudio(chat_id,audio=open(file_name,'rb'))
		bot.deleteMessage((chat_id, DownloadingMsg['message_id']))
		bot.sendMessage(chat_id, '✅ Sucess!')
		print ("Sucess!")
		os.remove(file_name)

	else:
		bot.sendMessage(chat_id, '‼️ Oops! Invalid command!\n'
			'Try: "*/music* _song name_"\n'
			'or: "*/music* _musician name - song name_"', parse_mode= 'Markdown')
		
bot.message_loop(recebendoMsg)

while True:
	pass
