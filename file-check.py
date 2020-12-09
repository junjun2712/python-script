import os
def scan_file():

    flist = ['bcbm','xlwh']
    for f in flist:
      dirs = "D:\jenkins\workspace\QP-UAT-PROD-CI-JOB\ci-uat-cocos-client\H5Framework_cc\assets\games\{}".format(f)
      #print (dirs)
      if not os.path.exists(dirs):
         print ("no")
      else:
         print ("ok")
if __name__ == "__main__":
    scan_file()
