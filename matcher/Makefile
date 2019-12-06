generate_csv:
	python main.py\
		--dataset ${dataset}\
		--gt ${gt}\
		--output csv/${dataset}_${gt}.csv
	python draw.py\
		--input csv/${dataset}_${gt}.csv\
		--dataset ${dataset}\
		--gt ${gt}
