from scanner import Scanner
import sys
def main():
    if len(sys.argv)==2:
        scan=Scanner()
        try:
            scan.scan(sys.argv[1])
            scan.saida()
        except FileNotFoundError as e:
            print(e)
    else:
        print('não foi passado arquivo de entrada')
if __name__=="__main__":
    main()