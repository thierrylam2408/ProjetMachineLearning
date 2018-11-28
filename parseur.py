#!usr/bin/python

import sys
import csv

def filterByFieldsName(filename, fields):
	result=[]
	with open(filename, encoding='utf-8') as csvfile:
		data = list(csv.reader(csvfile))
		index = [data[0].index(field) for field in fields]
		for row in data[1::]:
			result.append([row[i] for i in index])
	return result

def test():
	print(filterByFieldsName("tmdb_5000_movies.csv", ["overview", "original_title", "genres"])[0])