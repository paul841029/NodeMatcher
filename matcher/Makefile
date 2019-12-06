generate_csv:
	python main.py\
		--dataset ${dataset}\
		--gt ${gt}\
		--output ${dataset}_${gt}.csv
	python draw.py\
		--input ${dataset}_${gt}.csv\
		--dataset ${dataset}\
		--gt ${gt}
