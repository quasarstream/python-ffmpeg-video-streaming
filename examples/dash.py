import streaming
from streaming import Representation

rep = Representation(width=640, height=360, bitrate=190)
rep2 = Representation(width=625, height=853, bitrate=200)
rep3 = Representation(width=152, height=365, bitrate=630)
reps = (
    streaming
        .dash('c:\\test\\test.mp4')
        .adaption('id=0,streams=v id=1,streams=a')
        .add_rep(rep, rep2, rep3)
        .package()
)

for rep in reps:
    print(rep.size(), rep.bit_rate())

