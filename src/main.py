def main():
    print("Hello from mcysd-19-escape-room!")
    print(square(5))
    print(square_wrong(5))
    
def square(a: int) -> int:
    return a**2

def square_wrong(a: int) -> int:
    return a + a


if __name__ == "__main__":
    main()
