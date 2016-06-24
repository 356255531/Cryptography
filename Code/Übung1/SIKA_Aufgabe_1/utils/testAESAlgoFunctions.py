from Crypto.Cipher import AES
from Crypto import Random
import array

rndfile = Random.new()
PKey = array.array('B')
PPlain = array.array('B')
PExpected = array.array('B')
numEnc = 1
allCorrect = True
outputFile = open('AESTestResult.txt', 'w')

def generateRandomArray():
	result = array.array('B', rndfile.read(16))
	return result

def encryptArray(key, plain):
	obj = AES.new(key.tostring(), AES.MODE_ECB)
	ciphertext = obj.encrypt(plain.tostring())
	result = array.array('B', ciphertext)
	return result

def printArrayHex(arr, length):
        #for i in range(length):
        #        print("%02X" % arr[i]),
	print ("%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X" % ( arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], arr[14], arr[15]) ),
        print ""

def compareArrays(arr1, arr2):
	for i in range(len(arr1)):
		if (arr1[i] != arr2[i]):
			return False
	return True

def writeArrayToGDBValue(arr, valueName):
	for i in range(len(arr)):
		gdb.execute("set %s[%d]=%d" % (valueName, i, arr[i]))

class BeforeEncBreakpoint (gdb.Breakpoint):
	def stop(self):
		global PKey
		global PPlain
		global PExpected
		global numEnc

		PKey = generateRandomArray()
		PPlain = generateRandomArray()
		PExpected = encryptArray(PKey, PPlain)
		writeArrayToGDBValue(PKey, "key")
		writeArrayToGDBValue(PPlain, "buf")
		print "Key            : ",
		printArrayHex(PKey, len(PKey))
		
		numEnc = 1

class AfterEncBreakpoint (gdb.Breakpoint):
	def stop(self):
		global numEnc
		global PExpected
		global allCorrect
		global PKey
                global PPlain

		#print "\nEncryption %d\n" % numEnc
		print "Plaintext      : ",
		printArrayHex(PPlain, len(PPlain))
 		PRealCipher = gdb.parse_and_eval("buf")
		print "Computed Cipher: ",
		printArrayHex(PRealCipher, 16)
		print "Expected Cipher: ",
		printArrayHex(PExpected, len(PExpected))
		print ""
		if (compareArrays(PExpected,PRealCipher) == False):
			allCorrect = False
			print "Encryption incorrect!\n"
			outputFile.write('1')
			outputFile.close()
			gdb.execute("set logging off")
			gdb.execute("quit")
		else:
			print "Encryption correct!\n"

		PPlain = generateRandomArray()
		PExpected = encryptArray(PKey, PPlain)
		writeArrayToGDBValue(PPlain, "buf")

		numEnc = numEnc + 1

class FinalBreakpoint (gdb.Breakpoint):
	def stop(self):
		global allCorrect
		if allCorrect:
			print "All Tests passed!"
			outputFile.write('0')
			outputFile.close()
		else:
			print "One or more ciphers were incorrect!"
			outputFile.write('1')
			outputFile.close()
		gdb.execute("set logging off")
		gdb.execute("quit")

beforeEnc = BeforeEncBreakpoint("main.c:19")
afterEnc = AfterEncBreakpoint("main.c:25")
endBreak = FinalBreakpoint("main.c:29")
