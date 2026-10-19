
arr = [None] * 7
target = [0, 1, 2, 4]

for index in target:
    user = input(f"Enter a number for index: {index} ")
    arr[index] = int(user)

arr[3] = arr[0] ^ arr[1] ^ arr[2]
arr[5] = arr[0] ^ arr[1] ^ arr[4]
arr[6] = arr[0] ^ arr[2] ^ arr[4]

print("Generated Hamming code:", arr)

print("\nChange only 1 bit to simulate an error.")

recieve = [None] * 7

for i in range(len(recieve)):
    value = input(f"Enter a number for index {i}: ")
    recieve[i] = int(value)

print("Received code:", recieve)

x = recieve[3] ^ recieve[1] ^ recieve[2] ^ recieve[0]
y = recieve[5] ^ recieve[0] ^ recieve[1] ^ recieve[4]
z = recieve[6] ^ recieve[0] ^ recieve[2] ^ recieve[4]

result = f"{x}{y}{z}"

match result:
    case "111":
        recieve[0] ^= 1
    case "110":
        recieve[1] ^= 1
    case "101":
        recieve[2] ^= 1
    case "100":
        recieve[3] ^= 1
    case "011":
        recieve[4] ^= 1
    case "010":
        recieve[5] ^= 1
    case "001":
        recieve[6] ^= 1

print(f"Error position (syndrome): {result}")
print("Corrected Hamming code:", recieve)
