from flask import Flask

ss = [
    """                                                                                                                 
                                                                                                                 
  .--.--.    ,---,                                                .--.--.                          ,-.           
 /  /    '.,--.' |                    ,---,                      /  /    '.                    ,--/ /|           
|  :  /`. /|  |  :                  ,---.'|  ,---.          .---|  :  /`. /   ,---.          ,--. :/ |           
;  |  |--` :  :  :                  |   | : '   ,'\\        /. ./;  |  |--`   '   ,'\\         :  : ' / .--.--.    
|  :  ;_   :  |  |,--. ,--.--.      |   | |/   /   |    .-'-. ' |  :  ;_    /   /   |  ,---. |  '  / /  /    '   
 \\  \\    `.|  :  '   |/       \\   ,--.__| .   ; ,. :   /___/ \\: |\\  \\    `..   ; ,. : /     \\'  |  :|  :  /`./   
  `----.   |  |   /' .--.  .-. | /   ,'   '   | |: :.-'.. '   ' . `----.   '   | |: :/    / '|  |   |  :  ;_     
  __ \\  \\  '  :  | | |\\__\\/: . ..   '  /  '   | .; /___/ \\:     ' __ \\  \\  '   | .; .    ' / '  : |. \\  \\    `.  
 /  /`--'  |  |  ' | :," .--.; |'   ; |:  |   :    .   \\  ' .\\   /  /`--'  |   :    '   ; :__|  | ' \\ `----.   \\ 
'--'.     /|  :  :_:,/  /  ,.  ||   | '/  '\\   \\  / \\   \\   ' \\ '--'.     / \\   \\  /'   | '.''  : |--/  /`--'  / 
  `--'---' |  | ,'  ;  :   .'   |   :    :| `----'   \\   \\  |--"  `--'---'   `----' |   :    ;  |,' '--'.     /  
           `--''    |  ,     .-./\\   \\  /             \\   \\ |                        \\   \\  /'--'     `--'---'   
                     `--`---'     `----'               '---"                          `----'                     
                                                                                                                 """,
    """    o__ __o      o                               o                                       o__ __o                              o                 
   /v     v\\    <|>                             <|>                                     /v     v\\                            <|>                
  />       <\\   / >                             < \\                                    />       <\\                           / \\                
 _\\o____        \\o__ __o       o__ __o/    o__ __o/    o__ __o     o              o   _\\o____          o__ __o        __o__  \\o/  o/      __o__ 
      \\_\\__o__   |     v\\     /v     |    /v     |    /v     v\\   <|>            <|>       \\_\\__o__   /v     v\\      />  \\    |  /v      />  \\  
            \\   / \\     <\\   />     / \\  />     / \\  />       <\\  < >            < >             \\   />       <\\   o/        / \\/>       \\o     
  \\         /   \\o/     o/   \\      \\o/  \\      \\o/  \\         /   \\o    o/\\o    o/    \\         /   \\         /  <|         \\o/\\o        v\\    
   o       o     |     <|     o      |    o      |    o       o     v\\  /v  v\\  /v      o       o     o       o    \\\\         |  v\\        <\\   
   <\\__ __/>    / \\    / \\    <\\__  / \\   <\\__  / \\   <\\__ __/>      <\\/>    <\\/>       <\\__ __/>     <\\__ __/>     _\\o__</  / \\  <\\  _\\o__</   
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                """,
    """  /$$$$$$ /$$                     /$$                       /$$$$$$                   /$$               
 /$$__  $| $$                    | $$                      /$$__  $$                 | $$               
| $$  \\__| $$$$$$$  /$$$$$$  /$$$$$$$ /$$$$$$ /$$  /$$  /$| $$  \\__/ /$$$$$$  /$$$$$$| $$   /$$ /$$$$$$$
|  $$$$$$| $$__  $$|____  $$/$$__  $$/$$__  $| $$ | $$ | $|  $$$$$$ /$$__  $$/$$_____| $$  /$$//$$_____/
 \\____  $| $$  \\ $$ /$$$$$$| $$  | $| $$  \\ $| $$ | $$ | $$\\____  $| $$  \\ $| $$     | $$$$$$/|  $$$$$$ 
 /$$  \\ $| $$  | $$/$$__  $| $$  | $| $$  | $| $$ | $$ | $$/$$  \\ $| $$  | $| $$     | $$_  $$ \\____  $$
|  $$$$$$| $$  | $|  $$$$$$|  $$$$$$|  $$$$$$|  $$$$$/$$$$|  $$$$$$|  $$$$$$|  $$$$$$| $$ \\  $$/$$$$$$$/
 \\______/|__/  |__/\\_______/\\_______/\\______/ \\_____/\\___/ \\______/ \\______/ \\_______|__/  \\__|_______/ 
                                                                                                        
                                                                                                        
                                                                                                        """,
    """   _____ _               _                _____            _        
  / ____| |             | |              / ____|          | |       
 | (___ | |__   __ _  __| | _____      _| (___   ___   ___| | _____ 
  \\___ \\| '_ \\ / _` |/ _` |/ _ \\ \\ /\\ / /\\___ \\ / _ \\ / __| |/ / __|
  ____) | | | | (_| | (_| | (_) \\ V  V / ____) | (_) | (__|   <\\__ \\
 |_____/|_| |_|\\__,_|\\__,_|\\___/ \\_/\\_/ |_____/ \\___/ \\___|_|\\_|___/
                                                                    
                                                                    """,
    """  ________.__               .___             _________              __           
 /   _____|  |__ _____    __| _/______  _  _/   _____/ ____   ____ |  | __ ______
 \\_____  \\|  |  \\\\__  \\  / __ |/  _ \\ \\/ \\/ \\_____  \\ /  _ \\_/ ___\\|  |/ //  ___/
 /        |   Y  \\/ __ \\/ /_/ (  <_> \\     //        (  <_> \\  \\___|    < \\___ \\ 
/_______  |___|  (____  \\____ |\\____/ \\/\\_//_______  /\\____/ \\___  |__|_ /____  >
        \\/     \\/     \\/     \\/                    \\/            \\/     \\/    \\/ """,
    """        _           _       _   _               _           _           _            _           _            _            _           _        
       / /\\        / /\\    / /\\/ /\\            /\\ \\        /\\ \\        / /\\      _  / /\\        /\\ \\        /\\ \\          /\\_\\        / /\\      
      / /  \\      / / /   / / / /  \\          /  \\ \\____  /  \\ \\      / / /    / /\\/ /  \\      /  \\ \\      /  \\ \\        / / /  _    / /  \\     
     / / /\\ \\__  / /_/   / / / / /\\ \\        / /\\ \\_____\\/ /\\ \\ \\    / / /    / / / / /\\ \\__  / /\\ \\ \\    / /\\ \\ \\      / / /  /\\_\\ / / /\\ \\__  
    / / /\\ \\___\\/ /\\ \\__/ / / / /\\ \\ \\      / / /\\/___  / / /\\ \\ \\  / / /_   / / / / /\\ \\___\\/ / /\\ \\ \\  / / /\\ \\ \\    / / /__/ / // / /\\ \\___\\ 
    \\ \\ \\ \\/___/ /\\ \\___\\/ / / /  \\ \\ \\    / / /   / / / / /  \\ \\_\\/ /_//_/\\/ / /\\ \\ \\ \\/___/ / /  \\ \\_\\/ / /  \\ \\_\\  / /\\_____/ / \\ \\ \\ \\/___/ 
     \\ \\ \\    / / /\\/___/ / / /___/ /\\ \\  / / /   / / / / /   / / / _______/\\/ /  \\ \\ \\    / / /   / / / / /    \\/_/ / /\\_______/   \\ \\ \\       
 _    \\ \\ \\  / / /   / / / / /_____/ /\\ \\/ / /   / / / / /   / / / /  \\____\\  _    \\ \\ \\  / / /   / / / / /         / / /\\ \\ \\  _    \\ \\ \\      
/_/\\__/ / / / / /   / / / /_________/\\ \\ \\ \\ \\__/ / / / /___/ / /_/ /\\ \\ /\\ \\/_/\\__/ / / / / /___/ / / / /________ / / /  \\ \\ \\/_/\\__/ / /      
\\ \\/___/ / / / /   / / / / /_       __\\ \\_\\ \\___\\/ / / /____\\/ /\\_\\//_/ /_/ /\\ \\/___/ / / / /____\\/ / / /_________/ / /    \\ \\ \\ \\/___/ /       
 \\_____\\/  \\/_/    \\/_/\\_\\___\\     /____/_/\\/_____/\\/_________/     \\_\\/\\_\\/  \\_____\\/  \\/_________/\\/____________\\/_/      \\_\\_\\_____\\/        
                                                                                                                                                """,
    """      ___         ___         ___         ___         ___         ___         ___         ___         ___         ___         ___     
     /\\  \\       /\\__\\       /\\  \\       /\\  \\       /\\  \\       /\\__\\       /\\  \\       /\\  \\       /\\  \\       /\\__\\       /\\  \\    
    /::\\  \\     /:/  /      /::\\  \\     /::\\  \\     /::\\  \\     /:/ _/_     /::\\  \\     /::\\  \\     /::\\  \\     /:/  /      /::\\  \\   
   /:/\\ \\  \\   /:/__/      /:/\\:\\  \\   /:/\\:\\  \\   /:/\\:\\  \\   /:/ /\\__\\   /:/\\ \\  \\   /:/\\:\\  \\   /:/\\:\\  \\   /:/__/      /:/\\ \\  \\  
  _\\:\\~\\ \\  \\ /::\\  \\ ___ /::\\~\\:\\  \\ /:/  \\:\\__\\ /:/  \\:\\  \\ /:/ /:/ _/_ _\\:\\~\\ \\  \\ /:/  \\:\\  \\ /:/  \\:\\  \\ /::\\__\\____ _\\:\\~\\ \\  \\ 
 /\\ \\:\\ \\ \\__/:/\\:\\  /\\__/:/\\:\\ \\:\\__/:/__/ \\:|__/:/__/ \\:\\__/:/_/:/ /\\__/\\ \\:\\ \\ \\__/:/__/ \\:\\__/:/__/ \\:\\__/:/\\:::::\\__/\\ \\:\\ \\ \\__\\
 \\:\\ \\:\\ \\/__\\/__\\:\\/:/  \\/__\\:\\/:/  \\:\\  \\ /:/  \\:\\  \\ /:/  \\:\\/:/ /:/  \\:\\ \\:\\ \\/__\\:\\  \\ /:/  \\:\\  \\  \\/__\\/_|:|~~|~  \\:\\ \\:\\ \\/__/
  \\:\\ \\:\\__\\      \\::/  /     \\::/  / \\:\\  /:/  / \\:\\  /:/  / \\::/_/:/  / \\:\\ \\:\\__\\  \\:\\  /:/  / \\:\\  \\        |:|  |    \\:\\ \\:\\__\\  
   \\:\\/:/  /      /:/  /      /:/  /   \\:\\/:/  /   \\:\\/:/  /   \\:\\/:/  /   \\:\\/:/  /   \\:\\/:/  /   \\:\\  \\       |:|  |     \\:\\/:/  /  
    \\::/  /      /:/  /      /:/  /     \\::/__/     \\::/  /     \\::/  /     \\::/  /     \\::/  /     \\:\\__\\      |:|  |      \\::/  /   
     \\/__/       \\/__/       \\/__/       ~~          \\/__/       \\/__/       \\/__/       \\/__/       \\/__/       \\|__|       \\/__/    """,
    """  ________ __    __      __      ________     ______   __   __  ___  ________  ______   ______  __   ___  ________  
 /"       /" |  | "\\    /""\\    |"      "\\   /    " \\ |"  |/  \\|  "|/"       )/    " \\ /" _  "\\|/"| /  ")/"       ) 
(:   \\___(:  (__)  :)  /    \\   (.  ___  :) // ____  \\|'  /    \\:  (:   \\___/// ____  (: ( \\___(: |/   /(:   \\___/  
 \\___  \\  \\/      \\/  /' /\\  \\  |: \\   ) ||/  /    ) :|: /'        |\\___  \\ /  /    ) :\\/ \\    |    __/  \\___  \\    
  __/  \\\\ //  __  \\\\ //  __'  \\ (| (___\\ |(: (____/ // \\//  /\\'    | __/  \\(: (____/ ////  \\ _ (// _  \\   __/  \\\\   
 /" \\   :(:  (  )  :/   /  \\\\  \\|:       :)\\        /  /   /  \\\\   |/" \\   :\\        /(:   _) \\|: | \\  \\ /" \\   :)  
(_______/ \\__|  |__(___/    \\___(________/  \\"_____/  |___/    \\___(_______/ \\"_____/  \\_______(__|  \\__(_______/   
                                                                                                                    """,
    """ _______ __   __ _______ ______  _______ _     _ _______ _______ _______ ___   _ _______ 
|       |  | |  |   _   |      ||       | | _ | |       |       |       |   | | |       |
|  _____|  |_|  |  |_|  |  _    |   _   | || || |  _____|   _   |       |   |_| |  _____|
| |_____|       |       | | |   |  | |  |       | |_____|  | |  |       |      _| |_____ 
|_____  |       |       | |_|   |  |_|  |       |_____  |  |_|  |      _|     |_|_____  |
 _____| |   _   |   _   |       |       |   _   |_____| |       |     |_|    _  |_____| |
|_______|__| |__|__| |__|______||_______|__| |__|_______|_______|_______|___| |_|_______|""",
    """                                                   
 _____ _         _           _____         _       
|   __| |_ ___ _| |___ _ _ _|   __|___ ___| |_ ___ 
|__   |   | .'| . | . | | | |__   | . |  _| '_|_ -|
|_____|_|_|__,|___|___|_____|_____|___|___|_,_|___|
                                                   """,
    """                                                                             
 ,---. ,--.              ,--.                ,---.            ,--.           
'   .-'|  ,---. ,--,--.,-|  |,---.,--.   ,--'   .-' ,---. ,---|  |,-. ,---.  
`.  `-.|  .-.  ' ,-.  ' .-. | .-. |  |.'.|  `.  `-.| .-. | .--|     /(  .-'  
.-'    |  | |  \\ '-'  \\ `-' ' '-' |   .'.   .-'    ' '-' \\ `--|  \\  \\.-'  `) 
`-----'`--' `--'`--`--'`---' `---''--'   '--`-----' `---' `---`--'`--`----'  
                                                                             """,
    """ ______  __  __  ______  _____   ______  __     __  ______  ______  ______  __  __  ______    
/\\  ___\\/\\ \\_\\ \\/\\  __ \\/\\  __-./\\  __ \\/\\ \\  _ \\ \\/\\  ___\\/\\  __ \\/\\  ___\\/\\ \\/ / /\\  ___\\   
\\ \\___  \\ \\  __ \\ \\  __ \\ \\ \\/\\ \\ \\ \\/\\ \\ \\ \\/ ".\\ \\ \\___  \\ \\ \\/\\ \\ \\ \\___\\ \\  _"-\\ \\___  \\  
 \\/\\_____\\ \\_\\ \\_\\ \\_\\ \\_\\ \\____-\\ \\_____\\ \\__/".~\\_\\/\\_____\\ \\_____\\ \\_____\\ \\_\\ \\_\\/\\_____\\ 
  \\/_____/\\/_/\\/_/\\/_/\\/_/\\/____/ \\/_____/\\/_/   \\/_/\\/_____/\\/_____/\\/_____/\\/_/\\/_/\\/_____/ 
                                                                                              """,
    """█████████╗  ██╗█████╗██████╗ ██████╗██╗    █████████╗██████╗ ████████╗  █████████╗
██╔════██║  ████╔══████╔══████╔═══████║    ████╔════██╔═══████╔════██║ ██╔██╔════╝
███████████████████████║  ████║   ████║ █╗ ███████████║   ████║    █████╔╝███████╗
╚════████╔══████╔══████║  ████║   ████║███╗██╚════████║   ████║    ██╔═██╗╚════██║
█████████║  ████║  ████████╔╚██████╔╚███╔███╔███████╚██████╔╚████████║  █████████║
╚══════╚═╝  ╚═╚═╝  ╚═╚═════╝ ╚═════╝ ╚══╝╚══╝╚══════╝╚═════╝ ╚═════╚═╝  ╚═╚══════╝
                                                                                  """,
    """  ██████ ██░ ██ ▄▄▄     ▓█████▄ ▒█████  █     █░ ██████ ▒█████  ▄████▄  ██ ▄█▀ ██████ 
▒██    ▒▓██░ ██▒████▄   ▒██▀ ██▒██▒  ██▓█░ █ ░█▒██    ▒▒██▒  ██▒██▀ ▀█  ██▄█▒▒██    ▒ 
░ ▓██▄  ▒██▀▀██▒██  ▀█▄ ░██   █▒██░  ██▒█░ █ ░█░ ▓██▄  ▒██░  ██▒▓█    ▄▓███▄░░ ▓██▄   
  ▒   ██░▓█ ░██░██▄▄▄▄██░▓█▄   ▒██   ██░█░ █ ░█  ▒   ██▒██   ██▒▓▓▄ ▄██▓██ █▄  ▒   ██▒
▒██████▒░▓█▒░██▓▓█   ▓██░▒████▓░ ████▓▒░░██▒██▓▒██████▒░ ████▓▒▒ ▓███▀ ▒██▒ █▒██████▒▒
▒ ▒▓▒ ▒ ░▒ ░░▒░▒▒▒   ▓▒█░▒▒▓  ▒░ ▒░▒░▒░░ ▓░▒ ▒ ▒ ▒▓▒ ▒ ░ ▒░▒░▒░░ ░▒ ▒  ▒ ▒▒ ▓▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░▒ ░▒░ ░ ▒   ▒▒ ░░ ▒  ▒  ░ ▒ ▒░  ▒ ░ ░ ░ ░▒  ░ ░ ░ ▒ ▒░  ░  ▒  ░ ░▒ ▒░ ░▒  ░ ░
░  ░  ░  ░  ░░ ░ ░   ▒   ░ ░  ░░ ░ ░ ▒   ░   ░ ░  ░  ░ ░ ░ ░ ▒ ░       ░ ░░ ░░  ░  ░  
      ░  ░  ░  ░     ░  ░  ░       ░ ░     ░         ░     ░ ░ ░ ░     ░  ░        ░  
                         ░                                     ░                      """,
    """╔═╗┬ ┬┌─┐┌┬┐┌─┐┬ ┬╔═╗┌─┐┌─┐┬┌─┌─┐
╚═╗├─┤├─┤ │││ ││││╚═╗│ ││  ├┴┐└─┐
╚═╝┴ ┴┴ ┴─┴┘└─┘└┴┘╚═╝└─┘└─┘┴ ┴└─┘""",
    """   ▄████████    ▄█    █▄       ▄████████ ████████▄   ▄██████▄   ▄█     █▄     ▄████████  ▄██████▄   ▄████████    ▄█   ▄█▄    ▄████████ 
  ███    ███   ███    ███     ███    ███ ███   ▀███ ███    ███ ███     ███   ███    ███ ███    ███ ███    ███   ███ ▄███▀   ███    ███ 
  ███    █▀    ███    ███     ███    ███ ███    ███ ███    ███ ███     ███   ███    █▀  ███    ███ ███    █▀    ███▐██▀     ███    █▀  
  ███         ▄███▄▄▄▄███▄▄   ███    ███ ███    ███ ███    ███ ███     ███   ███        ███    ███ ███         ▄█████▀      ███        
▀███████████ ▀▀███▀▀▀▀███▀  ▀███████████ ███    ███ ███    ███ ███     ███ ▀███████████ ███    ███ ███        ▀▀█████▄    ▀███████████ 
         ███   ███    ███     ███    ███ ███    ███ ███    ███ ███     ███          ███ ███    ███ ███    █▄    ███▐██▄            ███ 
   ▄█    ███   ███    ███     ███    ███ ███   ▄███ ███    ███ ███ ▄█▄ ███    ▄█    ███ ███    ███ ███    ███   ███ ▀███▄    ▄█    ███ 
 ▄████████▀    ███    █▀      ███    █▀  ████████▀   ▀██████▀   ▀███▀███▀   ▄████████▀   ▀██████▀  ████████▀    ███   ▀█▀  ▄████████▀  
                                                                                                                ▀                      """,
    """ ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄    ▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░▌ ▐░▌ ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌▐░▌  ▐░▌          
▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌   ▄   ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌          ▐░▌░▌   ▐░█▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌          ▐░░▌    ▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌ ▐░▌░▌ ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░▌          ▐░▌░▌    ▀▀▀▀▀▀▀▀▀█░▌
          ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌▐░▌ ▐░▌▐░▌          ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌▐░▌            ▐░▌
 ▄▄▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌░▌   ▐░▐░▌ ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▌  ▄▄▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░░░░░░░░░░▌ ▐░░░░░░░░░░░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀▀  ▀▀       ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀    ▀  ▀▀▀▀▀▀▀▀▀▀▀ 
                                                                                                                                          """,
    """.▄▄ ·  ▄ .▄ ▄▄▄· ·▄▄▄▄       ▄▄▌ ▐ ▄▌.▄▄ ·        ▄▄· ▄ •▄ .▄▄ · 
▐█ ▀. ██▪▐█▐█ ▀█ ██▪ ██▪     ██· █▌▐█▐█ ▀. ▪     ▐█ ▌▪█▌▄▌▪▐█ ▀. 
▄▀▀▀█▄██▀▐█▄█▀▀█ ▐█· ▐█▌▄█▀▄ ██▪▐█▐▐▌▄▀▀▀█▄ ▄█▀▄ ██ ▄▄▐▀▀▄·▄▀▀▀█▄
▐█▄▪▐███▌▐▀▐█ ▪▐▌██. ██▐█▌.▐▌▐█▌██▐█▌▐█▄▪▐█▐█▌.▐▌▐███▌▐█.█▌▐█▄▪▐█
 ▀▀▀▀ ▀▀▀ · ▀  ▀ ▀▀▀▀▀• ▀█▄▀▪ ▀▀▀▀ ▀▪ ▀▀▀▀  ▀█▄▀▪·▀▀▀ ·▀  ▀ ▀▀▀▀ """,
    """ ▄▀▀▀▀▄  ▄▀▀▄ ▄▄   ▄▀▀█▄   ▄▀▀█▄▄   ▄▀▀▀▀▄   ▄▀▀▄    ▄▀▀▄  ▄▀▀▀▀▄  ▄▀▀▀▀▄   ▄▀▄▄▄▄   ▄▀▀▄ █  ▄▀▀▀▀▄ 
█ █   ▐ █  █   ▄▀ ▐ ▄▀ ▀▄ █ ▄▀   █ █      █ █   █    ▐  █ █ █   ▐ █      █ █ █    ▌ █  █ ▄▀ █ █   ▐ 
   ▀▄   ▐  █▄▄▄█    █▄▄▄█ ▐ █    █ █      █ ▐  █        █    ▀▄   █      █ ▐ █      ▐  █▀▄     ▀▄   
▀▄   █     █   █   ▄▀   █   █    █ ▀▄    ▄▀   █   ▄    █  ▀▄   █  ▀▄    ▄▀   █        █   █ ▀▄   █  
 █▀▀▀     ▄▀  ▄▀  █   ▄▀   ▄▀▄▄▄▄▀   ▀▀▀▀      ▀▄▀ ▀▄ ▄▀   █▀▀▀     ▀▀▀▀    ▄▀▄▄▄▄▀ ▄▀   █   █▀▀▀   
 ▐       █   █    ▐   ▐   █     ▐                    ▀     ▐               █     ▐  █    ▐   ▐      
         ▐   ▐            ▐                                                ▐        ▐               """,
    """   ▄▄▄▄▄    ▄  █ ██   ██▄   ████▄   ▄ ▄      ▄▄▄▄▄   ████▄ ▄█▄    █  █▀  ▄▄▄▄▄   
  █     ▀▄ █   █ █ █  █  █  █   █  █   █    █     ▀▄ █   █ █▀ ▀▄  █▄█   █     ▀▄ 
▄  ▀▀▀▀▄   ██▀▀█ █▄▄█ █   █ █   █ █ ▄   █ ▄  ▀▀▀▀▄   █   █ █   ▀  █▀▄ ▄  ▀▀▀▀▄   
 ▀▄▄▄▄▀    █   █ █  █ █  █  ▀████ █  █  █  ▀▄▄▄▄▀    ▀████ █▄  ▄▀ █  █ ▀▄▄▄▄▀    
              █     █ ███▀         █ █ █                   ▀███▀    █            
             ▀     █                ▀ ▀                            ▀             
                  ▀                                                              """,
    """ ::::::::  :::    :::     :::     :::::::::   ::::::::  :::       :::  ::::::::   ::::::::   ::::::::  :::    ::: ::::::::  
:+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:    :+: :+:       :+: :+:    :+: :+:    :+: :+:    :+: :+:   :+: :+:    :+: 
+:+        +:+    +:+  +:+   +:+  +:+    +:+ +:+    +:+ +:+       +:+ +:+        +:+    +:+ +:+        +:+  +:+  +:+        
+#++:++#++ +#++:++#++ +#++:++#++: +#+    +:+ +#+    +:+ +#+  +:+  +#+ +#++:++#++ +#+    +:+ +#+        +#++:++   +#++:++#++ 
       +#+ +#+    +#+ +#+     +#+ +#+    +#+ +#+    +#+ +#+ +#+#+ +#+        +#+ +#+    +#+ +#+        +#+  +#+         +#+ 
#+#    #+# #+#    #+# #+#     #+# #+#    #+# #+#    #+#  #+#+# #+#+#  #+#    #+# #+#    #+# #+#    #+# #+#   #+# #+#    #+# 
 ########  ###    ### ###     ### #########   ########    ###   ###    ########   ########   ########  ###    ### ########  """,
    """..######..##.....##....###....########...#######..##......##..######...#######...######..##....##..######.
.##....##.##.....##...##.##...##.....##.##.....##.##..##..##.##....##.##.....##.##....##.##...##..##....##
.##.......##.....##..##...##..##.....##.##.....##.##..##..##.##.......##.....##.##.......##..##...##......
..######..#########.##.....##.##.....##.##.....##.##..##..##..######..##.....##.##.......#####.....######.
.......##.##.....##.#########.##.....##.##.....##.##..##..##.......##.##.....##.##.......##..##.........##
.##....##.##.....##.##.....##.##.....##.##.....##.##..##..##.##....##.##.....##.##....##.##...##..##....##
..######..##.....##.##.....##.########...#######...###..###...######...#######...######..##....##..######.""",
    """   _____ _                  _                  _____               \\           
  (      /        ___    ___/   __.  ,  _  /  (        __.    ___  |   ,   ____
   `--.  |,---.  /   `  /   | .'   \\ |  |  |   `--.  .'   \\ .'   ` |  /   (    
      |  |'   ` |    | ,'   | |    | `  ^  '      |  |    | |      |-<    `--. 
 \\___.'  /    | `.__/| `___,'  `._.'  \\/ \\/  \\___.'   `._.'  `._.' /  \\_ \\___.'
                            `                                                  """,
    """                                                                                                                         
   _|_|_|  _|                        _|                                  _|_|_|                      _|                  
 _|        _|_|_|      _|_|_|    _|_|_|    _|_|    _|      _|      _|  _|          _|_|      _|_|_|  _|  _|      _|_|_|  
   _|_|    _|    _|  _|    _|  _|    _|  _|    _|  _|      _|      _|    _|_|    _|    _|  _|        _|_|      _|_|      
       _|  _|    _|  _|    _|  _|    _|  _|    _|    _|  _|  _|  _|          _|  _|    _|  _|        _|  _|        _|_|  
 _|_|_|    _|    _|    _|_|_|    _|_|_|    _|_|        _|      _|      _|_|_|      _|_|      _|_|_|  _|    _|  _|_|_|    
                                                                                                                         
                                                                                                                         """,
    """,d88~~\\ 888                      888                         ,d88~~\\                  888   _          
8888    888-~88e   /~~~8e   e88~\\888  e88~-_  Y88b    e    / 8888     e88~-_   e88~~\\ 888 e~ ~   d88~\\ 
`Y88b   888  888       88b d888  888 d888   i  Y88b  d8b  /  `Y88b   d888   i d888    888d8b    C888   
 `Y88b, 888  888  e88~-888 8888  888 8888   |   Y888/Y88b/    `Y88b, 8888   | 8888    888Y88b    Y88b  
   8888 888  888 C888  888 Y888  888 Y888   '    Y8/  Y8/       8888 Y888   ' Y888    888 Y88b    888D 
\\__88P' 888  888  "88_-888  "88_/888  "88_-~      Y    Y     \\__88P'  "88_-~   "88__/ 888  Y88b \\_88P  
                                                                                                       """,
    """  _// //                     _//                    _// //               _//           
_//    _/_//                 _//                  _//    _//             _//           
 _//     _//       _//       _//  _//  _//     _///_//       _//      _//_//  _//_//// 
   _//   _/ _/   _//  _//_// _//_//  _//_//  /  _//  _//   _//  _// _//  _// _//_//    
      _//_//  _/_//   _/_/   _/_//    _/_// _/  _//     _/_//    _/_//   _/_//    _/// 
_//    _/_/   _/_//   _/_/   _//_//  _//_/ _/ _/_/_//    _/_//  _// _//  _// _//    _//
  _// // _//  _// _// _//_// _//  _//  _///    _/// _// //   _//      _//_//  _/_// _//
                                                                                       """,
    """ .d8888b.  888                    888                         .d8888b.                    888               
d88P  Y88b 888                    888                        d88P  Y88b                   888               
Y88b.      888                    888                        Y88b.                        888               
 "Y888b.   88888b.   8888b.   .d88888  .d88b.  888  888  888  "Y888b.    .d88b.   .d8888b 888  888 .d8888b  
    "Y88b. 888 "88b     "88b d88" 888 d88""88b 888  888  888     "Y88b. d88""88b d88P"    888 .88P 88K      
      "888 888  888 .d888888 888  888 888  888 888  888  888       "888 888  888 888      888888K  "Y8888b. 
Y88b  d88P 888  888 888  888 Y88b 888 Y88..88P Y88b 888 d88P Y88b  d88P Y88..88P Y88b.    888 "88b      X88 
 "Y8888P"  888  888 "Y888888  "Y88888  "Y88P"   "Y8888888P"   "Y8888P"   "Y88P"   "Y8888P 888  888  88888P' 
                                                                                                            
                                                                                                            
                                                                                                            """,
    '''8""""8                                  8""""8                         
8      e   e eeeee eeeee eeeee e   e  e 8      eeeee eeee e   e  eeeee 
8eeeee 8   8 8   8 8   8 8  88 8   8  8 8eeeee 8  88 8  8 8   8  8   " 
    88 8eee8 8eee8 8e  8 8   8 8e  8  8     88 8   8 8e   8eee8e 8eeee 
e   88 88  8 88  8 88  8 8   8 88  8  8 e   88 8   8 88   88   8    88 
8eee88 88  8 88  8 88ee8 8eee8 88ee8ee8 8eee88 8eee8 88e8 88   8 8ee88 
                                                                       ''',
    """  /\\\\ \\\\                     /\\\\                    /\\\\ \\\\               /\\\\           
/\\\\    /\\/\\\\                 /\\\\                  /\\\\    /\\\\             /\\\\           
 /\\\\     /\\\\       /\\\\       /\\\\  /\\\\  /\\\\     /\\\\\\/\\\\       /\\\\      /\\\\/\\\\  /\\\\/\\\\\\\\ 
   /\\\\   /\\ /\\   /\\\\  /\\\\/\\\\ /\\\\/\\\\  /\\\\/\\\\  \\  /\\\\  /\\\\   /\\\\  /\\\\ /\\\\  /\\\\ /\\\\/\\\\    
      /\\\\/\\\\  /\\/\\\\   /\\/\\   /\\/\\\\    /\\/\\\\ /\\  /\\\\     /\\/\\\\    /\\/\\\\   /\\/\\\\    /\\\\\\ 
/\\\\    /\\/\\   /\\/\\\\   /\\/\\   /\\\\/\\\\  /\\\\/\\ /\\ /\\/\\/\\\\    /\\/\\\\  /\\\\ /\\\\  /\\\\ /\\\\    /\\\\
  /\\\\ \\\\ /\\\\  /\\\\ /\\\\ /\\\\/\\\\ /\\\\  /\\\\  /\\\\\\    /\\\\\\ /\\\\ \\\\   /\\\\      /\\\\/\\\\  /\\/\\\\ /\\\\
                                                                                       """,
    """         .-.               .                   .-.                   
   .--.-'   /             /              .--.-'             /        
  (  (_)   /-.  .-.  .-../ .-._.`)    ( (  (_).-._..-.     /-.   .   
   `-.    /   |(  | (   / (   ) /  .   ) `-. (   )(       /   ) / \\  
 _    )_.'    | `-'-'`-'-..`-' (_.' `-'_    ) `-'  `---'_/    \\/ ._) 
(_.--'                                (_.--'                  /      """,
    """.|'''| '||               ||`                .|'''|            '||          
||      ||               ||                 ||                 ||          
`|'''|, ||''|, '''|. .|''|| .|''|,'\\\\    //``|'''|,.|''|,.|'', || //`('''' 
 .   || ||  ||.|''|| ||  || ||  ||  \\\\/\\//   .   ||||  ||||    ||<<   `'') 
 |...|'.||  ||`|..||.`|..||.`|..|'   \\/\\/    |...|'`|..|'`|..'.|| \\\\.`...' 
                                                                           
                                                                           """,
    """                                                                                                                   
 @@@@@@   @@@  @@@   @@@@@@   @@@@@@@    @@@@@@   @@@  @@@  @@@   @@@@@@    @@@@@@    @@@@@@@  @@@  @@@   @@@@@@   
@@@@@@@   @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@  @@@@@@@   @@@@@@@@  @@@@@@@@  @@@  @@@  @@@@@@@   
!@@       @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@!  @@!  !@@       @@!  @@@  !@@       @@!  !@@  !@@       
!@!       !@!  @!@  !@!  @!@  !@!  @!@  !@!  @!@  !@!  !@!  !@!  !@!       !@!  @!@  !@!       !@!  @!!  !@!       
!!@@!!    @!@!@!@!  @!@!@!@!  @!@  !@!  @!@  !@!  @!!  !!@  @!@  !!@@!!    @!@  !@!  !@!       @!@@!@!   !!@@!!    
 !!@!!!   !!!@!!!!  !!!@!!!!  !@!  !!!  !@!  !!!  !@!  !!!  !@!   !!@!!!   !@!  !!!  !!!       !!@!!!     !!@!!!   
     !:!  !!:  !!!  !!:  !!!  !!:  !!!  !!:  !!!  !!:  !!:  !!:       !:!  !!:  !!!  :!!       !!: :!!        !:!  
    !:!   :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  :!:  :!:  :!:      !:!   :!:  !:!  :!:       :!:  !:!      !:!   
:::: ::   ::   :::  ::   :::   :::: ::  ::::: ::   :::: :: :::   :::: ::   ::::: ::   ::: :::   ::  :::  :::: ::   
:: : :     :   : :   :   : :  :: :  :    : :  :     :: :  : :    :: : :     : :  :    :: :: :   :   :::  :: : :    
                                                                                                                   """,
    """.---. .         .           .---.                 
\\___  |-. ,-. ,-| ,-. . , , \\___  ,-. ,-. . , ,-. 
    \\ | | ,-| | | | | |/|/      \\ | | |   |/  `-. 
`---' ' ' `-^ `-' `-' ' '   `---' `-' `-' |\\  `-' 
                                          ' `     
                                                  """,
    """___/\\/\\/\\/\\/\\__/\\/\\__________________________/\\/\\________________________________/\\/\\/\\/\\/\\__________________________/\\/\\___________________
_/\\/\\__________/\\/\\________/\\/\\/\\____________/\\/\\____/\\/\\/\\____/\\/\\______/\\/\\__/\\/\\____________/\\/\\/\\______/\\/\\/\\/\\__/\\/\\__/\\/\\____/\\/\\/\\/\\_
___/\\/\\/\\/\\____/\\/\\/\\/\\________/\\/\\______/\\/\\/\\/\\__/\\/\\__/\\/\\__/\\/\\__/\\__/\\/\\____/\\/\\/\\/\\____/\\/\\__/\\/\\__/\\/\\________/\\/\\/\\/\\____/\\/\\/\\/\\___
_________/\\/\\__/\\/\\__/\\/\\__/\\/\\/\\/\\____/\\/\\__/\\/\\__/\\/\\__/\\/\\__/\\/\\/\\/\\/\\/\\/\\__________/\\/\\__/\\/\\__/\\/\\__/\\/\\________/\\/\\/\\/\\__________/\\/\\_
_/\\/\\/\\/\\/\\____/\\/\\__/\\/\\__/\\/\\/\\/\\/\\____/\\/\\/\\/\\____/\\/\\/\\______/\\/\\__/\\/\\____/\\/\\/\\/\\/\\______/\\/\\/\\______/\\/\\/\\/\\__/\\/\\__/\\/\\__/\\/\\/\\/\\___
____________________________________________________________________________________________________________________________________________""",
    """  [.. ..                        [..                       [.. ..                  [..            
[..    [..[..                   [..                     [..    [..                [..            
 [..      [..        [..        [..   [..   [..     [... [..        [..       [...[..  [.. [.... 
   [..    [. [.    [..  [.. [.. [.. [..  [.. [..  .  [..   [..    [..  [..  [..   [.. [.. [..    
      [.. [..  [..[..   [..[.   [..[..    [..[.. [.  [..      [..[..    [..[..    [.[..     [... 
[..    [..[.   [..[..   [..[.   [.. [..  [.. [. [. [.[..[..    [..[..  [..  [..   [.. [..     [..
  [.. ..  [..  [..  [.. [...[.. [..   [..   [...    [...  [.. ..    [..       [...[..  [..[.. [..
                                                                                                 """,
    """ o-o  o           o               o-o           o        
|     |           |              |              | /      
 o-o  O--o  oo  o-O o-o o   o   o o-o  o-o  o-o OO   o-o 
    | |  | | | |  | | |  \\ / \\ /     | | | |    | \\   \\  
o--o  o  o o-o- o-o o-o   o   o  o--o  o-o  o-o o  o o-o 
                                                         
                                                         """,
    """  O~~ ~~                         O~~                        O~~ ~~                   O~~            
O~~    O~~O~~                    O~~                      O~~    O~~                 O~~            
 O~~      O~~        O~~         O~~   O~~    O~~      O~~ O~~         O~~       O~~~O~~  O~~ O~~~~ 
   O~~    O~ O~    O~~  O~~  O~~ O~~ O~~  O~~  O~~  ~  O~~   O~~     O~~  O~~  O~~   O~~ O~~ O~~    
      O~~ O~~  O~~O~~   O~~ O~   O~~O~~    O~~ O~~ O~  O~~      O~~ O~~    O~~O~~    O~O~~     O~~~ 
O~~    O~~O~   O~~O~~   O~~ O~   O~~ O~~  O~~  O~ O~ O~O~~O~~    O~~ O~~  O~~  O~~   O~~ O~~     O~~
  O~~ ~~  O~~  O~~  O~~ O~~~ O~~ O~~   O~~    O~~~     O~~  O~~ ~~     O~~       O~~~O~~  O~~O~~ O~~
                                                                                                    """,
]


app = Flask(__name__)
app.config.from_object("config")

from app import views, models