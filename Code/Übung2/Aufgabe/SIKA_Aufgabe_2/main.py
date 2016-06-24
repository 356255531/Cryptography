import student, random, sys, time

n = long(0xB935E2B84B83E9EB)
d = long(0xDEADBEEF00211989)

print "n: ", "".join(student.hex64(n)), " (", student.bin64(n), ")"
print "d: ", "".join(student.hex64(d)), " (", student.bin64(d), ")"

start_time = time.clock()

for i in xrange(10):
    y = long(random.getrandbits(64))
    w = pow(y, d, n)
    x = student.RSA_Decrypt(y,d,n)

    print "\n"
    print "y: ", "".join(student.hex64(y)), " (", student.bin64(y), ")"
    print "x: ", "".join(student.hex64(x)), " (", student.bin64(x), ")"
    print "w: ", "".join(student.hex64(w)), " (", student.bin64(w), ")"

    if x != w:
        print "FAILED"
        sys.exit(100)

print "\nALL PASSED"
print "\nExecution time: %f s" % (time.clock()-start_time)
sys.exit(0)
