
def horner(polynomial: list[int], x_value: int) -> int:
    """
    polynomial[i] is factor to x^i
    """
    value: float = 0
    
    for i in range(len(polynomial)-1, -1, -1):
        value *= x_value
        value += polynomial[i]
        
    return value

def main():
    assert horner([1,4,6,4,1], 1) == 16
    assert horner([1,4,6,4,1], 2) == 81

if __name__ == "__main__":
    main()