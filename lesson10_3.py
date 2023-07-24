#每個文件都有一個內建的變數叫做__name__
#print(__name__) #執行後會先執行進入點並跑出字串__main__，而c語言的進入點叫function main

def main():
    print("main function執行!")

if __name__ == '__main__':
    main()