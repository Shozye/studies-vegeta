def match(text: str, index: int, pattern: str):
    for i in range(len(pattern)):
        if text[index + i] != pattern[i]: 
            return False 
    return True


def isNiceGenome(text: str) -> bool:
    START_PART = "ATG"
    END_PARTS = ["TAA", "TAG", "TGA"]
    last_atg = -1
    for i in range(len(text)-2):
        if last_atg == -1:
            if match(text, i, START_PART):
                last_atg = i
        elif match(text, i, START_PART):
            last_atg = i
        else:
            found_end_part = False
            for part in END_PARTS:
                found_end_part = found_end_part or match(text, i, part)
            if found_end_part:
                if i - last_atg >= 33:
                    return True
                else:
                    last_atg = -1
    return False

def main():
    assert isNiceGenome("xd") == False

if __name__ == "__main__":
    main()