from tkinter import *
from tkinter import ttk
from pytube import YouTube
import tkinter
from pytube import Search
import vlc
import os
global count 
count = 1


# Initialize VLC instance
instance = vlc.Instance()
# Create a media player
player = instance.media_player_new()
root = tkinter.Tk()
root.title("NAPSTER2.0")
root.geometry('455x700')
root.resizable(False,False)
#place icon image here
#place main backgound image here
def downloadcanvas():
    download_canvas = tkinter.Canvas(root,width=455,height=700,bg='black')

    #place downloads background image here
    download_heading = download_canvas.create_text(210,60,text='DOWNLOAD',font=('Times',40),fill='white')
    download_text = download_canvas.create_text(85,190,text='SEARCH',fill='white', font=('Times',20))
    url = tkinter.Entry(download_canvas,bg='white',fg='black')
    download_canvas.create_window(186,206,anchor='sw',window=url)
    enter = tkinter.Button(download_canvas,fg='black',text='enter',command= lambda:download_song(url.get()))
    download_canvas.create_window(200,300,anchor='sw',window=enter)

    download_canvas.place(x=10,y=30)
def final_download(f_s,d):
    print(f_s,'\n', d)
    print(d[list(d.keys())[f_s]])

    link = r'https://www.youtube.com/watch?v=' + d[list(d.keys())[f_s]]
    yt = YouTube(link)
    print("Title:", yt.title)
    print("views", yt.views)
    yd = yt.streams.get_highest_resolution()

    audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
    download_path = r'Songs'
    audio_stream.download(output_path=download_path)
    print("Audio download complete.")

def download_song(song_keyword):
    s = Search(song_keyword)
    d={}
    for result in s.results:
        d[result.title] = result.video_id
    s_l = tkinter.Toplevel(root)
    s_l.geometry('300x500')
    s_l.title('Search Result')
    listbox1 = tkinter.Listbox(s_l)
    listbox1.pack()
    for i in d.keys():
        listbox1.insert(END,i)
    def selected_item():
        for i in listbox1.curselection():
            print(listbox1.get(i))
            final_download(i,d)
    select1 = tkinter.Button(s_l,text='Select',command= lambda:selected_item())
    select1.pack()

song_list = os.listdir('Songs')
current_song_index = 0

progress = tkinter.DoubleVar()
progress.set(0)  # Initialize progress to 0

def play_current_song():
    progress.set(0)
    if current_song_index < len(song_list):
        song = song_list[current_song_index]
        song_path = os.path.join('Songs', song)

        # Load and play the current song
        media = instance.media_new(song_path)
        player.set_media(media)
        player.play()
def pause_play():
    global count  # Add this line to access the global count variable
    if count % 2 == 0:
        player.play()
        count += 1
    else:
        player.pause()
        count += 1

def next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(song_list)
    play_current_song()

def prev_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(song_list)
    play_current_song()
def playlistcanvas():
    def update_progress():
        current_time = player.get_time()
        total_time = player.get_length()
        if total_time > 0:
            progress_value = int((current_time / total_time) * 100)
            progress.set(progress_value)
        playlist_canvas.after(1000, update_progress)  # Update the progress every second

    playlist_canvas = tkinter.Canvas(root, width=455, height=700, bg='black')
    playlist_heading = playlist_canvas.create_text(210, 60, text='PLAYLIST', font=('Times', 40))

    def select_song(event):
        global current_song_index
        selected_index = song_listbox.curselection()
        if selected_index:
            current_song_index = int(selected_index[0])
            play_current_song()

    # Create a listbox to display the songs
    song_listbox = tkinter.Listbox(playlist_canvas, selectmode=tkinter.SINGLE)
    song_listbox.place(x=100, y=150, width=255, height=200)

    # Add the songs to the listbox
    for song in song_list:
        song_listbox.insert(tkinter.END, song)

    song_listbox.bind('<Double-Button-1>', select_song)  # Make the list box clickable

    #play_current_song()  # Start playing the first song in the playlist

    back = tkinter.Button(playlist_canvas, text='<', font=('Times', 20), fg='green', padx=20, command=prev_song)
    playlist_canvas.create_window(100, 456, anchor='sw', window=back)

    pause_button = tkinter.Button(playlist_canvas, text='||', font=('Times', 20), fg='green', padx=21, command=pause_play)
    playlist_canvas.create_window(175, 456, anchor='sw', window=pause_button)

    next = tkinter.Button(playlist_canvas, text='>', font=('Times', 20), fg='green', padx=20, command=next_song)
    playlist_canvas.create_window(250, 456, anchor='sw', window=next)

    # Create a user-controllable progress bar
    user_progress_bar = ttk.Progressbar(playlist_canvas, orient='horizontal', length=255, mode='determinate', variable=progress)
    user_progress_bar.place(x=100, y=350)

    # Start updating the progress
    update_progress()

    playlist_canvas.place(x=10, y=30)


downloadcanvasbutton = tkinter.Button(root,text= 'download',padx=300,command=lambda:downloadcanvas())
downloadcanvasbutton.place(x=0,y=0,width=165)
playlistcanvasbutton = tkinter.Button(root,text= 'playlist',padx=300,command=lambda:playlistcanvas())
playlistcanvasbutton.place(x=165,y=0,width=165)
quitbutton = tkinter.Button(root,text='Quit',padx=200,command = root.quit)
quitbutton.place(x=325,y=0,width=130)
root.mainloop()
