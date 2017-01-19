import subprocess
from hdfs.client import Client

class SearchItems(object):

    def __init__(self, file, item = None, layer = 0, num = 50):
        self.item = item
        self.file = file
        self.layer = layer
        self.num = num
        self.cmd_hdfs_cat = "sudo -u spark hdfs dfs -cat "

    def Visualiztion_Category(self, category):
        if category == 0 and self.item is not None:
            cmd_header = "sudo -u spark spark-submit --master local[12] --class com.Main "
            return cmd_header + "/home/spark/JAR/SearchItems.jar " + self.item + " " + self.file + " " + self.layer
        elif category == 1:
            return self.cmd_hdfs_cat + self.file
        else:
            return self.cmd_hdfs_cat + self.file

    def SearchFromAlgorithm(self, category):
        items = []

        cmd = self.Visualiztion_Category(category)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=None)
        while True:
            line = proc.stdout.readline()
            # print line
            if len(items) > self.num:
                break
            if line == "":
                break
            items.append(line.strip())
        return items

    def SearchFromHDFS(self):
        items = []
        client = Client("http://hadoop2:50070")
        with client.read(self.file) as fs:
            for line in fs.readlines():
                items.append(line.strip())

        return items

#
# cmd_header = "spark-submit --master local[4] --class com.Main /home/spark/JAR/SearchItems.jar"
# proc = subprocess.Popen(cmd_header, shell=True, stdout=subprocess.PIPE, stderr=None)
# num = 0
# while True:
#     line = proc.stdout.readline()
#     print "line:%s $"%line
#     if line == "":
#         break