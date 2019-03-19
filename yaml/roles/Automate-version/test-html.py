import 



h = HTML()
table_data = [
		['Header1',		'Header2',		'Header3'],
		['P1',			'v1',			'D1'],
		['P2',			'v2',			'D2'],
		['P3',			'v3',			'D3'],
		['P4',			'v4',			'D4'],
		['P5',			'v5',			'D5'],
	]

h.table(table_data)
print(h)