import streaming

# print(streaming.dash().amin())
reps = (
    streaming
        .dash('c:\\test\\test.mp4')
        .amin()
        .auto_rep()
        .package()
)

for rep in reps:
    print(rep.size(), rep.bit_rate())

