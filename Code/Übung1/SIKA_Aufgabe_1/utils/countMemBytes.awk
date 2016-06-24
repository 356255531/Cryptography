BEGIN { numBytes = 0 }
/0x/ { if ($2 != 0 || $5 != 0)
{
numBytes++
}
}
END {
	print "Number of RAM bytes used: ",numBytes
	print numBytes > "MemBytes.txt"
}
