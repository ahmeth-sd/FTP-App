from ftplib import FTP

host = "ftp.danzonn.com"
username = "ahmet@danzonn.com"
password ="MzjS7NK9dTUggPn4jVF9"

#for local connection
#host = "127.0.0.1"
#username = "ahmet"
#password ="asd"



with FTP(host) as ftp:
    ftp.login(user=username, passwd=password)
    print(ftp.getwelcome())

    #Download a file
    #with open("mytest.txt", "wb") as f:
     #  ftp.retrbinary("RETR " + "test.txt", f.write, 1024)

    # Upload a file
    #with open("test.txt", "rb") as f:
     #   ftp.storbinary("STOR " + "upload.txt", f, 1024)

    # downlad another files from directory
    ftp.cwd("mydir") # change directory
    with open("specialfile.txt", "wb") as f:
        ftp.retrbinary("RETR " + "anotherone.txt", f.write, 1024)






    ftp.quit()