import pandas

pandas.set_option("display.max_columns", None)
pandas.set_option("display.max_rows", None)

# Veriyi hazırlama

dataframe_ = pandas.read_csv("Datasets/armut_data.csv")  # veriyi okututunuz.
dataframe = dataframe_.copy()
dataframe.head()

dataframe["Hizmet"] = [str(row[1]) + "_" + str(row[2]) for row in dataframe.values]
dataframe.head()

dataframe.info()

dataframe["CreateDate"] = pandas.to_datetime(dataframe["CreateDate"])

dataframe["NEW_DATE"] = dataframe["CreateDate"].dt.strftime("%Y-%m")
dataframe.head()

dataframe["SepetID"] = [str(row[0]) + "_" + str(row[5]) for row in dataframe.values]
dataframe.head()