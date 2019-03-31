import streaming
from streaming import Representation

rep1 = Representation(width=640, height=360, kilo_bitrate=190)
rep2 = Representation(width=625, height=853, kilo_bitrate=200)
rep3 = Representation(width=152, height=365, kilo_bitrate=630)
reps = (
    streaming
        .dash('c:\\test\\test.mp4', adaption='aaaaaaaaaaaaaa')
        # .add_rep(rep1, rep2, rep3)
        .auto_rep()
        .package()
)

print(reps.adaption)
# for rep in reps:
#     print(rep.size(), rep.bit_rate())

