import pandas as pd

onset = range(0,50000,5000)

raw_data = {'stimulus': ['calculvideo', 'calculaudio', 'clicDaudio', 'clicGaudio', 'clicDvideo', 'clicGvideo', 'CboardH', 'CboardV', 'phraseVideo', 'phraseAudio'], 
        'type': ['video', 'audio', 'audio', 'audio', 'video', 'video', 'video', 'video', 'video', 'audio'], 
        'onset': onset, 
        'filename-wl': ['calculez seize moins huit', 'calc40.wav', 'clic3D.wav', 'clic3G.wav', 'appuyez trois sur le bouton droit', 'appuyer 3 fois sur le bouton gauche', 'calc40.wav', 'calc40.wav','l''orage a effraye les animaux du zoo', 'ph5.wav']}
df = pd.DataFrame(raw_data, columns = ['stimulus', 'type', 'onset', 'filename-wl'])

df.to_csv('file.csv')

