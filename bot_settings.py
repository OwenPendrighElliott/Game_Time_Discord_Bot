class BotSettings():
    def __init__(self):
        # Volume for sounds when the bot greets members of channels 
        self.volume = 0.75

        # maps channel names to sounds
        # customise according to your discord
        # Bot lives in 2 discords so some double ups because I'm lazy
        self.chnl_snd_dict = {'General' : ['universal.mp3'],
                        'game-time' : ['hello_gamer.mp3', 'frickin_gaming.mp3', 'gaming_setup.mp3'], 
                        'kript-skiddies' : ['HACKERMAN.mp3'], 
                        'speed-run' : ['sonic.mp3']*99+['sanic.mp3'], 
                        'the-gulag' : ['inthegulag.mp3'],
                        '🎮 game-time 🎮' : ['hello_gamer.mp3', 'frickin_gaming.mp3', 'gaming_setup.mp3'], 
                        '💻 kript-skiddies 💻' : ['HACKERMAN.mp3'], 
                        '⏩ speed-run ⏩' : ['sonic.mp3']*99+['sanic.mp3'], 
                        '⛓ the-gulag ⛓' : ['inthegulag.mp3']}

        # List of channels that the bot won't follow people into, bot will still join these if someone has not moved from another channel
        self.stalk_exclude = ['General']