# testeQA



this project synchronizes two folders: source and replica.

the synchronization is periodically and set by the user or not it has 30sec default synctime.
all arguments goes to command line. ex:

python3 [--synctime SYNCTIME] [--logfilepath LOGFILEPATH] pathoriginal pathreplica

all content modification is logged on sync.log