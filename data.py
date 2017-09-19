import csv
import data_vo

def read_csv():
	csv_path = "Test-Orders_DB.csv"
	try:
		info_list = []
		f = open(csv_path, 'rb')
		reader = csv.reader(f)
		for row in reader:
			info_list.append(row)
		f.close()
		return info_list
	except Exception as e:
		raise

def manipulation_of_csv_data_list():
	try:
		final_list = []
		csv_data_list = read_csv()
		count = 0
		for row in csv_data_list:
			if count == 0:
				count+=1
				continue
			data = data_vo.DataVo()
			data.order_id = row[2]
			data.product_name = row[6]
			data.order_status = row[1]
			data.product_url = row[7]
			if row[23] != '' and row[23] is not None:
				data.cost_price = float(row[23]) * 66
			else:
				data.cost_price = row[23]
			final_list.append(data)
		return final_list
	except Exception as e:
		raise


def write_in_csv(order_id, product_name, order_status, product_url, cost_price):
	row = ['', order_status, order_id, '', '', '', product_name, product_url, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', cost_price, '', '']
	print row
	with open("Test-Orders_DB.csv", "a") as to_file:
		writer = csv.writer(to_file, delimiter=",")
		writer.writerow(row)
	
