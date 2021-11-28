from utils import keepTheLatestOneFile, readDirectory

imgDirs = readDirectory('F:/GitWorkspace/spider/assets/images/scenic-spot')
for imgDir in imgDirs:
    keepTheLatestOneFile(
        'F:/GitWorkspace/spider/assets/images/scenic-spot/'+imgDir)
