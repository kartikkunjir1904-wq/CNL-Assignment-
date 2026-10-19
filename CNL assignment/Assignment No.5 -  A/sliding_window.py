
def sliding_window():
    n = int(input("Enter the number of frames: "))
    w_size = int(input("Enter the window size: "))
    l_frame = int(input("Enter the frame number to simulate as lost: "))

    frames = list(range(1, n + 1))
    transmitted = []

    print("\nSliding Window Protocol")
    i = 0

    while i < n:
        window = frames[i:i + w_size]
        print(f"\nCurrent Window: {window}")

        for frame in window:
            if frame == l_frame:
                print(f"Frame {frame} -> LOST")
                print(f"Frame {frame} will be retransmitted...")
            else:
                print(f"Frame {frame} -> Successfully transmitted")
                transmitted.append(frame)

        if l_frame in window:
            print(f"Retransmitting Frame {l_frame}")
            print(f"Frame {l_frame} -> Successfully transmitted")
            transmitted.append(l_frame)
            l_frame = -1

        i += w_size

    print("\nTransmission Complete")
    print("Successfully transmitted frames:")

    transmitted.sort()
    for frame in transmitted:
        print(f"Frame {frame} -> Success")


sliding_window()
