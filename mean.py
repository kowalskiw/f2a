from os import chdir
from subprocess import Popen, PIPE
from sys import argv
from pandas import read_csv as rcsv
import pandas


class F2A:
    def __init__(self, time, orientation):
        self.time = time
        self.orientation = orientation
        chdir(argv[1])

    def readX(self, bounds, mesh):
        chid = argv[2]

        proc = Popen('cmd.exe', stdin=PIPE)
        for t in range(self.time[0], self.time[1], 10):
            for o in self.orientation:
                sas = 'f2a_{}_{}.csv'.format(t, o)
                c = ['fds2ascii', chid, '3', '1', 'y', bounds, '{} {}'.format(t, t + 10), o, '1', mesh, sas]
                [proc.stdin.write(bytes('{}\n'.format(com), encoding='utf8')) for com in c]
                print(sas)

    def split_csv(self, file):
        data = {}
        with open('temp.csv', 'w') as temp:
            temp.write(file)
        with open('temp.csv', 'r') as temp:
            f = temp.readlines()
        patch_no = f[0].split(' ')[0]
        with open('temp.csv', 'w') as temp:
            temp.writelines(f[1:])

        file = rcsv('temp.csv')
        file.drop(0, inplace=True)
        print(file.columns)

        # split according to Z

        file.drop([' X', 'Z'], axis='columns', inplace=True)

        # save in data dictionary as title:array(pandas df)
        # title = 'Patch{} X={} Z={}'.format(patch_no, x, z)
        # data{title:array}

        return data

    def mean(self):
        data_list = []

        for t in range(self.time[0], self.time[1], 10):
            for o in self.orientation:
                # split csv files for specified bounds
                with open('f2a_{}_{}.csv'.format(t, o))as temp:
                    files = temp.read().split('Patch ')
                [self.split_csv(f) for f in files[1:]]
                # merge splitted csv files using Y as key

                data_list.append(rcsv('f2a_{}_{}.csv'.format(t, o), sep=','))
                break
            break
        # count mean value of each cross section (Y)

        # add to the time array

        # draw temp(time) chart for given cross-section
        # draw temp(Y) chart for given time

        # enjoy your data!


f2a = F2A([0, 320], [-1, 1])
f2a.mean()
# readX([0, 600], [-1, 1], '3 4 25 35 6 8', 8)
