BEGIN {
	runAvg = 0
	cycleCount = 0
	numEnc = 0
}
{
	if ($5 == "begin:")
	{
		if (numEnc != 0)
		{
			stopEnc[numEnc-1] = $2
		}
		startEnc[numEnc] = $2
		numEnc = numEnc + 1
	}
	if ($5 == "end")
	{
		stopEnc[numEnc-1] = $2
	}

	if ($2 ~ /killed/)	#Matches the string "GDBServer: killed remotely" to catch the end of the last encryption
	{
		stopEnc[numEnc-1] = cycleCount
	}
	else
	{
		cycleCount = $2
	}
}
END { 
	for (i in startEnc)
	{
		print "Start of enc. ",i," at ",startEnc[i]
		print "End of enc. ",i," at ",stopEnc[i]

		runAvg = runAvg + stopEnc[i] - startEnc[i]

		lengthArr[i] = stopEnc[i] - startEnc[i]
		print "Runtime enc. ",i,": ",lengthArr[i]
	}
	runAvg = runAvg / numEnc
	print ""
	print "Average Encryption Runtime:",runAvg

	#Standard Deviation by Welford's method:
	M = 0
	S = 0
	k = 1
	for (i in lengthArr)
	{
		tmpM = M
		M = M + (lengthArr[i] - tmpM) / k
		S = S + (lengthArr[i] - tmpM) * (lengthArr[i] - M)
		k = k + 1
	}
	print "Standard Deviation Encryption Runtime:",sqrt(S / (k-1))

	if (debug == "1")
	{
		print "Mean value: ", runAvg > ".runtime"
		print "Standard deviation: ", sqrt(S / (k-1)) >> ".runtime"
	}
}
