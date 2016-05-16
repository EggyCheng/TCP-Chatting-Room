# TCP-Chatting-room
A TCP simple program.


          ▄▄▄██▀▀▀▀███▄     
        ▄▀▀           ▀█    
     ▄▄▀               ▀█   
    █     ▀▄  ▄▀        █   
    ▐██▄  ▀▄▀▀▄▀  ▄██▀ ▐▌   
    █▀█ ▀   ▀▀   ▀ █▀  ▐▌   
    █  ▀▐        ▌▀     █   
    █                   █   
     █  ▀▄    ▄▀        █   
     █           ▄▄    █    
      █▀██▀▀▀▀██▀      █    
      █  ▀████▀       █     
       █            ▄█      
        ██     █▄▄▀▀ █      
         ▀▀█▀▀▀▀      █     
          █            █ 
          
在執行程式前必須先背景執行cachealldata.py檔 (python3 cachealldata.py &)

先把user資料set進memcache裡

必須先啟動server.py再啟動client.py

server沒有任何指令可以下

client的指令有:

friendlist [to show all your friend and online/offline]

friendadd [to add a friend]

frienddel [to delete a friend]

send : [to send other user a message]

talk [to entry a talk mode with other user (exittalk to stop talking)]

filesend : [to send file to other user]

*chpasswd <password> [to change passwordd]

*log.txt is the login log file

*talk_history.txt is the talk history file

exit [to logout]

*目前talk指令只支援同一時間兩個user talk

os:寫法很爛寫一寫覺得用";"分隔要丟的參數是個很爛的方法,後來filesend改用json格式程式好寫多了

因為用memcache的關係找不到把所有key dump出來的方法,所以寫法也很爛只能讓aaaa,cccc user登入ㄏㄏ
