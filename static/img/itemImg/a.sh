for i in *
do
	for j in "$i/*"
	do
		#mv $j $i/main.jpg
		echo $j
	done
done
