import sys
from timeit import default_timer as timer

CONVERSION_TABLE = {
    0   : "0", 1   : "1", 2   : "2", 3   : "3", 4   : "4",
    5   : "5", 6   : "6", 7   : "7", 8   : "8", 9   : "9",
    10  : "A", 11  : "B", 12  : "C", 13  : "D", 14  : "E",
    15  : "F", 16  : "G", 17  : "H", 18  : "I", 19  : "J",
    20  : "K", 21  : "L", 22  : "M", 23  : "N", 24  : "O",
    25  : "P", 26  : "Q", 27  : "R", 28  : "S", 29  : "T",
    30  : "U", 31  : "V", 32  : "W", 33  : "X", 34  : "Y",
    35  : "Z"
}

def getKey(value):
    for key in CONVERSION_TABLE:
        if CONVERSION_TABLE[key] == value:
            return key
    return None

def isCorrectNumber(s, base):
    
    """ Checks whether passed string is correct number for a given base or not """

    isNegativeNumber = False
    isDecimal = False
    isNumber = True
    
    if len(s) == 0:
        return [False, False, False]
    
    if(s[0] == '-'):
        isNegativeNumber = True
        
    if isNegativeNumber:
        it = 1
    else:
        it = 0
    
    while it < len(s):
        if s[it] == ".":
            isDecimal = True
        elif ord(s[it]) >= ord('0') and ord(s[it]) <= ord('9'):
            if(int(s[it]) >= base):
                isNumber = False
                break
        elif s[it] in list(CONVERSION_TABLE.values()):
            key = getKey(s[it])
            if(key >= base):
                isNumber = False
                break
        else:
            isNumber = False
            break
        
        it += 1
    
    return [isNumber, isDecimal, isNegativeNumber] 

def toDecimal(number, base, isDecimal, isNegative):
    
    """ Converts passed number from a given base to decimal number (Base 10) """
    
    stringRepresentation = number

    if isNegative:
        start = 1
    else:
        start = 0
    
    number = 0
    exponent = 0
    if not isDecimal:
        # integer number
        for i in range(len(stringRepresentation)-1, start-1, -1):
            number += getKey(stringRepresentation[i]) * base**exponent
            exponent += 1
    else:
        # floating point number
        pointPosition = stringRepresentation.find(".")
        for i in range(pointPosition-1, start-1, -1):
            number += getKey(stringRepresentation[i]) * base**exponent
            exponent += 1
        
        exponent = -1
        for i in range(pointPosition+1, len(stringRepresentation)):
            number += getKey(stringRepresentation[i]) * base**exponent
            exponent -= 1
    
    if isNegative:
        number = number * (-1)
    return number
    
def fromDecimalToTarget(number, target, isDecimal, isNegative):
    
    """ Converts given decimal (Base 10) number to a target base """
    
    stringRepresentation = str(number)
    
    if isNegative:
        start = 1
    else:
        start = 0
        
    stringRepresentation = stringRepresentation[start:]
    
    resultString = ""
    if not isDecimal:
        remainder = 0
        integerPart = int(stringRepresentation)
        
        while integerPart != 0:
            remainder = integerPart % target
            integerPart = integerPart // target
            resultString = CONVERSION_TABLE[remainder] + resultString
        
    else:
        pointPosition = stringRepresentation.find(".")
        remainder = 0
        integerPart = int(stringRepresentation[0:pointPosition])
        
        while integerPart != 0:
            remainder = integerPart % target
            integerPart = integerPart // target
            resultString = CONVERSION_TABLE[remainder] + resultString
        
        if resultString == "":
            resultString += "0"
        resultString += "."
        
        decimalPart = float("0." + stringRepresentation[pointPosition+1:])
        remainder = 0
        decimalsCount = 0
        DECIMAL_LIMIT = int(decimalPart * 2 ** 6)
        
        while decimalPart != 0 and decimalsCount < DECIMAL_LIMIT:
            curr = decimalPart * target
            i = int(curr)
            r = curr - i
            
            resultString = resultString + CONVERSION_TABLE[i]
            decimalsCount += 1
            decimalPart = r
    
    if isNegative:
        resultString = "-" + resultString
    return resultString

def convert(number, base, target, isNegative, isDecimal):
    
    if base == target:
        return number

    decimalNumber = toDecimal(number, base, isDecimal, isNegative)

    if(target == 10):
        return decimalNumber
    
    return fromDecimalToTarget(decimalNumber, target, isDecimal, isNegative)

def main():
    
    print()
    print("\t\t=========================================================================================")
    print()
    print("\t\t ****  ****  ****  ****    ****  ****  **    * *       * ****  ****  *****  ****  ****  ")
    print("\t\t *  *  *  *  *     *       *     *  *  * *   *  *     *  *     *  *    *    *     *  *  ")
    print("\t\t ****  ****  ****  ****    *     *  *  *  *  *   *   *   ****  ****    *    ****  ****  ")
    print("\t\t *  *  *  *     *  *       *     *  *  *   * *    * *    *     ***     *    *     ***   ")
    print("\t\t ****  *  *  ****  ****    ****  ****  *    **     *     ****  *  **   *    ****  *  ** ")
    print()
    print("\t\t=========================================================================================")
    
    if len(sys.argv) == 4:
        inp = sys.argv[1]
        try:
            base = int(sys.argv[2])
            target = int(sys.argv[3])
        except:
            print("\n\t\tError: Integer values are required for base and target!", end="\n\n")
            return
    else:
        inp = input("\n\t\tEnter number for conversion: ").upper()
        try:
            base = int(input("\t\tBase: "))
            target = int(input("\t\tTarget: "))
            
            print("\n\t\t=========================================================================================")
            
        except:
            print("\n\t\t=========================================================================================")
            print("\n\t\tError: Integer values are required for base and target!", end="\n\n")
            return
    
    if(base > 36 or base < 2 or target > 36 or target < 2):
        print("\n\t\tError: Base and target must be in range [2,36]", end="\n\n")
        return
    
    test = isCorrectNumber(inp, base)
    if not test[0]:
        print("\n\t\tError: Passed input is not valid number!", end="\n\n")
        return
    
    isDecimal = test[1]
    isNegative = test[2]
    
    if isDecimal:
        if isNegative and inp[1] == ".":
            inp = "-0" + inp[1:]
        elif not isNegative and inp[0] == ".":
            inp = "0" + inp
    
    start = timer()
    solution = convert(inp, base, target, isNegative, isDecimal)
    end = timer()
    print("\n\t\tResult number: ", solution, "\n\t\tExecution time: ", round((end - start)*1000, 5), "ms", end="\n\n")
    
main()
print("\t\t=========================================================================================", end="\n\n")
